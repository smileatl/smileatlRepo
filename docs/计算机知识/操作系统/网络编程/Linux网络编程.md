## socket

### socket模型创建流程

IP地址：在网络环境中唯一标示一台主机

端口号：在主机中唯一标示一个过程

IP+port：在网络环境中唯一标示一个进程（socket）

```txt
socket是文件的一种类型：(伪文件，不会占用实际的存储空间)

普通文件、目录、软链接实际占用了存储空间

字符设备、块设备、管道、socket伪文件
```

accept返回的才是真正跟客户端连接的socket

![1684739134073s](assets/1684739134073.png)

server.c

1. socket()  建立套接字
2. bind()  绑定IP端口号  (struct socketaddr_in addr 初始化)
3. listen()  指定最大同时发起连接数
4. accept()  阻塞等待客户端发起连接
5. read()
6. 小——大
7. write 给客户端
8. close()

client.c

1. socket()
2. bind()  可以依赖”隐式绑定“
3. connect()  发起连接
4. write()  
5. read()
6. close()



bind(), accept(), connect()需要强转

```C
#include <arpa/inet.h>

uint32_t htonl(uint32_t hostlong);
uint16_t htons(uint16_t hostshort);
uint32_t ntohl(uint32_t netlong);
uint16_t ntohs(uint16_t netshort);
```

h表示host，n表示network，l表示32位长整数，s表示16位短整数。

32位对应的是IP地址，16位对应的是端口号

客户端的端口号是由操作系统来指定的

### socket函数

#### accept

```
#include<sys/types.h>
#include<sys/socket.h>

int accept(int s,struct sockaddr * addr,socklen_t * addrlen);
```

描述：

accept()用来接受参数**s**的socket连线。参数**s**的socket必需先经bind()、listen()函数处理过, 当有连线进来时accept()会返回一个新的socket处理代码, 往后的数据传送与读取就是经由新的socket处理, 

而原来参数**s**的socket能继续使用accept()来接受新的连线要求。连线成功时, 参数**addr**所指的结构会被系统填入远程主机的地址数据, 参数**addrlen**为scokaddr的结构长度。关于结构sockaddr的定义请参考bind()。



#### bind

```c
#include<sys/types.h>
#include<sys/socket.h>
int bind(int sockfd,struct sockaddr * my_addr,int addrlen);
```

描述：

用于将一个套接字（socket）与一个特定的IP地址和端口号绑定在一起的函数。在网络编程中，服务器通常需要绑定一个特定的IP地址和端口号，以便客户端可以通过这个地址和端口号来访问服务器。

bind()用来设置给参数**sockfd**的socket一个名称。此名称由参数**my_addr**指向一sockaddr结构, 对于不同的socket, domain定义了一个通用的数据结构

```c
struct sockaddr
{
    unsigned short int sa_family;
    char sa_data[14];
};
sa_family 为调用socket()时的domain参数, 即AF_xxxx值。
sa_data 最多使用14个字符长度。
此sockaddr结构会因使用不同的socket domain而有不同结构定义, 例如使用AF_INET domain, 其socketaddr结构定义便为
struct socketaddr_in
{
    unsigned short int sin_family;
    uint16_t sin_port;
    struct in_addr sin_addr;
    unsigned char sin_zero[8];
};
struct in_addr
{
    uint32_t s_addr;
};
sin_family 即为sa_family
sin_port 为使用的port编号
sin_addr.s_addr 为IP 地址
sin_zero 未使用。
```

参数：

addrlen为sockaddr的结构长度。

返回值：

成功则返回0, 失败返回-1, 错误原因存于errno中。



#### connect()

```
int connect(int sockfd, const struct sockaddr *addr, socklen_t addrlen);
```

描述：

用于建立TCP连接的函数，它将本地的套接字连接到指定的远程套接字。在TCP连接中，客户端使用connect()函数向服务器发送连接请求，服务器使用accept()函数接受连接请求并建立连接。

参数：

