# mkdocs

## mkdocs serve

mkdocs启动本地服务，可以进行调试

**出现错误**

self.socket.bind(self.server_address) OSError: [WinError 10013] 

这是因为酷狗音乐的默认端口号也是8000，导致冲突

**解决办法**

启动时自己指定端口

```shell
mkdocs serve -a 127.0.0.1:8080
```

