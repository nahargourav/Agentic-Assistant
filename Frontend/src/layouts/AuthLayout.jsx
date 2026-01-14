import React from 'react';
import './AuthLayout.css';

const AuthLayout = ({ children }) => {
  return (
    <div className="auth-layout">
      <div className="auth-content">
        <h1 className="app-logo">Assistant App</h1>
        {children}
      </div>
    </div>
  );
};

export default AuthLayout;