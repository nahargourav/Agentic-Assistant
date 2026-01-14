import React, { useContext } from 'react';
import AssistantUI from '../assistant/AssistantUI';
import { AuthContext } from '../../context/AuthContext';
import './Dashboard.css';

const Dashboard = () => {
  const { user } = useContext(AuthContext); // Access user data from the global AuthContext

  return (
    <div className="dashboard-container">
      <div className="welcome-banner">
        <h1>Welcome, {user?.name || 'User'}!</h1>
        <p>Talk to your assistant or give commands to get started.</p>
      </div>

      {/* Assistant Section */}
      <div className="assistant-section">
        <AssistantUI />
      </div>
    </div>
  );
};

export default Dashboard;