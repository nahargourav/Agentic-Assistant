import React, { useState } from 'react';
import { register } from '../../api/auth';
import { useNavigate } from 'react-router-dom';
import './Auth.css';

const SignUp = () => {
  const [name, setName] = useState('');
  const [email, setEmail] = useState('');
  const [password, setPassword] = useState('');
  const [error, setError] = useState(null);
  const navigate = useNavigate();

  const handleSignUp = async (e) => {
    e.preventDefault();
    try {
      await register(name, email, password);
      navigate('/signin'); // Navigate to sign-in page after successful registration
    } catch (e) {
      setError(e.message || 'Failed to sign up.');
    }
  };

  return (
    <div className="auth-container">
      <h2>Sign Up</h2>
      <form onSubmit={handleSignUp}>
        <input
          type="text"
          placeholder="Enter your full name"
          value={name}
          onChange={(e) => setName(e.target.value)}
          required
        />
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
        <button type="submit" className="btn primary">Sign Up</button>
        <p>
          Already have an account? <a href="/signin">Sign in here</a>
        </p>
      </form>
    </div>
  );
};

export default SignUp;