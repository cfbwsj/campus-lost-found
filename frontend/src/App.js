import React from 'react';
import { BrowserRouter as Router, Routes, Route } from 'react-router-dom';
import { ConfigProvider } from 'antd';
import zhCN from 'antd/locale/zh_CN';
import dayjs from 'dayjs';
import 'dayjs/locale/zh-cn';

// 导入页面组件
import Layout from './components/Layout';
import Home from './pages/Home';
import LostItems from './pages/LostItems';
import FoundItems from './pages/FoundItems';
import Search from './pages/Search';
import Upload from './pages/Upload';
import ItemDetail from './pages/ItemDetail';
import Login from './pages/Login';
import Register from './pages/Register';
import MyPosts from './pages/MyPosts';
import EditItem from './pages/EditItem';

// 设置dayjs中文
dayjs.locale('zh-cn');

function App() {
  return (
    <ConfigProvider locale={zhCN}>
      <Router>
        <Layout>
          <Routes>
            <Route path="/" element={<Home />} />
            <Route path="/lost" element={<LostItems />} />
            <Route path="/found" element={<FoundItems />} />
            <Route path="/search" element={<Search />} />
            <Route path="/upload" element={<Upload />} />
            <Route path="/item/:type/:id" element={<ItemDetail />} />
            <Route path="/login" element={<Login />} />
            <Route path="/register" element={<Register />} />
            <Route path="/myposts" element={<MyPosts />} />
            <Route path="/edit/:type/:id" element={<EditItem />} />
          </Routes>
        </Layout>
      </Router>
    </ConfigProvider>
  );
}

export default App;
