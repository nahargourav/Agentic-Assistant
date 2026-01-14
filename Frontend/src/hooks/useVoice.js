import { useState, useEffect } from 'react';

const useVoice = () => {
  const [isListening, setIsListening] = useState(false);
  const [transcription, setTranscription] = useState('');
  const [recognition, setRecognition] = useState(null);

  useEffect(() => {
    if (!('webkitSpeechRecognition' in window)) {
      console.error('Web Speech API is not supported in your browser.');
      return;
    }

    const speechRecognition = new window.webkitSpeechRecognition();
    speechRecognition.continuous = true;
    speechRecognition.interimResults = false;
    speechRecognition.lang = 'en-US';

    speechRecognition.onresult = (event) => {
      const transcript = Array.from(event.results)
        .map((result) => result[0].transcript)
        .join('');
      setTranscription(transcript);
    };

    speechRecognition.onerror = (event) => {
      console.error('Speech Recognition Error:', event.error);
      setIsListening(false);
    };

    speechRecognition.onend = () => {
      setIsListening(false);
    };

    setRecognition(speechRecognition);
  }, []);

  const startListening = () => {
    if (recognition && !isListening) {
      recognition.start();
      setIsListening(true);
    }
  };

  const stopListening = () => {
    if (recognition && isListening) {
      recognition.stop();
      setIsListening(false);
    }
  };

  return { isListening, transcription, startListening, stopListening };
};

export default useVoice;