import React, { useState, useRef } from 'react';
import './VoiceInput.css';

const VoiceInput = ({ onCommand }) => {
  const [isListening, setIsListening] = useState(false);
  const [transcription, setTranscription] = useState('');
  const recognitionRef = useRef(null);

  const startListening = () => {
    if (!('webkitSpeechRecognition' in window) && !('SpeechRecognition' in window)) {
      alert('Your browser does not support voice recognition.');
      return;
    }

    const SpeechRecognition = window.SpeechRecognition || window.webkitSpeechRecognition;
    const recognition = new SpeechRecognition();
    recognition.lang = 'en-US';
    recognition.continuous = false;
    recognition.interimResults = false;

    recognitionRef.current = recognition;
    setIsListening(true);

    recognition.onresult = (event) => {
      const transcript = Array.from(event.results)
        .map((result) => result[0].transcript)
        .join('');
      setTranscription(transcript);
    };

    recognition.onend = () => {
      setIsListening(false);
      if (transcription) {
        onCommand(transcription); // Pass command to parent component
        setTranscription('');
      }
    };

    recognition.onerror = (event) => {
      console.error('Speech recognition error:', event.error);
      setIsListening(false);
    };

    recognition.start();
  };

  const stopListening = () => {
    if (recognitionRef.current) {
      recognitionRef.current.stop();
      setIsListening(false);
    }
  };

  return (
    <div className="voice-input">
      <button
        onClick={isListening ? stopListening : startListening}
        className={`mic-button ${isListening ? 'listening' : ''}`}
      >
        🎤 {isListening ? 'Stop' : 'Start'}
      </button>
      {transcription && <p className="transcription">You said: {transcription}</p>}
    </div>
  );
};

export default VoiceInput;