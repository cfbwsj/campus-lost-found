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
    '手机/数码产品',
    '钱包/证件',
    '钥匙/门卡',
    '书籍/文具',
    '衣物/饰品',
    '眼镜/配饰',
    '运动用品',
    '其他'
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
      console.error('加载失物列表失败:', error);
      message.error('加载数据失败');
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
      lost: { color: 'orange', text: '丢失中' },
      found: { color: 'green', text: '已找到' },
      claimed: { color: 'default', text: '已认领' }
    };
    
    const statusInfo = statusMap[status] || statusMap['lost'];
    return <Tag color={statusInfo.color}>{statusInfo.text}</Tag>;
  };

  return (
    <div className="page-container">
      <div className="page-header">
        <h1>失物信息</h1>
        <p>查看所有失物信息，帮助找回丢失的物品</p>
      </div>

      <div className="page-content">
        {/* 筛选条件 */}
        <Card style={{ marginBottom: 24 }}>
          <Row gutter={[16, 16]} align="middle">
            <Col xs={24} sm={12} md={8}>
              <Select
                placeholder="选择分类"
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
                placeholder="选择状态"
                allowClear
                value={status}
                onChange={setStatus}
                style={{ width: '100%' }}
              >
                <Option value="lost">丢失中</Option>
                <Option value="found">已找到</Option>
                <Option value="claimed">已认领</Option>
              </Select>
            </Col>
            <Col xs={24} sm={12} md={8}>
              <div style={{ color: '#666' }}>
                共 {total} 条失物信息
              </div>
            </Col>
          </Row>
        </Card>

        {/* 失物列表 */}
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

            {/* 分页 */}
            {total > pageSize && (
              <div style={{ textAlign: 'center', marginTop: 24 }}>
                <Pagination
                  current={currentPage}
                  pageSize={pageSize}
                  total={total}
                  showSizeChanger
                  showQuickJumper
                  showTotal={(total, range) => 
                    `第 ${range[0]}-${range[1]} 条，共 ${total} 条`
                  }
                  onChange={handlePageChange}
                />
              </div>
            )}
          </>
        ) : (
          <Empty description="暂无失物信息" />
        )}
      </div>
    </div>
  );
};

export default LostItems;
