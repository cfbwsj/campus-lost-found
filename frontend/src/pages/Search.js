import React, { useState, useEffect } from 'react';
import {
  Card,
  Input,
  Button,
  Row,
  Col,
  Select,
  Tag,
  List,
  Avatar,
  Space,
  Pagination,
  message,
  Empty,
  Spin
} from 'antd';
import {
  SearchOutlined,
  FileSearchOutlined,
  BulbOutlined,
  EnvironmentOutlined,
  ClockCircleOutlined
} from '@ant-design/icons';
import { useNavigate, useSearchParams } from 'react-router-dom';
import { searchAPI } from '../services/api';

const { Search } = Input;
const { Option } = Select;

const Search = () => {
  const [searchParams, setSearchParams] = useSearchParams();
  const navigate = useNavigate();
  
  const [searchValue, setSearchValue] = useState('');
  const [category, setCategory] = useState('');
  const [location, setLocation] = useState('');
  const [itemType, setItemType] = useState('all');
  const [loading, setLoading] = useState(false);
  const [searchResults, setSearchResults] = useState([]);
  const [total, setTotal] = useState(0);
  const [currentPage, setCurrentPage] = useState(1);
  const [pageSize, setPageSize] = useState(20);
  
  const [categories, setCategories] = useState([]);
  const [locations, setLocations] = useState([]);
  const [hotKeywords, setHotKeywords] = useState([]);

  useEffect(() => {
    // 从URL参数初始化搜索条件
    const q = searchParams.get('q') || '';
    const cat = searchParams.get('category') || '';
    const loc = searchParams.get('location') || '';
    const type = searchParams.get('type') || 'all';
    
    setSearchValue(q);
    setCategory(cat);
    setLocation(loc);
    setItemType(type);
    
    loadInitialData();
    
    // 如果有搜索关键词，自动搜索
    if (q) {
      handleSearch(q, cat, loc, type);
    }
  }, [searchParams]);

  const loadInitialData = async () => {
    try {
      const [categoriesRes, locationsRes, keywordsRes] = await Promise.all([
        searchAPI.getCategories(),
        searchAPI.getLocations(),
        searchAPI.getHotKeywords()
      ]);
      
      setCategories(categoriesRes.categories || []);
      setLocations(locationsRes.locations || []);
      setHotKeywords(keywordsRes.keywords || []);
    } catch (error) {
      console.error('加载初始数据失败:', error);
    }
  };

  const handleSearch = async (query = searchValue, cat = category, loc = location, type = itemType) => {
    if (!query.trim()) {
      message.warning('请输入搜索关键词');
      return;
    }

    setLoading(true);
    try {
      const params = {
        q: query.trim(),
        category: cat || undefined,
        location: loc || undefined,
        item_type: type,
        limit: pageSize,
        offset: (currentPage - 1) * pageSize
      };

      const result = await searchAPI.searchItems(params);
      
      setSearchResults(result.items || []);
      setTotal(result.total || 0);
      
      // 更新URL参数
      const newParams = new URLSearchParams();
      newParams.set('q', query.trim());
      if (cat) newParams.set('category', cat);
      if (loc) newParams.set('location', loc);
      if (type !== 'all') newParams.set('type', type);
      setSearchParams(newParams);

    } catch (error) {
      console.error('搜索失败:', error);
      message.error('搜索失败');
    } finally {
      setLoading(false);
    }
  };

  const handlePageChange = (page, size) => {
    setCurrentPage(page);
    setPageSize(size);
    handleSearch();
  };

  const handleKeywordClick = (keyword) => {
    setSearchValue(keyword);
    setCurrentPage(1);
    handleSearch(keyword, category, location, itemType);
  };

  const handleItemClick = (item) => {
    const type = item.item_type || 'lost';
    navigate(`/item/${type}/${item.id}`);
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

  const getItemIcon = (type) => {
    return type === 'lost' ? <FileSearchOutlined /> : <BulbOutlined />;
  };

  return (
    <div className="page-container">
      <div className="page-header">
        <h1>? 智能搜索</h1>
        <p>支持模糊匹配、分类筛选和地点搜索</p>
      </div>

      <div className="page-content">
        {/* 搜索区域 */}
        <Card className="search-container">
          <Row gutter={[16, 16]} align="bottom">
            <Col xs={24} sm={12} md={8}>
              <Search
                placeholder="输入关键词搜索..."
                allowClear
                enterButton={<SearchOutlined />}
                size="large"
                value={searchValue}
                onChange={(e) => setSearchValue(e.target.value)}
                onSearch={() => handleSearch()}
              />
            </Col>
            <Col xs={24} sm={12} md={4}>
              <Select
                placeholder="分类"
                allowClear
                size="large"
                value={category}
                onChange={setCategory}
                style={{ width: '100%' }}
              >
                {categories.map(cat => (
                  <Option key={cat.key} value={cat.key}>
                    {cat.key} ({cat.count})
                  </Option>
                ))}
              </Select>
            </Col>
            <Col xs={24} sm={12} md={4}>
              <Select
                placeholder="地点"
                allowClear
                size="large"
                value={location}
                onChange={setLocation}
                style={{ width: '100%' }}
              >
                {locations.map(loc => (
                  <Option key={loc.key} value={loc.key}>
                    {loc.key} ({loc.count})
                  </Option>
                ))}
              </Select>
            </Col>
            <Col xs={24} sm={12} md={4}>
              <Select
                placeholder="类型"
                size="large"
                value={itemType}
                onChange={setItemType}
                style={{ width: '100%' }}
              >
                <Option value="all">全部</Option>
                <Option value="lost">失物</Option>
                <Option value="found">招领</Option>
              </Select>
            </Col>
            <Col xs={24} sm={12} md={4}>
              <Button
                type="primary"
                size="large"
                onClick={() => handleSearch()}
                loading={loading}
                block
              >
                搜索
              </Button>
            </Col>
          </Row>

          {/* 热门关键词 */}
          {hotKeywords.length > 0 && (
            <div style={{ marginTop: 16 }}>
              <Space wrap>
                <span style={{ color: '#666' }}>热门搜索：</span>
                {hotKeywords.map((keyword, index) => (
                  <Tag
                    key={index}
                    style={{ cursor: 'pointer', marginBottom: 4 }}
                    onClick={() => handleKeywordClick(keyword)}
                  >
                    {keyword}
                  </Tag>
                ))}
              </Space>
            </div>
          )}
        </Card>

        {/* 搜索结果 */}
        <Card title={`搜索结果 (${total} 条)`}>
          {loading ? (
            <div className="loading-container">
              <Spin size="large" />
            </div>
          ) : searchResults.length > 0 ? (
            <>
              <List
                itemLayout="horizontal"
                dataSource={searchResults}
                renderItem={(item) => (
                  <List.Item
                    style={{ cursor: 'pointer' }}
                    onClick={() => handleItemClick(item)}
                  >
                    <List.Item.Meta
                      avatar={
                        <Avatar 
                          src={item.image_url} 
                          icon={getItemIcon(item.item_type)}
                          size={80}
                          shape="square"
                        />
                      }
                      title={
                        <Space>
                          {item.title}
                          {getStatusTag(item.status, item.item_type)}
                        </Space>
                      }
                      description={
                        <Space direction="vertical" size={4}>
                          <div>{item.description}</div>
                          <Space size="small">
                            {item.category && <Tag>{item.category}</Tag>}
                            {item.location && (
                              <Tag icon={<EnvironmentOutlined />}>
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
                  </List.Item>
                )}
              />
              
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
            <Empty description="暂无搜索结果" />
          )}
        </Card>
      </div>
    </div>
  );
};

export default Search;
