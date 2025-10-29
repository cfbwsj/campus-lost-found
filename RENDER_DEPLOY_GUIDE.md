# 🚀 Render.com 免费部署教程（推荐）

## 为什么选择Render？

- ✅ **完全免费** - 无需信用卡
- ✅ **无限制** - 不需要验证
- ✅ **简单快速** - 5分钟部署
- ✅ **功能完整** - 免费PostgreSQL数据库
- ✅ **自动部署** - Git推送自动更新

---

## 📋 部署步骤（5分钟）

### Step 1: 注册Render账号 (1分钟)

1. **打开浏览器**，访问：
   ```
   https://render.com
   ```

2. 点击右上角 **"Get Started"** 或 **"Sign Up"**

3. 选择 **"Sign up with GitHub"**
   - 使用您的GitHub账号登录
   - 点击 "Authorize Render"

4. ✅ 注册完成！

---

### Step 2: 创建PostgreSQL数据库 (1分钟)

1. 在Render控制台，点击 **"New +"** 按钮

2. 选择 **"PostgreSQL"**

3. 填写信息：
   - **Name**: `campus-database`
   - **Database**: `campus_db`
   - **User**: `campus_user`
   - **Region**: 选择离您最近的（推荐 Singapore）
   - **Plan**: 选择 **"Free"**

4. 点击 **"Create Database"**

5. 等待约30秒，数据库创建完成

6. 进入数据库详情页，找到 **"Internal Database URL"**
   - 点击复制按钮 📋
   - 格式类似：`postgresql://campus_user:xxxx@dpg-xxx.singapore-postgres.render.com/campus_db`
   - **保存到记事本**，后面要用！

✅ 数据库创建完成！

---

### Step 3: 部署后端服务 (2分钟)

1. 回到Render控制台，点击 **"New +"**

2. 选择 **"Web Service"**

3. 选择 **"Connect a repository"**
   - 如果是第一次，需要授权Render访问GitHub
   - 点击 "Configure account"
   - 选择 "All repositories" 或只选择 `campus-lost-found`
   - 点击 "Install"

4. 在仓库列表中找到 **"campus-lost-found"**，点击 **"Connect"**

5. 填写配置信息：

   **基本设置**：
   - **Name**: `campus-backend`
   - **Region**: Singapore（或您选择的区域）
   - **Branch**: `main`
   - **Root Directory**: `backend`
   - **Runtime**: `Python 3`
   - **Build Command**: 
     ```
     pip install -r requirements.txt
     ```
   - **Start Command**: 
     ```
     uvicorn main:app --host 0.0.0.0 --port $PORT
     ```

6. 向下滚动，选择 **"Free"** 套餐

7. 点击 **"Advanced"** 展开高级选项

8. 添加环境变量（点击 "Add Environment Variable"）：

   | Key | Value |
   |-----|-------|
   | `DATABASE_URL` | *粘贴Step 2复制的数据库URL* |
   | `ELASTICSEARCH_HOST` | `localhost` |
   | `REDIS_URL` | `redis://localhost:6379` |
   | `PYTHON_VERSION` | `3.9.18` |

9. 点击 **"Create Web Service"**

10. 等待2-3分钟，Render开始构建和部署

11. 部署成功后，会显示您的后端URL：
    ```
    https://campus-backend.onrender.com
    ```
    **保存这个URL！**

✅ 后端部署完成！

---

### Step 4: 部署前端 (1分钟)

#### 方式A: 使用Render部署静态网站

1. 点击 **"New +"** → **"Static Site"**

2. 选择 **"campus-lost-found"** 仓库

3. 填写配置：
   - **Name**: `campus-frontend`
   - **Branch**: `main`
   - **Root Directory**: `frontend`
   - **Build Command**: 
     ```
     npm install && npm run build
     ```
   - **Publish Directory**: `build`

4. 添加环境变量：
   | Key | Value |
   |-----|-------|
   | `REACT_APP_API_URL` | *粘贴Step 3的后端URL* |

5. 点击 **"Create Static Site"**

6. 等待3-5分钟编译

