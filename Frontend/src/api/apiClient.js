import axios from 'axios';
import { getAuthToken } from '../services/authService';

// Create an Axios instance
const apiClient = axios.create({
  baseURL: process.env.REACT_APP_API_URL || 'http://localhost:8000', // Base API URL (backend URL)
  timeout: 10000, // Timeout after 10 seconds
  headers: {
    'Content-Type': 'application/json',
  },
});

// Add a request interceptor to include the JWT token in the request header
apiClient.interceptors.request.use(
  (config) => {
    const token = getAuthToken(); // Retrieve token from authService
    if (token) {
      config.headers.Authorization = `Bearer ${token}`;
    }
    return config;
  },
  (error) => {
    // Handle request errors globally
    return Promise.reject(error);
  }
);

// Add a response interceptor to handle errors globally
apiClient.interceptors.response.use(
  (response) => response,
  (error) => {
    if (error.response) {
      // Handle common errors (e.g., 401 Unauthorized, 403 Forbidden)
      if (error.response.status === 401) {
        alert('Session has expired. Please log in again.');
        // Optionally, perform logout logic or redirect to the login page
      }
    }
    return Promise.reject(error);
  }
);

export default apiClient;