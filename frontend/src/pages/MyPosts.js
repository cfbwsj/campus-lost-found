import React, { useEffect, useState } from 'react';
import { Card, Tabs, List, Avatar, Tag, Space, Button, message, Empty, Spin } from 'antd';
import { EnvironmentOutlined, ClockCircleOutlined, EditOutlined, DeleteOutlined } from '@ant-design/icons';
import api, { authAPI } from '../services/api';
import { useNavigate } from 'react-router-dom';

const MyPosts = () => {
  const [loading, setLoading] = useState(false);
  const [items, setItems] = useState([]);
  const [type, setType] = useState('all');
  const [me, setMe] = useState(null);
  const navigate = useNavigate();

  useEffect(() => {
    const token = localStorage.getItem('access_token');
    if (!token) {
      message.warning('请先登录');
      navigate('/login');
      return;
    }
    loadMe();
  }, []);

  useEffect(() => {
    loadItems();
  }, [type]);

  const loadMe = async () => {
    try {
      const res = await authAPI.me();
      setMe(res);
    } catch (e) {
      // ignore
    }
  };

  const loadItems = async () => {
    setLoading(true);
    try {
      const res = await api.get('/api/items/my', { params: { item_type: type } });
      setItems(res.items || []);
    } catch (e) {
      message.error('加载失败');
    } finally {
      setLoading(false);
    }
  };

  const handleEdit = (it) => {
    const itemType = it.status === 'lost' ? 'lost' : 'found';
    navigate(`/edit/${itemType}/${it.id}`);
  };

  const handleDelete = async (it) => {
    try {
      const endpoint = it.status === 'lost' ? `/api/items/lost/${it.id}` : `/api/items/found/${it.id}`;
      await api.delete(endpoint);
      message.success('已删除');
      loadItems();
    } catch (e) {
      message.error('删除失败');
    }
  };

  return (
    <div className="page-container">
      <Card title="我的发布">
        <Tabs
          activeKey={type}
          onChange={setType}
          items={[
            { key: 'all', label: '全部' },
            { key: 'lost', label: '失物' },
            { key: 'found', label: '招领' },
          ]}
        />

        {loading ? (
          <div className="loading-container"><Spin size="large" /></div>
        ) : items.length === 0 ? (
          <Empty description="暂无发布" />
        ) : (
          <List
            itemLayout="horizontal"
            dataSource={items}
            renderItem={(item) => (
              <List.Item
                actions={[
                  <Button key="edit" icon={<EditOutlined />} onClick={() => handleEdit(item)}>编辑</Button>,
                  <Button key="del" danger icon={<DeleteOutlined />} onClick={() => handleDelete(item)}>删除</Button>,
                ]}
              >
                <List.Item.Meta
                  avatar={<Avatar src={item.image_url} shape="square" size={72} />}
                  title={
                    <Space>
                      {item.title}
                      <Tag color={item.status === 'lost' ? 'orange' : item.status === 'found' ? 'green' : 'default'}>
                        {item.status}
                      </Tag>
                    </Space>
                  }
                  description={
                    <Space direction="vertical" size={4}>
                      <div>{item.description}</div>
                      <Space size="small">
                        {item.location && (
                          <Tag icon={<EnvironmentOutlined />}>{item.location}</Tag>
                        )}
                        <Tag icon={<ClockCircleOutlined />}>{new Date(item.created_at).toLocaleDateString()}</Tag>
                      </Space>
                    </Space>
                  }
                />
              </List.Item>
            )}
          />
        )}
      </Card>
    </div>
  );
};

export default MyPosts;


