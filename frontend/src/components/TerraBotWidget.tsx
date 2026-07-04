import { useState, useEffect, useCallback } from 'react';
import { ChatWindow } from './chat/ChatWindow';
import { useLanguage } from '../context/LanguageContext';

/**
 * TerraBot Chat Widget
 *
 * Hai chế độ:
 *  - normal   → floating panel góc dưới phải, kích thước clamp theo viewport
 *  - expanded → modal overlay chiếm phần lớn màn hình, có backdrop blur
 *
 * Không có pixel cứng; mọi kích thước đều dùng CSS clamp() / viewport units.
 */

type ChatMode = 'normal' | 'expanded';

export function TerraBotWidget() {
  const [isOpen,  setIsOpen]  = useState(false);
  const [mode,    setMode]    = useState<ChatMode>('normal');
  const { t } = useLanguage();

  const isExpanded = mode === 'expanded';

  const toggleMode = () => setMode(m => m === 'normal' ? 'expanded' : 'normal');

  // Đóng expanded khi nhấn Escape
  const handleKeyDown = useCallback((e: KeyboardEvent) => {
    if (e.key === 'Escape') {
      if (isExpanded) { setMode('normal'); }
      else            { setIsOpen(false);  }
    }
  }, [isExpanded]);

  useEffect(() => {
    document.addEventListener('keydown', handleKeyDown);
    return () => document.removeEventListener('keydown', handleKeyDown);
  }, [handleKeyDown]);

  // Ngăn scroll body khi expanded
  useEffect(() => {
    document.body.style.overflow = (isOpen && isExpanded) ? 'hidden' : '';
    return () => { document.body.style.overflow = ''; };
  }, [isOpen, isExpanded]);

  return (
    <>
      {/* ────────────────────────────────────────────
          BACKDROP — Chỉ hiện khi expanded
      ──────────────────────────────────────────── */}
      {isOpen && isExpanded && (
        <div
          className="fixed inset-0 z-[200] bg-black/50 backdrop-blur-sm animate-in fade-in duration-200"
          onClick={() => setMode('normal')}
          aria-hidden="true"
        />
      )}

      {/* ────────────────────────────────────────────
          MAIN CHAT BOX — Duy trì một <ChatWindow /> duy nhất
          để không bị reset state (messages/scroll) khi đổi mode
      ──────────────────────────────────────────── */}
      {isOpen && (
        <div
          role={isExpanded ? 'dialog' : undefined}
          aria-modal={isExpanded ? 'true' : undefined}
          aria-label="TerraBot Chat"
          className={`
            fixed flex flex-col bg-slate-900 border border-slate-700/60 rounded-2xl overflow-hidden
            transition-all duration-300 ease-in-out
            ${
              isExpanded
                ? 'z-[201] inset-3 sm:inset-6 md:inset-10 lg:inset-16 shadow-[0_32px_80px_-8px_rgba(0,0,0,0.7)] animate-in zoom-in-95 fade-in duration-200'
                : 'z-[100] bottom-[5.5rem] right-4 sm:right-6 shadow-2xl shadow-black/40 animate-in slide-in-from-bottom-4 fade-in duration-200'
            }
          `}
          style={
            isExpanded
              ? undefined
              : {
                  width: 'clamp(320px, calc(100vw - 2rem), 420px)',
                  height: 'clamp(380px, calc(100vh - 9rem), 600px)',
                }
          }
        >
          <ChatHeader
            mode={mode}
            onToggleMode={toggleMode}
            onClose={() => { setIsOpen(false); setMode('normal'); }}
          />
          <div className="flex-1 overflow-hidden">
            <ChatWindow />
          </div>
        </div>
      )}

      {/* ────────────────────────────────────────────
          FAB — Floating Action Button (luôn hiển thị)
      ──────────────────────────────────────────── */}
      <div className="fixed bottom-4 right-4 sm:bottom-6 sm:right-6 z-[202]">
        {/* Pulse ring khi chưa mở */}
        {!isOpen && (
          <span className="absolute inset-0 rounded-full bg-blue-500 opacity-30 animate-ping pointer-events-none" />
        )}
        <button
          onClick={() => setIsOpen(o => !o)}
          aria-label={isOpen ? t('bot.closeBot') : t('bot.openBot')}
          className={`
            relative w-14 h-14 rounded-full flex items-center justify-center text-2xl
            shadow-lg transition-all duration-200 transform
            hover:scale-110 active:scale-95 focus:outline-none focus-visible:ring-2 focus-visible:ring-blue-400
            ${isOpen
              ? 'bg-slate-700 hover:bg-slate-600 shadow-slate-600/40'
              : 'bg-blue-600 hover:bg-blue-500 shadow-blue-600/50 hover:shadow-blue-500/60'}
          `}
        >
          <span
            className={`transition-transform duration-300 ${isOpen ? 'rotate-45 scale-90' : 'rotate-0'}`}
          >
            {isOpen ? '✕' : '💬'}
          </span>
        </button>
      </div>
    </>
  );
}

