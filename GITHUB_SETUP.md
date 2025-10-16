# GitHub仓库设置指南

## 创建GitHub仓库

1. 访问 [GitHub](https://github.com)
2. 登录您的账户
3. 点击右上角的 "+" 按钮，选择 "New repository"
4. 填写仓库信息：
   - Repository name: `campus-lost-found`
   - Description: `基于AI技术的智能校园失物招领平台 - AI-powered campus lost & found system`
   - 选择 Public 或 Private
   - 不要勾选 "Add a README file"（我们已经有了）
   - 不要勾选 "Add .gitignore"（我们已经有了）
   - 不要选择 License（稍后可以添加）
5. 点击 "Create repository"

## 连接本地仓库到GitHub

创建GitHub仓库后，执行以下命令：

```bash
# 添加远程仓库（替换YOUR_USERNAME为您的GitHub用户名）
git remote add origin https://github.com/YOUR_USERNAME/campus-lost-found.git

# 推送代码到GitHub
git branch -M main
git push -u origin main
```

## 验证上传

上传完成后，您可以：
1. 访问您的GitHub仓库页面
2. 确认所有文件都已正确上传
3. 检查README.md是否正确显示

## 后续步骤

1. **添加许可证**：在GitHub仓库页面点击 "Add file" -> "Create new file"，文件名输入 `LICENSE`
2. **设置分支保护**：在Settings -> Branches中设置main分支保护
3. **配置CI/CD**：可以添加GitHub Actions进行自动测试和部署
4. **添加Issues模板**：在.github/ISSUE_TEMPLATE/中添加问题模板

## 项目特色

这个校园失物招领系统包含以下特色功能：

### ? 智能识别
- **OCR文字识别**：使用Tesseract自动识别上传照片中的文字信息
- **AI物品分类**：智能识别失物类别（手机、钱包、钥匙、书籍等）
- **多语言支持**：支持中英文文字识别

### ? 智能搜索
- **模糊匹配**：基于ElasticSearch的关键字模糊搜索
- **语义搜索**：支持自然语言查询
- **分类筛选**：按物品类别快速筛选

### ? 用户友好
- **响应式设计**：支持手机、平板、电脑多端访问
- **图片上传**：拖拽上传，支持多种图片格式
- **实时更新**：失物信息实时同步

### ?? 技术栈
- **后端**：Python + FastAPI + PostgreSQL + ElasticSearch
- **前端**：React + Ant Design
- **AI**：TensorFlow/PyTorch + Tesseract OCR
- **部署**：Docker + Docker Compose

## 快速开始

```bash
# 克隆项目
git clone https://github.com/YOUR_USERNAME/campus-lost-found.git
cd campus-lost-found

# 使用Docker启动所有服务
docker-compose up -d

# 访问应用
# 前端：http://localhost:3000
# 后端API：http://localhost:8000
# API文档：http://localhost:8000/docs
```

## 贡献指南

欢迎贡献代码！请：
1. Fork 本仓库
2. 创建特性分支
3. 提交更改
4. 创建 Pull Request
