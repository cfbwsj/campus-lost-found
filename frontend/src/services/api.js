import axios from 'axios';

// 创建axios实例
const api = axios.create({
  baseURL: process.env.REACT_APP_API_URL || 'http://localhost:8000',
  timeout: 10000,
  headers: {
    'Content-Type': 'application/json',
  },
});

// 请求拦截器
api.interceptors.request.use(
  (config) => {
    // 可以在这里添加token等认证信息
    return config;
  },
  (error) => {
    return Promise.reject(error);
  }
);

// 响应拦截器
api.interceptors.response.use(
  (response) => {
    return response.data;
  },
  (error) => {
    console.error('API Error:', error);
    return Promise.reject(error);
  }
);

// 失物管理API
export const lostItemsAPI = {
  // 获取失物列表
  getLostItems: (params) => api.get('/api/items/lost', { params }),
  
  // 获取失物详情
  getLostItem: (id) => api.get(`/api/items/lost/${id}`),
  
  // 创建失物
  createLostItem: (data) => api.post('/api/items/lost', data),
  
  // 更新失物
  updateLostItem: (id, data) => api.put(`/api/items/lost/${id}`, data),
  
  // 删除失物
  deleteLostItem: (id) => api.delete(`/api/items/lost/${id}`),
};

// 招领管理API
export const foundItemsAPI = {
  // 获取招领列表
  getFoundItems: (params) => api.get('/api/items/found', { params }),
  
  // 获取招领详情
  getFoundItem: (id) => api.get(`/api/items/found/${id}`),
  
  // 创建招领
  createFoundItem: (data) => api.post('/api/items/found', data),
  
  // 更新招领
  updateFoundItem: (id, data) => api.put(`/api/items/found/${id}`, data),
  
  // 删除招领
  deleteFoundItem: (id) => api.delete(`/api/items/found/${id}`),
};

// 搜索API
export const searchAPI = {
  // 综合搜索
  searchItems: (params) => api.get('/api/search', { params }),
  
  // 搜索失物
  searchLostItems: (params) => api.get('/api/search/lost', { params }),
  
  // 搜索招领
  searchFoundItems: (params) => api.get('/api/search/found', { params }),
  
  // 获取搜索建议
  getSuggestions: (params) => api.get('/api/search/suggestions', { params }),
  
  // 获取热门关键词
  getHotKeywords: () => api.get('/api/search/hot-keywords'),
  
  // 获取分类
  getCategories: () => api.get('/api/search/categories'),
  
  // 获取地点
  getLocations: () => api.get('/api/search/locations'),
};

// 文件上传API
export const uploadAPI = {
  // 上传单个文件
  uploadFile: (file) => {
    const formData = new FormData();
    formData.append('file', file);
    return api.post('/api/upload', formData, {
      headers: {
        'Content-Type': 'multipart/form-data',
      },
    });
  },
  
  // 上传多个文件
  uploadMultipleFiles: (files) => {
    const formData = new FormData();
    files.forEach(file => {
      formData.append('files', file);
    });
    return api.post('/api/upload/multiple', formData, {
      headers: {
        'Content-Type': 'multipart/form-data',
      },
    });
  },
  
  // 删除文件
  deleteFile: (filename) => api.delete(`/api/upload/${filename}`),
  
  // 获取上传信息
  getUploadInfo: () => api.get('/api/upload/info'),
};

// OCR API
export const ocrAPI = {
  // OCR识别
  extractText: (file, language = 'chi_sim+eng') => {
    const formData = new FormData();
    formData.append('file', file);
    formData.append('language', language);
    return api.post('/api/ocr', formData, {
      headers: {
        'Content-Type': 'multipart/form-data',
      },
    });
  },
  
  // 从URL识别
  extractTextFromUrl: (imageUrl, language = 'chi_sim+eng') => 
    api.post('/api/ocr/url', { image_url: imageUrl, language }),
  
  // 获取支持的语言
  getLanguages: () => api.get('/api/ocr/languages'),
};

// AI分类API
export const classifyAPI = {
  // 图片分类
  classifyImage: (file) => {
    const formData = new FormData();
    formData.append('file', file);
    return api.post('/api/classify', formData, {
      headers: {
        'Content-Type': 'multipart/form-data',
      },
    });
  },
  
  // 从URL分类
  classifyImageFromUrl: (imageUrl) => 
    api.post('/api/classify/url', { image_url: imageUrl }),
  
  // 获取分类信息
  getCategories: () => api.get('/api/classify/categories'),
  
  // 获取模型信息
  getModelInfo: () => api.get('/api/classify/model-info'),
};

// 通用API
export const commonAPI = {
  // 获取分类列表
  getCategories: () => api.get('/api/items/categories'),
  
  // 健康检查
  healthCheck: () => api.get('/health'),
};

export default api;
