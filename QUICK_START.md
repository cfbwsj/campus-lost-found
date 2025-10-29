# 快速开始指南

## 🚀 一键启动（推荐）

### Windows用户
直接双击运行：
- `start.bat` - 启动所有服务
- `stop.bat` - 停止所有服务

### 手动启动
```bash
# 启动所有服务
docker-compose up -d

# 查看服务状态
docker-compose ps

# 查看日志
docker-compose logs -f

# 停止服务
docker-compose down
```

## 📋 前置要求

### 必须安装
- [Docker Desktop](https://www.docker.com/products/docker-desktop)
  - Windows: 下载安装包并安装
  - 安装完成后启动Docker Desktop

### 可选安装（本地开发）
- Python 3.8+
- Node.js 16+
- PostgreSQL 12+
- Tesseract OCR

## 🎯 三种运行方式

### 方式一：Docker一键部署（最简单）

**适用场景：** 快速体验、学习、演示

```bash
# 1. 启动所有服务
docker-compose up -d

# 2. 访问应用
# 前端：http://localhost:3000
# 后端：http://localhost:8000
# API文档：http://localhost:8000/docs
```

**包含的服务：**
- ✅ PostgreSQL数据库
- ✅ ElasticSearch搜索引擎
- ✅ Redis缓存
- ✅ 后端API服务
- ✅ 前端界面

### 方式二：本地开发（需要手动安装依赖）

**适用场景：** 开发调试、修改代码

#### 后端启动
```bash
# 1. 安装Python依赖
cd backend
pip install -r requirements.txt

# 2. 安装Tesseract OCR
# Windows: 下载安装 https://github.com/UB-Mannheim/tesseract/wiki
# 安装后配置环境变量

# 3. 配置数据库（需要先安装PostgreSQL）
# 编辑 backend/.env 文件

# 4. 初始化数据库
python -c "from models.database import init_db; init_db()"

# 5. 启动后端
python main.py
```

#### 前端启动
```bash
# 1. 安装依赖
cd frontend
npm install

# 2. 启动前端
npm start
```

### 方式三：云服务器部署

**适用场景：** 正式使用、公网访问

详见 [部署文档](docs/DEPLOYMENT.md)

## 🔧 常见问题

### 1. Docker启动失败
```bash
# 检查Docker是否运行
docker ps

# 检查端口占用
netstat -ano | findstr :8000
netstat -ano | findstr :3000
```

### 2. 数据库连接失败
```bash
# 检查PostgreSQL是否运行
docker-compose ps postgres

# 查看PostgreSQL日志
docker-compose logs postgres
```

### 3. 前端无法访问后端
```bash
# 检查后端是否运行
docker-compose ps backend

# 查看后端日志
docker-compose logs backend
```

### 4. OCR识别失败
```bash
# 检查Tesseract是否正确安装
tesseract --version

# 查看OCR日志
docker-compose logs backend | grep OCR
```

## 📊 数据库说明

### Docker方式（自动）
- PostgreSQL自动在Docker容器中运行
- 数据存储在Docker卷中
- 无需手动配置

### 本地方式（手动）
1. 安装PostgreSQL
2. 创建数据库：`CREATE DATABASE campus_lost_found;`
3. 配置连接：编辑 `backend/.env`
4. 初始化表：`python -c "from models.database import init_db; init_db()"`

## 🎓 学习路径

### 第一步：快速体验
```bash
# 使用Docker一键启动
docker-compose up -d
# 访问 http://localhost:3000
```

### 第二步：了解架构
- 阅读 `README.md` 了解项目结构
- 查看 `docs/DEPLOYMENT.md` 了解部署细节
- 访问 http://localhost:8000/docs 查看API文档

### 第三步：本地开发
- 克隆代码到本地
- 安装开发环境
- 修改代码并测试

### 第四步：部署上线
- 购买云服务器
- 按照部署文档配置
- 上线运行

## 📞 获取帮助

- 查看 [GitHub Issues](https://github.com/cfbwsj/campus-lost-found/issues)
- 阅读 [部署文档](docs/DEPLOYMENT.md)
- 查看 [API文档](http://localhost:8000/docs)

## 🎉 开始使用

现在就开始吧！

```bash
# 方式一：双击运行 start.bat（Windows）
# 或

# 方式二：命令行运行
docker-compose up -d
```

然后访问 http://localhost:3000 开始使用！🚀
