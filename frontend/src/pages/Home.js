import React, { useState, useEffect } from 'react';
import { 
  Card, 
  Row, 
  Col, 
  Statistic, 
  Typography, 
  Input, 
  Button, 
  Tag,
  List,
  Avatar,
  Space,
  message
} from 'antd';
import { 
  SearchOutlined, 
  FileSearchOutlined, 
  BulbOutlined,
  PlusOutlined,
  ClockCircleOutlined
} from '@ant-design/icons';
import { useNavigate } from 'react-router-dom';
import { searchAPI, lostItemsAPI, foundItemsAPI } from '../services/api';

const { Title, Paragraph } = Typography;
const { Search } = Input;

const Home = () => {
  const [searchValue, setSearchValue] = useState('');
  const [hotKeywords, setHotKeywords] = useState([]);
  const [recentItems, setRecentItems] = useState([]);
  const [stats, setStats] = useState({
    lostCount: 0,
    foundCount: 0,
    totalCount: 0
  });
  const navigate = useNavigate();

  useEffect(() => {
    loadHomeData();
  }, []);

  const loadHomeData = async () => {
    try {
      // 加载热门关键词
      const keywordsRes = await searchAPI.getHotKeywords();
      setHotKeywords(keywordsRes.keywords || []);

      // 加载最近发布的物品
      const [lostRes, foundRes] = await Promise.all([
        lostItemsAPI.getLostItems({ limit: 5 }),
        foundItemsAPI.getFoundItems({ limit: 5 })
      ]);

      const recentLost = (lostRes || []).map(item => ({ ...item, type: 'lost' }));
      const recentFound = (foundRes || []).map(item => ({ ...item, type: 'found' }));
      
      const allRecent = [...recentLost, ...recentFound]
        .sort((a, b) => new Date(b.created_at) - new Date(a.created_at))
        .slice(0, 8);

      setRecentItems(allRecent);

      // 模拟统计数据
      setStats({
        lostCount: 156,
        foundCount: 89,
        totalCount: 245
      });

    } catch (error) {
      console.error('加载首页数据失败:', error);
      message.error('加载数据失败');
    }
  };

  const handleSearch = (value) => {
    if (value.trim()) {
      navigate(`/search?q=${encodeURIComponent(value.trim())}`);
    }
  };

  const handleKeywordClick = (keyword) => {
    navigate(`/search?q=${encodeURIComponent(keyword)}`);
  };

  const handleItemClick = (item) => {
    navigate(`/item/${item.type}/${item.id}`);
  };

  const getStatusTag = (status, type) => {
    const statusMap = {
      lost: { color: 'orange', text: '丢失' },
      found: { color: 'green', text: '招领' },
      claimed: { color: 'default', text: '已认领' }
    };
    
    const statusInfo = statusMap[status] || statusMap[type];
    return <Tag color={statusInfo.color}>{statusInfo.text}</Tag>;
  };

  return (
    <div className="page-container">
      {/* 欢迎区域 */}
      <div className="page-header">
        <Row justify="center" align="middle">
          <Col xs={24} md={16} lg={12}>
            <div style={{ textAlign: 'center' }}>
              <Title level={1} style={{ marginBottom: 16 }}>
              校园失物招领系统
              </Title>
              <Paragraph style={{ fontSize: '16px', color: '#666', marginBottom: 32 }}>
              基于AI技术的智能失物招领平台，支持OCR识别、智能分类和模糊搜索
              </Paragraph>
              
              <Search
                placeholder="搜索失物或招领信息..."
                allowClear
                enterButton={<Button type="primary" icon={<SearchOutlined />}>搜索</Button>}
                size="large"
                value={searchValue}
                onChange={(e) => setSearchValue(e.target.value)}
                onSearch={handleSearch}
                style={{ maxWidth: 600 }}
              />
            </div>
          </Col>
        </Row>
      </div>

      <div className="page-content">
        {/* 统计信息 */}
        <Row gutter={[16, 16]} style={{ marginBottom: 32 }}>
          <Col xs={24} sm={8}>
            <Card>
              <Statistic
                title="失物总数"
                value={stats.lostCount}
                prefix={<FileSearchOutlined style={{ color: '#ff4d4f' }} />}
                valueStyle={{ color: '#ff4d4f' }}
              />
            </Card>
          </Col>
          <Col xs={24} sm={8}>
            <Card>
              <Statistic
                title="招领总数"
                value={stats.foundCount}
                prefix={<BulbOutlined style={{ color: '#52c41a' }} />}
                valueStyle={{ color: '#52c41a' }}
              />
            </Card>
          </Col>
          <Col xs={24} sm={8}>
            <Card>
              <Statistic
                title="总计"
                value={stats.totalCount}
                prefix={<PlusOutlined style={{ color: '#1890ff' }} />}
                valueStyle={{ color: '#1890ff' }}
              />
            </Card>
          </Col>
        </Row>

        {/* 热门关键词 */}
        <Card title="热门搜索" style={{ marginBottom: 24 }}>
          <Space wrap>
            {hotKeywords.map((keyword, index) => (
              <Tag
                key={index}
                style={{ cursor: 'pointer', marginBottom: 8 }}
                onClick={() => handleKeywordClick(keyword)}
              >
                {keyword}
              </Tag>
            ))}
          </Space>
        </Card>

        {/* 最近发布 */}
        <Card title="最近发布" extra={
          <Button type="link" onClick={() => navigate('/upload')}>
            发布信息
          </Button>
        }>
          <List
            itemLayout="horizontal"
            dataSource={recentItems}
            renderItem={(item) => (
              <List.Item
                style={{ cursor: 'pointer' }}
                onClick={() => handleItemClick(item)}
              >
                <List.Item.Meta
                  avatar={
                    <Avatar 
                      src={item.image_url} 
                      icon={item.type === 'lost' ? <FileSearchOutlined /> : <BulbOutlined />}
                      size={64}
                      shape="square"
                    />
                  }
                  title={
                    <Space>
                      {item.title}
                      {getStatusTag(item.status, item.type)}
                    </Space>
                  }
                  description={
                    <Space direction="vertical" size={4}>
                      <div>{item.description}</div>
                      <Space size="small">
                        <Tag>{item.category || '未分类'}</Tag>
                        <Tag icon={<ClockCircleOutlined />}>
                          {new Date(item.created_at).toLocaleDateString()}
                        </Tag>
                      </Space>
                    </Space>
                  }
                />
              </List.Item>
            )}
          />
        </Card>
      </div>
    </div>
  );
};

export default Home;

