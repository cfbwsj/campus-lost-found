# 🎓 校园失物招领系统

基于AI的智能校园失物招领平台

## ✨ 功能特性

- 📸 **图片上传** - 支持拖拽上传物品图片
- 🔍 **智能搜索** - 关键词搜索，多条件筛选
- 📊 **实时统计** - 失物/招领数据统计
- 💾 **数据持久化** - PostgreSQL数据库
- 🐳 **Docker部署** - 一键启动所有服务

## 🚀 快速开始（推荐）

### 前提条件

- 已安装 [Docker Desktop](https://www.docker.com/products/docker-desktop/)
- Windows 10/11 或 macOS 或 Linux

### 启动步骤

**双击运行：**
```
启动Docker.bat
```

等待5-10分钟后，访问：
- **前端**: http://localhost:3000
- **后端API文档**: http://localhost:8000/docs

### 停止服务

**双击运行：**
```
停止Docker.bat
```

## 📂 项目结构

```
campus-lost-found/
├── backend/              # FastAPI后端
│   ├── api/             # API路由
│   ├── models/          # 数据模型
│   ├── utils/           # 工具函数
│   └── uploads/         # 上传文件（自动创建）
├── frontend/            # React前端
│   ├── public/          # 静态资源
│   └── src/            # 源代码
├── docker-compose.yml   # Docker编排配置
├── 启动Docker.bat       # 一键启动脚本
└── 停止Docker.bat       # 停止服务脚本
```

## 🛠️ 技术栈

### 后端
- **FastAPI** - 高性能Web框架
- **PostgreSQL** - 关系型数据库
- **SQLAlchemy** - ORM框架
- **ElasticSearch** - 搜索引擎（可选）
- **Redis** - 缓存（可选）

### 前端
- **React 18** - UI框架
- **Ant Design** - UI组件库
- **React Router** - 路由管理
- **Axios** - HTTP客户端

## 🌐 服务端口

| 服务 | 端口 | 说明 |
|------|------|------|
| 前端 | 3000 | React应用 |
| 后端 | 8000 | FastAPI服务 |
| PostgreSQL | 5432 | 数据库 |
| ElasticSearch | 9200 | 搜索引擎 |
| Redis | 6379 | 缓存 |

## 📊 数据库信息

- **数据库**: PostgreSQL 13
- **地址**: localhost:5432
- **用户**: postgres
- **密码**: password
- **数据库名**: campus_db

## 🔧 手动操作

### 查看日志
```bash
docker-compose logs -f
```

### 重启服务
```bash
docker-compose restart
```

### 进入容器
```bash
# 进入后端容器
docker exec -it campus-backend bash

# 进入数据库容器
docker exec -it campus-postgres psql -U postgres -d campus_db
```

## 🐛 故障排除

### Docker启动失败

1. 确保Docker Desktop正在运行
2. 检查端口是否被占用（3000, 8000, 5432等）
3. 重启Docker Desktop

### 端口占用

**查看占用进程：**
```bash
netstat -ano | findstr :3000
netstat -ano | findstr :8000
```

**停止进程：**
```bash
taskkill /PID <进程ID> /F
```

### 清理所有数据

**双击运行：**
```
清理Docker数据.bat
```

**注意：此操作会删除所有数据，请谨慎操作！**

## 📝 开发说明

### 本地开发模式

**后端：**
```bash
cd backend
pip install -r requirements.txt
uvicorn main:app --reload
```

**前端：**
```bash
cd frontend
npm install
npm start
```

## 📄 许可证

MIT License

## 🙏 致谢

- FastAPI
- React
- Ant Design
- PostgreSQL
- Docker
