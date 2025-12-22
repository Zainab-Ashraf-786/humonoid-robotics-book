import React, { useState, useEffect, useRef } from 'react';
import './ChatbotWidget.css';

const ChatbotWidget: React.FC = () => {
  const [isOpen, setIsOpen] = useState(false);
  const [messages, setMessages] = useState<Array<{role: string, content: string}>>([]);
  const [inputValue, setInputValue] = useState('');
  const [isLoading, setIsLoading] = useState(false);
  const [selectedText, setSelectedText] = useState<string | null>(null);
  const messagesEndRef = useRef<HTMLDivElement>(null);

  // Toggle chat window open/close
  const toggleChat = () => {
    setIsOpen(!isOpen);
    if (!isOpen) {
      // Check for selected text when opening the chat
      const selection = window.getSelection();
      if (selection && selection.toString().trim() !== '') {
        setSelectedText(selection.toString().trim());
      }
    } else {
      setSelectedText(null);
    }
  };

  // Scroll to bottom of messages
  useEffect(() => {
    messagesEndRef.current?.scrollIntoView({ behavior: 'smooth' });
  }, [messages]);

  // Handle sending a message
  const handleSend = async () => {
    if (!inputValue.trim() || isLoading) return;

    // Add user message
    const userMessage = { role: 'user', content: inputValue };
    setMessages(prev => [...prev, userMessage]);
    const currentInput = inputValue;
    setInputValue('');
    setIsLoading(true);

    try {
      // Set headers without authentication
      const headers: Record<string, string> = { 'Content-Type': 'application/json' };

      // If there's selected text and it's relevant to the question, use selection endpoint
      if (selectedText && (currentInput.toLowerCase().includes('this') ||
          currentInput.toLowerCase().includes('selected') ||
          currentInput.toLowerCase().includes('above'))) {
        const requestBody = {
          selected_text: selectedText,
          question: currentInput
        };

        const response = await fetch('http://localhost:8000/chat-selection', {
          method: 'POST',
          headers: headers,
          body: JSON.stringify(requestBody),
        });

        if (!response.ok) {
          throw new Error(`API error: ${response.status} ${response.statusText}`);
        }

        const data = await response.json();
        setMessages(prev => [...prev, { role: 'assistant', content: data.answer }]);
      } else {
        // Use the regular chat endpoint
        const requestBody = {
          request: {
            message: currentInput,
          }
        };

        const response = await fetch('http://localhost:8000/chat', {
          method: 'POST',
          headers: headers,
          body: JSON.stringify(requestBody),
        });

        if (!response.ok) {
          throw new Error(`API error: ${response.status} ${response.statusText}`);
        }

        const data = await response.json();
        setMessages(prev => [...prev, { role: 'assistant', content: data.answer }]);
      }
    } catch (error) {
      console.error('Error sending message:', error);
      let errorMessage = 'Sorry, I encountered an error. ';

      if (error instanceof TypeError && error.message.includes('fetch')) {
        errorMessage += 'Unable to connect to the server. Make sure the backend is running on port 8000.';
      } else if (error instanceof Error && error.message.includes('API error')) {
        errorMessage += `Server responded with an error: ${(error as Error).message}`;
      } else {
        errorMessage += `Error details: ${(error as Error).message}`;
      }

      setMessages(prev => [...prev, {
        role: 'assistant',
        content: errorMessage
      }]);
    } finally {
      setIsLoading(false);
      setSelectedText(null);
    }
  };

  // Handle Enter key press
  const handleKeyPress = (e: React.KeyboardEvent) => {
    if (e.key === 'Enter' && !e.shiftKey) {
      e.preventDefault();
      handleSend();
    }
  };

  // Get selected text when user selects text on the page
  useEffect(() => {
    const handleSelection = () => {
      const selection = window.getSelection();
      if (selection && selection.toString().trim() !== '' && selection.toString().length < 500) {
        setSelectedText(selection.toString().trim());
      }
    };

    document.addEventListener('mouseup', handleSelection);
    return () => {
      document.removeEventListener('mouseup', handleSelection);
    };
  }, []);

  return (
    <>
      {/* Floating chat button */}
      {!isOpen && (
        <button
          className="chatbot-float-button"
          onClick={toggleChat}
          aria-label="Open chatbot"
        >
          <svg
            xmlns="http://www.w3.org/2000/svg"
            width="24"
            height="24"
            viewBox="0 0 24 24"
            fill="none"
            stroke="currentColor"
            strokeWidth="2"
            strokeLinecap="round"
            strokeLinejoin="round"
            className="chatbot-icon"
          >
            <path d="M21 15a2 2 0 0 1-2 2H7l-4 4V5a2 2 0 0 1 2-2h14a2 2 0 0 1 2 2z"></path>
          </svg>
        </button>
      )}

      {/* Chat window */}
      {isOpen && (
        <div className="chatbot-widget">
          <div className="chatbot-header">
            <h3>Book Assistant</h3>
            <button
              className="chatbot-close-button"
              onClick={toggleChat}
              aria-label="Close chat"
            >
              ×
            </button>
          </div>

          <div className="chatbot-messages">
            {messages.length === 0 ? (
              <div className="chatbot-welcome">
                <p>Hello! I'm your Physical AI & Humanoid Robotics assistant.</p>
                <p>You can ask me questions about the book content, or select text and ask about it specifically.</p>
              </div>
            ) : (
              messages.map((msg, index) => (
                <div
                  key={index}
                  className={`chatbot-message ${msg.role === 'user' ? 'user-message' : 'assistant-message'}`}
                >
                  <div className="chatbot-message-content">
                    {msg.content}
                  </div>
                </div>
              ))
            )}
            {isLoading && (
              <div className="chatbot-message assistant-message">
                <div className="chatbot-message-content">
                  <div className="typing-indicator">
                    <span></span>
                    <span></span>
                    <span></span>
                  </div>
                </div>
              </div>
            )}
            <div ref={messagesEndRef} />
          </div>

          {selectedText && (
            <div className="selected-text-preview">
              <small>Selected: "{selectedText.substring(0, 50)}{selectedText.length > 50 ? '...' : ''}"</small>
            </div>
          )}

          <div className="chatbot-input-area">
            <textarea
              value={inputValue}
              onChange={(e) => setInputValue(e.target.value)}
              onKeyPress={handleKeyPress}
              placeholder="Ask about the book content..."
              className="chatbot-input"
              rows={2}
            />
            <button
              onClick={handleSend}
              disabled={isLoading || !inputValue.trim()}
              className="chatbot-send-button"
            >
              Send
            </button>
          </div>
        </div>
      )}
    </>
  );
};

export default ChatbotWidget;