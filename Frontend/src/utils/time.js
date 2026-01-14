/* Format dates into a readable string (e.g., "January 1, 2023") */
export const formatDate = (isoDate) => {
  const date = new Date(isoDate);
  return date.toLocaleDateString('en-US', {
    year: 'numeric',
    month: 'long',
    day: 'numeric',
  });
};

/* Get the difference in seconds between two dates */
export const getSecondsDifference = (startDate, endDate) => {
  const start = new Date(startDate);
  const end = new Date(endDate);
  return Math.floor((end - start) / 1000);
};

/* Add seconds to a timestamp and return the updated timestamp */
export const addSecondsToTimestamp = (timestamp, seconds) => {
  const date = new Date(timestamp);
  date.setSeconds(date.getSeconds() + seconds);
  return date.toISOString();
};

/* Get human-readable relative time (e.g., "5 minutes ago") */
export const getRelativeTime = (isoDate) => {
  const now = new Date();
  const date = new Date(isoDate);
  const deltaSeconds = Math.floor((now - date) / 1000);

  if (deltaSeconds < 60) return `${deltaSeconds} seconds ago`;
  if (deltaSeconds < 3600) return `${Math.floor(deltaSeconds / 60)} minutes ago`;
  if (deltaSeconds < 86400) return `${Math.floor(deltaSeconds / 3600)} hours ago`;
  return `${Math.floor(deltaSeconds / 86400)} days ago`;
};