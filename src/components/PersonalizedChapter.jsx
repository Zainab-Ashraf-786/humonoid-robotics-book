import React from 'react';

const PersonalizedChapter = ({ children, fallbackContent }) => {
  // For now, just return the children since personalization is removed
  // This component no longer has authentication dependencies
  return (
    <div className="personalized-chapter">
      {children}
    </div>
  );
};

export default PersonalizedChapter;