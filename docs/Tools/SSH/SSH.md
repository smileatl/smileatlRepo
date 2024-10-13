## 1、ssh免密登录

[vscode远程连接服务器、免密码设置_vscode gitlen 到期要登录-CSDN博客](https://blog.csdn.net/qq_38925891/article/details/113100361)

正常就是公钥/私钥那一套

还是不行，就在本地的~/.ssh/config文件中按照对应ip增加内容，主要就是密钥文件的路径

```config
Host 10.60.23.154
  HostName 10.60.23.154
  User lsl
  PreferredAuthentications publickey
  IdentityFile D:/Users/yl6306/.ssh/centossshkey/id_rsa
```

## 2、github的ssh出问题

如果没有找到，也是要去config里添加私钥

```config
Host github.com
  HostName github.com
  User smileatl
  IdentityFile D:/Users/yl6306/.ssh/githubsshkey/id_rsa
```

