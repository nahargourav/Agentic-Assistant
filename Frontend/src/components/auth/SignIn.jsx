import React, { useState, useContext } from 'react';
import { login } from '../../api/auth';
import { AuthContext } from '../../context/AuthContext';
import { useNavigate } from 'react-router-dom';
import './Auth.css'; // Include shared styling for auth forms

const SignIn = () => {
  const [email, setEmail] = useState('');
  const [password, setPassword] = useState('');
  const [error, setError] = useState(null);
  const { login: contextLogin } = useContext(AuthContext); // Get login from context
  const navigate = useNavigate();

  const handleSignIn = async (e) => {
    e.preventDefault();
    setError(null);
    
    try {
      const response = await login(email, password);
      
      // Use the login function from AuthContext
      contextLogin(response.user, response.token);
      
      navigate('/dashboard'); // Redirect to dashboard
    } catch (err) {
      console.error('Login error:', err);
      setError(err.detail || err.message || 'Failed to sign in.');
    }
  };

  return (
    <div className="auth-container">
      <h2>Sign In</h2>
      <form onSubmit={handleSignIn}>
        <input
          type="email"
          placeholder="Enter your email"
          value={email}
          onChange={(e) => setEmail(e.target.value)}
          required
        />
        <input
          type="password"
          placeholder="Enter your password"
          value={password}
          onChange={(e) => setPassword(e.target.value)}
          required
        />
        {error && <p className="error-text">{error}</p>} {/* Display error */}
        <button type="submit" className="btn primary">Sign In</button>
        <p>
          Don't have an account? <a href="/signup">Sign up here</a>
        </p>
      </form>
    </div>
  );
};

export default SignIn;