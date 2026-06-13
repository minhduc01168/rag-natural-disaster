interface Message {
  id: string;
  text: string;
  sender: 'user' | 'bot';
  timestamp: Date;
  agent?: string;
  sources?: string[];
}

interface MessageBubbleProps {
  message: Message;
}

export function MessageBubble({ message }: MessageBubbleProps) {
  const isUser = message.sender === 'user';

  return (
    <div className={`flex ${isUser ? 'justify-end' : 'justify-start'} mb-4`}>
      <div
        className={`max-w-[70%] rounded-2xl px-4 py-3 ${
          isUser
            ? 'bg-primary-600 text-white rounded-br-md'
            : 'bg-white text-gray-900 rounded-bl-md shadow-sm'
        }`}
      >
        {!isUser && message.agent && (
          <div className="text-xs text-gray-400 mb-1">
            {message.agent}
          </div>
        )}
        
        <div className="whitespace-pre-wrap">{message.text}</div>

        {!isUser && message.sources && message.sources.length > 0 && (
          <div className="mt-2 pt-2 border-t border-gray-100">
            <p className="text-xs text-gray-400">Nguồn:</p>
            {message.sources.map((source, idx) => {
              const linkMatch = source.match(/\[([^\]]+)\]\(([^)]+)\)/);
              if (linkMatch) {
                return (
                  <a key={idx} href={linkMatch[2]} target="_blank" rel="noopener noreferrer" className="text-xs text-primary-600 hover:text-primary-700 hover:underline mr-2 inline-flex items-center">
                    📚 {linkMatch[1]}
                  </a>
                );
              }
              return (
                <span key={idx} className="text-xs text-primary-600 mr-2">
                  📚 {source}
                </span>
              );
            })}
          </div>
        )}

        <div className={`text-xs mt-1 ${isUser ? 'text-blue-100' : 'text-gray-400'}`}>
          {message.timestamp.toLocaleTimeString('vi-VN', {
            hour: '2-digit',
            minute: '2-digit',
          })}
        </div>
      </div>
    </div>
  );
}
