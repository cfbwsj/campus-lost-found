# Campus Lost & Found - Deploy & Troubleshooting Report

本报告记录了从云端到本地 Docker 全链路部署过程中遇到的主要问题、根因与最终修复方案，便于后续快速复现与排障。

## 一、环境与总体结构

- 前端：React 18 + Ant Design，Nginx 容器静态托管（生产）/ CRA 开发服务器（本地）
- 后端：FastAPI + SQLAlchemy + PostgreSQL +（可选）ElasticSearch
- 识别/搜索：Tesseract OCR、ResNet50（Torch）、ElasticSearch（提供 SQL 降级方案）
- 运行：Docker Compose（postgres、redis、elasticsearch、backend、frontend）

## 二、关键问题时间线与解决方案

### 1. 部署初期 CORS 报错（云端 Render）

症状：
- 浏览器报错：No 'Access-Control-Allow-Origin' header / net::ERR_FAILED
- 某些接口 307 → 500，前端被浏览器判定为跨域失败

根因：
- 后端端点定义使用了带/与不带/混用，FastAPI 默认会将无斜杠请求 307 重定向到带斜杠，部分代理或浏览器在跨域预检/重定向时丢失 CORS 头

修复：
- 全局关闭自动斜杠重定向：`app.router.redirect_slashes = False`
- 为关键路由同时注册有/无斜杠版本：
  - 文件上传：`/api/upload` 与 `/api/upload/`
  - 搜索：`/api/search` 与 `/api/search/`
  - OCR/分类：`/api/ocr`、`/api/classify` 同步处理
- CORS 白名单明确包含前端域名（本地为 http://localhost:3000）：
  - `allow_origins=["http://localhost:3000","http://127.0.0.1:3000"]`

结论：
- Render 上的最初 CORS 报错，根因不是“纯 CORS 配置”，而是 307 重定向导致的 CORS 头丢失。关闭自动斜杠并补齐双路由后恢复。

### 2. 本地 Docker 同样出现“像 CORS 的问题”，但实际是后端 500

症状：
- 浏览器仍提示 CORS/Network Error，接口看似跨域失败

根因：
- 后端新增权限功能后，为 `lost_items`/`found_items` 增加了 `owner_id` 字段，但数据库已有表结构未同步，导致 SQL 查询包含 `owner_id` 字段时报 500（psycopg2 UndefinedColumn）。浏览器统一将 500 显示为网络失败，从而误导为 CORS 问题。

修复：
- 添加轻量迁移逻辑（`init_db()` 中尝试 `ALTER TABLE ... ADD COLUMN IF NOT EXISTS owner_id`）
- 同时在排障时通过 `docker-compose exec postgres psql` 手动执行：
  - `ALTER TABLE lost_items ADD COLUMN IF NOT EXISTS owner_id INTEGER;`
  - `ALTER TABLE found_items ADD COLUMN IF NOT EXISTS owner_id INTEGER;`
- 重启后端容器

结论：
- 本地所谓的“CORS 问题”实为后端 500（缺列），修复表结构后前端恢复正常。

### 3. 上传接口 500：`UploadFile.size` 不存在

症状：
- 上传文件时 500，日志提示属性不存在

根因：
- `UploadFile` 对象无 `size` 属性

修复：
- 先 `await file.read()` 取字节计算大小，再回退 `seek(0)`，写入磁盘；返回体里的 `size` 使用计算值

### 4. 上传接口再次失败：UnboundLocalError（`os` 作用域）

症状：
- `UnboundLocalError: local variable 'os' referenced before assignment`

根因：
- 函数内重复 `import os`，导致作用域遮蔽

修复：
- 去除函数体内重复 import，统一使用文件顶层的 `import os`

### 5. 搜索接口 404 与 500

症状：
- `/api/search` 404（无斜杠），或 500（ES 不可用/空结果）

修复：
- 关闭自动斜杠，并为 `/api/search` 注册无斜杠版本
- 当 ES 不可用或返回空结果时，自动回退到数据库 SQL 搜索，并兼容排序字段类型（`created_at`）
- 分类/地点/热门关键词改为动态统计（去掉静态假数据）

### 6. 登录与权限接入后无法访问

症状：
- 后端容器重启循环，`ModuleNotFoundError: No module named 'jwt'`

修复：
- 在 `backend/requirements.txt` 增加 `PyJWT==2.8.0`，重建后端镜像
- Python 3.9 不支持 `timedelta | None` 的写法，改为 `Optional[timedelta]`

### 7. 登录 400（Bad Request）

症状：
- 登录提示 400，token 无法获取

