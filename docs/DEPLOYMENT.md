# ����ָ��

## ����Ҫ��

### ��������
- Docker 20.10+
- Docker Compose 2.0+
- Git

### ��ѡ���������ؿ�����
- Python 3.8+
- Node.js 16+
- PostgreSQL 12+
- ElasticSearch 7.x
- Tesseract OCR

## Docker�����Ƽ���

### 1. ��¡��Ŀ
```bash
git clone https://github.com/your-username/campus-lost-found.git
cd campus-lost-found
```

### 2. ���û�������
```bash
# ���ƻ�������ģ��
cp backend/env.example backend/.env

# �༭����������������Ҫ�޸ģ�
nano backend/.env
```

### 3. ��������
```bash
# �������з���
docker-compose up -d

# �鿴����״̬
docker-compose ps

# �鿴��־
docker-compose logs -f
```

### 4. ����Ӧ��
- ǰ�˽��棺http://localhost:3000
- ���API��http://localhost:8000
- API�ĵ���http://localhost:8000/docs
- ElasticSearch��http://localhost:9200

## ���ؿ�������

### 1. �������

#### ��װPython����
```bash
cd backend
pip install -r requirements.txt
```

#### ��װTesseract OCR
```bash
# Ubuntu/Debian
sudo apt-get install tesseract-ocr tesseract-ocr-chi-sim tesseract-ocr-chi-tra

# macOS
brew install tesseract tesseract-lang

# Windows
# ���ز���װ��https://github.com/UB-Mannheim/tesseract/wiki
```

#### �������ݿ�
```bash
# �������ݿ�
createdb campus_lost_found

# ����Ǩ��
python -c "from models.database import init_db; init_db()"
```

#### ������˷���
```bash
python main.py
```

### 2. ǰ������

```bash
cd frontend
npm install
npm start
```

### 3. ��װElasticSearch

```bash
# ʹ��Docker��װElasticSearch
docker run -d \
  --name elasticsearch \
  -p 9200:9200 \
  -p 9300:9300 \
  -e "discovery.type=single-node" \
  -e "ES_JAVA_OPTS=-Xms512m -Xmx512m" \
  elasticsearch:7.17.0
```

## ������������

### 1. ����������

#### ϵͳҪ��
- Ubuntu 20.04+ �� CentOS 8+
- 4GB+ RAM
- 20GB+ ���̿ռ�
- ������SSL֤��

#### ��װDocker
```bash
# Ubuntu
curl -fsSL https://get.docker.com -o get-docker.sh
sudo sh get-docker.sh
sudo usermod -aG docker $USER

# ��װDocker Compose
sudo curl -L "https://github.com/docker/compose/releases/download/v2.20.0/docker-compose-$(uname -s)-$(uname -m)" -o /usr/local/bin/docker-compose
sudo chmod +x /usr/local/bin/docker-compose
```

### 2. ����Nginx

����Nginx�����ļ���
```nginx
# /etc/nginx/sites-available/campus-lost-found
server {
    listen 80;
    server_name your-domain.com;
    
    # �ض���HTTPS
    return 301 https://$server_name$request_uri;
}

server {
    listen 443 ssl http2;
    server_name your-domain.com;
    
    # SSL֤������
    ssl_certificate /path/to/your/cert.pem;
    ssl_certificate_key /path/to/your/key.pem;
    
    # ǰ�˾�̬�ļ�
    location / {
        proxy_pass http://localhost:3000;
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
        proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
        proxy_set_header X-Forwarded-Proto $scheme;
    }
    
    # ���API
    location /api/ {
        proxy_pass http://localhost:8000;
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
        proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
        proxy_set_header X-Forwarded-Proto $scheme;
    }
    
    # �ļ��ϴ�
    location /uploads/ {
        proxy_pass http://localhost:8000;
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
        proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
        proxy_set_header X-Forwarded-Proto $scheme;
    }
}
```

����վ�㣺
```bash
sudo ln -s /etc/nginx/sites-available/campus-lost-found /etc/nginx/sites-enabled/
sudo nginx -t
sudo systemctl reload nginx
```

### 3. ������������

�����������ã�
```bash
# backend/.env
DATABASE_URL=postgresql://username:password@localhost:5432/campus_lost_found
ELASTICSEARCH_HOST=localhost
ELASTICSEARCH_PORT=9200
SECRET_KEY=your-production-secret-key
DEBUG=False
ALLOWED_HOSTS=your-domain.com,localhost
```

### 4. ���ݱ���

#### ���ݿⱸ��
```bash
# �������ݽű�
#!/bin/bash
BACKUP_DIR="/backup/campus-lost-found"
DATE=$(date +%Y%m%d_%H%M%S)

# ��������Ŀ¼
mkdir -p $BACKUP_DIR

# �������ݿ�
docker-compose exec postgres pg_dump -U postgres campus_lost_found > $BACKUP_DIR/db_$DATE.sql

# �����ϴ��ļ�
tar -czf $BACKUP_DIR/uploads_$DATE.tar.gz backend/uploads/

# ����ɱ��ݣ�����30�죩
find $BACKUP_DIR -name "*.sql" -mtime +30 -delete
find $BACKUP_DIR -name "*.tar.gz" -mtime +30 -delete
```

#### �Զ�����
```bash
# ��ӵ�crontab
crontab -e

# ÿ���賿2�㱸��
0 2 * * * /path/to/backup-script.sh
```

## ��غ�ά��

### 1. ��־���
```bash
# �鿴Ӧ����־
docker-compose logs -f backend
docker-compose logs -f frontend

# �鿴ϵͳ��־
journalctl -u docker -f
```

### 2. ���ܼ��
```bash
# �鿴��Դʹ�����
docker stats

# �鿴����ʹ��
df -h
du -sh backend/uploads/
```

### 3. ���²���
```bash
# ��ȡ���´���
git pull origin main

# ���¹���������
docker-compose down
docker-compose build --no-cache
docker-compose up -d
```

## �����ų�

### ��������

1. **�˿ڳ�ͻ**
   ```bash
   # �鿴�˿�ռ��
   netstat -tlnp | grep :8000
   
   # �޸�docker-compose.yml�еĶ˿�ӳ��
   ```

2. **�ڴ治��**
   ```bash
   # ����ElasticSearch�ڴ�����
   # ��docker-compose.yml���޸�ES_JAVA_OPTS
   ```

3. **�ļ�Ȩ������**
   ```bash
   # �޸��ϴ�Ŀ¼Ȩ��
   sudo chown -R 1000:1000 backend/uploads/
   ```

4. **���ݿ�����ʧ��**
   ```bash
   # ������ݿ�״̬
   docker-compose exec postgres pg_isready -U postgres
   
   # �������ݿ�
   docker-compose restart postgres
   ```

## ��ȫ����

1. **���ڸ�������**
   ```bash
   # ����Python����
   pip list --outdated
   pip install --upgrade package-name
   
   # ����Node.js����
   npm audit
   npm update
   ```

2. **���÷���ǽ**
   ```bash
   # ֻ�����Ҫ�˿�
   ufw allow 22    # SSH
   ufw allow 80    # HTTP
   ufw allow 443   # HTTPS
   ufw enable
   ```

3. **���ڱ���**
   - �����Զ����ݽű�
   - ���Ա��ݻָ�����
   - ��ش洢�����ļ�

4. **��ذ�ȫ��־**
   ```bash
   # �鿴��¼��־
   tail -f /var/log/auth.log
   
   # �鿴Nginx������־
   tail -f /var/log/nginx/access.log
   ```
