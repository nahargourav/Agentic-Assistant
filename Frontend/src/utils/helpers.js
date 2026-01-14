/* Helper to validate email addresses */
export const validateEmail = (email) => {
  const emailRegex = /^[^\s@]+@[^\s@]+\.[^\s@]+$/; // Matches typical email patterns
  return emailRegex.test(email);
};

/* Display friendly error messages */
export const displayErrorMessage = (error) => {
  if (typeof error === 'string') {
    return error;
  } else if (error?.response?.data?.message) {
    return error.response.data.message;
  } else {
    return 'An unknown error occurred.';
  }
};

/* Truncate long strings for UI display */
export const truncateText = (text, maxLength = 50) => {
  if (text.length > maxLength) {
    return `${text.substring(0, maxLength)}...`;
  }
  return text;
};

/* Capitalize the first letter of a string */
export const capitalize = (string) => {
  if (!string) return '';
  return string.charAt(0).toUpperCase() + string.slice(1);
};