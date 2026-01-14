import React from 'react';
import { AuthProvider } from './context/AuthContext';
import { ThemeProvider } from './context/ThemeContext';
import AppRouter from './routes/AppRouter';
import './styles/global.css'; // Include global styles
import './styles/themes.css'; // Include themes for light/dark mode
import './styles/animations.css'; // Include reusable animations

const App = () => {
  return (
    <AuthProvider> {/* Provides authentication state to the app */}
      <ThemeProvider> {/* Provides theme (light/dark mode) support */}
        <div className="app">
          <AppRouter />
        </div>
      </ThemeProvider>
    </AuthProvider>
  );
};

export default App;