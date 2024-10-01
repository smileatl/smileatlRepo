# conda创建删除环境

```bash
# 创建
conda create -n env_name python=x.x
# 删除
conda remove -n env_name --all

```



# conda激活环境、关闭环境

```bash
activate envname
conda activate envname   //在windows和linux下好像都不行
source activate envname



deactivate envname
conda deactivate envname
source deactivate envname
```

 

#  查看环境

```bash
conda info -e
```

