# Render 部署完整指南

## 📋 前置准备

1. GitHub 仓库已推送最新代码
2. Render 账号（https://render.com）

## 🚀 快速部署（3步）

### 1️⃣ 创建 PostgreSQL 数据库

1. Render Dashboard → "New +" → **PostgreSQL**
2. 配置：
   - Name: `campus-database`
   - Database: `campus_db`
   - User: `campus_user`
   - Plan: **Free**
3. 创建后，复制 **Internal Database URL**

### 2️⃣ 部署后端（Docker方式）

1. Render Dashboard → "New +" → **Web Service**
2. 连接 GitHub：`cfbwsj/campus-lost-found`
3. 配置：

   **必须配置：**
   ```
   Name: campus-backend
   Environment: Docker
   Region: 选择与数据库相同区域
   Branch: main
   Root Directory: backend
   Dockerfile Path: Dockerfile
   ```

   **环境变量：**
   ```
   DATABASE_URL = <步骤1复制的PostgreSQL URL>
   BASE_URL = https://campus-backend-xxxx.onrender.com （先填占位，部署后更新）
   ELASTICSEARCH_HOST = （留空）
   REDIS_URL = （留空）
   JWT_SECRET = <生成随机字符串>
   ```

4. 创建并等待部署（约5-10分钟）
5. 部署成功后，复制给你的 URL，更新 `BASE_URL` 环境变量

### 3️⃣ 初始化数据库和默认账号

部署成功后，执行一次初始化：

```bash
# 通过 Render Dashboard 的 Shell 或 curl 触发
curl https://your-backend-url.onrender.com/health
```

后端启动时会自动：
- 创建表结构
- 添加 `owner_id` 字段（如果不存在）
- 创建默认管理员账号：`admin` / `123456`

## ⚙️ 重要配置说明

### 环境变量详解

| 变量名 | 值 | 说明 |
|--------|-----|------|
| `DATABASE_URL` | PostgreSQL 连接串 | 必须从 Render 数据库服务复制 |
| `BASE_URL` | 后端完整URL | 用于生成文件访问链接 |
| `JWT_SECRET` | 随机字符串 | 用于JWT token签名 |
| `PORT` | 10000 | Render 自动设置，无需手动配置 |

### 数据库初始化

后端首次启动会自动：
1. 创建所有表（users, lost_items, found_items）
2. 为已有表添加 `owner_id` 列（如果不存在）
3. 创建默认管理员账号（如果不存在）

### 静态文件存储

⚠️ **注意**：Render 免费层的磁盘是**临时**的，容器重启后上传的文件会丢失。

**解决方案：**
1. **开发测试**：接受数据丢失，测试功能
2. **生产环境**：使用外部存储（AWS S3、Cloudinary、或升级到 Render 付费计划启用持久磁盘）

## 🔍 验证部署

### 1. 健康检查
```
curl https://your-backend-url.onrender.com/health
```
应返回：`{"status":"healthy","message":"Service is running normally"}`

### 2. API 文档
访问：`https://your-backend-url.onrender.com/docs`

### 3. 测试登录
```bash
curl -X POST https://your-backend-url.onrender.com/api/auth/login \
  -H "Content-Type: application/x-www-form-urlencoded" \
  -d "username=admin&password=123456"
```
应返回 token。

## 🐛 常见问题

### Q1: 部署失败，日志显示 "ModuleNotFoundError"
**A**: 确保 `backend/requirements.txt` 包含所有依赖，特别是 `PyJWT==2.8.0`

### Q2: 数据库连接失败
**A**: 
- 检查 `DATABASE_URL` 是否使用 **Internal Database URL**（不是 External）
- 确保数据库和后端在同一区域

### Q3: CORS 错误
**A**: 
- 检查 `BASE_URL` 是否正确设置为后端完整 URL
- 确认后端 `main.py` 中 CORS 配置包含前端域名

### Q4: 上传文件后找不到
**A**: Render 免费层磁盘是临时的，容器重启后文件丢失。需要外部存储或升级计划。

### Q5: 服务休眠
**A**: Render 免费层服务 15 分钟无访问会休眠，首次访问需要等待约 30 秒唤醒。

## 📝 前端部署建议

前端建议使用 **Vercel** 或 **Netlify**：

### Vercel 部署
1. 访问 https://vercel.com
2. 导入 GitHub 仓库
3. 配置：
   - Framework Preset: Create React App
   - Root Directory: `frontend`
   - Build Command: `npm run build`
   - Output Directory: `build`
   - 环境变量：`REACT_APP_API_URL=https://your-backend-url.onrender.com`

### 或 Netlify 部署
类似配置，使用 Netlify 的自动构建。

## 🎯 最终检查清单

- [ ] PostgreSQL 数据库已创建并运行
- [ ] 后端服务已部署（Docker方式）
- [ ] 环境变量已正确配置
- [ ] 健康检查通过
- [ ] 可以访问 `/docs` API 文档
- [ ] 可以成功登录（admin/123456）
- [ ] 前端已部署并配置后端URL

## 📞 需要帮助？

查看详细排障文档：`DEPLOY_TROUBLESHOOTING_REPORT.md`

