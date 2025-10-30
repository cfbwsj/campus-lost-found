@echo off
chcp 65001 > nul
echo ========================================
echo 停止所有Docker服务
echo ========================================
echo.

cd /d D:\AIweb\campus-lost-found

docker-compose down

echo.
echo ✅ 所有服务已停止
echo.
pause

