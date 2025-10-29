# 校园失物招领系统

一个基于AI技术的智能校园失物招领平台，支持照片上传、OCR文字识别、智能物品分类和模糊搜索功能。

## 功能特性

### ✨ 智能识别
- **OCR文字识别**：使用Tesseract自动识别上传照片中的文字信息
- **AI物品分类**：智能识别失物类别（手机、钱包、钥匙、书籍等）
- **多语言支持**：支持中英文文字识别

### 🔍 智能搜索
- **模糊匹配**：基于ElasticSearch的关键字模糊搜索
- **语义搜索**：支持自然语言查询
- **分类筛选**：按物品类别快速筛选

### 👥 用户友好
- **响应式设计**：支持手机、平板、电脑多端访问
- **图片上传**：拖拽上传，支持多种图片格式
- **实时更新**：失物信息实时同步

## 技术栈

### 后端
- **Python 3.8+**
- **FastAPI**：高性能Web框架
- **Tesseract OCR**：文字识别引擎
- **ElasticSearch**：搜索引擎
- **OpenCV**：图像处理
- **TensorFlow/PyTorch**：AI模型

### 前端
- **React 18**：用户界面框架
- **Ant Design**：UI组件库
- **Axios**：HTTP客户端
- **React Router**：路由管理

### 数据库
- **PostgreSQL**：主数据库
- **ElasticSearch**：搜索引擎
- **Redis**：缓存

## 项目结构

```
campus-lost-found/
├── backend/                 # 后端代码
│   ├── api/                # API接口
│   ├── models/             # 数据模型
│   ├── utils/              # 工具函数
│   ├── uploads/            # 上传文件目录
│   └── requirements.txt    # Python依赖
├── frontend/               # 前端代码
│   ├── src/                # 源代码
│   ├── public/             # 静态资源
│   └── package.json        # Node.js依赖
├── docs/                   # 文档
└── README.md              # 项目说明
```

## 快速开始

### 环境要求
- Python 3.8+
- Node.js 16+
- ElasticSearch 7.x
- PostgreSQL 12+
- Tesseract OCR

### 安装步骤

1. **克隆项目**
```bash
git clone https://github.com/your-username/campus-lost-found.git
cd campus-lost-found
```

2. **后端设置**
```bash
cd backend
pip install -r requirements.txt
python main.py
```

3. **前端设置**
```bash
cd frontend
npm install
npm start
```

4. **启动服务**
- 后端API：http://localhost:8000
- 前端界面：http://localhost:3000
- API文档：http://localhost:8000/docs

## API文档

### 失物管理
- `POST /api/items` - 发布失物信息
- `GET /api/items` - 获取失物列表
- `GET /api/items/{id}` - 获取失物详情
- `PUT /api/items/{id}` - 更新失物信息
- `DELETE /api/items/{id}` - 删除失物信息

### 搜索功能
- `GET /api/search` - 关键字搜索
- `GET /api/search/image` - 图片相似搜索
- `GET /api/categories` - 获取物品分类

### 图片处理
- `POST /api/upload` - 上传图片
- `POST /api/ocr` - OCR文字识别
- `POST /api/classify` - AI物品分类

## 部署指南

### Docker部署
```bash
docker-compose up -d
```

### 生产环境部署
详见 [部署文档](docs/deployment/)

## 贡献指南

1. Fork 本仓库
2. 创建特性分支 (`git checkout -b feature/AmazingFeature`)
3. 提交更改 (`git commit -m 'Add some AmazingFeature'`)
4. 推送到分支 (`git push origin feature/AmazingFeature`)
5. 打开 Pull Request

## 许可证

本项目采用 MIT 许可证 - 查看 [LICENSE](LICENSE) 文件了解详情。

## 联系方式

- 项目维护者：[cfbwsj]
- 邮箱：2514912874@qq.com
- 项目链接：https://github.com/your-username/campus-lost-found

## 致谢

- [Tesseract OCR](https://github.com/tesseract-ocr/tesseract)
- [ElasticSearch](https://www.elastic.co/)
- [FastAPI](https://fastapi.tiangolo.com/)
- [React](https://reactjs.org/)
- [Ant Design](https://ant.design/)

