# Ubuntu20.04 下如何安装 Docker

1. 更新软件包索引:
sudo apt-get update
sudo apt-get install apt-transport-https ca-certificates curl gnupg lsb-release

2. 添加 Docker 的官方 GPG 密钥:
curl -fsSL https://download.docker.com/linux/ubuntu/gpg | sudo gpg --dearmor -o /usr/share/keyrings/docker-archive-keyring.gpg

3. 设置 Docker 仓库:
```
echo \
"deb [arch=$(dpkg --print-architecture) signed-by=/usr/share/keyrings/docker-archive-keyring.gpg] https://download.docker.com/linux/ubuntu \
$(lsb_release -cs) stable" | sudo tee /etc/apt/sources.list.d/docker.list > /dev/null
```
4. 再次更新软件包索引,安装 Docker
```
sudo apt-get update
sudo apt-get install docker-ce docker-ce-cli containerd.io
```

5. 验证 Docker 是否安装成功
```
docker --version   
```


# 如何使用
1. 启动：sudo systemctl start docker
2. 构建镜像： sudo docker build -t intellif-buildroot .
3. 查看镜像：sudo docker images
4. 运行镜像：sudo docker run  -it intellif-buildroot /bin/bash
5. 保存镜像：sudo docker save -o intellif-buildroot.tar intellif-buildroot:latest
6. gzip压缩：gzip intellif-buildroot.tar

