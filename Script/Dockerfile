# 基础镜像
FROM python:3.9-slim-buster as sadas

# 将本地文件夹复制到容器内的工作目录
COPY . /app

# 设置工作目录
WORKDIR /app

# 安装应用程序依赖
RUN pip install --no-cache-dir -r requirements.txt

# 入口命令
CMD ["python", "app.py"]