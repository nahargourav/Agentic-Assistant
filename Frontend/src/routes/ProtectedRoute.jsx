import React, { useContext } from 'react';
import { Navigate } from 'react-router-dom';
import { AuthContext } from '../context/AuthContext'; // Auth context to check the user's state

const ProtectedRoute = ({ children }) => {
  const { user } = useContext(AuthContext);

  if (!user) {
    // If no user is found, redirect to sign-in page
    return <Navigate to="/signin" replace />;
  }

  return children;
};

export default ProtectedRoute;