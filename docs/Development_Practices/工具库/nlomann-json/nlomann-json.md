# nlomann-json

在使用 `nlohmann::json` 库时，访问 JSON 对象中的元素有两种常见方式：使用 `operator[]` 和 `at()` 方法。

### `operator[]` 和 `at()` 的区别

- **`operator[]`**：
  - 如果指定的键不存在，会在 JSON 对象中插入一个新的键，并将其值设置为 `null`。
  - 不会抛出异常。

- **`at()`**：
  - 如果指定的键不存在，会抛出 `std::out_of_range` 异常。
  - 更适合在你确定键存在的情况下使用，或者你希望在键不存在时捕获异常进行处理。

在你的代码中，如果你确定 `requestJson` 一定包含 `"method"` 键，并且你希望在键不存在时捕获异常，那么使用 `at()` 会更安全。

### 修改后的代码

```cpp
switch_status_t BlegClientHttp::SendMsgSync(const bleg_msg_t* msg, int timeout)
{
    nlohmann::json requestJson;
    nlohmann::json assertionsJson;
    try {
        requestJson = nlohmann::json::parse(msg->request, nullptr, true);
        assertionsJson = nlohmann::json::parse(msg->assertions, nullptr, true);
    } catch (const std::exception& e) {
        switch_log_printf(SWITCH_CHANNEL_LOG, SWITCH_LOG_ERROR, "request or assertions json invalid\n");
        return SWITCH_STATUS_INVAL;
    }

    switch_status_t status = SWITCH_STATUS_SUCCESS;
    std::lock_guard<std::mutex> guard(m_connectionMutex);

    if (!m_curlInterface) {
        return SWITCH_STATUS_NOT_INITALIZED;
    }
    if (!msg || !msg->data_len || !msg->request) {
        switch_log_printf(SWITCH_CHANNEL_LOG, SWITCH_LOG_ERROR, "[clientId=%u][%s:%d]SendMsgSync failed,msg or data is null\n", m_clientId, m_remoteIp.c_str(), m_remotePort);
        return SWITCH_STATUS_INVAL;
    }
    if (!m_isConnected) {
        switch_log_printf(SWITCH_CHANNEL_LOG, SWITCH_LOG_WARNING, "[clientId=%u][%s:%d]SendMsgSync failed,m_isConnected=false\n",
            m_clientId, m_remoteIp.c_str(), m_remotePort);
        return SWITCH_STATUS_IGNORE;
    }

    switch_curl_http_req_t req;
    switch_curl_http_resp_t* resp = nullptr;
    char httpUrl[1024] = { 0 };
    const char* httpUrlPrefix = m_usedigestHttpauth ? "https" : "http";

    snprintf(httpUrl, sizeof(httpUrl), "%s://%s:%d%s", httpUrlPrefix, m_remoteIp.c_str(), m_remotePort, m_httpPath.c_str());

    memset(&req, 0, sizeof(switch_curl_http_req_t));

    // 设置请求方法
    std::string method;
    try {
        method = requestJson.at("method");
    } catch (const std::out_of_range& e) {
        switch_log_printf(SWITCH_CHANNEL_LOG, SWITCH_LOG_ERROR, "Method not found in request JSON\n");
        return SWITCH_STATUS_INVAL;
    }

    if (method == "POST") {
        req.method = HTTP_POST;
    } else if (method == "GET") {
        req.method = HTTP_GET;
    } else if (method == "PUT") {
        req.method = HTTP_PUT;
    } else if (method == "DELETE") {
        req.method = HTTP_DELETE;
    } else if (method == "PATCH") {
        req.method = HTTP_PATCH;
    } else if (method == "OPTIONS") {
        req.method = HTTP_OPTIONS;
    } else if (method == "HEAD") {
        req.method = HTTP_HEAD;
    } else if (method == "CONNECT") {
        req.method = HTTP_CONNECT;
    } else if (method == "TRACE") {
        req.method = HTTP_TRACE;
    } else {
        switch_log_printf(SWITCH_CHANNEL_LOG, SWITCH_LOG_ERROR, "Unsupported HTTP method: %s\n", method.c_str());
        return SWITCH_STATUS_INVAL;
    }

    req.url = httpUrl;
    req.options.log_opt = CURL_LOG_DEFAULT;

    // 设置认证信息
    if (m_isAuth && m_usedigestHttpauth) { // 开启摘要认证
        req.options.auth_type = SWITCH_CURLAUTH_DIGEST;
        req.options.auth_username = (char*)m_authUsername.c_str();
        req.options.auth_password = (char*)m_authPassword.c_str();
    }

    // 本地地址
    if (m_localIp.size()) {
        req.options.local_addr = (char*)m_localIp.c_str();
    }

    // 设置请求头
    switch_curl_slist_t* headers = nullptr;
    for (const auto& header : requestJson["headers"]) {
        std::string header_str = header["key"] + ": " + header["value"];
        headers = m_curlInterface->switch_curl_slist_append(headers, header_str.c_str());
    }
    req.http_headers = headers;

    // 设置请求体
    if (requestJson.contains("body")) {
        std::string body = requestJson["body"];
        req.data = (void*)body.c_str();
        req.data_len = body.size();
        req.content_type = "application/json"; // 假设请求体是 JSON 格式
    }

    // 发送请求
    resp = m_curlInterface->switch_curl_http_request(nullptr, &req);
    if (!resp) {
        switch_log_printf(SWITCH_CHANNEL_LOG, SWITCH_LOG_WARNING, "[clientId=%u][%s:%d]SendMsgSync failed,switch_curl_http_request return null,url=%s\n",
            m_clientId, m_remoteIp.c_str(), m_remotePort, httpUrl);
        status = SWITCH_STATUS_GENERR;
        goto end;
    }
    if (resp->resp_code != 200) {
        switch_log_printf(SWITCH_CHANNEL_LOG, SWITCH_LOG_WARNING, "[clientId=%u][%s:%d]SendMsgSync failed,switch_curl_http_request return %ld,url=%s\n",
            m_clientId, m_remoteIp.c_str(), m_remotePort, resp->resp_code, httpUrl);
        status = SWITCH_STATUS_GENERR;
        goto end;
    }

    switch_log_printf(SWITCH_CHANNEL_LOG, SWITCH_LOG_INFO, "[clientId=%u][%s:%d]BlegClientHttp::SendMsgSync:%.*s\n", m_clientId, m_remoteIp.c_str(), m_remotePort, msg->data_len, msg->request);

end:
    if (resp) {
        m_curlInterface->switch_curl_http_resp_destroy(resp);
    }
    if (headers) {
        m_curlInterface->switch_curl_slist_free_all(headers);
    }
    return status;
}
```

### 代码解释

1. **解析 JSON 数据**：
   - 使用 `nlohmann/json` 库的 `json::parse` 方法解析 `char*` 类型的 JSON 字符串。

2. **设置请求方法**：
   - 使用 `requestJson.at("method")` 获取请求方法字符串。如果键不存在，则捕获 `std::out_of_range` 异常，并记录错误日志。

3. **构建 HTTP 请求**：
   - 根据解析后的 JSON 数据构建 `switch_curl_http_req_t` 结构体，包括设置请求方法、URL、头信息和请求体。

4. **使用 `mod_curl` 接口发送 HTTP 请求**：
   - 调用 `mod_curl` 提供的接口函数 `switch_curl_http_request` 发送 HTTP 请求，并接收响应。

5. **处理响应**：
   - 根据响应的状态码和内容进行日志记录和错误处理。

### 依赖库

- `nlohmann/json`：用于解析和处理 JSON 数据。

### 依赖库安装

- 安装 `nlohmann/json`：
  可以通过包管理器安装，也可以直接在项目中包含 `json.hpp` 头文件。

通过这种方式，你可以更安全地访问 JSON 对象中的元素，并处理可能的异常情况。