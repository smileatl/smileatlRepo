## 5、http请求报文和响应报文

HTTP报文主要分为两种类型：请求报文和响应报文。以下是对这两种类型的详细解释：

### HTTP 请求报文 (HTTP Request Message)

HTTP 请求报文由客户端（通常是浏览器）发送到服务器，包含请求方法、URI、协议版本、请求头部字段和可选的请求体。其结构如下：

```
请求行
请求头部字段
空行
请求体（可选）
```

#### 请求行 (Request Line)
请求行包含三个部分：请求方法、请求URI和HTTP版本。示例：

```
GET /index.html HTTP/1.1
```

- **请求方法**：常见的方法包括 GET、POST、PUT、DELETE、HEAD、OPTIONS 等。
- **请求URI**：资源的路径，如 `/index.html`。
- **HTTP版本**：如 `HTTP/1.1`。

#### 请求头部字段 (Request Headers)
请求头部字段提供关于客户端请求和客户端自身的信息。示例：

```
Host: www.example.com
User-Agent: Mozilla/5.0
Accept: text/html
```

#### 请求体 (Request Body)
请求体包含请求的实际数据，通常在 POST 或 PUT 请求中使用。例如，提交表单数据或上传文件。

### HTTP 响应报文 (HTTP Response Message)

HTTP 响应报文由服务器发送到客户端，包含状态行、响应头部字段和可选的响应体。其结构如下：

```
状态行
响应头部字段
空行
响应体（可选）
```

#### 状态行 (Status Line)
状态行包含三个部分：HTTP版本、状态码和状态描述。示例：

```
HTTP/1.1 200 OK
```

- **HTTP版本**：如 `HTTP/1.1`。
- **状态码**：三位数字表示请求的处理结果，如 `200` 表示成功，`404` 表示未找到。
- **状态描述**：对状态码的简短描述，如 `OK` 或 `Not Found`。

#### 响应头部字段 (Response Headers)
响应头部字段提供关于服务器和响应的元数据。示例：

```
Content-Type: text/html
Content-Length: 1234
Server: Apache/2.4.1 (Unix)
```

#### 响应体 (Response Body)
响应体包含实际的响应数据，如 HTML 文档、图片、JSON 数据等。

### 示例

#### 请求报文示例

```
GET /index.html HTTP/1.1
Host: www.example.com
User-Agent: Mozilla/5.0
Accept: text/html

```

#### 响应报文示例

```
HTTP/1.1 200 OK
Content-Type: text/html
Content-Length: 1234
Server: Apache/2.4.1 (Unix)

<!DOCTYPE html>
<html>
<head>
    <title>Example</title>
</head>
<body>
    <h1>Hello, World!</h1>
</body>
</html>
```

### 总结

- **请求报文**：由请求行、请求头部字段、空行和可选的请求体组成。
- **响应报文**：由状态行、响应头部字段、空行和可选的响应体组成。

这些报文结构确保了客户端和服务器之间能够有效地通信和交换数据。



## 10、http请求方法

"HTTP 请求方法定义了客户端希望在服务器上执行的操作。以下是常见的 HTTP 请求方法及其用途：

### GET
- **用途**：请求指定资源的表示形式。使用 GET 方法的请求应该只用于获取数据。
- **特点**：GET 请求不应产生任何副作用（即是幂等的），可以被缓存。

### POST
- **用途**：向指定资源提交数据，通常用于提交表单或上传文件。服务器会根据请求体的数据进行处理。
- **特点**：POST 请求可能会产生副作用（如更新数据库），通常不会被缓存。

### PUT
- **用途**：向指定资源上传其最新的表示形式。通常用于更新资源。
- **特点**：PUT 请求是幂等的（多次请求的结果相同），可以创建或更新资源。

### DELETE
- **用途**：删除指定的资源。
- **特点**：DELETE 请求是幂等的。

### HEAD
- **用途**：与 GET 方法一样，只是服务器只返回响应头，不返回响应体。用于获取资源的元数据。
- **特点**：HEAD 请求是幂等的。

### OPTIONS
- **用途**：用于描述目标资源的通信选项。客户端可以通过 OPTIONS 请求来了解服务器支持哪些请求方法。
- **特点**：OPTIONS 请求是幂等的。

### PATCH
- **用途**：对资源应用部分修改。不同于 PUT，PATCH 只修改资源的部分内容。
- **特点**：PATCH 请求不是幂等的。

### TRACE
- **用途**：回显服务器收到的请求，主要用于测试或诊断。
- **特点**：TRACE 请求是幂等的。

### CONNECT
- **用途**：建立一个到目标资源的隧道，通常用于代理服务器。
- **特点**：CONNECT 请求通常用于 HTTPS 通过 HTTP 代理进行的隧道连接。

### 示例

#### GET 请求示例
```http
GET /index.html HTTP/1.1
Host: www.example.com
User-Agent: Mozilla/5.0
Accept: text/html
```

#### POST 请求示例
```http
POST /submit-form HTTP/1.1
Host: www.example.com
Content-Type: application/x-www-form-urlencoded
Content-Length: 27

name=John&age=30&city=New+York
```

### 总结
- **GET**：获取资源
- **POST**：提交数据
- **PUT**：更新资源
- **DELETE**：删除资源
- **HEAD**：获取资源元数据
- **OPTIONS**：获取通信选项
- **PATCH**：部分修改资源
- **TRACE**：回显请求
- **CONNECT**：建立隧道

这些方法共同定义了 HTTP 的操作语义，确保客户端和服务器能够进行有效的通信。