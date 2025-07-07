@echo off
echo === PDF转Word转换器 Windows部署脚本 ===
echo.

REM 检查Docker是否安装
docker --version >nul 2>&1
if %errorlevel% neq 0 (
    echo 请先安装Docker Desktop for Windows
    echo 下载地址: https://www.docker.com/products/docker-desktop
    pause
    exit /b 1
)

REM 检查Docker Compose是否可用
docker-compose --version >nul 2>&1
if %errorlevel% neq 0 (
    echo Docker Compose未找到，请确保Docker Desktop已正确安装
    pause
    exit /b 1
)

echo 正在构建Docker镜像...
docker-compose build

if %errorlevel% neq 0 (
    echo Docker构建失败
    pause
    exit /b 1
)

echo 正在启动服务...
docker-compose up -d

if %errorlevel% neq 0 (
    echo 服务启动失败
    pause
    exit /b 1
)

echo.
echo === 部署完成 ===
echo 本地访问地址: http://localhost
echo.
echo 查看服务状态: docker-compose ps
echo 查看日志: docker-compose logs
echo 停止服务: docker-compose down
echo.

REM 等待服务启动
timeout /t 5 /nobreak >nul

REM 检查服务是否正常运行
curl -s http://localhost >nul 2>&1
if %errorlevel% equ 0 (
    echo 服务正在正常运行！
    echo 正在打开浏览器...
    start http://localhost
) else (
    echo 服务可能还在启动中，请稍等片刻后访问 http://localhost
)

pause
