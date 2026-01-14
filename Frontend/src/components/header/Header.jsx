import React, { useContext } from 'react';
import { AuthContext } from '../../context/AuthContext';
import { ThemeContext } from '../../context/ThemeContext';
import './Header.css';

const Header = () => {
  const { user, logout } = useContext(AuthContext); // Access user-related context
  const { theme, toggleTheme } = useContext(ThemeContext); // Access theme context

  return (
    <header className="header">
      <div className="header-left">
        <h1 className="logo">Assistant Dashboard</h1>
      </div>
      <div className="header-right">
        <button className="theme-toggle btn secondary" onClick={toggleTheme}>
          {theme === 'light' ? '🌙 Dark Mode' : '☀️ Light Mode'}
        </button>
        {user && (
          <button className="logout-btn btn secondary" onClick={logout}>
            Logout
          </button>
        )}
      </div>
    </header>
  );
};

export default Header;