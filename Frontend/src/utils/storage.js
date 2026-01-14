/* Save data to local storage */
export const saveToLocalStorage = (key, value) => {
  try {
    localStorage.setItem(key, JSON.stringify(value));
  } catch (error) {
    console.error('Failed to save to local storage:', error);
  }
};

/* Retrieve data from local storage */
export const getFromLocalStorage = (key) => {
  try {
    const data = localStorage.getItem(key);
    return data ? JSON.parse(data) : null;
  } catch (error) {
    console.error('Failed to read from local storage:', error);
    return null;
  }
};

/* Remove an item from local storage */
export const removeFromLocalStorage = (key) => {
  try {
    localStorage.removeItem(key);
  } catch (error) {
    console.error('Failed to remove from local storage:', error);
  }
};

/* Save to session storage */
export const saveToSessionStorage = (key, value) => {
  try {
    sessionStorage.setItem(key, JSON.stringify(value));
  } catch (error) {
    console.error('Failed to save to session storage:', error);
  }
};

/* Retrieve from session storage */
export const getFromSessionStorage = (key) => {
  try {
    const data = sessionStorage.getItem(key);
    return data ? JSON.parse(data) : null;
  } catch (error) {
    console.error('Failed to read from session storage:', error);
    return null;
  }
};