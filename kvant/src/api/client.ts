import axios from 'axios';

const apiOrigin = import.meta.env.VITE_API_URL
  ? import.meta.env.VITE_API_URL.replace(/\/$/, '')
  : '';

export const apiBaseUrl = `${apiOrigin}/api`;

const apiClient = axios.create({
  baseURL: apiBaseUrl || '/api',
});

apiClient.interceptors.request.use((config) => {
  const token = localStorage.getItem('authToken');
  if (token) {
    config.headers['X-Auth-Token'] = token;
  }
  return config;
});

export default apiClient;
