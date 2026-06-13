import { useState } from 'react';
import { ChatWindow } from './chat/ChatWindow';

export function TerraBotWidget() {
  const [isOpen, setIsOpen] = useState(false);

  return (
    <div className="fixed bottom-6 right-6 z-[100]">
      {/* Chat Window */}
      {isOpen && (
        <div className="absolute bottom-16 right-0 w-[380px] h-[600px] max-h-[80vh] bg-slate-900 border border-slate-700 shadow-2xl rounded-2xl overflow-hidden flex flex-col mb-4 transition-all animate-in slide-in-from-bottom-4">
          <div className="bg-gradient-to-r from-blue-600 to-indigo-600 px-4 py-3 flex justify-between items-center text-white">
            <div className="flex items-center gap-2">
              <span className="text-xl">🤖</span>
              <span className="font-semibold">TerraBot</span>
            </div>
            <button 
              onClick={() => setIsOpen(false)}
              className="text-white/80 hover:text-white transition-colors"
            >
              ✕
            </button>
          </div>
          <div className="flex-1 overflow-hidden">
            <ChatWindow />
          </div>
        </div>
      )}

      {/* Floating Action Button */}
      <button
        onClick={() => setIsOpen(!isOpen)}
        className="w-14 h-14 bg-blue-600 hover:bg-blue-500 text-white rounded-full shadow-lg hover:shadow-blue-500/50 flex items-center justify-center text-2xl transition-all transform hover:scale-105 active:scale-95"
        title="Trò chuyện với TerraBot"
      >
        {isOpen ? '✕' : '💬'}
      </button>
    </div>
  );
}
