import apiClient from './apiClient';

// Send a command to the assistant (text-based interaction)
export const sendCommand = async (command) => {
  try {
    const response = await apiClient.post('/assistant/command', { command });
    return response.data; // Returns assistant's response
  } catch (error) {
    throw error.response?.data || error.message;
  }
};

// Stream voice input data for the assistant
export const sendVoiceCommand = async (audioFile) => {
  const formData = new FormData();
  formData.append('audio', audioFile);

  try {
    const response = await apiClient.post('/assistant/voice', formData, {
      headers: { 'Content-Type': 'multipart/form-data' },
    });
    return response.data; // Returns assistant's response
  } catch (error) {
    throw error.response?.data || error.message;
  }
};