根因：
- 数据库尚无用户，`/api/auth/login` 校验失败

修复：
- `init_db()` 中增加默认管理员账号（admin/123456，仅本地开发）
- 同时提供 `/api/auth/register` 供前端注册；前端新增注册页

### 8. 详情页编辑按钮可见性与编辑空白页

症状：
- 编辑按钮总显示/编辑页空白

修复：
- 详情页仅在“管理员或数据 owner”显示编辑/删除按钮
- 新增 `EditItem` 页面（`/edit/:type/:id`），拉取详情预填表单，提交 PUT 按权限更新

## 三、后端要点清单

1) CORS
- `app.add_middleware(CORSMiddleware, allow_origins=["http://localhost:3000","http://127.0.0.1:3000"], allow_credentials=True, allow_methods=["*"], allow_headers=["*"])`
- `app.router.redirect_slashes = False`，并为关键路由注册无斜杠变体

2) 文件上传
- `UploadFile` 大小需通过读取内容计算
- 生成完整可跨域访问的图片 URL：`BASE_URL + /uploads/...`

3) 搜索
- ES 不可用或返回空时自动回退 SQL；动态返回分类/地点/热门关键词统计

4) 权限/认证
- `users` 表 + JWT 登录（PyJWT）
- 创建/更新/删除权限：管理员可操作全部；普通用户仅可操作 `owner_id == 自己` 的数据
- 旧数据 `owner_id` 为空时，默认不允许普通用户改删

5) 轻量迁移
- `init_db()` 中尝试执行 `ALTER TABLE ... ADD COLUMN IF NOT EXISTS owner_id`（PostgreSQL）

## 四、前端要点清单

1) API 基础
- Axios 全局 `baseURL = http://localhost:8000`，拦截器自动附加 `Authorization: Bearer <token>`

2) 登录/注册
- 登录页 `/login`：表单 x-www-form-urlencoded 提交 `/api/auth/login`
- 注册页 `/register`：提交 `/api/auth/register` 创建普通用户

3) 上传与发布
- 未登录禁止发布（前端校验并重定向登录）
- 上传成功自动进行 OCR/AI 分类，并预填描述与类别

4) 详情与编辑
- 详情页仅在“管理员或数据 owner”显示编辑/删除按钮
- 编辑页 `/edit/:type/:id` 预填并更新（PUT）

5) 路由
- `/api/search`、`/api/upload`、`/api/ocr`、`/api/classify` 同时支持无斜杠
- SPA 刷新 404 由前端 Nginx `_redirects` 或对应配置处理（云端）

## 五、常见排障步骤（本地 Docker）

1) 看容器状态与端口映射
```
docker-compose ps
```

2) 看后端日志
```
docker-compose logs backend --tail=200
```

3) 如果看到 CORS/Network Error，先打开浏览器 Network 面板看实际 HTTP 状态码：
- 若是 500：优先排查后端异常（如列缺失、依赖缺失）
- 若是 307：检查是否斜杠重定向引起，补充无斜杠路由/关闭自动斜杠

4) 数据库结构相关
```
docker-compose exec postgres psql -U postgres -d campus_db -c "\dt"
docker-compose exec postgres psql -U postgres -d campus_db -c "ALTER TABLE lost_items ADD COLUMN IF NOT EXISTS owner_id INTEGER;"
docker-compose exec postgres psql -U postgres -d campus_db -c "ALTER TABLE found_items ADD COLUMN IF NOT EXISTS owner_id INTEGER;"
```

5) 依赖变更
- 后端改动 `requirements.txt` 后需要：
```
docker-compose build backend
docker-compose up -d backend
```
- 前端有新页面/路由/打包配置改动后需要：
```
docker-compose build frontend
docker-compose up -d frontend
```

## 六、最终状态与账号

- 后端 API: http://localhost:8000
- 文档: http://localhost:8000/docs
- 前端: http://localhost:3000
- 账号：
  - 管理员：admin / 123456
  - 测试用户：user1 / 123456

## 七、经验总结（TL;DR）

- “像 CORS 的错误”并不总是 CORS：浏览器 Network 面板的真实状态码最关键。我们多次定位出实为后端 500（缺列/依赖）或 307（斜杠重定向）。
- 本地与云端的“CORS”差异，源于代理/重定向行为不同，解决方案是路由层面禁用自动斜杠并补齐无斜杠端点。
- 权限上线要同步数据结构：为历史表补列、初始化默认管理员、前端受控展示编辑/删除。
- 搜索需要优雅降级：ES 不可用时自动退回 SQL，保证核心功能可用。


