# 使用Python 3.11官方镜像
FROM python:3.11-slim

# 设置工作目录
WORKDIR /app

# 安装系统依赖
RUN apt-get update && apt-get install -y \
    libreoffice \
    && rm -rf /var/lib/apt/lists/*

# 复制requirements文件
COPY requirements.txt .

# 安装Python依赖
RUN pip install --no-cache-dir -r requirements.txt

# 复制应用代码
COPY . .

# 创建必要的目录
RUN mkdir -p uploads converted

# 暴露端口
EXPOSE 5000

# 设置环境变量
ENV FLASK_APP=simple_web.py
ENV FLASK_ENV=production

# 启动命令
CMD ["python", "simple_web.py"]
