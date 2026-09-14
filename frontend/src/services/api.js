import axios from 'axios';

// Defaults to localhost in dev, or VITE_API_URL set in Vercel for production
const API_BASE_URL = import.meta.env.VITE_API_URL || 'http://localhost:8000';

const apiClient = axios.create({
  baseURL: API_BASE_URL,
  timeout: 60000, // 60s timeout to allow for free-tier CPU cold start / inference
});

export const detectImage = async (file, includeHeatmap = true) => {
  const formData = new FormData();
  formData.append('file', file);

  const response = await apiClient.post('/api/v1/detect', formData, {
    params: { include_heatmap: includeHeatmap },
    headers: {
      'Content-Type': 'multipart/form-data',
    },
  });

  return response.data;
};

export const checkHealth = async () => {
  const response = await apiClient.get('/health');
  return response.data;
};
