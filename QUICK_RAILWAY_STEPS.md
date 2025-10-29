# 🚀 Railway 快速部署 - 3分钟上线

## 📱 第一步：打开Railway网站

**复制这个链接到浏览器**：
```
https://railway.app
```

点击右上角 **"Login"** → 选择 **"Login with GitHub"**

---

## 🔗 第二步：部署项目（一键完成）

登录后，点击下面这个链接，**自动**部署您的项目：

```
https://railway.app/new/template
```

然后在搜索框输入您的仓库：
```
cfbwsj/campus-lost-found
```

或者手动操作：
1. 点击 **"New Project"**
2. 选择 **"Deploy from GitHub repo"**
3. 找到 **"campus-lost-found"**
4. 点击 **"Deploy Now"**

---

## 🗄️ 第三步：添加数据库

在项目页面：
1. 点击 **"+ New"**
2. 选择 **"Database"**
3. 选择 **"Add PostgreSQL"**
4. 等待30秒创建完成

---

## ⚙️ 第四步：配置后端

### 4.1 点击 backend 服务卡片

### 4.2 进入 Settings，设置：
- **Root Directory**: `backend`
- **Start Command**: `uvicorn main:app --host 0.0.0.0 --port $PORT`

### 4.3 进入 Variables，添加：

| 变量名 | 变量值 |
|--------|--------|
| `DATABASE_URL` | *(从PostgreSQL服务复制)* |
| `ELASTICSEARCH_HOST` | `localhost` |
| `REDIS_URL` | `redis://localhost:6379` |

### 4.4 生成域名：
- Settings → Networking → **"Generate Domain"**
- 复制这个域名（后面要用）

---

## 🎨 第五步：配置前端

### 5.1 添加新服务
1. 点击 **"+ New"**
2. 选择 **"GitHub Repo"**
3. 再次选择 **"campus-lost-found"**

### 5.2 点击新服务，进入 Settings：
- **Root Directory**: `frontend`
- **Build Command**: `npm install && npm run build`
- **Start Command**: `npx serve -s build -l $PORT`

### 5.3 进入 Variables，添加：

| 变量名 | 变量值 |
|--------|--------|
| `REACT_APP_API_URL` | *(粘贴第四步复制的后端域名)* |

### 5.4 生成域名：
- Settings → Networking → **"Generate Domain"**
- **这就是您的网站地址！** 🎉

---

## ✅ 完成！访问您的网站

等待3-5分钟部署完成后：

### 您的网站地址：
```
https://campus-lost-found-production-xxxx.up.railway.app
```

### API文档地址：
```
https://backend-production-xxxx.up.railway.app/docs
```

---

## 📊 检查部署状态

### 查看是否部署成功：
1. 点击服务卡片
2. 进入 **"Deployments"** 标签
3. 看到绿色 ✅ **"SUCCESS"** = 部署成功
4. 看到红色 ❌ **"FAILED"** = 部署失败，查看日志

---

## 🔧 如果部署失败

### 常见问题：

#### 问题1: Python依赖安装失败
**解决**：检查 `requirements.txt` 是否正确

#### 问题2: 端口错误
**解决**：确保Start Command使用了 `$PORT`

#### 问题3: 前端空白页
**解决**：检查 `REACT_APP_API_URL` 是否设置正确

---

## 💡 提示

### Railway自动部署
以后修改代码，只需：
```bash
git add .
git commit -m "更新"
git push
```
Railway会**自动**重新部署！

### 免费额度
- 每月 $5 额度（够用！）
- 约500小时运行时间

### 查看用量
右上角头像 → **"Usage"**

---

## 🎉 恭喜！

您的网站已经上线，全球可访问！

**可以做的事**：
- ✅ 分享链接给朋友
- ✅ 添加到简历作品集
- ✅ 绑定自己的域名
- ✅ 继续开发新功能

---

**需要详细教程？查看 `RAILWAY_DEPLOY_GUIDE.md`**

