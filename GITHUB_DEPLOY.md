# GitHub部署指南

本指南将帮助您将校园失物招领系统部署到GitHub。

## 📋 前提条件

1. 已安装Git
2. 拥有GitHub账号
3. 已创建GitHub仓库：https://github.com/cfbwsj/campus-lost-found

## 🚀 部署步骤

### 1. 初始化Git仓库（如果还没有）

```bash
cd D:\AIweb\campus-lost-found

# 初始化Git仓库
git init

# 添加远程仓库
git remote add origin https://github.com/cfbwsj/campus-lost-found.git
```

### 2. 检查.gitignore文件

确保`.gitignore`文件包含以下内容（已配置）：
- `node_modules/` - Node.js依赖
- `__pycache__/` - Python缓存
- `.env` - 环境变量文件
- `backend/uploads/` - 上传文件目录
- `venv/` - Python虚拟环境

### 3. 添加所有文件到Git

```bash
# 查看文件状态
git status

# 添加所有文件
git add .

# 查看将要提交的文件
git status
```

### 4. 创建首次提交

```bash
# 提交代码
git commit -m "初始提交：完整版校园失物招领系统

功能特性：
- ✅ OCR文字识别（Tesseract）
- ✅ AI物品分类（PyTorch + ResNet）
- ✅ 模糊搜索（ElasticSearch）
- ✅ 图片上传和管理
- ✅ 失物招领信息管理
- ✅ Docker容器化部署
- ✅ React前端界面
- ✅ FastAPI后端服务
- ✅ MySQL数据库支持
- ✅ 完整的API文档

技术栈：
- 后端：Python 3.9, FastAPI, SQLAlchemy, PyTorch, Tesseract
- 前端：React 18, Ant Design, Axios
- 数据库：MySQL, ElasticSearch, Redis
- 部署：Docker, Docker Compose"
```

### 5. 推送到GitHub

```bash
# 首次推送（如果仓库是空的）
git push -u origin main

# 或者如果主分支是master
git push -u origin master

# 如果远程仓库已有内容，可能需要先拉取
git pull origin main --allow-unrelated-histories
git push -u origin main
```

## 🔧 常见问题解决

### 问题1: 远程仓库已存在内容

```bash
# 先拉取远程内容
git pull origin main --allow-unrelated-histories

# 解决可能的冲突后
git push -u origin main
```

### 问题2: 认证失败

GitHub已不支持密码认证，需要使用个人访问令牌（PAT）：

1. 访问 https://github.com/settings/tokens
2. 点击"Generate new token"
3. 选择权限（至少需要`repo`）
4. 生成并复制令牌
5. 推送时使用令牌作为密码

或使用SSH方式：
```bash
# 修改远程仓库地址为SSH
git remote set-url origin git@github.com:cfbwsj/campus-lost-found.git

# 确保已配置SSH密钥
```

### 问题3: 文件过大

如果某些文件过大无法推送：

```bash
# 查看大文件
du -sh * | sort -hr | head -20

# 将大文件添加到.gitignore
echo "large-file.zip" >> .gitignore

# 从Git历史中移除
git rm --cached large-file.zip
git commit -m "移除大文件"
git push
```

## 📝 更新代码到GitHub

以后更新代码时：

```bash
# 查看修改的文件
git status

# 添加修改的文件
git add .

# 提交修改
git commit -m "描述你的修改"

# 推送到GitHub
git push
```

## 🌟 GitHub仓库设置建议

### 1. 添加README徽章

在`README.md`顶部添加：

```markdown
![Python](https://img.shields.io/badge/Python-3.9+-blue)
![FastAPI](https://img.shields.io/badge/FastAPI-0.104-green)
![React](https://img.shields.io/badge/React-18.2-blue)
![License](https://img.shields.io/badge/License-MIT-yellow)
```

### 2. 设置GitHub Pages（可选）

如果要部署前端到GitHub Pages：

1. 在GitHub仓库设置中启用GitHub Pages
2. 选择`gh-pages`分支
3. 运行以下命令：

```bash
cd frontend
npm run build

# 安装gh-pages
npm install --save-dev gh-pages

# 在package.json中添加：
# "homepage": "https://cfbwsj.github.io/campus-lost-found",
# "scripts": {
#   "predeploy": "npm run build",
#   "deploy": "gh-pages -d build"
# }

# 部署
npm run deploy
```

### 3. 设置Issues模板

创建`.github/ISSUE_TEMPLATE/bug_report.md`：

```markdown
---
name: Bug报告
about: 创建报告帮助我们改进
title: '[BUG] '
labels: bug
assignees: ''
---

**描述bug**
简要描述bug的内容。

**重现步骤**
1. 访问 '...'
2. 点击 '....'
3. 滚动到 '....'
4. 看到错误

**期望行为**
描述你期望发生什么。

**截图**
如果可以，添加截图帮助解释问题。

**环境信息：**
 - OS: [e.g. Windows 10]
 - Browser [e.g. chrome, safari]
 - Version [e.g. 22]
```

### 4. 添加贡献指南

创建`CONTRIBUTING.md`：

```markdown
# 贡献指南

感谢您对校园失物招领系统的关注！

## 如何贡献

1. Fork本仓库
2. 创建特性分支 (`git checkout -b feature/AmazingFeature`)
3. 提交更改 (`git commit -m 'Add some AmazingFeature'`)
4. 推送到分支 (`git push origin feature/AmazingFeature`)
5. 打开Pull Request

## 代码规范

- Python代码遵循PEP 8
- JavaScript代码使用ESLint
- 提交信息使用中文，清晰描述修改内容

## 测试

在提交PR前，请确保：
- 所有测试通过
- 代码已经过linter检查
- 添加了必要的文档
```

## 🔒 安全提示

### 不要提交敏感信息

确保以下文件不会被提交：
- `.env` - 包含数据库密码等
- `config.json` - 包含API密钥
- `*.key` / `*.pem` - SSL证书和密钥

### 检查提交历史

```bash
# 查看提交历史中是否有敏感信息
git log -p | grep -i password
git log -p | grep -i secret
git log -p | grep -i api_key
```

如果不小心提交了敏感信息：

```bash
# 从历史中移除文件（危险操作！）
git filter-branch --tree-filter 'rm -f path/to/sensitive/file' HEAD
git push --force
```

## 📊 设置GitHub Actions（可选）

创建`.github/workflows/ci.yml`实现自动化测试和部署：

```yaml
name: CI/CD

on:
  push:
    branches: [ main ]
  pull_request:
    branches: [ main ]

jobs:
  test:
    runs-on: ubuntu-latest
    
    steps:
    - uses: actions/checkout@v2
    
    - name: Set up Python
      uses: actions/setup-python@v2
      with:
        python-version: 3.9
    
    - name: Install dependencies
      run: |
        cd backend
        pip install -r requirements.txt
    
    - name: Run tests
      run: |
        cd backend
        pytest
```

## ✅ 检查清单

推送到GitHub前，请确认：

- [ ] 所有简化版和临时文件已删除
- [ ] `.gitignore`配置正确
- [ ] 敏感信息（密码、密钥）未包含
- [ ] README.md内容完整
- [ ] 代码可以正常运行
- [ ] Docker配置文件正确
- [ ] 数据库初始化脚本存在
- [ ] 文档齐全（DEPLOY.md, README.md等）

## 🎉 完成！

完成以上步骤后，您的项目就成功部署到GitHub了！

访问您的仓库：https://github.com/cfbwsj/campus-lost-found

下一步可以：
1. 完善README文档
2. 添加项目演示截图或视频
3. 邀请其他开发者协作
4. 设置CI/CD自动化部署

