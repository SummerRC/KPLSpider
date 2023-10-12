# version3.0: 用virtualenv构建编译环境(还多了1M)
# 第一阶段
# 基于的基础镜像，注意slim、Alphine、buster的区别
FROM python:3.7.8-buster AS builder-image
WORKDIR /py_venv
COPY requirements.txt .
ENV PATH="/py_venv/bin:$PATH"
RUN python -m venv --copies /py_venv &&\
    pip3 install --no-cache-dir -r requirements.txt -i https://pypi.tuna.tsinghua.edu.cn/simple


# 第二阶段
# 选择小一点的基础镜像
FROM python:3.7.8-slim as code_image
ENV PATH=/py_venv/bin:$PATH
WORKDIR /app
COPY . /app
COPY --from=builder-image /py_venv /py_venv
# 1、创建logparser需要的目录，在运行logparser需要的目录时指定该目录
# 2、添加文件的执行权限
# 3、修改时区，否则时间不准
RUN mkdir ./logs &&\
    chmod +x /app/run.sh &&\
    /bin/cp /usr/share/zoneinfo/Asia/Shanghai /etc/localtime && echo 'Asia/Shanghai' >/etc/timezone
# 指定监控的端口
EXPOSE 6800 5000
ENTRYPOINT ["/app/run.sh"]