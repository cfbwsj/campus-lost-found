# 🔧 手动修复 Upload.js 编译错误

## 问题
前端部署失败，错误信息：
```
[eslint] 
src/pages/Upload.js
  Line 149:27:  'itemType' is not defined  no-undef
  Line 168:32:  'itemType' is not defined  no-undef
```

---

## 解决方案：在GitHub网页上修改

### 步骤1：打开文件

访问：https://github.com/cfbwsj/campus-lost-found/blob/main/frontend/src/pages/Upload.js

---

### 步骤2：点击编辑

点击右上角的 **铅笔图标**（Edit this file）

---

### 步骤3：找到第32行

搜索：`const UploadPage = () => {`

应该看到：
```javascript
const UploadPage = () => {
  const [form] = Form.useForm();
  const [loading, setLoading] = useState(false);
  const [uploadedFiles, setUploadedFiles] = useState([]);
  const [ocrResult, setOcrResult] = useState(null);
  const [aiClassification, setAiClassification] = useState(null);
  const [processing, setProcessing] = useState(false);
```

---

### 步骤4：在第39行添加一行

**在 `const [processing, setProcessing] = useState(false);` 下面添加**：

```javascript
  const [itemType, setItemType] = useState('lost'); // 'lost' 或 'found'
```

**修改后应该是**：
```javascript
const UploadPage = () => {
  const [form] = Form.useForm();
  const [loading, setLoading] = useState(false);
  const [uploadedFiles, setUploadedFiles] = useState([]);
  const [ocrResult, setOcrResult] = useState(null);
  const [aiClassification, setAiClassification] = useState(null);
  const [processing, setProcessing] = useState(false);
  const [itemType, setItemType] = useState('lost'); // 'lost' 或 'found'
```

---

### 步骤5：找到表单部分（约第198行）

搜索：`<Form`

找到这部分代码：
```javascript
              <Form
                form={form}
                layout="vertical"
                onFinish={handleSubmit}
              >
                <Form.Item
                  name="type"
                  label="信息类型"
```

---

### 步骤6：在 Form.Item 之前添加类型选择器

**在 `<Form.Item name="type"` 之前添加**：

```javascript
                <Form.Item
                  label="发布类型"
                  name="publish_type"
                  initialValue="lost"
                >
                  <Select onChange={(value) => setItemType(value)}>
                    <Option value="lost">我丢失了物品（发布失物信息）</Option>
                    <Option value="found">我捡到了物品（发布招领信息）</Option>
                  </Select>
                </Form.Item>

```

**修改后应该是**：
```javascript
              <Form
                form={form}
                layout="vertical"
                onFinish={handleSubmit}
              >
                <Form.Item
                  label="发布类型"
                  name="publish_type"
                  initialValue="lost"
                >
                  <Select onChange={(value) => setItemType(value)}>
                    <Option value="lost">我丢失了物品（发布失物信息）</Option>
                    <Option value="found">我捡到了物品（发布招领信息）</Option>
                  </Select>
                </Form.Item>

                <Form.Item
                  name="type"
                  label="信息类型"
```

---

### 步骤7：提交修改

1. 滚动到页面底部
2. 在 "Commit changes" 对话框中输入：
   ```
   修复Upload组件：添加itemType状态和类型选择器
   ```
3. 选择 "Commit directly to the main branch"
4. 点击 "Commit changes" 按钮

---

## ✅ 完成

提交后：
- Render会自动检测到更新
- 3-5分钟后前端会重新部署
- 编译错误会消失
- 网站可以正常访问

---

## 📊 修改总结

| 文件 | 修改位置 | 修改内容 |
|------|---------|---------|
| Upload.js | 第39行 | 添加 `itemType` 状态 |
| Upload.js | 第203-213行 | 添加类型选择器 |

---

## 🧪 验证

部署成功后，访问：
```
https://campus-frontend-d5j1.onrender.com/upload
```

应该看到：
- ✅ "发布类型" 下拉选择器
- ✅ 可以选择"失物"或"招领"
- ✅ 填写信息后可以成功发布

---

如果有任何问题，请告诉我！

