import axios from 'axios';

// ����axiosʵ��
const api = axios.create({
  baseURL: process.env.REACT_APP_API_URL || 'http://localhost:8000',
  timeout: 10000,
  headers: {
    'Content-Type': 'application/json',
  },
});

// ����������
api.interceptors.request.use(
  (config) => {
    // �������������token����֤��Ϣ
    return config;
  },
  (error) => {
    return Promise.reject(error);
  }
);

// ��Ӧ������
api.interceptors.response.use(
  (response) => {
    return response.data;
  },
  (error) => {
    console.error('API Error:', error);
    return Promise.reject(error);
  }
);

// ʧ�����API
export const lostItemsAPI = {
  // ��ȡʧ���б�
  getLostItems: (params) => api.get('/api/items/lost', { params }),
  
  // ��ȡʧ������
  getLostItem: (id) => api.get(`/api/items/lost/${id}`),
  
  // ����ʧ��
  createLostItem: (data) => api.post('/api/items/lost', data),
  
  // ����ʧ��
  updateLostItem: (id, data) => api.put(`/api/items/lost/${id}`, data),
  
  // ɾ��ʧ��
  deleteLostItem: (id) => api.delete(`/api/items/lost/${id}`),
};

// �������API
export const foundItemsAPI = {
  // ��ȡ�����б�
  getFoundItems: (params) => api.get('/api/items/found', { params }),
  
  // ��ȡ��������
  getFoundItem: (id) => api.get(`/api/items/found/${id}`),
  
  // ��������
  createFoundItem: (data) => api.post('/api/items/found', data),
  
  // ��������
  updateFoundItem: (id, data) => api.put(`/api/items/found/${id}`, data),
  
  // ɾ������
  deleteFoundItem: (id) => api.delete(`/api/items/found/${id}`),
};

// ����API
export const searchAPI = {
  // �ۺ�����
  searchItems: (params) => api.get('/api/search', { params }),
  
  // ����ʧ��
  searchLostItems: (params) => api.get('/api/search/lost', { params }),
  
  // ��������
  searchFoundItems: (params) => api.get('/api/search/found', { params }),
  
  // ��ȡ��������
  getSuggestions: (params) => api.get('/api/search/suggestions', { params }),
  
  // ��ȡ���Źؼ���
  getHotKeywords: () => api.get('/api/search/hot-keywords'),
  
  // ��ȡ����
  getCategories: () => api.get('/api/search/categories'),
  
  // ��ȡ�ص�
  getLocations: () => api.get('/api/search/locations'),
};

// �ļ��ϴ�API
export const uploadAPI = {
  // �ϴ������ļ�
  uploadFile: (file) => {
    const formData = new FormData();
    formData.append('file', file);
    return api.post('/api/upload', formData, {
      headers: {
        'Content-Type': 'multipart/form-data',
      },
    });
  },
  
  // �ϴ�����ļ�
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
  
  // ɾ���ļ�
  deleteFile: (filename) => api.delete(`/api/upload/${filename}`),
  
  // ��ȡ�ϴ���Ϣ
  getUploadInfo: () => api.get('/api/upload/info'),
};

// OCR API
export const ocrAPI = {
  // OCRʶ��
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
  
  // ��URLʶ��
  extractTextFromUrl: (imageUrl, language = 'chi_sim+eng') => 
    api.post('/api/ocr/url', { image_url: imageUrl, language }),
  
  // ��ȡ֧�ֵ�����
  getLanguages: () => api.get('/api/ocr/languages'),
};

// AI����API
export const classifyAPI = {
  // ͼƬ����
  classifyImage: (file) => {
    const formData = new FormData();
    formData.append('file', file);
    return api.post('/api/classify', formData, {
      headers: {
        'Content-Type': 'multipart/form-data',
      },
    });
  },
  
  // ��URL����
  classifyImageFromUrl: (imageUrl) => 
    api.post('/api/classify/url', { image_url: imageUrl }),
  
  // ��ȡ������Ϣ
  getCategories: () => api.get('/api/classify/categories'),
  
  // ��ȡģ����Ϣ
  getModelInfo: () => api.get('/api/classify/model-info'),
};

// ͨ��API
export const commonAPI = {
  // ��ȡ�����б�
  getCategories: () => api.get('/api/items/categories'),
  
  // �������
  healthCheck: () => api.get('/health'),
};

export default api;
