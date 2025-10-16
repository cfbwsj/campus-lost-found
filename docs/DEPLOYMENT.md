# 部署指南

## 环境要求

### 基础环境
- Docker 20.10+
- Docker Compose 2.0+
- Git

### 可选环境（本地开发）
- Python 3.8+
- Node.js 16+
- PostgreSQL 12+
- ElasticSearch 7.x
- Tesseract OCR

## Docker部署（推荐）

### 1. 克隆项目
```bash
git clone https://github.com/your-username/campus-lost-found.git
cd campus-lost-found
```

### 2. 配置环境变量
```bash
# 复制环境变量模板
cp backend/env.example backend/.env

# 编辑环境变量（根据需要修改）
nano backend/.env
```

### 3. 启动服务
```bash
# 启动所有服务
docker-compose up -d

# 查看服务状态
docker-compose ps

# 查看日志
docker-compose logs -f
```

### 4. 访问应用
- 前端界面：http://localhost:3000
- 后端API：http://localhost:8000
- API文档：http://localhost:8000/docs
- ElasticSearch：http://localhost:9200

## 本地开发部署

### 1. 后端设置

#### 安装Python依赖
```bash
cd backend
pip install -r requirements.txt
```

#### 安装Tesseract OCR
```bash
# Ubuntu/Debian
sudo apt-get install tesseract-ocr tesseract-ocr-chi-sim tesseract-ocr-chi-tra

# macOS
brew install tesseract tesseract-lang

# Windows
# 下载并安装：https://github.com/UB-Mannheim/tesseract/wiki
```

#### 配置数据库
```bash
# 创建数据库
createdb campus_lost_found

# 运行迁移
python -c "from models.database import init_db; init_db()"
```

#### 启动后端服务
```bash
python main.py
```

### 2. 前端设置

```bash
cd frontend
npm install
npm start
```

### 3. 安装ElasticSearch

```bash
# 使用Docker安装ElasticSearch
docker run -d \
  --name elasticsearch \
  -p 9200:9200 \
  -p 9300:9300 \
  -e "discovery.type=single-node" \
  -e "ES_JAVA_OPTS=-Xms512m -Xmx512m" \
  elasticsearch:7.17.0
```

## 生产环境部署

### 1. 服务器配置

#### 系统要求
- Ubuntu 20.04+ 或 CentOS 8+
- 4GB+ RAM
- 20GB+ 磁盘空间
- 域名和SSL证书

#### 安装Docker
```bash
# Ubuntu
curl -fsSL https://get.docker.com -o get-docker.sh
sudo sh get-docker.sh
sudo usermod -aG docker $USER

# 安装Docker Compose
sudo curl -L "https://github.com/docker/compose/releases/download/v2.20.0/docker-compose-$(uname -s)-$(uname -m)" -o /usr/local/bin/docker-compose
sudo chmod +x /usr/local/bin/docker-compose
```

### 2. 配置Nginx

创建Nginx配置文件：
```nginx
# /etc/nginx/sites-available/campus-lost-found
server {
    listen 80;
    server_name your-domain.com;
    
    # 重定向到HTTPS
    return 301 https://$server_name$request_uri;
}

server {
    listen 443 ssl http2;
    server_name your-domain.com;
    
    # SSL证书配置
    ssl_certificate /path/to/your/cert.pem;
    ssl_certificate_key /path/to/your/key.pem;
    
    # 前端静态文件
    location / {
        proxy_pass http://localhost:3000;
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
        proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
        proxy_set_header X-Forwarded-Proto $scheme;
    }
    
    # 后端API
    location /api/ {
        proxy_pass http://localhost:8000;
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
        proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
        proxy_set_header X-Forwarded-Proto $scheme;
    }
    
    # 文件上传
    location /uploads/ {
        proxy_pass http://localhost:8000;
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
        proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
        proxy_set_header X-Forwarded-Proto $scheme;
    }
}
```

启用站点：
```bash
sudo ln -s /etc/nginx/sites-available/campus-lost-found /etc/nginx/sites-enabled/
sudo nginx -t
sudo systemctl reload nginx
```

### 3. 环境变量配置

生产环境配置：
```bash
# backend/.env
DATABASE_URL=postgresql://username:password@localhost:5432/campus_lost_found
ELASTICSEARCH_HOST=localhost
ELASTICSEARCH_PORT=9200
SECRET_KEY=your-production-secret-key
DEBUG=False
ALLOWED_HOSTS=your-domain.com,localhost
```

### 4. 数据备份

#### 数据库备份
```bash
# 创建备份脚本
#!/bin/bash
BACKUP_DIR="/backup/campus-lost-found"
DATE=$(date +%Y%m%d_%H%M%S)

# 创建备份目录
mkdir -p $BACKUP_DIR

# 备份数据库
docker-compose exec postgres pg_dump -U postgres campus_lost_found > $BACKUP_DIR/db_$DATE.sql

# 备份上传文件
tar -czf $BACKUP_DIR/uploads_$DATE.tar.gz backend/uploads/

# 清理旧备份（保留30天）
find $BACKUP_DIR -name "*.sql" -mtime +30 -delete
find $BACKUP_DIR -name "*.tar.gz" -mtime +30 -delete
```

#### 自动备份
```bash
# 添加到crontab
crontab -e

# 每天凌晨2点备份
0 2 * * * /path/to/backup-script.sh
```

## 监控和维护

### 1. 日志监控
```bash
# 查看应用日志
docker-compose logs -f backend
docker-compose logs -f frontend

# 查看系统日志
journalctl -u docker -f
```

### 2. 性能监控
```bash
# 查看资源使用情况
docker stats

# 查看磁盘使用
df -h
du -sh backend/uploads/
```

### 3. 更新部署
```bash
# 拉取最新代码
git pull origin main

# 重新构建并启动
docker-compose down
docker-compose build --no-cache
docker-compose up -d
```

## 故障排除

### 常见问题

1. **端口冲突**
   ```bash
   # 查看端口占用
   netstat -tlnp | grep :8000
   
   # 修改docker-compose.yml中的端口映射
   ```

2. **内存不足**
   ```bash
   # 增加ElasticSearch内存限制
   # 在docker-compose.yml中修改ES_JAVA_OPTS
   ```

3. **文件权限问题**
   ```bash
   # 修复上传目录权限
   sudo chown -R 1000:1000 backend/uploads/
   ```

4. **数据库连接失败**
   ```bash
   # 检查数据库状态
   docker-compose exec postgres pg_isready -U postgres
   
   # 重启数据库
   docker-compose restart postgres
   ```

## 安全建议

1. **定期更新依赖**
   ```bash
   # 更新Python依赖
   pip list --outdated
   pip install --upgrade package-name
   
   # 更新Node.js依赖
   npm audit
   npm update
   ```

2. **配置防火墙**
   ```bash
   # 只允许必要端口
   ufw allow 22    # SSH
   ufw allow 80    # HTTP
   ufw allow 443   # HTTPS
   ufw enable
   ```

3. **定期备份**
   - 设置自动备份脚本
   - 测试备份恢复流程
   - 异地存储备份文件

4. **监控安全日志**
   ```bash
   # 查看登录日志
   tail -f /var/log/auth.log
   
   # 查看Nginx访问日志
   tail -f /var/log/nginx/access.log
   ```
