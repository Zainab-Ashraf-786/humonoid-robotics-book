import React from 'react';
import ChatbotWidget from './ChatbotWidget/ChatbotWidget';

// Root component that wraps the entire site with chatbot
// Translation context is now handled by the new Root component in src/theme/Root.tsx
const RootWrapper = ({ children }) => {
  return (
    <>
      {children}
      <ChatbotWidget />
    </>
  );
};

export default RootWrapper;