# yml

## 续行符

yml文件中的续行符。同Bash或其他shell脚本中的长命令，使用

```
\
```

## rsync

### --inplace 

使用 `--inplace` 选项可以避免 `rsync` 生成临时文件，直接对目标文件进行覆盖，从而减少文件 "消失" 的机会

在我的实践中有效避免了file has vanished的出现

### --delete

如果目标是让目标目录和源目录保持一致（包括文件的删除），`--delete` 会有用。当源目录中某些文件被删除时，`--delete` 会在目标目录中删除这些文件。

在我的实践中无法避免file has vanishe的问题，但是这个参数挺符合我的用法，可以两个参数一起用`--inplace --delete`
