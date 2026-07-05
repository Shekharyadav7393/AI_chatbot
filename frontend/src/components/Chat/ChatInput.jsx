import React, { useState, useRef, useEffect } from 'react';
import { HiPaperAirplane } from 'react-icons/hi2';

const ChatInput = ({ onSend, disabled }) => {
  const [message, setMessage] = useState('');
  const textareaRef = useRef(null);

  const adjustHeight = () => {
    const textarea = textareaRef.current;
    if (textarea) {
      textarea.style.height = 'auto';
      textarea.style.height = `${Math.min(textarea.scrollHeight, 150)}px`;
    }
  };

  useEffect(() => {
    adjustHeight();
  }, [message]);

  const handleKeyDown = (e) => {
    if (e.key === 'Enter' && !e.shiftKey) {
      e.preventDefault();
      handleSend();
    }
  };

  const handleSend = () => {
    const trimmed = message.trim();
    if (trimmed && !disabled) {
      onSend(trimmed);
      setMessage('');
      if (textareaRef.current) {
        textareaRef.current.style.height = 'auto';
      }
    }
  };

  return (
    <div className="relative p-6 bg-gradient-to-t from-[#0a0a1a] via-[#0a0a1a]/95 to-transparent z-20">
      <div className="max-w-4xl mx-auto relative">
        {/* Glow effect around input on focus */}
        <div className="absolute -inset-0.5 bg-gradient-to-r from-brand-500 to-purple-600 rounded-2xl blur opacity-15 group-focus-within:opacity-30 transition duration-1000 group"></div>
        
        <div className="relative flex items-end gap-2 bg-slate-900/80 backdrop-blur-xl border border-slate-700/40 rounded-2xl p-2.5 shadow-2xl focus-within:border-brand-500/60 focus-within:ring-1 focus-within:ring-brand-500/50 transition-all duration-300">
          <textarea
            ref={textareaRef}
            value={message}
            onChange={(e) => setMessage(e.target.value)}
            onKeyDown={handleKeyDown}
            disabled={disabled}
            placeholder={disabled ? "AI is typing..." : "Ask me anything (general queries or about documents)..."}
            className="w-full max-h-[150px] bg-transparent text-slate-100 placeholder-slate-500 px-3 py-2 resize-none outline-none overflow-y-auto text-sm leading-relaxed"
            rows={1}
          />
          
          <button
            onClick={handleSend}
            disabled={!message.trim() || disabled}
            className="p-3 rounded-xl bg-gradient-to-r from-brand-600 to-indigo-600 hover:from-brand-500 hover:to-indigo-500 text-white disabled:opacity-40 disabled:pointer-events-none transition-all duration-300 shadow-lg shadow-brand-500/20 flex-shrink-0 mb-0.5 active:scale-95"
          >
            <HiPaperAirplane className="w-5 h-5 -rotate-45 ml-0.5" />
          </button>
        </div>
      </div>
      <div className="text-center mt-3">
        <p className="text-[10px] text-slate-500 font-medium tracking-wide uppercase">
          AI can make mistakes. Verify important info from source documents.
        </p>
      </div>
    </div>
  );
};

export default ChatInput;
