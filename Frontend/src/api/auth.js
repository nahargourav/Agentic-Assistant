import apiClient from './apiClient';

// User login (Sign In)
export const login = async (email, password) => {
  try {
    const response = await apiClient.post('/auth/login', { email, password });
    return response.data; // Returns user data and token
  } catch (error) {
    throw error.response?.data || error.message;
  }
};

// User registration (Sign Up)
export const register = async (name, email, password) => {
  try {
    const response = await apiClient.post('/auth/register', { name, email, password });
    return response.data; // Returns confirmation message or user data
  } catch (error) {
    throw error.response?.data || error.message;
  }
};

// Validate the JWT token
export const validateToken = async () => {
  try {
    const response = await apiClient.get('/auth/validate');
    return response.data; // Returns validation details (e.g., isTokenValid: true/false)
  } catch (error) {
    throw error.response?.data || error.message;
  }
};