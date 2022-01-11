#!/bin/bash
REVISION=$(git rev-parse --short HEAD)

docker build -t dockerhub.qingcloud.com/eachchat/sydent:$REVISION -f docker/Dockerfile-pro .
# 镜像推送 此命令会推送打包好的镜像到仓库
docker push dockerhub.qingcloud.com/eachchat/sydent:$REVISION
