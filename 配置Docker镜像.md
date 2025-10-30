# 🔧 配置Docker镜像加速器

## 问题原因
Docker Hub官方源在国内访问受限，需要配置镜像加速器。

---

## ✅ 解决方案：配置Docker Desktop镜像

### 步骤1：打开Docker Desktop设置
1. 右键点击Docker Desktop图标
2. 选择 "Settings"（设置）

### 步骤2：配置镜像加速器
1. 点击左侧 "Docker Engine"
2. 在JSON配置中添加以下内容：

```json
{
  "registry-mirrors": [
    "https://docker.1ms.run",
    "https://docker.wanpeng.top",
    "https://docker.chenby.cn"
  ],
  "builder": {
    "gc": {
      "defaultKeepStorage": "20GB",
      "enabled": true
    }
  },
  "experimental": false
}
```

### 步骤3：应用并重启
1. 点击 "Apply & Restart"
2. 等待Docker重启完成（约30秒）

---

## 🚀 重新启动构建

Docker重启后，运行：

```powershell
cd D:\AIweb\campus-lost-found
docker-compose up -d --build
```

或双击：
```
启动Docker.bat
```

---

## 📊 预计时间

配置镜像加速后：
- 拉取镜像：2-5分钟（大幅加快）
- 构建总时间：15-20分钟

---

## ⚠️ 如果还是失败

### 方案1：使用备用镜像源

在Docker Engine配置中替换为：

```json
{
  "registry-mirrors": [
    "https://hub.rat.dev",
    "https://docker.1panel.live"
  ]
}
```

### 方案2：手动拉取镜像

```bash
# 拉取Python镜像
docker pull python:3.9-slim

# 拉取Node镜像  
docker pull node:18-alpine

# 拉取其他镜像
docker pull postgres:13-alpine
docker pull elasticsearch:7.17.0
docker pull redis:6-alpine
docker pull nginx:alpine
```

然后再运行：
```bash
docker-compose up -d --build
```

---

## 💡 验证镜像加速是否生效

```bash
docker info
```

查看输出中是否有：
```
Registry Mirrors:
  https://docker.1ms.run/
```

如果有，说明配置成功！

---

**现在去配置Docker镜像加速器，然后重新启动！** 🚀

