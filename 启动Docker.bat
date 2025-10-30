@echo off
chcp 65001 > nul
echo ========================================
echo 校园失物招领系统 - Docker启动
echo ========================================
echo.

cd /d D:\AIweb\campus-lost-found

echo [1/4] 检查Docker是否运行...
docker version >nul 2>&1
if %errorlevel% neq 0 (
    echo ❌ Docker未运行，请先启动Docker Desktop
    pause
    exit /b 1
)
echo ✅ Docker运行正常

echo.
echo [2/4] 拉取基础镜像...
docker pull postgres:13-alpine
docker pull elasticsearch:7.17.0
docker pull redis:6-alpine
docker pull python:3.9-slim
docker pull node:18-alpine

echo.
echo [3/4] 构建并启动所有服务...
docker-compose up -d --build

echo.
echo [4/4] 等待服务启动...
timeout /t 10 /nobreak > nul

echo.
echo ========================================
echo ✅ 所有服务已启动！
echo ========================================
echo.
echo 📊 服务地址：
echo   前端：http://localhost:3000
echo   后端：http://localhost:8000
echo   API文档：http://localhost:8000/docs
echo.
echo 📂 数据库管理：
echo   数据库：PostgreSQL
echo   地址：localhost:5432
echo   用户：postgres
echo   密码：password
echo   数据库：campus_db
echo.
echo 🔧 查看日志：
echo   docker-compose logs -f
echo.
echo 🛑 停止服务：
echo   docker-compose down
echo.
pause

