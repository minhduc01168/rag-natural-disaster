import { useState, useRef, useEffect } from 'react';
import { MessageBubble } from './MessageBubble';
import { ChatInput } from './ChatInput';
import { useLanguage } from '../../context/LanguageContext';

interface Message {
  id: string;
  text: string;
  sender: 'user' | 'bot';
  timestamp: Date;
  agent?: string;
  sources?: string[];
}

const API_BASE_URL = 'http://localhost:8000';

export function ChatWindow() {
  const { t } = useLanguage();
  const [messages, setMessages] = useState<Message[]>([]);
  const [isLoading, setIsLoading] = useState(false);
  const messagesEndRef = useRef<HTMLDivElement>(null);

  // Initialize welcome message when language changes or on first mount
  useEffect(() => {
    if (messages.length === 0) {
      setMessages([
        {
          id: 'welcome',
          text: t('bot.welcome'),
          sender: 'bot',
          timestamp: new Date(),
          agent: 'TerraBot',
        },
      ]);
    } else if (messages[0]?.id === 'welcome') {
      setMessages((prev) => [
        {
          ...prev[0],
          text: t('bot.welcome'),
        },
        ...prev.slice(1),
      ]);
    }
  }, [t]);

  const scrollToBottom = () => {
    messagesEndRef.current?.scrollIntoView({ behavior: 'smooth' });
  };

  useEffect(() => {
    scrollToBottom();
  }, [messages]);

  const handleSend = async (text: string) => {
    // Add user message
    const userMessage: Message = {
      id: Date.now().toString(),
      text,
      sender: 'user',
      timestamp: new Date(),
    };

    setMessages((prev) => [...prev, userMessage]);
    setIsLoading(true);

    try {
      // Call API
      const response = await fetch(`${API_BASE_URL}/api/v1/rag/chat`, {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify({ query: text }),
      });

      if (!response.ok) {
        throw new Error('Failed to get response');
      }

      const data = await response.json();

      // Add bot response
      const botMessage: Message = {
        id: (Date.now() + 1).toString(),
        text: data.answer,
        sender: 'bot',
        timestamp: new Date(),
        agent: data.route_taken === 'knowledge' ? 'TerraBot Cẩm Nang' : `TerraBot ${data.route_taken}`,
        sources: data.sources,
      };

      setMessages((prev) => [...prev, botMessage]);
    } catch (error) {
      // Add error message
      const errorMessage: Message = {
        id: (Date.now() + 1).toString(),
        text: t('bot.errorMsg'),
        sender: 'bot',
        timestamp: new Date(),
        agent: 'System',
      };

      setMessages((prev) => [...prev, errorMessage]);
    } finally {
      setIsLoading(false);
    }
  };

  const quickReplies = [
    t('bot.replyWeather'),
    t('bot.replyCpr'),
    t('bot.replyFlood'),
    t('bot.replyWater'),
  ];

  return (
    <div className="flex flex-col h-full bg-slate-950/30">
      {/* Messages area */}
      <div className="flex-1 overflow-y-auto p-4 space-y-1 scroll-smooth">
        {messages.map((message) => (
          <MessageBubble key={message.id} message={message} />
        ))}

        {isLoading && (
          <div className="flex justify-start mb-3">
            <div className="bg-slate-800 border border-slate-700 rounded-2xl rounded-bl-md px-4 py-3">
              <div className="flex items-center gap-1.5">
                <div className="w-2 h-2 bg-blue-400 rounded-full animate-bounce [animation-delay:0ms]" />
                <div className="w-2 h-2 bg-blue-400 rounded-full animate-bounce [animation-delay:150ms]" />
                <div className="w-2 h-2 bg-blue-400 rounded-full animate-bounce [animation-delay:300ms]" />
              </div>
            </div>
          </div>
        )}

        <div ref={messagesEndRef} />
      </div>

      {/* Quick Replies */}
      <div className="px-3 py-2 border-t border-slate-800/60">
        <div className="flex flex-wrap gap-1.5">
          {quickReplies.map((reply) => (
            <button
              key={reply}
              onClick={() => handleSend(reply)}
              disabled={isLoading}
              className="px-3 py-1 bg-slate-800 hover:bg-slate-700 border border-slate-700 hover:border-slate-500
                         rounded-full text-xs text-slate-300 hover:text-white transition-all disabled:opacity-40 shadow-sm hover:scale-105"
            >
              {reply}
            </button>
          ))}
        </div>
      </div>

      {/* Input */}
      <ChatInput onSend={handleSend} disabled={isLoading} />
    </div>
  );
}
