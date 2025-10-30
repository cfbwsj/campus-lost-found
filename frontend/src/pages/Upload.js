import React, { useState } from 'react';
import {
  Card,
  Form,
  Input,
  Select,
  Button,
  Upload,
  message,
  Row,
  Col,
  Typography,
  Tag,
  Divider,
  Space,
  Progress
} from 'antd';
import {
  PlusOutlined,
  UploadOutlined,
  EyeOutlined,
  RobotOutlined,
  FileTextOutlined
} from '@ant-design/icons';
import { useDropzone } from 'react-dropzone';
import { uploadAPI, ocrAPI, classifyAPI } from '../services/api';

const { Title, Paragraph } = Typography;
const { TextArea } = Input;
const { Option } = Select;

const UploadPage = () => {
  const [form] = Form.useForm();
  const [loading, setLoading] = useState(false);
  const [uploadedFiles, setUploadedFiles] = useState([]);
  const [ocrResult, setOcrResult] = useState(null);
  const [aiClassification, setAiClassification] = useState(null);
  const [processing, setProcessing] = useState(false);
  const [itemType, setItemType] = useState('lost'); // 'lost' 或 'found'

  const categories = [
    '手机/数码产品',
    '钱包/证件',
    '钥匙/门卡',
    '书籍/文具',
    '衣物/饰品',
    '眼镜/配饰',
    '运动用品',
    '其他'
  ];

  const { getRootProps, getInputProps, isDragActive } = useDropzone({
    accept: {
      'image/*': ['.png', '.jpg', '.jpeg', '.gif', '.bmp', '.webp']
    },
    maxFiles: 5,
    maxSize: 10 * 1024 * 1024, // 10MB
    onDrop: handleFileDrop,
    disabled: loading || processing
  });

  async function handleFileDrop(acceptedFiles) {
    if (acceptedFiles.length === 0) return;

    setLoading(true);
    try {
      const uploadPromises = acceptedFiles.map(file => uploadAPI.uploadFile(file));
      const results = await Promise.all(uploadPromises);
      
      const newFiles = results.map((result, index) => ({
        id: Date.now() + index,
        file: acceptedFiles[index],
        url: result.url,
        filename: result.filename,
        size: result.size
      }));

      setUploadedFiles(prev => [...prev, ...newFiles]);
      message.success(`成功上传 ${acceptedFiles.length} 个文件`);

      // 自动进行OCR和AI分类
      if (acceptedFiles.length > 0) {
        await processImage(acceptedFiles[0], results[0].url);
      }

    } catch (error) {
      console.error('文件上传失败:', error);
      message.error('文件上传失败');
    } finally {
      setLoading(false);
    }
  }

  const processImage = async (file, imageUrl) => {
    setProcessing(true);
    try {
      // 并行进行OCR和AI分类
      const [ocrRes, classifyRes] = await Promise.all([
        ocrAPI.extractText(file),
        classifyAPI.classifyImage(file)
      ]);

      setOcrResult(ocrRes);
      setAiClassification(classifyRes);

      // 自动填充表单
      if (ocrRes.text) {
        form.setFieldsValue({
          description: ocrRes.text
        });
      }

      if (classifyRes.category) {
        form.setFieldsValue({
          category: classifyRes.category
        });
      }

      message.success('图片处理完成');

    } catch (error) {
      console.error('图片处理失败:', error);
      message.error('图片处理失败');
    } finally {
      setProcessing(false);
    }
  };

  const handleRemoveFile = (fileId) => {
    setUploadedFiles(prev => prev.filter(file => file.id !== fileId));
  };

  const handleSubmit = async (values) => {
    if (uploadedFiles.length === 0) {
      message.error('请至少上传一张图片');
      return;
    }

    setLoading(true);
    try {
      const submitData = {
        ...values,
        image_url: uploadedFiles[0].url,
        ocr_text: ocrResult?.text || '',
        ai_category: aiClassification?.category || '',
        confidence: aiClassification?.confidence || 0
      };

      // 根据表单类型调用对应的API
      const apiEndpoint = itemType === 'lost' ? '/api/items/lost' : '/api/items/found';
      const response = await fetch(`${process.env.REACT_APP_API_URL || 'http://localhost:8000'}${apiEndpoint}`, {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify(submitData),
      });

      if (!response.ok) {
        throw new Error('提交失败');
      }

      const result = await response.json();
      
      message.success('发布成功！');
      
      // 延迟跳转，让用户看到成功消息
      setTimeout(() => {
        window.location.href = itemType === 'lost' ? '/lost' : '/found';
      }, 1500);
      form.resetFields();
      setUploadedFiles([]);
      setOcrResult(null);
      setAiClassification(null);

    } catch (error) {
      console.error('提交失败:', error);
      message.error('提交失败');
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className="page-container">
      <div className="page-header">
        <Title level={2}>发布失物/招领信息</Title>
        <Paragraph>
          上传物品照片，系统将自动进行OCR文字识别和AI物品分类
        </Paragraph>
      </div>

      <div className="page-content">
        <Row gutter={[24, 24]}>
          {/* 左侧：表单 */}
          <Col xs={24} lg={14}>
            <Card title="基本信息">
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
                  rules={[{ required: true, message: '请选择信息类型' }]}
                >
                  <Select placeholder="请选择">
                    <Option value="lost">失物信息</Option>
                    <Option value="found">招领信息</Option>
                  </Select>
                </Form.Item>

                <Form.Item
                  name="title"
                  label="标题"
                  rules={[{ required: true, message: '请输入标题' }]}
                >
                  <Input placeholder="请输入物品标题" />
                </Form.Item>

                <Form.Item
                  name="description"
                  label="详细描述"
                  rules={[{ required: true, message: '请输入详细描述' }]}
                >
                  <TextArea 
                    rows={4} 
                    placeholder="请详细描述物品特征、发现地点等信息"
                  />
                </Form.Item>

                <Row gutter={16}>
                  <Col span={12}>
                    <Form.Item
                      name="category"
                      label="物品类别"
                    >
                      <Select placeholder="请选择类别" allowClear>
                        {categories.map(category => (
                          <Option key={category} value={category}>
                            {category}
                          </Option>
                        ))}
                      </Select>
                    </Form.Item>
                  </Col>
                  <Col span={12}>
                    <Form.Item
                      name="location"
                      label="发现地点"
                    >
                      <Input placeholder="请输入发现地点" />
                    </Form.Item>
                  </Col>
                </Row>

                <Form.Item
                  name="contact_info"
                  label="联系方式"
                  rules={[{ required: true, message: '请输入联系方式' }]}
                >
                  <Input placeholder="请输入您的联系方式" />
                </Form.Item>

                <Form.Item>
                  <Button 
                    type="primary" 
                    htmlType="submit" 
                    loading={loading}
                    size="large"
                    block
                  >
                    发布信息
                  </Button>
                </Form.Item>
              </Form>
            </Card>
          </Col>

          {/* 右侧：图片上传和处理结果 */}
          <Col xs={24} lg={10}>
            {/* 图片上传 */}
            <Card title="上传图片" style={{ marginBottom: 24 }}>
              <div
                {...getRootProps()}
                className={`upload-dragger ${isDragActive ? 'ant-upload-drag-hover' : ''}`}
              >
                <input {...getInputProps()} />
                {isDragActive ? (
                  <p>将图片拖拽到这里...</p>
                ) : (
                  <div>
                    <UploadOutlined style={{ fontSize: 48, color: '#1890ff', marginBottom: 16 }} />
                    <p>点击或拖拽图片到此区域上传</p>
                    <p style={{ color: '#999', fontSize: '12px' }}>
                      支持 PNG、JPG、JPEG、GIF、BMP、WEBP 格式，单个文件不超过 10MB
                    </p>
                  </div>
                )}
              </div>

              {loading && (
                <div style={{ marginTop: 16 }}>
                  <Progress percent={50} status="active" />
                  <p style={{ textAlign: 'center', marginTop: 8 }}>正在上传...</p>
                </div>
              )}

              {processing && (
                <div style={{ marginTop: 16 }}>
                  <Progress percent={75} status="active" />
                  <p style={{ textAlign: 'center', marginTop: 8 }}>
                    <RobotOutlined /> 正在AI处理中...
                  </p>
                </div>
              )}

              {/* 已上传的文件 */}
              {uploadedFiles.length > 0 && (
                <div style={{ marginTop: 16 }}>
                  <Title level={5}>已上传的图片：</Title>
                  <Row gutter={[8, 8]}>
                    {uploadedFiles.map(file => (
                      <Col key={file.id} span={8}>
                        <div style={{ position: 'relative' }}>
                          <img
                            src={file.url}
                            alt={file.filename}
                            style={{
                              width: '100%',
                              height: '80px',
                              objectFit: 'cover',
                              borderRadius: '4px'
                            }}
                          />
                          <Button
                            size="small"
                            danger
                            style={{
                              position: 'absolute',
                              top: 4,
                              right: 4
                            }}
                            onClick={() => handleRemoveFile(file.id)}
                          >
                            删除
                          </Button>
                        </div>
                      </Col>
                    ))}
                  </Row>
                </div>
              )}
            </Card>

            {/* OCR结果 */}
            {ocrResult && (
              <Card title={
                <Space>
                  <FileTextOutlined />
                  OCR识别结果
                  <Tag color="green">置信度: {(ocrResult.confidence || 0).toFixed(1)}%</Tag>
                </Space>
              } style={{ marginBottom: 24 }}>
                <div className="ocr-result">
                  <Paragraph copyable={{ text: ocrResult.text }}>
                    {ocrResult.text || '未识别到文字'}
                  </Paragraph>
                </div>
              </Card>
            )}

            {/* AI分类结果 */}
            {aiClassification && (
              <Card title={
                <Space>
                  <RobotOutlined />
                  AI物品分类
                  <Tag color="blue">置信度: {(aiClassification.confidence * 100).toFixed(1)}%</Tag>
                </Space>
              }>
                <div className="ai-classification">
                  <Title level={4}>识别类别：{aiClassification.category}</Title>
                  {aiClassification.subcategories && (
                    <div style={{ marginTop: 12 }}>
                      <Title level={5}>可能的类别：</Title>
                      <Space wrap>
                        {aiClassification.subcategories.map((sub, index) => (
                          <Tag key={index}>{sub}</Tag>
                        ))}
                      </Space>
                    </div>
                  )}
                </div>
              </Card>
            )}
          </Col>
        </Row>
      </div>
    </div>
  );
};

export default UploadPage;
