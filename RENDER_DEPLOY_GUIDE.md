# Render 部署指南

## 一、部署方式选择

**推荐：使用 Docker 方式部署后端**

原因：
- ✅ 与本地环境一致，包含所有系统依赖（Tesseract OCR、OpenCV 库等）
- ✅ 环境变量和启动命令统一
- ✅ 避免手动配置系统包

## 二、部署步骤

### 步骤 1：创建 PostgreSQL 数据库

1. 登录 Render Dashboard：https://dashboard.render.com
2. 点击 "New +" → "PostgreSQL"
3. 配置：
   - **Name**: `campus-database`
   - **Database**: `campus_db`
   - **User**: `campus_user`
   - **Plan**: Free
   - **Region**: 选择离你最近的区域
4. 创建后，**复制 Internal Database URL**（格式：`postgresql://user:password@host:5432/database`）

### 步骤 2：部署后端服务

1. 在 Render Dashboard，点击 "New +" → "Web Service"
2. 连接你的 GitHub 仓库：`https://github.com/cfbwsj/campus-lost-found`
3. 配置服务：

   **基本信息：**
   - **Name**: `campus-backend`
   - **Region**: 与数据库同一区域
   - **Branch**: `main`
   - **Root Directory**: `backend`
   - **Runtime**: `Docker` ⭐（重要！）

   **环境变量：**
   ```
   DATABASE_URL = <从步骤1复制的PostgreSQL内部URL>
   BASE_URL = https://campus-backend-xxxx.onrender.com （部署后会给你，先填占位符）
   ELASTICSEARCH_HOST = （留空，不使用ES）
   REDIS_URL = （留空，不使用Redis）
   JWT_SECRET = <随机生成的长字符串，如：your-super-secret-jwt-key-change-me>
   PORT = 10000 （Render自动设置，但可以显式指定）
   ```

   **构建和启动：**
   - **Dockerfile Path**: `Dockerfile`（在backend目录下）
   - **Docker Context**: `.`（backend目录作为上下文）

   **高级设置（可选）：**
   - **Health Check Path**: `/health`
   - **Auto-Deploy**: Yes（Git push自动部署）

4. 点击 "Create Web Service"
5. 等待构建完成（约 5-10 分钟）
6. 部署成功后，复制给你的 URL（如：`https://campus-backend-xxxx.onrender.com`）

### 步骤 3：更新 BASE_URL 环境变量

1. 回到后端服务设置
2. 编辑环境变量 `BASE_URL`，设置为你的实际后端 URL
3. 保存后服务会自动重启

### 步骤 4：部署前端（可选，推荐单独部署）

#### 选项 A：Render Static Site（推荐）

1. 在 Render Dashboard，点击 "New +" → "Static Site"
2. 连接 GitHub 仓库
！！！注意：静态文件使用 Render 免费层会自动休眠，15 分钟无访问会暂停。如需持久运行，请升级到付费计划。

#### 选项 B：Vercel/Netlify（更推荐用于前端）

前端更适合部署到 Vercel 或 Netlify：
- 免费层更稳定
- 自动 HTTPS
- CDN 加速
- 不会休眠

/node_modules
/.pnp
.pnp.js

# testing
/coverage

# production
/build

# misc
.DS_Store
.env.local
.env.development.local
.env.test.local
.env.production.local

npm-debug.log*
yarn-debug.log*
yarn-error.log*
