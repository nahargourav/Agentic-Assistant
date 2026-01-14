export const getTheme = () => {
  return localStorage.getItem('theme') || 'light'; // Retrieve the theme from localStorage (default to 'light')
};

export const setTheme = (theme) => {
  localStorage.setItem('theme', theme); // Save the theme to localStorage
};

export const applyTheme = (theme) => {
  // Apply the theme by setting the `data-theme` attribute on the HTML tag
  document.documentElement.setAttribute('data-theme', theme);
};