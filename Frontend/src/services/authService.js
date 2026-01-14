export const getAuthToken = () => {
  return localStorage.getItem('authToken'); // Retrieve the auth token from localStorage
};

export const setAuthToken = (token) => {
  localStorage.setItem('authToken', token); // Save an auth token to localStorage
};

export const clearAuthToken = () => {
  localStorage.removeItem('authToken'); // Remove the auth token from localStorage
};