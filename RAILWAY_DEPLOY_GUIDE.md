# 🚂 Railway.app 部署完整教程

## 📋 部署步骤总览

1. ✅ 注册Railway账号（2分钟）
2. ✅ 连接GitHub仓库（1分钟）
3. ✅ 部署数据库（2分钟）
4. ✅ 部署后端服务（3分钟）
5. ✅ 部署前端服务（2分钟）
6. ✅ 获取访问链接（1分钟）

**总计**: 约10分钟

---

## 🎯 步骤1: 注册Railway账号

### 操作步骤：

1. **打开浏览器**，访问：https://railway.app

2. **点击右上角 "Login"**

3. **选择 "Login with GitHub"**（使用您的GitHub账号登录）

4. **授权Railway访问您的GitHub**
   - 点击 "Authorize Railway"
   - 这样Railway就能访问您的仓库了

5. **完成！** 您现在已经登录Railway

---

## 🎯 步骤2: 创建新项目

### 操作步骤：

1. **点击 "New Project"** 按钮（紫色大按钮）

2. **选择 "Deploy from GitHub repo"**

3. **在列表中找到并点击**：
   ```
   cfbwsj/campus-lost-found
   ```

4. Railway会自动开始分析您的项目

---

## 🎯 步骤3: 添加PostgreSQL数据库

### 操作步骤：

1. **在项目面板中，点击 "+ New"**

2. **选择 "Database"**

3. **选择 "Add PostgreSQL"**

4. **等待数据库创建**（约30秒）

5. **复制数据库连接URL**：
   - 点击PostgreSQL服务
   - 进入 "Variables" 标签
   - 找到 `DATABASE_URL`
   - 点击复制按钮

6. **记下这个URL**，格式类似：
   ```
   postgresql://postgres:password@containers-us-west-xxx.railway.app:7432/railway
   ```

---

## 🎯 步骤4: 配置后端服务

### 操作步骤：

1. **找到backend服务**（Railway自动识别的）

2. **点击backend服务卡片**

3. **进入 "Settings" 标签**

4. **配置Root Directory**：
   - 找到 "Root Directory"
   - 输入：`backend`
   - 点击保存

5. **配置Start Command**：
   - 找到 "Start Command"
   - 输入：`uvicorn main:app --host 0.0.0.0 --port $PORT`
   - 点击保存

6. **进入 "Variables" 标签**，添加环境变量：

   点击 "+ New Variable"，逐个添加：

   ```
   变量名: DATABASE_URL
   变量值: (粘贴步骤3复制的数据库URL)
   ```

   ```
   变量名: ELASTICSEARCH_HOST
   变量值: localhost
   ```

   ```
   变量名: REDIS_URL
   变量值: redis://localhost:6379
   ```

7. **生成公开域名**：
   - 进入 "Settings" 标签
   - 找到 "Networking"
   - 点击 "Generate Domain"
   - 复制生成的域名，格式如：
     ```
     https://campus-backend-production-xxxx.up.railway.app
     ```

8. **等待部署完成**（约2-3分钟）
   - 在 "Deployments" 标签查看进度
   - 显示绿色 "SUCCESS" 即表示成功

---

## 🎯 步骤5: 配置前端服务

### 操作步骤：

1. **在项目面板中，点击 "+ New"**

2. **选择 "GitHub Repo"**

3. **再次选择 `cfbwsj/campus-lost-found`**

4. **点击新创建的服务**

5. **进入 "Settings" 标签**

6. **配置Root Directory**：
   - 找到 "Root Directory"
   - 输入：`frontend`
   - 点击保存

7. **配置Build Command**：
   - 找到 "Build Command"
   - 输入：`npm install && npm run build`
   - 点击保存

8. **配置Start Command**：
   - 找到 "Start Command"
   - 输入：`npx serve -s build -l $PORT`
   - 点击保存

9. **进入 "Variables" 标签**，添加环境变量：

   ```
   变量名: REACT_APP_API_URL
   变量值: (粘贴步骤4中后端的域名)
   ```

10. **生成公开域名**：
    - 进入 "Settings" 标签
    - 找到 "Networking"
    - 点击 "Generate Domain"
    - **这就是您的网站地址！** 格式如：
      ```
      https://campus-frontend-production-xxxx.up.railway.app
      ```

11. **等待部署完成**（约3-5分钟）

---

## 🎯 步骤6: 验证部署成功

### 检查后端：

1. 打开后端URL（步骤4复制的）
2. 添加 `/docs` 后缀，如：
   ```
   https://campus-backend-production-xxxx.up.railway.app/docs
   ```
3. 应该能看到API文档页面

### 检查前端：

1. 打开前端URL（步骤5复制的）
   ```
   https://campus-frontend-production-xxxx.up.railway.app
   ```
