import React from 'react';
import { HiOutlineHandThumbUp, HiOutlineHandThumbDown, HiOutlineDocumentText } from 'react-icons/hi2';

const MessageBubble = ({ message, onFeedback }) => {
  const isUser = message.role === 'user';
  
  const formatTime = (dateStr) => {
    if (!dateStr) return 'Just now';
    return new Date(dateStr).toLocaleTimeString('en-US', {
      hour: '2-digit',
      minute: '2-digit',
      hour12: false,
    });
  };
  
  // Custom markdown bold/italic/code block parsing for text
  const formatText = (text) => {
    if (!text) return null;
    
    // Split by code blocks first
    const codeParts = text.split(/(```[\s\S]*?```)/g);
    
    return codeParts.map((part, index) => {
      if (part.startsWith('```') && part.endsWith('```')) {
        // Extract language and code content
        const lines = part.slice(3, -3).trim().split('\n');
        let language = 'code';
        let code = lines.join('\n');
        
        if (lines[0] && lines[0].length < 15 && !lines[0].includes(' ') && lines.length > 1) {
          language = lines[0];
          code = lines.slice(1).join('\n');
        }
        
        return (
          <div key={index} className="my-3 rounded-lg overflow-hidden border border-slate-700/40 bg-slate-950/60 font-mono text-xs shadow-inner">
            <div className="flex justify-between items-center px-4 py-1.5 bg-slate-900/80 text-slate-400 text-[10px] uppercase font-bold tracking-wider border-b border-slate-800/60">
              <span>{language}</span>
            </div>
            <pre className="p-4 overflow-x-auto text-slate-300 leading-relaxed">
              <code>{code}</code>
            </pre>
          </div>
        );
      }
      
      // Otherwise, parse inline elements (bold/inline code)
      const inlineParts = part.split(/(\*\*.*?\*\*|`.*?`)/g);
      return inlineParts.map((inlinePart, i) => {
        if (inlinePart.startsWith('**') && inlinePart.endsWith('**')) {
          return <strong key={i} className="text-white font-extrabold">{inlinePart.slice(2, -2)}</strong>;
        }
        if (inlinePart.startsWith('`') && inlinePart.endsWith('`')) {
          return <code key={i} className="px-1.5 py-0.5 rounded bg-slate-900/80 border border-slate-800 text-brand-400 font-mono text-xs">{inlinePart.slice(1, -1)}</code>;
        }
        return <span key={i}>{inlinePart}</span>;
      });
    });
  };

  return (
    <div className={`flex w-full mb-6 ${isUser ? 'justify-end' : 'justify-start'} group/bubble animate-fade-in`}>
      <div className={`flex max-w-[85%] md:max-w-[75%] ${isUser ? 'flex-row-reverse' : 'flex-row'} gap-3.5 items-start`}>
        
        {/* Avatar */}
        <div className={`w-9 h-9 rounded-full flex-shrink-0 flex items-center justify-center shadow-md border transition-transform duration-300 group-hover/bubble:scale-105
          ${isUser 
            ? 'bg-gradient-to-br from-brand-500 to-indigo-600 border-brand-400/20 text-white font-bold' 
            : 'bg-slate-900/90 border-slate-700/60 text-brand-400'
          }`}
        >
          {isUser ? <span className="text-xs">U</span> : <span className="text-xs font-black tracking-tighter">AI</span>}
        </div>

        {/* Message Content Bubble */}
        <div className={`relative px-5 py-4 shadow-2xl transition-all duration-300 ${
          isUser 
            ? 'bg-gradient-to-br from-brand-600 via-brand-600 to-indigo-600 hover:to-indigo-500 text-white rounded-2xl rounded-tr-sm border border-brand-400/20' 
            : 'bg-slate-850/80 backdrop-blur-xl border border-slate-700/40 text-slate-200 rounded-2xl rounded-tl-sm hover:border-slate-600/40'
        }`}>
          <div className="prose prose-invert max-w-none text-sm md:text-[14.5px] leading-relaxed break-words whitespace-pre-wrap">
            {formatText(message.content)}
          </div>
          
          <div className={`text-[10px] mt-2.5 flex items-center gap-2 ${isUser ? 'text-brand-100/70 justify-end' : 'text-slate-500'}`}>
            <span>{formatTime(message.created_at)}</span>
          </div>

          {/* Sources list */}
          {!isUser && message.sources && message.sources.length > 0 && (
            <div className="mt-4 pt-3 border-t border-slate-700/40">
              <p className="text-[11px] text-slate-400 mb-2 font-semibold uppercase tracking-wider">Sources:</p>
              <div className="flex flex-wrap gap-2">
                {message.sources.map((source, idx) => (
                  <div key={idx} className="flex items-center gap-1.5 px-2.5 py-1 bg-slate-900/60 hover:bg-slate-900/80 rounded-md border border-slate-800 text-[11px] text-slate-300 transition-colors">
                    <HiOutlineDocumentText className="w-3.5 h-3.5 text-brand-400" />
                    <span className="truncate max-w-[150px]" title={source.document}>{source.document}</span>
                  </div>
                ))}
              </div>
            </div>
          )}

          {/* Feedback buttons (Only on hover, side of bubble) */}
          {!isUser && (
            <div className="absolute left-full top-1/2 -translate-y-1/2 ml-3 flex items-center gap-1.5 opacity-0 group-hover/bubble:opacity-100 transition-opacity duration-300">
              <button 
                onClick={() => onFeedback && onFeedback(message.id, 5)}
                className="p-1.5 bg-slate-900/90 hover:bg-slate-800 text-slate-400 hover:text-emerald-400 rounded-lg border border-slate-700/50 transition-colors shadow-lg"
                title="Helpful"
              >
                <HiOutlineHandThumbUp className="w-3.5 h-3.5" />
              </button>
              <button 
                onClick={() => onFeedback && onFeedback(message.id, 1)}
                className="p-1.5 bg-slate-900/90 hover:bg-slate-800 text-slate-400 hover:text-rose-400 rounded-lg border border-slate-700/50 transition-colors shadow-lg"
                title="Not helpful"
              >
                <HiOutlineHandThumbDown className="w-3.5 h-3.5" />
              </button>
            </div>
          )}
        </div>
      </div>
    </div>
  );
};

export default MessageBubble;
