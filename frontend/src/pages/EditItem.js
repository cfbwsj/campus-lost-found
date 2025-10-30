import React, { useEffect, useState } from 'react';
import { Card, Form, Input, Select, Button, message, Row, Col, Typography } from 'antd';
import { useParams, useNavigate } from 'react-router-dom';
import { lostItemsAPI, foundItemsAPI } from '../services/api';

const { Title } = Typography;
const { Option } = Select;

const categoriesList = [
  '手机/数码产品', '钱包/证件', '钥匙/门卡', '书籍/文具',
  '衣物/饰品', '眼镜/配饰', '运动用品', '其他'
];

const EditItem = () => {
  const { type, id } = useParams();
  const navigate = useNavigate();
  const [form] = Form.useForm();
  const [loading, setLoading] = useState(false);
  const [initialLoading, setInitialLoading] = useState(true);

  useEffect(() => {
    load();
  }, [type, id]);

  const load = async () => {
    setInitialLoading(true);
    try {
      const token = localStorage.getItem('access_token');
      if (!token) {
        message.warning('请先登录');
        navigate('/login');
        return;
      }
      const item = type === 'lost'
        ? await lostItemsAPI.getLostItem(id)
        : await foundItemsAPI.getFoundItem(id);
      form.setFieldsValue({
        title: item.title,
        description: item.description,
        category: item.category,
        location: item.location,
        contact_info: item.contact_info,
        status: item.status,
      });
    } catch (e) {
      message.error('加载信息失败，可能无权限或数据不存在');
    } finally {
      setInitialLoading(false);
    }
  };

  const onFinish = async (values) => {
    setLoading(true);
    try {
      const token = localStorage.getItem('access_token');
      const apiBase = process.env.REACT_APP_API_URL || 'http://localhost:8000';
      const endpoint = type === 'lost'
        ? `${apiBase}/api/items/lost/${id}`
        : `${apiBase}/api/items/found/${id}`;
      const res = await fetch(endpoint, {
        method: 'PUT',
        headers: {
          'Content-Type': 'application/json',
          ...(token ? { Authorization: `Bearer ${token}` } : {}),
        },
        body: JSON.stringify(values),
      });
      if (!res.ok) {
        const t = await res.text();
        throw new Error(t || '更新失败');
      }
      message.success('更新成功');
      navigate(`/item/${type}/${id}`);
    } catch (e) {
      message.error('更新失败：' + (e.message || ''));
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className="page-container">
      <div className="page-header">
        <Title level={2}>编辑信息</Title>
      </div>
      <div className="page-content">
        <Row gutter={[24, 24]}>
          <Col xs={24} lg={14}>
            <Card loading={initialLoading} title="基本信息">
              <Form form={form} layout="vertical" onFinish={onFinish}>
                <Form.Item name="title" label="标题" rules={[{ required: true, message: '请输入标题' }]}> 
                  <Input placeholder="请输入标题" />
                </Form.Item>
                <Form.Item name="description" label="详细描述" rules={[{ required: true, message: '请输入描述' }]}> 
                  <Input.TextArea rows={4} placeholder="请输入详细描述" />
                </Form.Item>
                <Row gutter={16}>
                  <Col span={12}>
                    <Form.Item name="category" label="物品类别">
                      <Select placeholder="请选择类别" allowClear>
                        {categoriesList.map(c => <Option key={c} value={c}>{c}</Option>)}
                      </Select>
                    </Form.Item>
                  </Col>
                  <Col span={12}>
                    <Form.Item name="location" label="地点">
                      <Input placeholder="请输入地点" />
                    </Form.Item>
                  </Col>
                </Row>
                <Form.Item name="contact_info" label="联系方式" rules={[{ required: true, message: '请输入联系方式' }]}> 
                  <Input placeholder="请输入联系方式" />
                </Form.Item>
                <Form.Item name="status" label="状态">
                  <Select>
                    {type === 'lost' ? (
                      <>
                        <Option value="lost">丢失中</Option>
                        <Option value="found">招领中</Option>
                        <Option value="claimed">已认领</Option>
                      </>
                    ) : (
                      <>
                        <Option value="found">招领中</Option>
                        <Option value="claimed">已认领</Option>
                      </>
                    )}
                  </Select>
                </Form.Item>
                <Form.Item>
                  <Button type="primary" htmlType="submit" loading={loading} block>
                    保存修改
                  </Button>
                </Form.Item>
              </Form>
            </Card>
          </Col>
        </Row>
      </div>
    </div>
  );
};

export default EditItem;


