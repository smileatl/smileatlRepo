# libevent

bufferevent是libevent中用于读写事件的结构体

`_std::lock_guard_` 是一个智能锁，它在构造时自动锁定`_mutex_`，并在析构时自动解锁，避免了忘记解锁导致的死锁问题