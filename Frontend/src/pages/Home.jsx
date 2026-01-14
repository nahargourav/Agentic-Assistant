import React from 'react';
import { useNavigate } from 'react-router-dom';
import './Home.css';

const Home = () => {
  const navigate = useNavigate();

  return (
    <div className="home-container">
      <h1>Welcome to the Assistant App</h1>
      <p>Your personal assistant to streamline daily tasks.</p>
      <div className="home-actions">
        <button className="btn primary" onClick={() => navigate('/signin')}>
          Sign In
        </button>
        <button className="btn secondary" onClick={() => navigate('/signup')}>
          Get Started
        </button>
      </div>
    </div>
  );
};

export default Home;