7. 部署完成！您的网站地址：
   ```
   https://campus-frontend.onrender.com
   ```

#### 方式B: 使用Vercel部署前端（更快）

1. 访问 https://vercel.com

2. 点击 **"Sign Up"** → **"Continue with GitHub"**

3. 点击 **"Import Project"**

4. 选择 **"campus-lost-found"** 仓库

5. 配置：
   - **Framework Preset**: Create React App
   - **Root Directory**: `frontend`
   - **Build Command**: `npm run build`
   - **Output Directory**: `build`

6. 添加环境变量：
   - Name: `REACT_APP_API_URL`
   - Value: *后端URL*

7. 点击 **"Deploy"**

8. 1分钟后部署完成！

✅ 前端部署完成！

---

## 🎉 部署完成！

### 您的网站地址：

**前端网站**：
```
https://campus-frontend.onrender.com
```
或
```
https://campus-lost-found.vercel.app
```

**后端API文档**：
```
https://campus-backend.onrender.com/docs
```

---

## ⚠️ 重要提示

### Render免费套餐限制：

**优点**：
- ✅ 完全免费
- ✅ 无需信用卡
- ✅ 自动HTTPS
- ✅ 免费PostgreSQL

**注意事项**：
- ⚠️ 15分钟无访问会自动休眠
- ⚠️ 休眠后首次访问需要30-60秒唤醒
- ⚠️ 每月750小时免费运行时间（约31天）

### 解决休眠问题（可选）：

使用免费的定时Ping服务保持唤醒：

1. 访问 https://cron-job.org
2. 注册账号
3. 创建新任务：
   - URL: 您的后端健康检查地址
   - 频率: 每10分钟
4. 这样服务就不会休眠了！

---

## 🔧 故障排除

### 问题1: 后端部署失败

**查看日志**：
1. 点击后端服务
2. 查看 "Logs" 标签
3. 找到错误信息

**常见错误**：
- Python版本：确保使用Python 3.9
- 依赖问题：检查 `requirements.txt`
- 端口配置：必须使用 `$PORT`

### 问题2: 前端空白页

**检查API地址**：
1. 确保 `REACT_APP_API_URL` 正确
2. URL格式：`https://campus-backend.onrender.com`（无斜杠）
3. 修改后需要重新部署

### 问题3: 数据库连接失败

**检查连接字符串**：
1. 使用 "Internal Database URL" 而不是 "External"
2. 格式：`postgresql://...`
3. 确保复制完整

---

## 📊 免费额度说明

### Render Free套餐：

✅ **Web Service**:
- 512 MB RAM
- 0.1 CPU
- 每月750小时（约31天）

✅ **PostgreSQL**:
- 1 GB 存储
- 自动备份（保留90天）
- 无连接数限制

✅ **Static Site**:
- 无限流量
- 100 GB带宽/月
- 自动CDN

**总结**：完全够用，完全免费！

---

## 🎓 添加到简历

**项目展示**：
```
项目名称：校园失物招领系统
在线演示：https://campus-frontend.onrender.com
API文档：https://campus-backend.onrender.com/docs
源码地址：https://github.com/cfbwsj/campus-lost-found

技术栈：
- 前端：React 18 + Ant Design
- 后端：Python FastAPI + SQLAlchemy
- 数据库：PostgreSQL
- AI技术：PyTorch (物品识别) + Tesseract (OCR)
- 搜索：ElasticSearch
- 部署：Render + Vercel

项目特色：
- 实现OCR文字识别功能
- AI智能物品分类
- 模糊搜索引擎
- 前后端分离架构
- RESTful API设计
- Docker容器化
```

---

## 🔄 更新部署

修改代码后：

```bash
git add .
git commit -m "更新功能"
git push
```

Render会自动检测并重新部署！

---

## 💡 提示

1. **首次访问较慢**：免费套餐休眠后需要30秒唤醒
2. **保持唤醒**：使用cron-job.org定时ping
3. **数据库备份**：定期导出数据
4. **监控日志**：在Render控制台查看实时日志

---

**祝您部署顺利！** 🎉

