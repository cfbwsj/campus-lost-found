# Render 前端部署路由404问题修复指南

## 问题描述
前端在 Render 上部署后，除了主页，其他页面（如 `/lost`、`/found`、`/upload`）刷新时返回 404 Not Found。

## 原因分析

### 本地 Docker 正常的原因
本地 Docker Compose 使用 Nginx，配置了 `try_files $uri $uri/ /index.html;`，所有不存在路径都会返回 `index.html`，React Router 可以处理路由。

### Render 上 404 的原因
Render 有两种前端部署方式：

1. **Static Site 部署**：需要 `_redirects` 文件（已创建）
2. **Docker 部署**：需要 Nginx 配置正确处理 SPA 路由（已修复）

## 解决方案

### 方案 A：Render Static Site（推荐）

1. **检查 `_redirects` 文件是否存在**
   - 文件路径：`frontend/public/_redirects`
   - 内容：`/*    /index.html   200`

2. **构建时确保文件被复制**
   - `package.json` 的 build 脚本已自动创建 `build/_redirects`
   - 构建后检查 `build/_redirects` 是否存在

3. **Render Static Site 配置**
   - **Build Command**: `cd frontend && npm install && npm run build`
   - **Publish Directory**: `frontend/build`
   - **环境变量**:
     ```
     REACT_APP_API_URL=https://your-backend-url.onrender.com
     ```

### 方案 B：Render Docker 部署前端

如果前端也用 Docker 部署：

1. **检查 Nginx 配置**
   - 文件：`frontend/nginx.conf`
   - 确保包含：`try_files $uri $uri/ /index.html;`

2. **Render Web Service 配置**
   - **Environment**: Docker
   - **Root Directory**: `frontend`
   - **Dockerfile Path**: `Dockerfile`
   - **环境变量**:
     ```
     REACT_APP_API_URL=https://your-backend-url.onrender.com
     PORT=3000
     ```

3. **端口映射**
   - Render 会自动注入 `$PORT` 环境变量
   - 如果 Nginx 需要监听动态端口，需要修改 Dockerfile

## 验证步骤

1. **检查构建产物**
   ```bash
   # 本地构建测试
   cd frontend
   npm run build
   cat build/_redirects  # 应该显示：/*    /index.html   200
   ```

2. **测试路由**
   - 访问：`https://your-frontend-url.onrender.com`
   - 点击导航到 `/lost` 或 `/found`
   - **刷新页面**（F5），应该不再 404

3. **检查网络请求**
   - 打开浏览器 DevTools → Network
   - 刷新 `/lost` 页面
   - 应该返回 `index.html`（200状态码），而不是 404

## 常见问题

### Q1: Static Site 部署后还是 404
**A**: 
- 确认 `build/_redirects` 文件存在
- 检查 Render Static Site 的 Publish Directory 是否正确指向 `frontend/build`
- 尝试手动在 Render Dashboard 重新部署

### Q2: Docker 部署前端，路由还是 404
**A**:
- 检查 Nginx 日志：`docker logs <container-name>`
- 确认 `try_files` 配置已生效
- 检查端口映射是否正确

### Q3: 本地正常，Render 上不行
**A**:
- 本地使用的是开发服务器（`npm start`），自动处理 SPA 路由
- Render 是生产构建（Nginx/Static），需要显式配置重定向

## 快速修复命令

如果构建后 `_redirects` 文件缺失：

```bash
cd frontend
npm run build
echo '/*    /index.html   200' > build/_redirects
# 然后重新部署到 Render
```

## 最终检查清单

- [ ] `frontend/public/_redirects` 文件存在
- [ ] `frontend/package.json` build 脚本包含创建 _redirects 的步骤
- [ ] `frontend/nginx.conf`（如果 Docker 部署）包含 SPA 路由支持
- [ ] Render 部署配置正确（Publish Directory 或 Root Directory）
- [ ] 环境变量 `REACT_APP_API_URL` 已设置
- [ ] 重新部署后测试路由刷新不再 404

