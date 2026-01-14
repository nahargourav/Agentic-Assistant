export const API_BASE_URL = process.env.REACT_APP_API_URL || 'http://localhost:8000';
export const APP_NAME = 'Assistant App';

/* Authentication Keys */
export const AUTH_TOKEN_KEY = 'authToken';

/* Theme Constants */
export const LIGHT_THEME = 'light';
export const DARK_THEME = 'dark';

/* Error Messages */
export const ERROR_MESSAGES = {
  generic: 'Something went wrong. Please try again.',
  network: 'Unable to connect to the server. Check your internet connection.',
};

/* Regex Patterns */
export const REGEX = {
  email: /^[^\s@]+@[^\s@]+\.[^\s@]+$/, // Standard email validation
};