import React, { useState, useEffect } from 'react';
import {
  Card,
  Row,
  Col,
  Typography,
  Tag,
  Space,
  Button,
  Image,
  Divider,
  message,
  Spin,
  Empty,
  Modal
} from 'antd';
import {
  EnvironmentOutlined,
  ClockCircleOutlined,
  UserOutlined,
  PhoneOutlined,
  RobotOutlined,
  FileTextOutlined,
  EditOutlined,
  DeleteOutlined
} from '@ant-design/icons';
import { useParams, useNavigate } from 'react-router-dom';
import { lostItemsAPI, foundItemsAPI } from '../services/api';

const { Title, Paragraph, Text } = Typography;

const ItemDetail = () => {
  const { type, id } = useParams();
  const navigate = useNavigate();
  const [loading, setLoading] = useState(false);
  const [item, setItem] = useState(null);
  const [deleteModalVisible, setDeleteModalVisible] = useState(false);

  useEffect(() => {
    loadItemDetail();
  }, [type, id]);

  const loadItemDetail = async () => {
    setLoading(true);
    try {
      let result;
      if (type === 'lost') {
        result = await lostItemsAPI.getLostItem(id);
      } else {
        result = await foundItemsAPI.getFoundItem(id);
      }
      setItem(result);
    } catch (error) {
      console.error('������Ʒ����ʧ��:', error);
      message.error('��������ʧ��');
    } finally {
      setLoading(false);
    }
  };

  const handleDelete = async () => {
    try {
      if (type === 'lost') {
        await lostItemsAPI.deleteLostItem(id);
      } else {
        await foundItemsAPI.deleteFoundItem(id);
      }
      message.success('ɾ���ɹ�');
      navigate(type === 'lost' ? '/lost' : '/found');
    } catch (error) {
      console.error('ɾ��ʧ��:', error);
      message.error('ɾ��ʧ��');
    }
    setDeleteModalVisible(false);
  };

  const getStatusTag = (status) => {
    const statusMap = {
      lost: { color: 'orange', text: '��ʧ��' },
      found: { color: 'green', text: '������' },
      claimed: { color: 'default', text: '������' }
    };
    
    const statusInfo = statusMap[status] || { color: 'default', text: 'δ֪' };
    return <Tag color={statusInfo.color}>{statusInfo.text}</Tag>;
  };

  const formatDate = (dateString) => {
    return new Date(dateString).toLocaleString('zh-CN');
  };

  if (loading) {
    return (
      <div className="page-container">
        <div className="loading-container">
          <Spin size="large" />
        </div>
      </div>
    );
  }

  if (!item) {
    return (
      <div className="page-container">
        <Empty description="��Ʒ��Ϣ������" />
      </div>
    );
  }

  return (
    <div className="page-container">
      <div className="page-header">
        <Row justify="space-between" align="middle">
          <Col>
            <Title level={2}>{item.title}</Title>
            <Space>
              {getStatusTag(item.status)}
              {item.category && <Tag>{item.category}</Tag>}
            </Space>
          </Col>
          <Col>
            <Space>
              <Button 
                icon={<EditOutlined />}
                onClick={() => navigate(`/edit/${type}/${id}`)}
              >
                �༭
              </Button>
              <Button 
                danger 
                icon={<DeleteOutlined />}
                onClick={() => setDeleteModalVisible(true)}
              >
                ɾ��
              </Button>
            </Space>
          </Col>
        </Row>
      </div>

      <div className="page-content">
        <Row gutter={[24, 24]}>
          {/* ��ࣺͼƬ����Ϣ */}
          <Col xs={24} lg={16}>
            {/* ͼƬչʾ */}
            <Card title="��ƷͼƬ" style={{ marginBottom: 24 }}>
              {item.image_url ? (
                <Image
                  src={item.image_url}
                  alt={item.title}
                  style={{ width: '100%', maxHeight: 400 }}
                  fallback="/placeholder.png"
                />
              ) : (
                <div style={{ 
                  textAlign: 'center', 
                  padding: '40px',
                  background: '#f5f5f5',
                  borderRadius: '6px'
                }}>
                  <Text type="secondary">����ͼƬ</Text>
                </div>
              )}
            </Card>

            {/* ��ϸ��Ϣ */}
            <Card title="��ϸ��Ϣ">
              <Space direction="vertical" size="large" style={{ width: '100%' }}>
                <div>
                  <Title level={4}>��Ʒ����</Title>
                  <Paragraph>{item.description || '��������'}</Paragraph>
                </div>

                {item.location && (
                  <div>
                    <Title level={4}>
                      <EnvironmentOutlined /> ���ֵص�
                    </Title>
                    <Text>{item.location}</Text>
                  </div>
                )}

                {item.contact_info && (
                  <div>
                    <Title level={4}>
                      <PhoneOutlined /> ��ϵ��ʽ
                    </Title>
                    <Text copyable>{item.contact_info}</Text>
                  </div>
                )}

                <div>
                  <Title level={4}>
                    <ClockCircleOutlined /> ����ʱ��
                  </Title>
                  <Text>{formatDate(item.created_at)}</Text>
                </div>
              </Space>
            </Card>
          </Col>

          {/* �ҲࣺAI������� */}
          <Col xs={24} lg={8}>
            {/* OCRʶ���� */}
            {item.ocr_text && (
              <Card 
                title={
                  <Space>
                    <FileTextOutlined />
                    OCRʶ����
                  </Space>
                }
                style={{ marginBottom: 24 }}
              >
                <div className="ocr-result">
                  <Paragraph copyable={{ text: item.ocr_text }}>
                    {item.ocr_text}
                  </Paragraph>
                </div>
              </Card>
            )}

            {/* AI������ */}
            {item.ai_category && (
              <Card 
                title={
                  <Space>
                    <RobotOutlined />
                    AI��Ʒ����
                    {item.confidence && (
                      <Tag color="blue">
                        ���Ŷ�: {(item.confidence * 100).toFixed(1)}%
                      </Tag>
                    )}
                  </Space>
                }
                style={{ marginBottom: 24 }}
              >
                <div className="ai-classification">
                  <Title level={4}>ʶ�����{item.ai_category}</Title>
                  <Paragraph>
                    AIģ���Զ�ʶ�����Ʒ��𣬿����ڸ������������
                  </Paragraph>
                </div>
              </Card>
            )}

            {/* ��ϵ��Ƭ */}
            <Card title="��ϵ��Ϣ" style={{ marginBottom: 24 }}>
              <Space direction="vertical" style={{ width: '100%' }}>
                <div>
                  <Text strong>��ϵ��ʽ��</Text>
                  <br />
                  <Text copyable>{item.contact_info || 'δ�ṩ'}</Text>
                </div>
                
                <Divider />
                
                <div>
                  <Text strong>��Ʒ״̬��</Text>
                  <br />
                  {getStatusTag(item.status)}
                </div>
                
                <Divider />
                
                <Button 
                  type="primary" 
                  size="large" 
                  block
                  onClick={() => {
                    if (item.contact_info) {
                      // ������������ϵ����
                      message.success('����ϵ������ȷ����Ʒ��Ϣ');
                    } else {
                      message.warning('������δ�ṩ��ϵ��ʽ');
                    }
                  }}
                >
                  <UserOutlined /> ��ϵ������
                </Button>
              </Space>
            </Card>
          </Col>
        </Row>
      </div>

      {/* ɾ��ȷ��ģ̬�� */}
      <Modal
        title="ȷ��ɾ��"
        open={deleteModalVisible}
        onOk={handleDelete}
        onCancel={() => setDeleteModalVisible(false)}
        okText="ȷ��ɾ��"
        cancelText="ȡ��"
        okButtonProps={{ danger: true }}
      >
        <p>��ȷ��Ҫɾ�����{item.type === 'lost' ? 'ʧ��' : '����'}��Ϣ��</p>
        <p style={{ color: '#ff4d4f' }}>�˲������ɻָ���</p>
      </Modal>
    </div>
  );
};

export default ItemDetail;
