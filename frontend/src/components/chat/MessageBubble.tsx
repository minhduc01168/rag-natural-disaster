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

/** Rút gọn tên file dài: "cam_nang_phong_chong_thien_tai_2023.pdf" → "cam_nang...2023.pdf" */
function shortenFilename(name: string, maxLen = 40): string {
  if (name.length <= maxLen) return name;
  const ext = name.lastIndexOf('.') > 0 ? name.slice(name.lastIndexOf('.')) : '';
  const base = name.slice(0, name.lastIndexOf('.') > 0 ? name.lastIndexOf('.') : name.length);
  const keep = maxLen - ext.length - 3;
  return base.slice(0, Math.max(keep, 8)) + '...' + ext;
}

/** Xác định icon theo extension */
function fileIcon(src: string): string {
  if (src.endsWith('.pdf'))  return '📄';
  if (src.endsWith('.docx') || src.endsWith('.doc')) return '📝';
  if (src.endsWith('.md'))   return '📋';
  if (src.endsWith('.txt'))  return '📃';
  return '📚';
}

export function MessageBubble({ message }: MessageBubbleProps) {
  const isUser = message.sender === 'user';

  return (
    <div className={`flex ${isUser ? 'justify-end' : 'justify-start'} mb-3`}>
      <div
        className={`max-w-[78%] rounded-2xl px-4 py-3 ${
          isUser
            ? 'bg-blue-600 text-white rounded-br-md'
            : 'bg-white text-gray-900 rounded-bl-md shadow-sm border border-gray-100'
        }`}
      >
        {/* Agent label */}
        {!isUser && message.agent && (
          <div className="text-[10px] font-semibold text-blue-500 mb-1 uppercase tracking-wide">
            {message.agent}
          </div>
        )}

        {/* Message text */}
        <div className="whitespace-pre-wrap text-sm leading-relaxed">
          {message.text}
        </div>

        {/* Source citations */}
        {!isUser && message.sources && message.sources.length > 0 && (
          <div className="mt-3 pt-2 border-t border-gray-100">
            <p className="text-[10px] text-gray-400 uppercase tracking-wide mb-1.5 font-medium">
              📖 Nguồn tài liệu
            </p>
            <div className="flex flex-wrap gap-1.5">
              {message.sources.map((source, idx) => {
                // Kiểm tra nếu là markdown link [text](url)
                const linkMatch = source.match(/\[([^\]]+)\]\(([^)]+)\)/);
                if (linkMatch) {
                  return (
                    <a
                      key={idx}
                      href={linkMatch[2]}
                      target="_blank"
                      rel="noopener noreferrer"
                      className="inline-flex items-center gap-1 px-2 py-1 bg-blue-50 border border-blue-200 rounded-full text-[11px] text-blue-600 hover:bg-blue-100 hover:border-blue-300 transition-colors"
                    >
                      {fileIcon(linkMatch[1])}
                      <span className="max-w-[200px] truncate">{shortenFilename(linkMatch[1])}</span>
                    </a>
                  );
                }
                // Trường hợp thường: tên file hoặc text snippet
                const isFilename = /\.(pdf|docx?|md|txt|pptx?)$/i.test(source);
                return (
                  <span
                    key={idx}
                    title={source}
                    className={`inline-flex items-center gap-1 px-2 py-1 rounded-full text-[11px] transition-colors ${
                      isFilename
                        ? 'bg-blue-50 border border-blue-200 text-blue-600'
                        : 'bg-gray-50 border border-gray-200 text-gray-500'
                    }`}
                  >
                    {fileIcon(source)}
                    <span className="max-w-[200px] truncate">{shortenFilename(source)}</span>
                  </span>
                );
              })}
            </div>
          </div>
        )}

        {/* Timestamp */}
        <div className={`text-[10px] mt-1.5 ${isUser ? 'text-blue-100' : 'text-gray-400'}`}>
          {message.timestamp.toLocaleTimeString('vi-VN', {
            hour: '2-digit',
            minute: '2-digit',
          })}
        </div>
      </div>
    </div>
  );
}
