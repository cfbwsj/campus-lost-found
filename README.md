# У԰ʧ������ϵͳ

һ������AI����������У԰ʧ������ƽ̨��֧����Ƭ�ϴ���OCR����ʶ��������Ʒ�����ģ���������ܡ�

## ��������

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

## ����ջ

### ���
- **Python 3.8+**
- **FastAPI**��������Web���
- **Tesseract OCR**������ʶ������
- **ElasticSearch**����������
- **OpenCV**��ͼ����
- **TensorFlow/PyTorch**��AIģ��

### ǰ��
- **React 18**���û�������
- **Ant Design**��UI�����
- **Axios**��HTTP�ͻ���
- **React Router**��·�ɹ���

### ���ݿ�
- **PostgreSQL**�������ݿ�
- **ElasticSearch**����������
- **Redis**������

## ��Ŀ�ṹ

```
campus-lost-found/
������ backend/                 # ��˴���
��   ������ api/                # API�ӿ�
��   ������ models/             # ����ģ��
��   ������ utils/              # ���ߺ���
��   ������ uploads/            # �ϴ��ļ�Ŀ¼
��   ������ requirements.txt    # Python����
������ frontend/               # ǰ�˴���
��   ������ src/                # Դ����
��   ������ public/             # ��̬��Դ
��   ������ package.json        # Node.js����
������ docs/                   # �ĵ�
������ README.md              # ��Ŀ˵��
```

## ���ٿ�ʼ

### ����Ҫ��
- Python 3.8+
- Node.js 16+
- ElasticSearch 7.x
- PostgreSQL 12+
- Tesseract OCR

### ��װ����

1. **��¡��Ŀ**
```bash
git clone https://github.com/your-username/campus-lost-found.git
cd campus-lost-found
```

2. **�������**
```bash
cd backend
pip install -r requirements.txt
python main.py
```

3. **ǰ������**
```bash
cd frontend
npm install
npm start
```

4. **��������**
- ���API��http://localhost:8000
- ǰ�˽��棺http://localhost:3000
- API�ĵ���http://localhost:8000/docs

## API�ĵ�

### ʧ�����
- `POST /api/items` - ����ʧ����Ϣ
- `GET /api/items` - ��ȡʧ���б�
- `GET /api/items/{id}` - ��ȡʧ������
- `PUT /api/items/{id}` - ����ʧ����Ϣ
- `DELETE /api/items/{id}` - ɾ��ʧ����Ϣ

### ��������
- `GET /api/search` - �ؼ�������
- `GET /api/search/image` - ͼƬ��������
- `GET /api/categories` - ��ȡ��Ʒ����

### ͼƬ����
- `POST /api/upload` - �ϴ�ͼƬ
- `POST /api/ocr` - OCR����ʶ��
- `POST /api/classify` - AI��Ʒ����

## ����ָ��

### Docker����
```bash
docker-compose up -d
```

### ������������
��� [�����ĵ�](docs/deployment/)

## ����ָ��

1. Fork ���ֿ�
2. �������Է�֧ (`git checkout -b feature/AmazingFeature`)
3. �ύ���� (`git commit -m 'Add some AmazingFeature'`)
4. ���͵���֧ (`git push origin feature/AmazingFeature`)
5. �� Pull Request

## ���֤

����Ŀ���� MIT ���֤ - �鿴 [LICENSE](LICENSE) �ļ��˽����顣

## ��ϵ��ʽ

- ��Ŀά���ߣ�[Your Name]
- ���䣺your.email@example.com
- ��Ŀ���ӣ�https://github.com/your-username/campus-lost-found

## ��л

- [Tesseract OCR](https://github.com/tesseract-ocr/tesseract)
- [ElasticSearch](https://www.elastic.co/)
- [FastAPI](https://fastapi.tiangolo.com/)
- [React](https://reactjs.org/)
- [Ant Design](https://ant.design/)
