import React, { createContext, useState } from 'react';
import { clearAuthToken } from '../services/authService';

export const AuthContext = createContext();

export const AuthProvider = ({ children }) => {
  const [user, setUser] = useState(() => {
    // Retrieve the user from local storage on initial load, if available
    const savedUser = localStorage.getItem('user');
    return savedUser ? JSON.parse(savedUser) : null;
  });

  const login = (user, token) => {
    // Store user data and token locally
    localStorage.setItem('authToken', token);
    localStorage.setItem('user', JSON.stringify(user));
    setUser(user); // Update state
  };

  const logout = () => {
    // Clear local storage and reset user state
    clearAuthToken();
    localStorage.removeItem('user');
    setUser(null);
    window.location.href = '/signin'; // Redirect to sign-in page
  };

  return (
    <AuthContext.Provider value={{ user, setUser, login, logout }}>
      {children}
    </AuthContext.Provider>
  );
};