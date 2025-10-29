# 校园失物招领系统 - 部署指南

## 📋 目录
- [系统要求](#系统要求)
- [Docker部署（推荐）](#docker部署推荐)
- [本地部署](#本地部署)
- [数据库设置](#数据库设置)
- [环境配置](#环境配置)
- [故障排除](#故障排除)

## 系统要求

### 硬件要求
- **CPU**: 2核心以上
- **内存**: 4GB以上（推荐8GB）
- **磁盘空间**: 10GB以上

### 软件要求
- **Docker**: 20.10+（Docker部署）
- **Docker Compose**: 2.0+（Docker部署）
- **Python**: 3.9+（本地部署）
- **Node.js**: 16+（本地部署）
- **MySQL**: 5.7+或8.0+（本地部署）

## Docker部署（推荐）

### 1. 安装Docker

**Windows**:
1. 下载并安装 [Docker Desktop](https://www.docker.com/products/docker-desktop)
2. 启动Docker Desktop并等待其完全启动
3. 验证安装：
```bash
docker --version
docker-compose --version
```

**Linux**:
```bash
# 安装Docker
curl -fsSL https://get.docker.com -o get-docker.sh
sudo sh get-docker.sh

# 安装Docker Compose
sudo curl -L "https://github.com/docker/compose/releases/latest/download/docker-compose-$(uname -s)-$(uname -m)" -o /usr/local/bin/docker-compose
sudo chmod +x /usr/local/bin/docker-compose

# 验证安装
docker --version
docker-compose --version
```

### 2. 启动服务

```bash
# 进入项目目录
cd campus-lost-found

# 启动所有服务
docker-compose up -d

# 查看服务状态
docker-compose ps

# 查看日志
docker-compose logs -f
```

### 3. 访问系统

启动成功后，可以通过以下地址访问：

- **前端界面**: http://localhost:3000
- **后端API**: http://localhost:8000
- **API文档**: http://localhost:8000/docs
- **ElasticSearch**: http://localhost:9200
- **PostgreSQL**: localhost:5432

### 4. 停止服务

```bash
# 停止所有服务
docker-compose down

# 停止并删除所有数据
docker-compose down -v
```

## 本地部署

### 1. 后端设置

```bash
# 进入后端目录
cd backend

# 创建虚拟环境
python -m venv venv

# 激活虚拟环境
# Windows:
venv\Scripts\activate
# Linux/Mac:
source venv/bin/activate

# 安装依赖
pip install -r requirements.txt

# 配置环境变量
cp env.example .env
# 编辑 .env 文件，设置数据库连接等配置

# 启动后端服务
python main.py
```

后端服务将在 http://localhost:8000 启动

### 2. 前端设置

```bash
# 打开新终端，进入前端目录
cd frontend

# 安装依赖
npm install

# 启动开发服务器
npm start
```

前端服务将在 http://localhost:3000 启动

### 3. 数据库设置

#### MySQL配置

```bash
# 登录MySQL
mysql -u root -p

# 创建数据库
CREATE DATABASE aiweb CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci;

# 导入表结构和示例数据
USE aiweb;
SOURCE backend/database_schema.sql;

# 验证表创建
SHOW TABLES;
```

#### ElasticSearch配置

```bash
# 使用Docker运行ElasticSearch
docker run -d \
  --name elasticsearch \
  -p 9200:9200 -p 9300:9300 \
  -e "discovery.type=single-node" \
  -e "ES_JAVA_OPTS=-Xms256m -Xmx256m" \
  elasticsearch:7.17.0

# 验证ElasticSearch运行
curl http://localhost:9200
```

## 数据库设置

### 数据库表结构

系统使用两个主要数据表：

1. **lost_items** - 失物信息表
   - id: 主键
   - title: 失物标题
   - description: 详细描述
   - category: 物品类别
   - location: 丢失地点
   - contact_info: 联系方式
   - image_url: 图片URL
   - ocr_text: OCR识别文字
   - ai_category: AI识别类别
   - confidence: 识别置信度
   - status: 状态（lost/found/claimed）
   - created_at: 创建时间
   - updated_at: 更新时间
   - is_active: 是否有效

2. **found_items** - 招领信息表
   - 结构与lost_items相同

### 初始化数据

数据库表结构文件位于：`backend/database_schema.sql`

该文件包含：
- 表结构定义
- 索引创建
- 示例数据插入

执行方式：
```bash
mysql -u root -p aiweb < backend/database_schema.sql
```

## 环境配置

### 后端环境变量 (.env)

在 `backend` 目录创建 `.env` 文件：

```env
# 数据库配置
DATABASE_URL=mysql+pymysql://root:your_password@localhost:3306/aiweb?charset=utf8mb4

# ElasticSearch配置
ELASTICSEARCH_HOST=localhost
ELASTICSEARCH_PORT=9200

# Redis配置（可选）
REDIS_URL=redis://localhost:6379

# 文件上传配置
UPLOAD_DIR=./uploads
MAX_FILE_SIZE=10485760  # 10MB

# OCR配置
TESSERACT_CMD=tesseract  # Windows需要指定完整路径

# 日志配置
LOG_LEVEL=INFO
```

### 前端环境配置

在 `frontend` 目录创建 `.env` 文件（可选）：

```env
REACT_APP_API_URL=http://localhost:8000
```

## 故障排除

### 1. Docker相关问题

**问题**: Docker容器无法启动
```bash
# 查看容器日志
docker-compose logs backend
docker-compose logs frontend

# 重新构建容器
docker-compose build --no-cache
docker-compose up -d
```

**问题**: 端口已被占用
```bash
# 查看端口占用
netstat -ano | findstr :8000  # Windows
lsof -i :8000  # Linux/Mac

# 修改docker-compose.yml中的端口映射
```

### 2. 数据库连接问题

**问题**: 无法连接到MySQL

1. 检查MySQL服务是否运行
2. 验证数据库用户名和密码
3. 确认数据库名称正确
4. 检查防火墙设置

```bash
# 测试MySQL连接
mysql -u root -p -h localhost

# 检查MySQL服务状态
# Windows:
net start mysql
# Linux:
sudo systemctl status mysql
```

### 3. 前端构建问题

**问题**: npm install失败
```bash
# 清除缓存
npm cache clean --force

# 删除node_modules重新安装
rm -rf node_modules package-lock.json
npm install
```

**问题**: 前端启动报错
```bash
# 清除React缓存
rm -rf node_modules/.cache

# 设置环境变量
Remove-Item Env:HOST -ErrorAction SilentlyContinue
npm start
```

### 4. OCR和AI功能问题

**问题**: Tesseract未找到

**Windows**:
1. 下载并安装 [Tesseract OCR](https://github.com/UB-Mannheim/tesseract/wiki)
2. 将安装路径添加到系统PATH
3. 或在代码中指定路径：`pytesseract.pytesseract.tesseract_cmd = r'C:\Program Files\Tesseract-OCR\tesseract.exe'`

**Linux**:
```bash
# Ubuntu/Debian
sudo apt-get install tesseract-ocr tesseract-ocr-chi-sim

# CentOS/RHEL
sudo yum install tesseract tesseract-langpack-chi_sim
```

**问题**: PyTorch安装失败
```bash
# 安装CPU版本
pip install torch torchvision --index-url https://download.pytorch.org/whl/cpu

# 安装GPU版本（需要CUDA）
pip install torch torchvision --index-url https://download.pytorch.org/whl/cu118
```

### 5. ElasticSearch问题

**问题**: ElasticSearch无法启动

检查内存设置：
```bash
# 修改docker-compose.yml中的ES_JAVA_OPTS
ES_JAVA_OPTS=-Xms256m -Xmx256m
```

### 6. 内存优化

如果系统内存不足，可以采取以下措施：

1. **减少ElasticSearch内存**:
```yaml
# docker-compose.yml
elasticsearch:
  environment:
    - "ES_JAVA_OPTS=-Xms256m -Xmx256m"
```

2. **清理Docker缓存**:
```bash
# 清理未使用的镜像
docker image prune -a

# 清理未使用的容器
docker container prune

# 清理所有未使用资源
docker system prune -a
```

3. **移动Docker数据目录到其他盘**:
   - Docker Desktop -> Settings -> Resources -> Advanced
   - 修改"Disk image location"

## 性能优化建议

1. **生产环境部署**:
   - 使用nginx作为反向代理
   - 启用gzip压缩
   - 配置CDN加速静态资源
   - 使用Redis缓存热点数据

2. **数据库优化**:
   - 定期清理过期数据
   - 为常用查询字段添加索引
   - 配置数据库连接池

3. **ElasticSearch优化**:
   - 定期优化索引
   - 配置分片和副本
   - 使用bulk API批量插入

## 联系与支持

如遇到其他问题，请：
1. 查看项目 [GitHub Issues](https://github.com/cfbwsj/campus-lost-found/issues)
2. 提交新的Issue描述问题
3. 查看API文档：http://localhost:8000/docs

## 许可证

MIT License

