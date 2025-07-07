# 部署指南 - PDF转Word转换器

## 项目概述
这是一个基于Flask的PDF转Word在线转换工具，支持PDF到Word和Word到PDF的双向转换。

## 部署选项

### 1. 使用云服务器部署（推荐）

#### 1.1 购买云服务器
- 阿里云ECS、腾讯云CVM、华为云ECS等
- 配置建议：1核2G内存，系统盘40GB
- 操作系统：Ubuntu 20.04 LTS

#### 1.2 服务器配置步骤

```bash
# 1. 更新系统
sudo apt update && sudo apt upgrade -y

# 2. 安装Docker
curl -fsSL https://get.docker.com -o get-docker.sh
sudo sh get-docker.sh
sudo usermod -aG docker $USER

# 3. 安装Docker Compose
sudo curl -L "https://github.com/docker/compose/releases/download/v2.20.0/docker-compose-$(uname -s)-$(uname -m)" -o /usr/local/bin/docker-compose
sudo chmod +x /usr/local/bin/docker-compose

# 4. 重新登录以应用Docker组权限
exit
# 重新SSH登录

# 5. 克隆项目代码
git clone <your-repo-url> pdf-converter
cd pdf-converter

# 6. 构建并启动服务
docker-compose up -d

# 7. 检查服务状态
docker-compose ps
docker-compose logs
```

#### 1.3 域名解析配置
1. 登录您的域名管理面板
2. 添加A记录：
   - 主机记录：@ (或www)
   - 记录类型：A
   - 记录值：您的服务器公网IP
   - TTL：600

#### 1.4 安装SSL证书（HTTPS）
```bash
# 安装Nginx和Certbot
sudo apt install nginx certbot python3-certbot-nginx -y

# 配置Nginx
sudo nano /etc/nginx/sites-available/fakelin.cn
```

Nginx配置文件内容：
```nginx
server {
    listen 80;
    server_name fakelin.cn www.fakelin.cn;
    
    location / {
        proxy_pass http://localhost:5000;
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
        proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
        proxy_set_header X-Forwarded-Proto $scheme;
    }
}
```

```bash
# 启用站点
sudo ln -s /etc/nginx/sites-available/fakelin.cn /etc/nginx/sites-enabled/
sudo nginx -t
sudo systemctl reload nginx

# 申请SSL证书
sudo certbot --nginx -d fakelin.cn -d www.fakelin.cn
```

### 2. 使用Vercel部署（免费）

#### 2.1 准备Vercel配置
创建 `vercel.json` 文件：

```json
{
  "version": 2,
  "builds": [
    {
      "src": "simple_web.py",
      "use": "@vercel/python"
    }
  ],
  "routes": [
    {
      "src": "/(.*)",
      "dest": "simple_web.py"
    }
  ]
}
```

#### 2.2 部署步骤
1. 将代码推送到GitHub
2. 在Vercel官网注册并连接GitHub
3. 导入项目并部署
4. 在Vercel中配置自定义域名 `fakelin.cn`

### 3. 使用Heroku部署

```bash
# 安装Heroku CLI
# 登录Heroku
heroku login

# 创建应用
heroku create your-app-name

# 设置环境变量
heroku config:set FLASK_ENV=production

# 部署
git add .
git commit -m "Deploy to Heroku"
git push heroku main

# 配置自定义域名
heroku domains:add fakelin.cn
```

## 环境变量配置

在生产环境中设置以下环境变量：

```bash
export FLASK_ENV=production
export SECRET_KEY=your-secret-key-here
export PORT=5000
```

## 安全建议

1. 设置强密码的secret_key
2. 限制文件上传大小
3. 定期清理临时文件
4. 配置防火墙规则
5. 启用HTTPS
6. 定期备份数据

## 监控和维护

1. 设置日志记录
2. 配置监控告警
3. 定期更新依赖包
4. 备份重要数据

## 故障排除

### 常见问题
1. 端口被占用：修改docker-compose.yml中的端口映射
2. 内存不足：增加服务器内存或优化代码
3. 文件权限问题：检查uploads和converted目录权限

### 日志查看
```bash
# Docker日志
docker-compose logs -f

# Nginx日志
sudo tail -f /var/log/nginx/error.log
sudo tail -f /var/log/nginx/access.log
```

## 联系信息
如需技术支持，请联系系统管理员。