2. 应该能看到您的校园失物招领系统首页！

---

## 🎉 部署成功！

恭喜！您的网站已经成功部署到云端，全球任何人都可以访问！

### 您的访问地址：
- 📱 **前端网站**: `https://campus-frontend-production-xxxx.up.railway.app`
- 🔧 **后端API**: `https://campus-backend-production-xxxx.up.railway.app`
- 📖 **API文档**: `https://campus-backend-production-xxxx.up.railway.app/docs`

### 下一步可以做的：

1. **分享链接**：把前端URL分享给朋友访问
2. **添加到简历**：这是一个完整的全栈项目
3. **自定义域名**（可选）：Railway支持绑定自己的域名
4. **监控运行**：在Railway控制台查看访问日志

---

## 🔧 常见问题解决

### Q1: 部署失败怎么办？

**查看日志**：
1. 点击失败的服务
2. 进入 "Deployments" 标签
3. 点击失败的部署
4. 查看 "Build Logs" 或 "Deploy Logs"

**常见问题**：
- Python版本：确保使用Python 3.9+
- 依赖安装失败：检查 `requirements.txt`
- 端口配置：确保使用 `$PORT` 环境变量

### Q2: 前端显示404或空白页？

**检查API地址**：
1. 确保 `REACT_APP_API_URL` 设置正确
2. URL末尾不要加斜杠 `/`
3. 重新部署前端服务

### Q3: 数据库连接失败？

**检查连接URL**：
1. 确保 `DATABASE_URL` 复制完整
2. 格式应该是：`postgresql://...`
3. 在后端服务的Variables中重新设置

### Q4: 超出免费额度怎么办？

**Railway免费额度**：
- 每月 $5 额度
- 或 500小时运行时间
- 对于演示项目完全够用

**如果超出**：
- 可以暂停不用的服务
- 或升级到付费套餐（$5/月起）

---

## 💰 费用说明

### Railway免费套餐包含：

✅ $5 月度使用额度（按实际使用计费）  
✅ 或 500 小时运行时间  
✅ 无限项目数  
✅ 无限服务数  
✅ 免费HTTPS  
✅ 免费域名  

### 实际使用情况（估算）：

- **PostgreSQL数据库**: ~$1/月
- **后端服务**: ~$2/月
- **前端服务**: ~$1/月
- **总计**: ~$4/月（在免费额度内！）

### 如何查看用量：

1. 点击右上角头像
2. 选择 "Usage"
3. 查看本月使用情况

---

## 🎨 自定义域名（可选）

如果您有自己的域名，可以绑定：

### 步骤：

1. **进入服务的Settings**
2. **找到 "Domains" 部分**
3. **点击 "Custom Domain"**
4. **输入您的域名**（如：`www.yourdomain.com`）
5. **在域名DNS设置中添加CNAME记录**：
   ```
   类型: CNAME
   名称: www
   值: (Railway提供的域名)
   ```

---

## 📱 移动端访问

您的网站是响应式设计，可以在手机上完美访问：

1. 打开手机浏览器
2. 输入前端URL
3. 可以添加到手机主屏幕，像APP一样使用！

---

## 🔄 如何更新代码

以后修改代码后，只需：

```bash
# 1. 提交代码
git add .
git commit -m "更新功能"
git push

# 2. Railway自动部署
# 无需任何操作，Railway会自动检测GitHub推送并重新部署！
```

---

## 📊 监控和管理

### 查看访问日志：
1. 进入服务详情
2. 点击 "Deployments"
3. 选择当前运行的部署
4. 查看实时日志

### 查看资源使用：
1. 进入服务详情
2. 点击 "Metrics"
3. 查看CPU、内存、网络使用情况

### 暂停服务（省额度）：
1. 进入服务Settings
2. 找到 "Danger Zone"
3. 点击 "Pause Service"

---

## 🎓 展示建议

### 写在简历上：

**项目名称**: 校园失物招领系统  
**技术栈**: React + FastAPI + PostgreSQL + ElasticSearch  
**项目链接**: https://your-frontend.up.railway.app  
**源码地址**: https://github.com/cfbwsj/campus-lost-found  
**项目描述**: 
- 实现了OCR文字识别和AI物品分类功能
- 使用ElasticSearch实现模糊搜索
- 前后端分离架构，Docker容器化部署
- 部署在Railway云平台，支持全球访问

---

## 📞 需要帮助？

如果遇到任何问题：

1. **查看Railway文档**: https://docs.railway.app
2. **查看项目文档**: 
   - DEPLOY.md
   - DEPLOYMENT_OPTIONS.md
3. **GitHub Issues**: https://github.com/cfbwsj/campus-lost-found/issues

---

**祝您部署顺利！🎉**

