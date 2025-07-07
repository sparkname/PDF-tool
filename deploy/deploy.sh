#!/bin/bash

# 一键部署脚本 - PDF转Word转换器
# 适用于Ubuntu/Debian系统

echo "=== PDF转Word转换器一键部署脚本 ==="
echo "正在为域名 fakelin.cn 部署服务..."

# 检查是否为root用户
if [ "$EUID" -eq 0 ]; then
    echo "请不要使用root用户运行此脚本"
    exit 1
fi

# 更新系统
echo "正在更新系统包..."
sudo apt update && sudo apt upgrade -y

# 安装必要软件
echo "正在安装Docker..."
if ! command -v docker &> /dev/null; then
    curl -fsSL https://get.docker.com -o get-docker.sh
    sudo sh get-docker.sh
    sudo usermod -aG docker $USER
    rm get-docker.sh
fi

echo "正在安装Docker Compose..."
if ! command -v docker-compose &> /dev/null; then
    sudo curl -L "https://github.com/docker/compose/releases/download/v2.20.0/docker-compose-$(uname -s)-$(uname -m)" -o /usr/local/bin/docker-compose
    sudo chmod +x /usr/local/bin/docker-compose
fi

# 安装Nginx
echo "正在安装Nginx..."
sudo apt install nginx -y

# 构建并启动Docker容器
echo "正在构建Docker镜像..."
docker-compose build

echo "正在启动服务..."
docker-compose up -d

# 配置Nginx
echo "正在配置Nginx..."
sudo tee /etc/nginx/sites-available/fakelin.cn > /dev/null <<EOF
server {
    listen 80;
    server_name fakelin.cn www.fakelin.cn;
    
    # 文件上传限制
    client_max_body_size 100M;
    
    location / {
        proxy_pass http://localhost:5000;
        proxy_set_header Host \$host;
        proxy_set_header X-Real-IP \$remote_addr;
        proxy_set_header X-Forwarded-For \$proxy_add_x_forwarded_for;
        proxy_set_header X-Forwarded-Proto \$scheme;
        proxy_connect_timeout 60s;
        proxy_send_timeout 60s;
        proxy_read_timeout 60s;
    }
}
EOF

# 启用站点
sudo ln -sf /etc/nginx/sites-available/fakelin.cn /etc/nginx/sites-enabled/
sudo rm -f /etc/nginx/sites-enabled/default

# 测试Nginx配置
sudo nginx -t

if [ $? -eq 0 ]; then
    sudo systemctl reload nginx
    echo "Nginx配置成功！"
else
    echo "Nginx配置错误，请检查配置文件"
    exit 1
fi

# 安装Certbot用于SSL证书
echo "正在安装SSL证书工具..."
sudo apt install certbot python3-certbot-nginx -y

echo ""
echo "=== 部署完成 ==="
echo "下一步操作："
echo "1. 确保域名 fakelin.cn 已解析到此服务器IP"
echo "2. 运行以下命令申请SSL证书："
echo "   sudo certbot --nginx -d fakelin.cn -d www.fakelin.cn"
echo ""
echo "服务状态检查："
echo "   docker-compose ps"
echo "   docker-compose logs"
echo ""
echo "访问地址: http://fakelin.cn"
echo "管理员面板: http://fakelin.cn/admin"
