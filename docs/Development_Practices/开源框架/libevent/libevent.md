# libevent

## bufferevent

bufferevent是libevent中用于读写事件的结构体

`_std::lock_guard_` 是一个智能锁，它在构造时自动锁定`_mutex_`，并在析构时自动解锁，避免了忘记解锁导致的死锁问题

- `bufferevent_data_cb` 是一个函数指针类型，用于定义处理读写数据的回调函数；回调函数通常在缓冲区有数据可读或可写时被调用。
- `bufferevent_event_cb` 是一个函数指针类型，用于定义处理事件的回调函数；事件包括读取错误、写入错误、EOF（文件结束）等。

## bufferevent的三种回调

**自带buffer的事件-bufferevent**

bufferevent实际上也是一个event, 只不过比普通的event高级一些, 它的内部有两个缓冲区, 以及一个文件描述符（网络套接字）。一个网络套接字有读和写两个缓冲区, bufferevent同样也带有两个缓冲区, 还有就是libevent事件驱动的核心回调函数, 那么四个缓冲区以及触发回调的关系如下：

![9.png](resource/img/gakb7l6zxdcoc_4fd1cfed4a18469692bf6e5fe4c6bff3.png)

从图中可以得知, 一个bufferevent对应两个缓冲区, 三个回调函数, 分别是写回调, 读回调和事件回调

bufferevent有三个回调函数：

**读回调** – 当bufferevent将底层读缓冲区的数据读到自身的读缓冲区时触发读事件回调.

**写回调** – 当bufferevent将自身写缓冲的数据写到底层写缓冲区的时候触发写事件回调, 由于数据最终是写入了内核的写缓冲区中, 应用程序已经无法控制, 这个事件对于应用程序来说基本没什么用, 只是通知功能.

**事件回调** – 当bufferevent绑定的socket连接, 断开或者异常的时候触发事件回调.



## 函数调用

### bufferevent_write

```c
/**
  向 bufferevent 缓冲区写入数据。

  bufferevent_write() 函数可用于将数据写入文件描述符。数据会被追加到输出缓冲区，并在文件描述符可写时自动写入。

  @param bufev 要写入的 bufferevent 对象
  @param data 指向要写入数据的指针
  @param size 数据的长度，以字节为单位
  @return 成功返回 0，发生错误返回 -1
  @see bufferevent_write_buffer()
  */
EVENT2_EXPORT_SYMBOL
int bufferevent_write(struct bufferevent *bufev,
                      const void *data, size_t size);
```

## event_base_loopexit和event_base_dispatch

重新进入下一次循环是指在当前循环结束后，程序会再次检查循环条件并执行循环体的过程。在你的代码中，这意味着在每次 `event_base_dispatch` 调用结束后，程序会回到 `while` 循环的开头，再次检查 `m_isRunning` 的值，如果 `m_isRunning` 仍然为 `true`，则再次执行循环体的内容。

具体来说，这段代码的执行过程如下：

1. **检查循环条件**：
   - 检查 `m_isRunning` 是否为 `true`。如果 `m_isRunning` 为 `true`，则进入循环体；否则，退出循环。

2. **设置事件循环超时时间**：
   - 调用 `event_base_loopexit(m_eventBase, &timeout)`，设置事件循环将在 `timeout`（100 毫秒）后退出。

3. **运行事件循环**：
   - 调用 `event_base_dispatch(m_eventBase)`，启动事件循环，处理所有挂起的事件。

4. **处理事件**：
   - 如果在 100 毫秒内有事件发生，事件处理函数将被调用。事件处理函数根据事件类型和数据执行相应的操作。
   - 如果没有事件发生，事件循环将在 100 毫秒后自动退出。

5. **重新检查循环条件**：
   - `event_base_dispatch` 返回后，程序回到 `while` 循环的开头，再次检查 `m_isRunning` 的值。
   - 如果 `m_isRunning` 仍然为 `true`，则重新进入下一次循环，重复上述步骤。
   - 如果 `m_isRunning` 为 `false`，则退出循环。

### 示例代码的执行流程

假设 `m_isRunning` 初始为 `true`，下面是每次循环的详细执行流程：