/* ─────────────────────────────────────────────────────────────────
   Header component — dùng chung cho cả normal và expanded
───────────────────────────────────────────────────────────────── */
interface ChatHeaderProps {
  mode: ChatMode;
  onToggleMode: () => void;
  onClose: () => void;
}

function ChatHeader({ mode, onToggleMode, onClose }: ChatHeaderProps) {
  const isExpanded = mode === 'expanded';
  const { t } = useLanguage();

  return (
    <div className="
      bg-gradient-to-r from-blue-600 via-blue-600 to-indigo-600
      px-4 py-3 flex items-center justify-between
      text-white shrink-0 select-none
    ">
      {/* Left: Avatar + Info */}
      <div className="flex items-center gap-3">
        <div className="relative">
          <div className="w-9 h-9 bg-white/20 rounded-full flex items-center justify-center text-xl">
            🤖
          </div>
          {/* Online dot */}
          <span className="absolute -bottom-0.5 -right-0.5 w-3 h-3 bg-emerald-400 border-2 border-blue-600 rounded-full" />
        </div>
        <div>
          <p className="font-semibold text-sm leading-tight">{t('bot.title')}</p>
          <p className="text-[10px] text-blue-200 leading-tight">{t('bot.subtitle')}</p>
        </div>
      </div>

      {/* Right: Controls */}
      <div className="flex items-center gap-0.5">
        {/* Expand / Collapse */}
        <button
          onClick={onToggleMode}
          title={isExpanded ? t('bot.collapseTooltip') : t('bot.expandTooltip')}
          className="
            w-8 h-8 flex items-center justify-center rounded-lg
            text-white/70 hover:text-white hover:bg-white/15
            transition-all duration-150 text-sm
          "
        >
          {isExpanded ? (
            /* Thu nhỏ icon */
            <svg viewBox="0 0 20 20" fill="currentColor" className="w-4 h-4">
              <path d="M5 8a1 1 0 0 1 1-1h3V4a1 1 0 1 1 2 0v3h3a1 1 0 1 1 0 2h-3v3a1 1 0 1 1-2 0V9H6a1 1 0 0 1-1-1z"
                transform="rotate(45 10 10)" />
              <path fillRule="evenodd" clipRule="evenodd"
                d="M3 3a1 1 0 0 1 1-1h4a1 1 0 0 1 0 2H5.414l3.293 3.293a1 1 0 0 1-1.414 1.414L4 5.414V8a1 1 0 0 1-2 0V4a1 1 0 0 1 1-1zm14 0a1 1 0 0 0-1-1h-4a1 1 0 0 0 0 2h2.586l-3.293 3.293a1 1 0 0 0 1.414 1.414L16 5.414V8a1 1 0 0 0 2 0V4a1 1 0 0 0-1-1zM3 17a1 1 0 0 0 1 1h4a1 1 0 0 0 0-2H5.414l3.293-3.293a1 1 0 0 0-1.414-1.414L4 14.586V12a1 1 0 0 0-2 0v4zm14 0a1 1 0 0 1-1 1h-4a1 1 0 0 1 0-2h2.586l-3.293-3.293a1 1 0 0 1 1.414-1.414L16 14.586V12a1 1 0 0 1 2 0v4z" />
            </svg>
          ) : (
            /* Phóng to icon */
            <svg viewBox="0 0 20 20" fill="currentColor" className="w-4 h-4">
              <path fillRule="evenodd" clipRule="evenodd"
                d="M3 3a1 1 0 0 1 1-1h4a1 1 0 0 1 0 2H5.414l3.293 3.293a1 1 0 0 1-1.414 1.414L4 5.414V8a1 1 0 0 1-2 0V4a1 1 0 0 1 1-1zm14 0a1 1 0 0 0-1-1h-4a1 1 0 0 0 0 2h2.586l-3.293 3.293a1 1 0 0 0 1.414 1.414L16 5.414V8a1 1 0 0 0 2 0V4a1 1 0 0 0-1-1zM3 17a1 1 0 0 0 1 1h4a1 1 0 0 0 0-2H5.414l3.293-3.293a1 1 0 0 0-1.414-1.414L4 14.586V12a1 1 0 0 0-2 0v4zm14 0a1 1 0 0 1-1 1h-4a1 1 0 0 1 0-2h2.586l-3.293-3.293a1 1 0 0 1 1.414-1.414L16 14.586V12a1 1 0 0 1 2 0v4z" />
            </svg>
          )}
        </button>

        {/* Divider */}
        <div className="w-px h-5 bg-white/20 mx-1" />

        {/* Close */}
        <button
          onClick={onClose}
          title={t('bot.closeTooltip')}
          className="
            w-8 h-8 flex items-center justify-center rounded-lg
            text-white/70 hover:text-white hover:bg-red-500/30
            transition-all duration-150 text-base leading-none
          "
        >
          ✕
        </button>
      </div>
    </div>
  );
}
