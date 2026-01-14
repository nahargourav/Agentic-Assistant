import React, { useState } from 'react';
import AssistantBubble from '../animations/AssistantBubble';
import VoiceInput from './VoiceInput';
import { sendCommand } from '../../api/assistant';
import './AssistantUI.css';

const AssistantUI = () => {
  const [assistantState, setAssistantState] = useState('idle'); // 'idle', 'listening', 'speaking'
  const [conversation, setConversation] = useState([]); // Tracks conversation log
  const [inputText, setInputText] = useState('');

  const handleCommand = async (userInput) => {
    if (!userInput || !userInput.trim()) return;
    
    setAssistantState('listening');
    setConversation((prev) => [...prev, { sender: 'user', message: userInput }]);

    try {
      // Call the backend API
      const response = await sendCommand(userInput);
      
      setAssistantState('speaking');
      const aiResponse = response.response || "I'm processing your request...";
      setConversation((prev) => [...prev, { sender: 'assistant', message: aiResponse }]);
      
      // Return to idle after a short delay
      setTimeout(() => {
        setAssistantState('idle');
      }, 2000);
    } catch (error) {
      console.error('Error sending command:', error);
      setAssistantState('idle');
      setConversation((prev) => [...prev, { 
        sender: 'assistant', 
        message: 'Sorry, I encountered an error processing your request.' 
      }]);
    }
  };

  const handleTextSubmit = (e) => {
    e.preventDefault();
    handleCommand(inputText);
    setInputText('');
  };

  return (
    <div className="assistant-ui">
      {/* Assistant animation */}
      <div className="animation-wrapper">
        <AssistantBubble state={assistantState} />
      </div>

      {/* Chat conversation log */}
      <div className="conversation-log">
        {conversation.map((line, idx) => (
          <div
            key={idx}
            className={`conversation-line ${line.sender === 'user' ? 'user' : 'assistant'}`}
          >
            {line.message}
          </div>
        ))}
      </div>

      {/* Text Input */}
      <form onSubmit={handleTextSubmit} className="text-input-form">
        <input
          type="text"
          value={inputText}
          onChange={(e) => setInputText(e.target.value)}
          placeholder="Type your command..."
          className="text-input"
        />
        <button type="submit" className="send-button">Send</button>
      </form>

      {/* Voice Input / Commands */}
      <VoiceInput onCommand={handleCommand} />
    </div>
  );
};

export default AssistantUI;