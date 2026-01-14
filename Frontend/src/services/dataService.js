import apiClient from '../api/apiClient';

// Generic data fetcher
export const fetchData = async (endpoint) => {
  try {
    const response = await apiClient.get(endpoint);
    return response.data;
  } catch (error) {
    throw error.response?.data || error.message;
  }
};

// Example: Fetch user dashboard data
export const fetchDashboardData = async () => {
  return await fetchData('/dashboard');
};