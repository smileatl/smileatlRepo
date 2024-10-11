# libevent

bufferevent是libevent中用于读写事件的结构体

`_std::lock_guard_` 是一个智能锁，它在构造时自动锁定`_mutex_`，并在析构时自动解锁，避免了忘记解锁导致的死锁问题

- `bufferevent_data_cb` 是一个函数指针类型，用于定义处理读写数据的回调函数；回调函数通常在缓冲区有数据可读或可写时被调用。
- 
- `bufferevent_event_cb` 是一个函数指针类型，用于定义处理事件的回调函数；事件包括读取错误、写入错误、EOF（文件结束）等。