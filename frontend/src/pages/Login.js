import React, { useState } from 'react';
import { Card, Form, Input, Button, message } from 'antd';
import { authAPI } from '../services/api';
import { useNavigate } from 'react-router-dom';

const Login = () => {
  const [loading, setLoading] = useState(false);
  const navigate = useNavigate();

  const onFinish = async (values) => {
    setLoading(true);
    try {
      const res = await authAPI.login(values.username, values.password);
      if (res && res.access_token) {
        localStorage.setItem('access_token', res.access_token);
        message.success('登录成功');
        navigate('/');
      } else {
        message.error('登录失败');
      }
    } catch (e) {
      message.error('账号或密码错误');
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className="page-container">
      <Card title="登录" style={{ maxWidth: 400, margin: '0 auto' }}>
        <Form layout="vertical" onFinish={onFinish}>
          <Form.Item name="username" label="用户名" rules={[{ required: true, message: '请输入用户名' }]}> 
            <Input placeholder="用户名" />
          </Form.Item>
          <Form.Item name="password" label="密码" rules={[{ required: true, message: '请输入密码' }]}> 
            <Input.Password placeholder="密码" autoComplete="current-password" />
          </Form.Item>
          <Form.Item>
            <Button type="primary" htmlType="submit" loading={loading} block>
              登录
            </Button>
          </Form.Item>
          <Button type="link" onClick={() => navigate('/register')} block>
            没有账号？去注册
          </Button>
        </Form>
      </Card>
    </div>
  );
};

export default Login;


