import { useState, useRef, useEffect } from 'react';
import { MessageBubble } from './MessageBubble';
import { ChatInput } from './ChatInput';

interface Message {
  id: string;
  text: string;
  sender: 'user' | 'bot';
  timestamp: Date;
  agent?: string;
  sources?: string[];
}

const API_BASE_URL = 'http://localhost:8000';

const WELCOME_MESSAGE: Message = {
  id: 'welcome',
  text: `Xin chào! Tôi là TerraBot, trợ lý AI của hệ thống TerraAlert.

Tôi có thể giúp bạn với:
• Thông tin thời tiết và cảnh báo
• Kiến thức phòng chống thiên tai
• Kỹ năng sinh tồn và sơ cấp cứu
• Thông tin địa lý và bản đồ

Hãy đặt câu hỏi cho tôi!`,
  sender: 'bot',
  timestamp: new Date(),
  agent: 'TerraBot',
};

export function ChatWindow() {
  const [messages, setMessages] = useState<Message[]>([WELCOME_MESSAGE]);
  const [isLoading, setIsLoading] = useState(false);
  const messagesEndRef = useRef<HTMLDivElement>(null);

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
        text: 'Xin lỗi, tôi không thể kết nối lúc này. Vui lòng thử lại sau.',
        sender: 'bot',
        timestamp: new Date(),
        agent: 'System',
      };

      setMessages((prev) => [...prev, errorMessage]);
    } finally {
      setIsLoading(false);
    }
  };

  return (
    <div className="flex flex-col h-[600px] bg-gray-50 rounded-xl shadow-lg overflow-hidden">
      {/* Header */}
      <div className="bg-primary-600 text-white px-6 py-4">
        <div className="flex items-center gap-3">
          <div className="w-10 h-10 bg-white rounded-full flex items-center justify-center">
            <span className="text-2xl">🤖</span>
          </div>
          <div>
            <h3 className="font-semibold">TerraBot</h3>
            <p className="text-sm text-blue-100">Trợ lý AI • Sẵn sàng hỗ trợ</p>
          </div>
        </div>
      </div>

      {/* Messages */}
      <div className="flex-1 overflow-y-auto p-4 space-y-2">
        {messages.map((message) => (
          <MessageBubble key={message.id} message={message} />
        ))}
        
        {isLoading && (
          <div className="flex justify-start mb-4">
            <div className="bg-white rounded-2xl rounded-bl-md px-4 py-3 shadow-sm">
              <div className="flex space-x-2">
                <div className="w-2 h-2 bg-gray-400 rounded-full animate-bounce" />
                <div className="w-2 h-2 bg-gray-400 rounded-full animate-bounce" style={{ animationDelay: '0.1s' }} />
                <div className="w-2 h-2 bg-gray-400 rounded-full animate-bounce" style={{ animationDelay: '0.2s' }} />
              </div>
            </div>
          </div>
        )}
        
        <div ref={messagesEndRef} />
      </div>

      {/* Quick Replies */}
      <div className="px-4 pb-2">
        <div className="flex flex-wrap gap-2">
          {['Thời tiết hôm nay', 'Sơ cấp cứu CPR', 'Xử lý lũ lụt', 'Tìm nước sạch'].map((reply) => (
            <button
              key={reply}
              onClick={() => handleSend(reply)}
              className="px-3 py-1.5 bg-white border border-gray-200 rounded-full text-sm text-gray-600 hover:bg-gray-50 transition-colors"
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
