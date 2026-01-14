import React from 'react';
import Lottie from 'lottie-react';
import assistantIdle from '../../assets/animations/assistant_idle.json';
import assistantListening from '../../assets/animations/assistant_listening.json';
import assistantSpeaking from '../../assets/animations/assistant_speaking.json';

const AssistantBubble = ({ state = 'idle' }) => {
  // Determine which animation to use based on the assistant's state
  const getAnimation = () => {
    switch (state) {
      case 'speaking':
        return assistantSpeaking;
      case 'listening':
        return assistantListening;
      default:
        return assistantIdle;
    }
  };

  return (
    <div className="assistant-bubble">
      <Lottie
        animationData={getAnimation()}
        loop
        style={{ height: '100px', width: '100px' }}
      />
    </div>
  );
};

export default AssistantBubble;