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
import { lostItemsAPI, foundItemsAPI, authAPI } from '../services/api';

const { Title, Paragraph, Text } = Typography;

const ItemDetail = () => {
  const { type, id } = useParams();
  const navigate = useNavigate();
  const [loading, setLoading] = useState(false);
  const [item, setItem] = useState(null);
  const [deleteModalVisible, setDeleteModalVisible] = useState(false);
  const [me, setMe] = useState(null);

  useEffect(() => {
    loadItemDetail();
  }, [type, id]);

  useEffect(() => {
    (async () => {
      try {
        const token = localStorage.getItem('access_token');
        if (!token) return;
        const res = await authAPI.me();
        setMe(res);
      } catch (e) {
        // ignore
      }
    })();
  }, []);

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
      console.error('加载物品详情失败:', error);
      message.error('加载详情失败');
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
      message.success('删除成功');
      navigate(type === 'lost' ? '/lost' : '/found');
    } catch (error) {
      console.error('删除失败:', error);
      message.error('删除失败');
    }
    setDeleteModalVisible(false);
  };

  const getStatusTag = (status) => {
    const statusMap = {
      lost: { color: 'orange', text: '丢失中' },
      found: { color: 'green', text: '招领中' },
      claimed: { color: 'default', text: '已认领' }
    };
    
    const statusInfo = statusMap[status] || { color: 'default', text: '未知' };
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
        <Empty description="物品信息不存在" />
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
              {me && (me.role === 'admin' || me.id === item.owner_id) && (<>
              <Button 
                icon={<EditOutlined />}
                onClick={() => navigate(`/edit/${type}/${id}`)}
              >
                编辑
              </Button>
              <Button 
                danger 
                icon={<DeleteOutlined />}
                onClick={() => setDeleteModalVisible(true)}
              >
                删除
              </Button>
              </>)}
            </Space>
          </Col>
        </Row>
      </div>

      <div className="page-content">
        <Row gutter={[24, 24]}>
          {/* 左侧：图片和信息 */}
          <Col xs={24} lg={16}>
            {/* 图片展示 */}
            <Card title="物品图片" style={{ marginBottom: 24 }}>
              {item.image_url ? (
                <Image
                  src={item.image_url}
                  alt={item.title}
                  style={{ width: '100%', maxHeight: 400 }}
                  fallback={'data:image/png;base64,iVBORw0KGgoAAAANSUhEUgAAAAEAAAABCAQAAAC1HAwCAAAAC0lEQVR42mP8Xw8AAoMBix5s6CwAAAAASUVORK5CYII='}
                />
              ) : (
                <div style={{ 
                  textAlign: 'center', 
                  padding: '40px',
                  background: '#f5f5f5',
                  borderRadius: '6px'
                }}>
                  <Text type="secondary">暂无图片</Text>
                </div>
              )}
            </Card>

            {/* 详细信息 */}
            <Card title="详细信息">
              <Space direction="vertical" size="large" style={{ width: '100%' }}>
                <div>
                  <Title level={4}>物品描述</Title>
                  <Paragraph>{item.description || '暂无描述'}</Paragraph>
                </div>

                {item.location && (
                  <div>
                    <Title level={4}>
                      <EnvironmentOutlined /> 发现地点
                    </Title>
                    <Text>{item.location}</Text>
                  </div>
                )}

                {item.contact_info && (
                  <div>
                    <Title level={4}>
                      <PhoneOutlined /> 联系方式
                    </Title>
                    <Text copyable>{item.contact_info}</Text>
                  </div>
                )}

                <div>
                  <Title level={4}>
                    <ClockCircleOutlined /> 发布时间
                  </Title>
                  <Text>{formatDate(item.created_at)}</Text>
                </div>
              </Space>
            </Card>
          </Col>

          {/* 右侧：AI分析结果 */}
          <Col xs={24} lg={8}>
            {/* OCR识别结果 */}
            {item.ocr_text && (
              <Card 
                title={
                  <Space>
                    <FileTextOutlined />
                    OCR识别结果
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

            {/* AI分类结果 */}
            {item.ai_category && (
              <Card 
                title={
                  <Space>
                    <RobotOutlined />
                    AI物品分类
                    {item.confidence && (
                      <Tag color="blue">
                        置信度: {(item.confidence * 100).toFixed(1)}%
                      </Tag>
                    )}
                  </Space>
                }
                style={{ marginBottom: 24 }}
              >
                <div className="ai-classification">
                  <Title level={4}>识别类别：{item.ai_category}</Title>
                  <Paragraph>
                  AI模型自动识别的物品类别，可用于辅助分类和搜索
                  </Paragraph>
                </div>
              </Card>
            )}

            {/* 联系卡片 */}
            <Card title="联系信息" style={{ marginBottom: 24 }}>
              <Space direction="vertical" style={{ width: '100%' }}>
                <div>
                  <Text strong>联系方式：</Text>
                  <br />
                  <Text copyable>{item.contact_info || '未提供'}</Text>
                </div>
                
                <Divider />
                
                <div>
                  <Text strong>物品状态：</Text>
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
                      // 这里可以添加联系功能
                      message.success('请联系发布者确认物品信息');
                    } else {
                      message.warning('发布者未提供联系方式');
                    }
                  }}
                >
                  <UserOutlined /> 联系发布者
                </Button>
              </Space>
            </Card>
          </Col>
        </Row>
      </div>

      {/* 删除确认模态框 */}
      <Modal
        title="确认删除"
        open={deleteModalVisible}
        onOk={handleDelete}
        onCancel={() => setDeleteModalVisible(false)}
        okText="确认删除"
        cancelText="取消"
        okButtonProps={{ danger: true }}
      >
        <p>您确定要删除这个{item.type === 'lost' ? '失物' : '招领'}信息吗？</p>
        <p style={{ color: '#ff4d4f' }}>此操作不可恢复！</p>
      </Modal>
    </div>
  );
};

export default ItemDetail;
