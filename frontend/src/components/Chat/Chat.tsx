import React, { useState, useRef, useEffect } from 'react';
import styles from './Chat.module.css';

interface Message {
  id: string;
  role: 'user' | 'bot';
  content: string;
  timestamp: string;
  sources?: Source[];
}

interface Source {
  chapter: string;
  module: string;
  score: number;
}

interface ChatProps {
  apiUrl?: string;
  userId?: number;
}

const Chat: React.FC<ChatProps> = ({ apiUrl = 'http://localhost:8000', userId = 1 }) => {
  const [messages, setMessages] = useState<Message[]>([]);
  const [input, setInput] = useState('');
  const [isLoading, setIsLoading] = useState(false);
  const [isCollapsed, setIsCollapsed] = useState(false);
  const [error, setError] = useState<string | null>(null);
  const messagesEndRef = useRef<HTMLDivElement>(null);

  const scrollToBottom = () => {
    messagesEndRef.current?.scrollIntoView({ behavior: 'smooth' });
  };

  useEffect(() => {
    scrollToBottom();
  }, [messages]);

  const formatTime = (timestamp: string) => {
    return new Date(timestamp).toLocaleTimeString([], { 
      hour: '2-digit', 
      minute: '2-digit' 
    });
  };

  const sendMessage = async () => {
    if (!input.trim() || isLoading) return;

    const selectedText = window.getSelection()?.toString().trim() || '';
    
    const userMessage: Message = {
      id: Date.now().toString(),
      role: 'user',
      content: input.trim() + (selectedText ? ` (Selected: "${selectedText.substring(0, 50)}${selectedText.length > 50 ? '...' : ''}")` : ''),
      timestamp: new Date().toISOString(),
    };

    setMessages(prev => [...prev, userMessage]);
    setInput('');
    setIsLoading(true);
    setError(null);

    try {
      let url = `${apiUrl}/chat/?user_id=${userId}&message=${encodeURIComponent(input.trim())}`;
      if (selectedText) {
        url += `&selected_text=${encodeURIComponent(selectedText)}`;
      }

      const response = await fetch(url, {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
      });

      if (!response.ok) {
        throw new Error(`HTTP error! status: ${response.status}`);
      }

      const data = await response.json();

      const botMessage: Message = {
        id: (Date.now() + 1).toString(),
        role: 'bot',
        content: data.response,
        timestamp: new Date().toISOString(),
        sources: data.sources || [],
      };

      setMessages(prev => [...prev, botMessage]);
    } catch (err) {
      const errorMessage = err instanceof Error ? err.message : 'Failed to send message';
      setError(errorMessage);
      
      const errorMessageObj: Message = {
        id: (Date.now() + 1).toString(),
        role: 'bot',
        content: `I apologize, but I encountered an error: ${errorMessage}. Please try again.`,
        timestamp: new Date().toISOString(),
      };
      
      setMessages(prev => [...prev, errorMessageObj]);
    } finally {
      setIsLoading(false);
    }
  };

  const handleKeyPress = (e: React.KeyboardEvent<HTMLInputElement>) => {
    if (e.key === 'Enter' && !e.shiftKey) {
      e.preventDefault();
      sendMessage();
    }
  };

  const toggleChat = () => {
    setIsCollapsed(!isCollapsed);
  };

  return (
    <div className={`${styles.chatContainer} ${isCollapsed ? styles.collapsed : ''}`}>
      <div className={styles.chatHeader} onClick={toggleChat}>
        <h3>🤖 AI Textbook Assistant</h3>
        <div className={styles.chatHeaderActions}>
          <button className={styles.chatToggleBtn}>
            {isCollapsed ? '💬' : '−'}
          </button>
        </div>
      </div>

      {!isCollapsed && (
        <>
          <div className={styles.chatMessages}>
            {messages.length === 0 ? (
              <div className={styles.chatWelcome}>
                <div className={styles.chatWelcomeIcon}>📚</div>
                <div className={styles.chatWelcomeTitle}>
                  Ask me anything about the textbook!
                </div>
                <div className={styles.chatWelcomeText}>
                  I can help you understand concepts from ROS 2, digital twins, 
                  NVIDIA Isaac, and Vision-Language-Action models.
                </div>
              </div>
            ) : (
              messages.map((message) => (
                <div
                  key={message.id}
                  className={`${styles.chatMessage} ${
                    message.role === 'user' ? styles.user : styles.bot
                  }`}
                >
                  <div className={styles.chatMessageSender}>
                    {message.role === 'user' ? 'You' : 'AI Assistant'}
                  </div>
                  <div className={styles.chatMessageContent}>
                    {message.content}
                  </div>
                  <div className={styles.chatMessageTime}>
                    {formatTime(message.timestamp)}
                  </div>
                  
                  {message.sources && message.sources.length > 0 && (
                    <div className={styles.chatSources}>
                      <div className={styles.chatSourcesTitle}>📖 Sources:</div>
                      {message.sources.map((source, idx) => (
                        <div key={idx} className={styles.chatSourceItem}>
                          <span>
                            {source.chapter} ({source.module})
                          </span>
                          <span className={styles.chatSourceScore}>
                            {(source.score * 100).toFixed(0)}%
                          </span>
                        </div>
                      ))}
                    </div>
                  )}
                </div>
              ))
            )}

            {isLoading && (
              <div className={`${styles.chatMessage} ${styles.bot}`}>
                <div className={styles.chatMessageSender}>AI Assistant</div>
                <div className={styles.chatMessageContent}>
                  <div className={styles.chatTyping}>
                    <div className={styles.chatTypingDot}></div>
                    <div className={styles.chatTypingDot}></div>
                    <div className={styles.chatTypingDot}></div>
                  </div>
                </div>
              </div>
            )}

            {error && (
              <div className={styles.chatError}>
                ⚠️ {error}
              </div>
            )}

            <div ref={messagesEndRef} />
          </div>

          <div className={styles.chatInputContainer}>
            <input
              type="text"
              className={styles.chatInput}
              value={input}
              onChange={(e) => setInput(e.target.value)}
              onKeyPress={handleKeyPress}
              placeholder="Ask a question about the textbook..."
              disabled={isLoading}
            />
            <button
              className={styles.chatSendBtn}
              onClick={sendMessage}
              disabled={!input.trim() || isLoading}
            >
              ➤
            </button>
          </div>
        </>
      )}
    </div>
  );
};

export default Chat;
