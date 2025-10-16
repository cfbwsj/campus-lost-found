# GitHub�ֿ�����ָ��

## ����GitHub�ֿ�

1. ���� [GitHub](https://github.com)
2. ��¼�����˻�
3. ������Ͻǵ� "+" ��ť��ѡ�� "New repository"
4. ��д�ֿ���Ϣ��
   - Repository name: `campus-lost-found`
   - Description: `����AI����������У԰ʧ������ƽ̨ - AI-powered campus lost & found system`
   - ѡ�� Public �� Private
   - ��Ҫ��ѡ "Add a README file"�������Ѿ����ˣ�
   - ��Ҫ��ѡ "Add .gitignore"�������Ѿ����ˣ�
   - ��Ҫѡ�� License���Ժ������ӣ�
5. ��� "Create repository"

## ���ӱ��زֿ⵽GitHub

����GitHub�ֿ��ִ���������

```bash
# ���Զ�ֿ̲⣨�滻YOUR_USERNAMEΪ����GitHub�û�����
git remote add origin https://github.com/YOUR_USERNAME/campus-lost-found.git

# ���ʹ��뵽GitHub
git branch -M main
git push -u origin main
```

## ��֤�ϴ�

�ϴ���ɺ������ԣ�
1. ��������GitHub�ֿ�ҳ��
2. ȷ�������ļ�������ȷ�ϴ�
3. ���README.md�Ƿ���ȷ��ʾ

## ��������

1. **������֤**����GitHub�ֿ�ҳ���� "Add file" -> "Create new file"���ļ������� `LICENSE`
2. **���÷�֧����**����Settings -> Branches������main��֧����
3. **����CI/CD**���������GitHub Actions�����Զ����ԺͲ���
4. **���Issuesģ��**����.github/ISSUE_TEMPLATE/���������ģ��

## ��Ŀ��ɫ

���У԰ʧ������ϵͳ����������ɫ���ܣ�

### ? ����ʶ��
- **OCR����ʶ��**��ʹ��Tesseract�Զ�ʶ���ϴ���Ƭ�е�������Ϣ
- **AI��Ʒ����**������ʶ��ʧ������ֻ���Ǯ����Կ�ס��鼮�ȣ�
- **������֧��**��֧����Ӣ������ʶ��

### ? ��������
- **ģ��ƥ��**������ElasticSearch�Ĺؼ���ģ������
- **��������**��֧����Ȼ���Բ�ѯ
- **����ɸѡ**������Ʒ������ɸѡ

### ? �û��Ѻ�
- **��Ӧʽ���**��֧���ֻ���ƽ�塢���Զ�˷���
- **ͼƬ�ϴ�**����ק�ϴ���֧�ֶ���ͼƬ��ʽ
- **ʵʱ����**��ʧ����Ϣʵʱͬ��

### ?? ����ջ
- **���**��Python + FastAPI + PostgreSQL + ElasticSearch
- **ǰ��**��React + Ant Design
- **AI**��TensorFlow/PyTorch + Tesseract OCR
- **����**��Docker + Docker Compose

## ���ٿ�ʼ

```bash
# ��¡��Ŀ
git clone https://github.com/YOUR_USERNAME/campus-lost-found.git
cd campus-lost-found

# ʹ��Docker�������з���
docker-compose up -d

# ����Ӧ��
# ǰ�ˣ�http://localhost:3000
# ���API��http://localhost:8000
# API�ĵ���http://localhost:8000/docs
```

## ����ָ��

��ӭ���״��룡�룺
1. Fork ���ֿ�
2. �������Է�֧
3. �ύ����
4. ���� Pull Request
