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

const Upload = () => {
  const [form] = Form.useForm();
  const [loading, setLoading] = useState(false);
  const [uploadedFiles, setUploadedFiles] = useState([]);
  const [ocrResult, setOcrResult] = useState(null);
  const [aiClassification, setAiClassification] = useState(null);
  const [processing, setProcessing] = useState(false);

  const categories = [
    '�ֻ�/�����Ʒ',
    'Ǯ��/֤��',
    'Կ��/�ſ�',
    '�鼮/�ľ�',
    '����/��Ʒ',
    '�۾�/����',
    '�˶���Ʒ',
    '����'
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
      message.success(`�ɹ��ϴ� ${acceptedFiles.length} ���ļ�`);

      // �Զ�����OCR��AI����
      if (acceptedFiles.length > 0) {
        await processImage(acceptedFiles[0], results[0].url);
      }

    } catch (error) {
      console.error('�ļ��ϴ�ʧ��:', error);
      message.error('�ļ��ϴ�ʧ��');
    } finally {
      setLoading(false);
    }
  }

  const processImage = async (file, imageUrl) => {
    setProcessing(true);
    try {
      // ���н���OCR��AI����
      const [ocrRes, classifyRes] = await Promise.all([
        ocrAPI.extractText(file),
        classifyAPI.classifyImage(file)
      ]);

      setOcrResult(ocrRes);
      setAiClassification(classifyRes);

      // �Զ�����
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

      message.success('ͼƬ�������');

    } catch (error) {
      console.error('ͼƬ����ʧ��:', error);
      message.error('ͼƬ����ʧ��');
    } finally {
      setProcessing(false);
    }
  };

  const handleRemoveFile = (fileId) => {
    setUploadedFiles(prev => prev.filter(file => file.id !== fileId));
  };

  const handleSubmit = async (values) => {
    if (uploadedFiles.length === 0) {
      message.error('�������ϴ�һ��ͼƬ');
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

      // ������ݱ����;��������ĸ�API
      // const result = await lostItemsAPI.createLostItem(submitData);
      
      message.success('�����ɹ���');
      form.resetFields();
      setUploadedFiles([]);
      setOcrResult(null);
      setAiClassification(null);

    } catch (error) {
      console.error('�ύʧ��:', error);
      message.error('�ύʧ��');
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className="page-container">
      <div className="page-header">
        <Title level={2}>����ʧ��/������Ϣ</Title>
        <Paragraph>
          �ϴ���Ʒ��Ƭ��ϵͳ���Զ�����OCR����ʶ���AI��Ʒ����
        </Paragraph>
      </div>

      <div className="page-content">
        <Row gutter={[24, 24]}>
          {/* ��ࣺ�� */}
          <Col xs={24} lg={14}>
            <Card title="������Ϣ">
              <Form
                form={form}
                layout="vertical"
                onFinish={handleSubmit}
              >
                <Form.Item
                  name="type"
                  label="��Ϣ����"
                  rules={[{ required: true, message: '��ѡ����Ϣ����' }]}
                >
                  <Select placeholder="��ѡ��">
                    <Option value="lost">ʧ����Ϣ</Option>
                    <Option value="found">������Ϣ</Option>
                  </Select>
                </Form.Item>

                <Form.Item
                  name="title"
                  label="����"
                  rules={[{ required: true, message: '���������' }]}
                >
                  <Input placeholder="��������Ʒ����" />
                </Form.Item>

                <Form.Item
                  name="description"
                  label="��ϸ����"
                  rules={[{ required: true, message: '��������ϸ����' }]}
                >
                  <TextArea 
                    rows={4} 
                    placeholder="����ϸ������Ʒ���������ֵص����Ϣ"
                  />
                </Form.Item>

                <Row gutter={16}>
                  <Col span={12}>
                    <Form.Item
                      name="category"
                      label="��Ʒ���"
                    >
                      <Select placeholder="��ѡ�����" allowClear>
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
                      label="���ֵص�"
                    >
                      <Input placeholder="�����뷢�ֵص�" />
                    </Form.Item>
                  </Col>
                </Row>

                <Form.Item
                  name="contact_info"
                  label="��ϵ��ʽ"
                  rules={[{ required: true, message: '��������ϵ��ʽ' }]}
                >
                  <Input placeholder="������������ϵ��ʽ" />
                </Form.Item>

                <Form.Item>
                  <Button 
                    type="primary" 
                    htmlType="submit" 
                    loading={loading}
                    size="large"
                    block
                  >
                    ������Ϣ
                  </Button>
                </Form.Item>
              </Form>
            </Card>
          </Col>

          {/* �ҲࣺͼƬ�ϴ��ʹ����� */}
          <Col xs={24} lg={10}>
            {/* ͼƬ�ϴ� */}
            <Card title="�ϴ�ͼƬ" style={{ marginBottom: 24 }}>
              <div
                {...getRootProps()}
                className={`upload-dragger ${isDragActive ? 'ant-upload-drag-hover' : ''}`}
              >
                <input {...getInputProps()} />
                {isDragActive ? (
                  <p>��ͼƬ��ק������...</p>
                ) : (
                  <div>
                    <UploadOutlined style={{ fontSize: 48, color: '#1890ff', marginBottom: 16 }} />
                    <p>�������קͼƬ���������ϴ�</p>
                    <p style={{ color: '#999', fontSize: '12px' }}>
                      ֧�� PNG��JPG��JPEG��GIF��BMP��WEBP ��ʽ�������ļ������� 10MB
                    </p>
                  </div>
                )}
              </div>

              {loading && (
                <div style={{ marginTop: 16 }}>
                  <Progress percent={50} status="active" />
                  <p style={{ textAlign: 'center', marginTop: 8 }}>�����ϴ�...</p>
                </div>
              )}

              {processing && (
                <div style={{ marginTop: 16 }}>
                  <Progress percent={75} status="active" />
                  <p style={{ textAlign: 'center', marginTop: 8 }}>
                    <RobotOutlined /> ����AI������...
                  </p>
                </div>
              )}

              {/* ���ϴ����ļ� */}
              {uploadedFiles.length > 0 && (
                <div style={{ marginTop: 16 }}>
                  <Title level={5}>���ϴ���ͼƬ��</Title>
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
                            ɾ��
                          </Button>
                        </div>
                      </Col>
                    ))}
                  </Row>
                </div>
              )}
            </Card>

            {/* OCR��� */}
            {ocrResult && (
              <Card title={
                <Space>
                  <FileTextOutlined />
                  OCRʶ����
                  <Tag color="green">���Ŷ�: {(ocrResult.confidence || 0).toFixed(1)}%</Tag>
                </Space>
              } style={{ marginBottom: 24 }}>
                <div className="ocr-result">
                  <Paragraph copyable={{ text: ocrResult.text }}>
                    {ocrResult.text || 'δʶ������'}
                  </Paragraph>
                </div>
              </Card>
            )}

            {/* AI������ */}
            {aiClassification && (
              <Card title={
                <Space>
                  <RobotOutlined />
                  AI��Ʒ����
                  <Tag color="blue">���Ŷ�: {(aiClassification.confidence * 100).toFixed(1)}%</Tag>
                </Space>
              }>
                <div className="ai-classification">
                  <Title level={4}>ʶ�����{aiClassification.category}</Title>
                  {aiClassification.subcategories && (
                    <div style={{ marginTop: 12 }}>
                      <Title level={5}>���ܵ����</Title>
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

export default Upload;