- sockfd是本地套接字描述符，
- addr是指向远程套接字地址结构体的指针，
- addrlen是远程套接字地址结构体的长度。

返回值：

如果连接成功，该函数返回0，否则返回-1并设置errno变量以指示错误类型。



#### listen

```
#include<sys/socket.h>
int listen(int s,int backlog);
```

描述：

listen()用来等待参数**s** 的socket连线。参数**backlog**指定同时能处理的最大连接要求, 如果连接数目达此上限则client端将收到ECONNREFUSED的错误。

Listen()并未开始接收连线, 只是设置socket为listen模式, 真正接收client端连线的是accept()。通常listen()会在socket(), bind()之后调用, 接着才调用accept()。



#### recv

```c
#include<sys/types.h>
#include<sys/socket.h>
int recv(int s,void *buf,int len,unsigned int flags);
```

描述：

recv()用来接收远端主机经指定的**socket**传来的数据, 并把数据存到由参数**buf**指向的内存空间, 参数**len**为可接收数据的最大长度。

flags一般设0。其他数值定义如下:
MSG_OOB 接收以out-of-band 送出的数据。
MSG_PEEK 返回来的数据并不会在系统内删除, 如果再调用recv()会返回相同的数据内容。
MSG_WAITALL强迫接收到len大小的数据后才能返回, 除非有错误或信号产生。
MSG_NOSIGNAL此操作不愿被SIGPIPE信号中断返回值成功则返回接收到的字符数, 失败返回-1, 错误原因存于errno中。

返回值：

成功则返回接收到的字符数, 失败返回-1, 错误原因存于errno中。

错误代码：

EBADF 参数s非合法的socket处理代码
EFAULT 参数中有一指针指向无法存取的内存空间
ENOTSOCK 参数s为一文件描述词, 非socket。
EINTR 被信号所中断
EAGAIN 此动作会令进程阻断, 但参数s的socket为不可阻断
ENOBUFS 系统的缓冲内存不足。
ENOMEM 核心内存不足
EINVAL 传给系统调用的参数不正确。

#### socket()

```
#include <sys/types.h>
#include <sys/socket.h>
int socket(int domain, int type, int protocol);
```

描述：

网络编程中使用的一个系统调用函数，用于创建一个新的套接字，套接字是网络通信中的一种抽象概念，可以理解为一种通信端点，它可以用于在不同的主机之间进行通信。

参数：

- domain参数指定了套接字的协议族，比如AF_INET表示IPv4协议族，AF_INET6表示IPv6协议族；
- type参数指定了套接字的类型，比如SOCK_STREAM表示面向连接的流式套接字，SOCK_DGRAM表示无连接的数据报套接字；
- protocol参数指定协议类型，通常为0，表示使用默认协议。

返回值：

socket()函数执行成功后会返回一个新的套接字描述符，这个描述符可以用于后续的通信操作。如果函数执行失败，则返回-1，并设置errno变量来指示错误的原因。

#### send

```c
#include<sys/types.h>
#include<sys/socket.h>
int send(int s,const void * msg,int len,unsigned int falgs);
```

描述：

send()用来将数据由指定的socket 传给对方主机。参数**s**为已建立好连接的socket。参数**msg**指向欲连线的数据内容, 参数**len**则为数据长度。

参数flags一般设0, 其他数值定义如下

- MSG_OOB 传送的数据以out-of-band 送出。
- MSG_DONTROUTE 取消路由表查询
- MSG_DONTWAIT 设置为不可阻断运作
- MSG_NOSIGNAL 此动作不愿被SIGPIPE 信号中断。

返回值：

成功则返回实际传送出去的字符数, 失败返回-1。错误原因存于errno

### 字节序转换

#### inet_pton

```c
#include <arpa/inet.h>

int inet_pton(int af, const char *src, void *dst);
```

描述：

用于将一个 IPv4 或 IPv6 的网络地址从文本格式转换为二进制格式。

参数：

