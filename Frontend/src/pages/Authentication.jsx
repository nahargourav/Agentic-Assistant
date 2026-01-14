import React from 'react';
import { Routes, Route, useLocation } from 'react-router-dom';
import AuthLayout from '../layouts/AuthLayout';
import SignIn from '../components/auth/SignIn';
import SignUp from '../components/auth/SignUp';

const Authentication = () => {
  const location = useLocation();
  const isSignUp = location.pathname.includes('signup');
  
  return (
    <AuthLayout>
      {isSignUp ? <SignUp /> : <SignIn />}
    </AuthLayout>
  );
};

export default Authentication;