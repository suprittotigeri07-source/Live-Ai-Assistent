import { useState, useRef, useEffect, useCallback } from 'react';
import { Zap, RotateCcw } from 'lucide-react';

import Sidebar from './components/Sidebar';
import ChatMessage from './components/ChatMessage';
import ChatInput from './components/ChatInput';
import { streamMessage, clearMemory, checkHealth } from './api/client';

const SUGGESTIONS = [
  'Explain how neural networks work',
  'Search latest AI news today',
  'What is 1234 * 5678 + 91?',
  'Write a Python quicksort function',
];

export default function App() {
  const [messages, setMessages] = useState([]);
  const [isStreaming, setIsStreaming] = useState(false);
  const [health, setHealth] = useState({ status: 'checking', version: '' });
  const messagesEndRef = useRef(null);

  // Auto-scroll to bottom
  const scrollToBottom = useCallback(() => {
    messagesEndRef.current?.scrollIntoView({ behavior: 'smooth' });
  }, []);

  useEffect(() => {
    scrollToBottom();
  }, [messages, scrollToBottom]);

  // Health check on mount
  useEffect(() => {
    const doCheck = async () => {
      const result = await checkHealth();
      setHealth(result);
    };
    doCheck();
    const interval = setInterval(doCheck, 30000);
    return () => clearInterval(interval);
  }, []);

  /**
   * Send a message and stream the response.
   */
  const handleSend = useCallback(
    async (text) => {
      if (isStreaming) return;

      // Add user message
      const userMsg = { role: 'user', content: text };
      setMessages((prev) => [...prev, userMsg]);

      // Start streaming placeholder
      const assistantMsg = { role: 'assistant', content: '' };
      setMessages((prev) => [...prev, assistantMsg]);
      setIsStreaming(true);

      try {
        await streamMessage(text, (chunk) => {
          setMessages((prev) => {
            const updated = [...prev];
            const last = updated[updated.length - 1];
            updated[updated.length - 1] = {
              ...last,
              content: last.content + chunk,
            };
            return updated;
          });
        });
      } catch (err) {
        console.error('Stream error:', err);
        setMessages((prev) => {
          const updated = [...prev];
          updated[updated.length - 1] = {
            role: 'assistant',
            content: `⚠️ **Error:** ${err.message}\n\nMake sure the backend server is running at \`http://127.0.0.1:8000\`.`,
          };
          return updated;
        });
      } finally {
        setIsStreaming(false);
      }
    },
    [isStreaming]
  );

  /**
   * Start a new chat (client-side only).
   */
  const handleNewChat = useCallback(() => {
    setMessages([]);
  }, []);

  /**
   * Clear both client messages and backend memory.
   */
  const handleClearMemory = useCallback(async () => {
    setMessages([]);
    try {
      await clearMemory();
    } catch (err) {
      console.error('Clear memory error:', err);
    }
  }, []);

  const showWelcome = messages.length === 0;

  return (
    <div className="app-layout">
      <Sidebar
        onNewChat={handleNewChat}
        onClearMemory={handleClearMemory}
        health={health}
      />

      <main className="chat-main">
        {/* Header */}
        <header className="chat-header">
          <div>
            <div className="chat-header-title">Chat</div>
            <div className="chat-header-subtitle">
              {messages.length > 0
                ? `${messages.filter((m) => m.role === 'user').length} messages`
                : 'Start a new conversation'}
            </div>
          </div>
          <div className="chat-header-actions">
            <button
              className="header-icon-btn"
              onClick={handleClearMemory}
              title="Reset conversation"
              id="reset-btn"
            >
              <RotateCcw />
            </button>
          </div>
        </header>

        {/* Messages */}
        <div className="chat-messages" id="chat-messages">
          {showWelcome ? (
            <div className="welcome-screen">
              <div className="welcome-icon">
                <Zap />
              </div>
              <h1 className="welcome-title">Live AI Assistant</h1>
              <p className="welcome-subtitle">
                Your intelligent companion powered by local AI. Ask questions,
                search the web, perform calculations, and more.
              </p>
              <div className="welcome-suggestions">
                {SUGGESTIONS.map((s, i) => (
                  <button
                    key={i}
                    className="suggestion-card"
                    onClick={() => handleSend(s)}
                    id={`suggestion-${i}`}
                  >
                    {s}
                  </button>
                ))}
              </div>
            </div>
          ) : (
            <>
              {messages.map((msg, i) => (
                <ChatMessage key={i} message={msg} />
              ))}
              {isStreaming && (
                <div className="typing-indicator">
                  <div className="typing-dot" />
                  <div className="typing-dot" />
                  <div className="typing-dot" />
                </div>
              )}
            </>
          )}
          <div ref={messagesEndRef} />
        </div>

        {/* Input */}
        <ChatInput onSend={handleSend} disabled={isStreaming} />
      </main>
    </div>
  );
}