- **af** 参数指定了地址族，可以是 AF_INET 表示 IPv4 地址族，也可以是 AF_INET6 表示 IPv6 地址族；
- **src** 参数是一个字符串指针，表示待转换的网络地址；
- **dst** 参数是一个 void 指针，指向一个用于存储转换结果的缓冲区。

返回值：

函数返回值为 1 表示转换成功，0 表示 src 参数不是有效的网络地址，-1 表示发生错误，具体的错误信息可以通过 errno 变量获取。

#### inet_pton

```c
const char *inet_ntop(int af, const void *src, char *dst, socklen_t size);
```

描述：

`inet_ntop`是一个用于将网络字节序的IP地址转换为字符串表示（本地字节序）的函数。

`inet_ntop`函数将网络字节序的IP地址转换为字符串表示，并将结果存储在`dst`指向的缓冲区中。转换后的IP地址字符串的格式取决于地址族的类型。

参数：

- `af`：地址族（Address Family），指定了要转换的IP地址的类型。常见的值有`AF_INET`（IPv4）和`AF_INET6`（IPv6）。
- `src`：指向存储要转换的IP地址的内存块的指针。这个内存块的大小取决于地址族的类型。
- `dst`：指向存储转换后IP地址的字符串的缓冲区的指针。
- `size`：缓冲区的大小，用于防止缓冲区溢出。

返回值：

函数的返回值是一个指向转换后的IP地址字符串的指针，即`dst`指针。如果转换成功，返回值指向`dst`指针；如果发生错误，返回值为NULL，并且可以通过检查全局变量`errno`来获取错误的具体原因。

#### htons

```
uint16_t htons(uint16_t hostshort);
```

描述：

htons() 是一个网络字节序转换函数，用于将16位的主机字节序转换为网络字节序（大端字节序）。通常在网络编程中使用，以保证在不同机器之间传输数据时字节序的一致性。

参数：

**hostshort** 表示需要转换的16位主机字节序整数、

返回值：

函数返回值为转换后的网络字节序整数。

#### ntohs

```c
uint16_t ntohs(uint16_t netshort);
```

描述：

`ntohs`函数将网络字节序的16位无符号整数转换为主机字节序（本机字节序）的16位无符号整数，

参数：

- `netshort`：网络字节序的16位无符号整数。

返回：

并返回转换后的结果。

## epoll

### epoll_wait

描述：

epoll_wait 是 Linux 下使用 epoll I/O 多路复用机制时的一个系统调用函数，用于等待事件就绪并获取已就绪的事件。

```c++
int epoll_wait(int epfd, struct epoll_event *events, int maxevents, int timeout);
```
参数说明：
- `epfd`：epoll 文件描述符，由 epoll_create 或 epoll_create1 返回的文件描述符。
- `events`：指向 epoll_event 结构体数组的指针，用于存储返回的已就绪事件。
- `maxevents`：`events` 数组的长度，即最多能够存储的事件个数。
- `timeout`：超时时间，单位是毫秒。如果传入负值，则表示无限等待；如果传入 0，则表示立即返回，不阻塞；如果传入正值，则表示等待的时间上限。

函数返回值：
- 成功时，返回已就绪的事件个数。
- 失败时，返回 -1，并设置 errno 来指示错误类型。

epoll_wait 函数会阻塞等待，直到有事件就绪或者超过指定的超时时间。当有事件就绪时，将把已就绪的事件从内核事件表复制到 `events` 数组中，并返回已就绪的事件个数。

每个 `events` 中的 epoll_event 结构体包含了就绪事件的相关信息，比如文件描述符、事件类型和用户定义的数据等。

应用程序需要根据返回的已就绪事件进行相应的处理，例如读写数据、关闭连接等。

总结：epoll_wait 是使用 epoll I/O 多路复用机制时的系统调用函数，用于等待事件就绪并获取已就绪的事件。通过传入 epoll 文件描述符和事件数组，可以获取到已就绪的事件信息，并进行相应的处理。