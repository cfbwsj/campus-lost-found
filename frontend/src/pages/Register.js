import React, { useState } from 'react';
import { Card, Form, Input, Button, message } from 'antd';
import { authAPI } from '../services/api';
import { useNavigate } from 'react-router-dom';

const Register = () => {
  const [loading, setLoading] = useState(false);
  const navigate = useNavigate();

  const onFinish = async (values) => {
    setLoading(true);
    try {
      await authAPI.register(values.username, values.password, 'user');
      message.success('注册成功，请登录');
      navigate('/login');
    } catch (e) {
      message.error('注册失败，用户名可能已存在');
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className="page-container">
      <Card title="注册" style={{ maxWidth: 400, margin: '0 auto' }}>
        <Form layout="vertical" onFinish={onFinish}>
          <Form.Item name="username" label="用户名" rules={[{ required: true, message: '请输入用户名' }]}> 
            <Input placeholder="用户名" />
          </Form.Item>
          <Form.Item name="password" label="密码" rules={[{ required: true, message: '请输入密码' }]}> 
            <Input.Password placeholder="密码" autoComplete="new-password" />
          </Form.Item>
          <Form.Item>
            <Button type="primary" htmlType="submit" loading={loading} block>
              注册
            </Button>
          </Form.Item>
        </Form>
      </Card>
    </div>
  );
};

export default Register;


