import { useState, KeyboardEvent } from 'react';
import { useLanguage } from '../../context/LanguageContext';

interface ChatInputProps {
  onSend: (message: string) => void;
  disabled?: boolean;
}

export function ChatInput({ onSend, disabled }: ChatInputProps) {
  const [message, setMessage] = useState('');
  const { t } = useLanguage();

  const handleSend = () => {
    if (message.trim() && !disabled) {
      onSend(message.trim());
      setMessage('');
    }
  };

  const handleKeyPress = (e: KeyboardEvent) => {
    if (e.key === 'Enter' && !e.shiftKey) {
      e.preventDefault();
      handleSend();
    }
  };

  return (
    <div className="flex items-end gap-2 p-3 bg-white border-t border-slate-200/90">
      <textarea
        value={message}
        onChange={(e) => setMessage(e.target.value)}
        onKeyPress={handleKeyPress}
        placeholder={t('bot.placeholder')}
        disabled={disabled}
        rows={1}
        className="
          flex-1 resize-none rounded-xl
          bg-slate-50 border border-slate-200
          px-4 py-2.5 text-sm text-slate-900 placeholder-slate-400
          focus:outline-none focus:ring-2 focus:ring-blue-500 focus:border-transparent
          max-h-32 min-h-[42px] transition-colors font-medium
        "
      />
      <button
        onClick={handleSend}
        disabled={disabled || !message.trim()}
        className={`
          p-2.5 rounded-xl transition-all shrink-0
          ${disabled || !message.trim()
            ? 'bg-slate-100 text-slate-400 cursor-not-allowed border border-slate-200'
            : 'bg-blue-600 hover:bg-blue-700 text-white shadow-md shadow-blue-500/20 hover:scale-105 active:scale-95'}
        `}
        aria-label={t('bot.send')}
        title={t('bot.send')}
      >
        <svg className="w-5 h-5" fill="none" stroke="currentColor" viewBox="0 0 24 24">
          <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2}
            d="M12 19l9 2-9-18-9 18 9-2zm0 0v-8" />
        </svg>
      </button>
    </div>
  );
}



