@echo off
chcp 65001 > nul
echo ========================================
echo Docker镜像加速配置助手
echo ========================================
echo.
echo 请按以下步骤操作：
echo.
echo 1. 打开Docker Desktop
echo 2. 点击右上角设置图标（齿轮）
echo 3. 选择 "Docker Engine"
echo 4. 在JSON配置中添加以下内容：
echo.
echo {
echo   "registry-mirrors": [
echo     "https://docker.1ms.run",
echo     "https://docker.wanpeng.top",
echo     "https://docker.chenby.cn"
echo   ]
echo }
echo.
echo 5. 点击 "Apply & Restart"
echo 6. 等待Docker重启完成
echo.
echo ========================================
echo.
echo 配置完成后，按任意键继续构建...
pause > nul
echo.
echo 开始构建...
docker-compose up -d --build
pause