```cpp
while (m_isRunning) {
    // 设置事件循环将在 100 毫秒后退出
    event_base_loopexit(m_eventBase, &timeout);

    // 运行事件循环，处理所有挂起的事件
    event_base_dispatch(m_eventBase);
}
```

#### 第一次循环

1. **检查 `m_isRunning`**：`m_isRunning` 为 `true`，进入循环体。
2. **设置超时时间**：调用 `event_base_loopexit(m_eventBase, &timeout)`，设置事件循环将在 100 毫秒后退出。
3. **运行事件循环**：调用 `event_base_dispatch(m_eventBase)`，开始处理事件。
   - 如果有事件在 100 毫秒内发生，处理相应的事件。
   - 如果没有事件发生，事件循环将在 100 毫秒后退出。
4. **检查 `m_isRunning`**：`event_base_dispatch` 返回后，再次检查 `m_isRunning` 的值。
   - 如果 `m_isRunning` 为 `true`，进入下一次循环。
   - 如果 `m_isRunning` 为 `false`，退出循环。

#### 第二次及后续循环

重复上述步骤，直到 `m_isRunning` 为 `false`。

### 重新进入下一次循环的意义

重新进入下一次循环的意义在于确保事件循环能够持续运行并不断地检查和处理新的事件，同时允许程序在每个循环迭代之间进行一些检查或设置，例如调整超时时间或处理其他逻辑。

通过在每次循环中设置一个超时时间，程序可以定期检查 `m_isRunning` 的状态，这样可以在需要停止事件循环时及时响应。此外，这种设计还允许程序在没有事件发生时避免长时间阻塞，从而提高系统的响应性和灵活性。

### 总结

重新进入下一次循环是指在当前循环结束后，程序再次检查循环条件并执行循环体的过程。在你的代码中，这意味着在每次 `event_base_dispatch` 调用结束后，程序会回到 `while` 循环的开头，再次检查 `m_isRunning` 的值，如果 `m_isRunning` 仍然为 `true`，则再次执行循环体的内容，继续处理事件或等待新的事件发生。

## 为什么要把event_base_loopexit和event_base_dispatch一起配合使用

### `event_base_dispatch` 的作用

`event_base_dispatch` 是 libevent 库中的一个函数，用于启动事件循环。它会一直运行，处理所有挂起的事件，直到没有事件需要处理或者被显式中断。其行为如下：

- **处理事件**：当有事件发生时，调用相应的事件处理程序。
- **阻塞**：如果没有事件发生，`event_base_dispatch` 会阻塞，直到有事件发生或被中断。
- **退出条件**：如果没有事件需要处理，事件循环会退出。

### `event_base_loopexit` 的作用

`event_base_loopexit` 是另一个 libevent 函数，用于设置一个超时时间，当这个时间到达时，事件循环将退出。其作用如下：

- **设置超时退出**：指定一个时间段，事件循环将在这个时间段结束后自动退出。
- **非阻塞**：`event_base_loopexit` 本身不会阻塞，它只是设置一个退出时间。

### 配合使用的原因

将 `event_base_loopexit` 和 `event_base_dispatch` 配合使用，可以实现对事件循环的精细控制，特别是控制事件循环的运行时间和频率。以下是具体原因：

1. **定时检查和控制**：
   - 使用 `event_base_loopexit` 设置一个短的超时时间（例如 100 毫秒），可以确保事件循环在每个超时时间后退出。这允许程序在每个超时时间后检查和执行其他逻辑，如状态检查、资源管理等。
2. **避免长时间阻塞**：
   - 如果仅使用 `event_base_dispatch`，事件循环可能会长时间阻塞，直到有事件发生。这可能导致程序在没有事件时无法及时响应其他操作。通过设置定时退出，可以避免这种长时间阻塞。
3. **动态控制循环行为**：
   - 在每次事件循环结束后，可以根据当前状态（如 `m_isRunning`）动态决定是否继续运行事件循环。这使得程序可以灵活地控制事件循环的生命周期。
4. **提高响应性**：
   - 定期退出事件循环并重新检查条件，可以提高程序对外部控制信号（如停止信号）的响应速度。