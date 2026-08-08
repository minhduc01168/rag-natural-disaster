import React from 'react';

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

function renderInlineFormatting(text: string): React.ReactNode[] {
  const parts: React.ReactNode[] = [];
  const regex = /(\*\*.*?\*\*|__.*?__|`.*?`|\[.*?\]\(.*?\))/g;
  const tokens = text.split(regex);

  tokens.forEach((token, idx) => {
    if (!token) return;

    if ((token.startsWith('**') && token.endsWith('**')) || (token.startsWith('__') && token.endsWith('__'))) {
      const inner = token.slice(2, -2);
      parts.push(<strong key={idx} className="font-extrabold text-slate-900">{inner}</strong>);
    } else if (token.startsWith('`') && token.endsWith('`')) {
      const inner = token.slice(1, -1);
      parts.push(<code key={idx} className="bg-slate-100 text-blue-700 font-mono text-xs px-1.5 py-0.5 rounded border border-slate-200">{inner}</code>);
    } else if (token.startsWith('[') && token.includes('](') && token.endsWith(')')) {
      const match = token.match(/^\[(.*?)\]\((.*?)\)$/);
      if (match) {
        parts.push(
          <a key={idx} href={match[2]} target="_blank" rel="noopener noreferrer" className="text-blue-600 underline font-bold hover:text-blue-800">
            {match[1]}
          </a>
        );
      } else {
        parts.push(token);
      }
    } else {
      parts.push(token);
    }
  });

  return parts;
}

function FormattedMarkdown({ content, isUser }: { content: string; isUser: boolean }) {
  if (isUser) {
    return <div className="whitespace-pre-wrap text-sm leading-relaxed">{content}</div>;
  }

  const lines = content.split('\n');
  const blocks: React.ReactNode[] = [];
  let currentList: { type: 'ul' | 'ol'; items: string[] } | null = null;

  const flushList = (key: number) => {
    if (!currentList) return;
    if (currentList.type === 'ul') {
      blocks.push(
        <ul key={`list-${key}`} className="list-disc pl-5 my-1.5 space-y-1 text-slate-800 font-medium">
          {currentList.items.map((item, i) => (
            <li key={i}>{renderInlineFormatting(item)}</li>
          ))}
        </ul>
      );
    } else {
      blocks.push(
        <ol key={`list-${key}`} className="list-decimal pl-5 my-1.5 space-y-1 text-slate-800 font-medium">
          {currentList.items.map((item, i) => (
            <li key={i}>{renderInlineFormatting(item)}</li>
          ))}
        </ol>
      );
    }
    currentList = null;
  };

  lines.forEach((line, index) => {
    const trimmed = line.trim();

    if (trimmed.startsWith('#')) {
      flushList(index);
      const level = (trimmed.match(/^#+/) || ['#'])[0].length;
      const headingText = trimmed.replace(/^#+\s*/, '');
      blocks.push(
        <h4 key={index} className={`font-black text-slate-900 mt-2 mb-1 ${level <= 2 ? 'text-base' : 'text-sm'}`}>
          {renderInlineFormatting(headingText)}
        </h4>
      );
      return;
    }

    const bulletMatch = line.match(/^(\s*)([-*•])\s+(.*)$/);
    if (bulletMatch) {
      if (!currentList || currentList.type !== 'ul') {
        flushList(index);
        currentList = { type: 'ul', items: [] };
      }
      currentList.items.push(bulletMatch[3]);
      return;
    }

    const numberMatch = line.match(/^(\s*)(\d+)\.\s+(.*)$/);
    if (numberMatch) {
      if (!currentList || currentList.type !== 'ol') {
        flushList(index);
        currentList = { type: 'ol', items: [] };
      }
      currentList.items.push(numberMatch[3]);
      return;
    }

    flushList(index);
    if (trimmed === '') {
      blocks.push(<div key={index} className="h-1.5" />);
    } else {
      blocks.push(
        <p key={index} className="my-0.5 leading-relaxed text-slate-800 font-normal">
          {renderInlineFormatting(line)}
        </p>
      );
    }
  });

  flushList(lines.length);

  return <div className="text-sm leading-relaxed space-y-0.5">{blocks}</div>;
}

export function MessageBubble({ message }: MessageBubbleProps) {
  const isUser = message.sender === 'user';

  return (
    <div className={`flex ${isUser ? 'justify-end' : 'justify-start'} mb-3`}>
      <div
        className={`max-w-[85%] sm:max-w-[78%] rounded-2xl px-4 py-3 ${
          isUser
            ? 'bg-blue-600 text-white rounded-br-md shadow-sm'
            : 'bg-white text-slate-900 rounded-bl-md shadow-sm border border-slate-200/90'
        }`}
      >
        {/* Agent label */}
        {!isUser && message.agent && (
          <div className="text-[10px] font-bold text-blue-600 mb-1 uppercase tracking-wide">
            {message.agent}
          </div>
        )}

        {/* Message text */}
        <FormattedMarkdown content={message.text} isUser={isUser} />

        {/* Source citations */}
        {!isUser && message.sources && message.sources.length > 0 && (
          <div className="mt-3 pt-2.5 border-t border-slate-200/80">
            <p className="text-[10px] text-slate-500 uppercase tracking-wide mb-1.5 font-bold">
              📖 Nguồn tài liệu
            </p>
            <div className="flex flex-wrap gap-1.5">
              {message.sources.map((source, idx) => {
                const linkMatch = source.match(/\[([^\]]+)\]\(([^)]+)\)/);
                if (linkMatch) {
                  return (
                    <a
                      key={idx}
                      href={linkMatch[2]}
                      target="_blank"
                      rel="noopener noreferrer"
                      className="inline-flex items-center gap-1 px-2.5 py-1 bg-blue-50 border border-blue-200 rounded-full text-[11px] font-semibold text-blue-700 hover:bg-blue-100 hover:border-blue-300 transition-colors"
                    >
                      {fileIcon(linkMatch[1])}
                      <span className="max-w-[200px] truncate">{shortenFilename(linkMatch[1])}</span>
                    </a>
                  );
                }
                const isFilename = /\.(pdf|docx?|md|txt|pptx?)$/i.test(source);
                return (
                  <span
                    key={idx}
                    title={source}
                    className={`inline-flex items-center gap-1 px-2.5 py-1 rounded-full text-[11px] font-semibold transition-colors ${
                      isFilename
                        ? 'bg-blue-50 border border-blue-200 text-blue-700'
                        : 'bg-slate-100 border border-slate-200 text-slate-600'
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
        <div className={`text-[10px] mt-1.5 font-medium ${isUser ? 'text-blue-100' : 'text-slate-400'}`}>
          {message.timestamp.toLocaleTimeString('vi-VN', {
            hour: '2-digit',
            minute: '2-digit',
          })}
        </div>
      </div>
    </div>
  );
}

