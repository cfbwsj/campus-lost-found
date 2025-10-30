@echo off
chcp 65001 > nul
echo ========================================
echo ⚠️  清理Docker数据（会删除所有数据）
echo ========================================
echo.
echo 此操作将：
echo - 停止所有容器
echo - 删除所有容器
echo - 删除所有卷（数据库数据将丢失）
echo - 删除所有镜像
echo.
set /p confirm="确认清理？(输入 YES 继续): "
if /i not "%confirm%"=="YES" (
    echo 已取消
    pause
    exit /b 0
)

echo.
cd /d D:\AIweb\campus-lost-found

echo [1/4] 停止所有服务...
docker-compose down

echo [2/4] 删除所有卷...
docker-compose down -v

echo [3/4] 删除未使用的镜像...
docker image prune -a -f

echo [4/4] 清理系统...
docker system prune -a -f

echo.
echo ✅ 清理完成
echo.
pause

