import React, { useState, useEffect } from 'react';
import {
  Card,
  Row,
  Col,
  List,
  Avatar,
  Tag,
  Space,
  Pagination,
  Select,
  message,
  Spin,
  Empty
} from 'antd';
import {
  FileSearchOutlined,
  EnvironmentOutlined,
  ClockCircleOutlined,
  EyeOutlined
} from '@ant-design/icons';
import { useNavigate } from 'react-router-dom';
import { lostItemsAPI } from '../services/api';

const { Option } = Select;

const LostItems = () => {
  const navigate = useNavigate();
  const [loading, setLoading] = useState(false);
  const [lostItems, setLostItems] = useState([]);
  const [total, setTotal] = useState(0);
  const [currentPage, setCurrentPage] = useState(1);
  const [pageSize, setPageSize] = useState(12);
  const [category, setCategory] = useState('');
  const [status, setStatus] = useState('');

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

  useEffect(() => {
    loadLostItems();
  }, [currentPage, pageSize, category, status]);

  const loadLostItems = async () => {
    setLoading(true);
    try {
      const params = {
        skip: (currentPage - 1) * pageSize,
        limit: pageSize,
        category: category || undefined,
        status: status || undefined
      };

      const result = await lostItemsAPI.getLostItems(params);
      setLostItems(result || []);
      setTotal(result?.length || 0);

    } catch (error) {
      console.error('����ʧ���б�ʧ��:', error);
      message.error('��������ʧ��');
    } finally {
      setLoading(false);
    }
  };

  const handleItemClick = (item) => {
    navigate(`/item/lost/${item.id}`);
  };

  const handlePageChange = (page, size) => {
    setCurrentPage(page);
    setPageSize(size);
  };

  const getStatusTag = (status) => {
    const statusMap = {
      lost: { color: 'orange', text: '��ʧ��' },
      found: { color: 'green', text: '���ҵ�' },
      claimed: { color: 'default', text: '������' }
    };
    
    const statusInfo = statusMap[status] || statusMap['lost'];
    return <Tag color={statusInfo.color}>{statusInfo.text}</Tag>;
  };

  return (
    <div className="page-container">
      <div className="page-header">
        <h1>? ʧ����Ϣ</h1>
        <p>�鿴����ʧ����Ϣ�������һض�ʧ����Ʒ</p>
      </div>

      <div className="page-content">
        {/* ɸѡ���� */}
        <Card style={{ marginBottom: 24 }}>
          <Row gutter={[16, 16]} align="middle">
            <Col xs={24} sm={12} md={8}>
              <Select
                placeholder="ѡ�����"
                allowClear
                value={category}
                onChange={setCategory}
                style={{ width: '100%' }}
              >
                {categories.map(cat => (
                  <Option key={cat} value={cat}>{cat}</Option>
                ))}
              </Select>
            </Col>
            <Col xs={24} sm={12} md={8}>
              <Select
                placeholder="ѡ��״̬"
                allowClear
                value={status}
                onChange={setStatus}
                style={{ width: '100%' }}
              >
                <Option value="lost">��ʧ��</Option>
                <Option value="found">���ҵ�</Option>
                <Option value="claimed">������</Option>
              </Select>
            </Col>
            <Col xs={24} sm={12} md={8}>
              <div style={{ color: '#666' }}>
                �� {total} ��ʧ����Ϣ
              </div>
            </Col>
          </Row>
        </Card>

        {/* ʧ���б� */}
        {loading ? (
          <div className="loading-container">
            <Spin size="large" />
          </div>
        ) : lostItems.length > 0 ? (
          <>
            <Row gutter={[16, 16]}>
              {lostItems.map(item => (
                <Col xs={24} sm={12} md={8} lg={6} key={item.id}>
                  <Card
                    hoverable
                    className="item-card"
                    cover={
                      <img
                        alt={item.title}
                        src={item.image_url || '/placeholder.png'}
                        className="item-image"
                        onError={(e) => {
                          e.target.src = '/placeholder.png';
                        }}
                      />
                    }
                    actions={[
                      <EyeOutlined key="view" onClick={() => handleItemClick(item)} />
                    ]}
                    onClick={() => handleItemClick(item)}
                  >
                    <Card.Meta
                      title={
                        <Space>
                          {item.title}
                          {getStatusTag(item.status)}
                        </Space>
                      }
                      description={
                        <Space direction="vertical" size={4}>
                          <div style={{ 
                            overflow: 'hidden', 
                            textOverflow: 'ellipsis',
                            display: '-webkit-box',
                            WebkitLineClamp: 2,
                            WebkitBoxOrient: 'vertical'
                          }}>
                            {item.description}
                          </div>
                          <Space size="small" wrap>
                            {item.category && <Tag>{item.category}</Tag>}
                            {item.location && (
                              <Tag icon={<EnvironmentOutlined />} className="location-tag">
                                {item.location}
                              </Tag>
                            )}
                            <Tag icon={<ClockCircleOutlined />}>
                              {new Date(item.created_at).toLocaleDateString()}
                            </Tag>
                          </Space>
                        </Space>
                      }
                    />
                  </Card>
                </Col>
              ))}
            </Row>

            {/* ��ҳ */}
            {total > pageSize && (
              <div style={{ textAlign: 'center', marginTop: 24 }}>
                <Pagination
                  current={currentPage}
                  pageSize={pageSize}
                  total={total}
                  showSizeChanger
                  showQuickJumper
                  showTotal={(total, range) => 
                    `�� ${range[0]}-${range[1]} ������ ${total} ��`
                  }
                  onChange={handlePageChange}
                />
              </div>
            )}
          </>
        ) : (
          <Empty description="����ʧ����Ϣ" />
        )}
      </div>
    </div>
  );
};

export default LostItems;
