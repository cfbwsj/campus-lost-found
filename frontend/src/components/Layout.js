import React, { useState } from 'react';
import { Layout as AntLayout, Menu, Button, Drawer } from 'antd';
import { 
  HomeOutlined, 
  SearchOutlined, 
  PlusOutlined, 
  FileSearchOutlined,
  BulbOutlined,
  MenuOutlined
} from '@ant-design/icons';
import { useNavigate, useLocation } from 'react-router-dom';

const { Header, Content, Sider } = AntLayout;

const Layout = ({ children }) => {
  const [collapsed, setCollapsed] = useState(false);
  const [mobileMenuVisible, setMobileMenuVisible] = useState(false);
  const navigate = useNavigate();
  const location = useLocation();

  const menuItems = [
    {
      key: '/',
      icon: <HomeOutlined />,
      label: '��ҳ',
    },
    {
      key: '/lost',
      icon: <FileSearchOutlined />,
      label: 'ʧ����Ϣ',
    },
    {
      key: '/found',
      icon: <BulbOutlined />,
      label: '������Ϣ',
    },
    {
      key: '/search',
      icon: <SearchOutlined />,
      label: '��������',
    },
    {
      key: '/upload',
      icon: <PlusOutlined />,
      label: '������Ϣ',
    },
  ];

  const handleMenuClick = ({ key }) => {
    navigate(key);
    setMobileMenuVisible(false);
  };

  const isMobile = window.innerWidth <= 768;

  return (
    <AntLayout style={{ minHeight: '100vh' }}>
      <Header style={{ 
        display: 'flex', 
        alignItems: 'center', 
        justifyContent: 'space-between',
        padding: '0 24px',
        background: '#fff',
        boxShadow: '0 2px 8px rgba(0,0,0,0.1)'
      }}>
        <div style={{ 
          display: 'flex', 
          alignItems: 'center',
          fontSize: '20px',
          fontWeight: 'bold',
          color: '#1890ff'
        }}>
          ? У԰ʧ������
        </div>
        
        {isMobile ? (
          <Button 
            type="text" 
            icon={<MenuOutlined />}
            onClick={() => setMobileMenuVisible(true)}
          />
        ) : (
          <div style={{ color: '#666' }}>
            ����AI����������ʧ������ƽ̨
          </div>
        )}
      </Header>

      <AntLayout>
        {!isMobile && (
          <Sider
            width={200}
            collapsible
            collapsed={collapsed}
            onCollapse={setCollapsed}
            style={{ background: '#fff' }}
          >
            <Menu
              mode="inline"
              selectedKeys={[location.pathname]}
              items={menuItems}
              onClick={handleMenuClick}
              style={{ height: '100%', borderRight: 0 }}
            />
          </Sider>
        )}

        <Content style={{ margin: '24px 16px', padding: 24, background: '#fff', minHeight: 280 }}>
          {children}
        </Content>
      </AntLayout>

      {/* �ƶ��˳���˵� */}
      <Drawer
        title="�˵�"
        placement="left"
        onClose={() => setMobileMenuVisible(false)}
        open={mobileMenuVisible}
        width={250}
      >
        <Menu
          mode="inline"
          selectedKeys={[location.pathname]}
          items={menuItems}
          onClick={handleMenuClick}
        />
      </Drawer>
    </AntLayout>
  );
};

export default Layout;
