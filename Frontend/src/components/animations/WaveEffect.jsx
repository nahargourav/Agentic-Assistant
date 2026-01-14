import React from 'react';
import './WaveEffect.css'; // Defines keyframe animations for waves

const WaveEffect = ({ color = 'skyblue' }) => {
  // Make the wave animation responsive to different themes using color props
  return (
    <div className="wave-container">
      <div className="wave" style={{ backgroundColor: color }}></div>
      <div className="wave" style={{ backgroundColor: color, animationDelay: '-0.5s' }}></div>
      <div className="wave" style={{ backgroundColor: color, animationDelay: '-1s' }}></div>
    </div>
  );
};

export default WaveEffect;