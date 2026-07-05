import React, { useEffect, useRef } from 'react';
import MessageBubble from './MessageBubble';
import { HiOutlineChatBubbleBottomCenterText, HiOutlineSparkles, HiOutlineDocumentText } from 'react-icons/hi2';

const ChatWindow = ({ messages, loading }) => {
  const bottomRef = useRef(null);

  useEffect(() => {
    bottomRef.current?.scrollIntoView({ behavior: 'smooth' });
  }, [messages, loading]);

  if (!messages || messages.length === 0) {
    return (
      <div className="flex-1 flex flex-col items-center justify-center p-8 text-center relative overflow-hidden">
        {/* Decorative background glow for empty state */}
        <div className="absolute top-1/2 left-1/2 -translate-x-1/2 -translate-y-1/2 w-64 h-64 bg-brand-500/10 rounded-full blur-[80px] pointer-events-none"></div>
        
        <div className="relative z-10 flex flex-col items-center max-w-lg">
          <div className="w-20 h-20 bg-gradient-to-tr from-brand-600/30 via-indigo-600/20 to-purple-600/30 rounded-2xl flex items-center justify-center border border-brand-500/30 mb-6 shadow-2xl shadow-brand-500/10 relative group hover:scale-105 transition-transform duration-300">
            <div className="absolute inset-0 bg-brand-500/20 rounded-2xl blur-md opacity-50 group-hover:opacity-100 transition-opacity"></div>
            <HiOutlineSparkles className="w-10 h-10 text-brand-400 relative z-10 animate-pulse" />
          </div>
          
          <h3 className="text-3xl font-extrabold bg-clip-text text-transparent bg-gradient-to-r from-white via-slate-100 to-slate-300 tracking-tight mb-3">
            Ask Me Anything
          </h3>
          
          <p className="text-slate-400 text-sm md:text-base leading-relaxed mb-8 max-w-md">
            I am your personal AI Assistant. Ask general questions or inquire details about your uploaded company knowledge base.
          </p>

          {/* Prompt suggestions / Quick chips */}
          <div className="grid grid-cols-1 sm:grid-cols-2 gap-3 w-full max-w-md">
            <div className="p-3 bg-slate-850/40 hover:bg-slate-800/70 border border-slate-700/30 hover:border-brand-500/30 rounded-xl text-left text-xs text-slate-300 cursor-pointer transition-all duration-300 flex items-center gap-3">
              <div className="p-1.5 bg-brand-500/10 text-brand-400 rounded-lg"><HiOutlineSparkles className="w-4 h-4" /></div>
              <span>"What is Python and why is it popular?"</span>
            </div>
            <div className="p-3 bg-slate-850/40 hover:bg-slate-800/70 border border-slate-700/30 hover:border-brand-500/30 rounded-xl text-left text-xs text-slate-300 cursor-pointer transition-all duration-300 flex items-center gap-3">
              <div className="p-1.5 bg-indigo-500/10 text-indigo-400 rounded-lg"><HiOutlineDocumentText className="w-4 h-4" /></div>
              <span>"Summarize our company policies"</span>
            </div>
          </div>
        </div>
      </div>
    );
  }

  return (
    <div className="flex-1 overflow-y-auto p-4 md:p-6 scroll-smooth">
      <div className="max-w-4xl mx-auto flex flex-col">
        {messages.map((msg) => (
          <MessageBubble 
            key={msg.id} 
            message={msg} 
            onFeedback={(id, rating) => console.log('Feedback', id, rating)} 
          />
        ))}
        
        {loading && (
          <div className="flex w-full mb-6 justify-start animate-fade-in">
            <div className="flex items-end gap-3">
              <div className="w-8 h-8 rounded-full bg-slate-800 border border-slate-700/50 flex items-center justify-center shadow-lg">
                <span className="text-xs font-bold text-brand-400 animate-pulse">AI</span>
              </div>
              <div className="bg-slate-800/90 backdrop-blur-md border border-slate-700/30 px-5 py-4 rounded-2xl rounded-bl-sm shadow-xl">
                <div className="flex gap-2">
                  <div className="w-2.5 h-2.5 rounded-full bg-brand-500 animate-bounce" style={{ animationDelay: '0ms' }}></div>
                  <div className="w-2.5 h-2.5 rounded-full bg-indigo-400 animate-bounce" style={{ animationDelay: '150ms' }}></div>
                  <div className="w-2.5 h-2.5 rounded-full bg-purple-400 animate-bounce" style={{ animationDelay: '300ms' }}></div>
                </div>
              </div>
            </div>
          </div>
        )}
        <div ref={bottomRef} className="h-4" />
      </div>
    </div>
  );
};

export default ChatWindow;
