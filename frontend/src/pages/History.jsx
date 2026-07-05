import React, { useEffect } from 'react';
import { useNavigate } from 'react-router-dom';
import { HiOutlineChatBubbleLeftRight, HiOutlineTrash, HiOutlineClock } from 'react-icons/hi2';
import useChat from '../hooks/useChat';
import { formatDate } from '../utils/helpers';
import LoadingSpinner from '../components/Common/LoadingSpinner';

const History = () => {
  const { chats, loading, getHistory, deleteChat, deleteAllHistory } = useChat();
  const navigate = useNavigate();

  useEffect(() => {
    getHistory();
  }, [getHistory]);

  return (
    <div className="p-6 md:p-8 max-w-5xl mx-auto w-full">
      <div className="flex items-center justify-between mb-8">
        <div>
          <h1 className="text-3xl font-bold text-white mb-2">Chat History</h1>
          <p className="text-slate-400">View and manage your previous conversations</p>
        </div>
        {chats.length > 0 && (
          <button
            onClick={() => {
              if (window.confirm('Are you sure you want to delete all chat history?')) {
                deleteAllHistory();
              }
            }}
            className="flex items-center gap-2 px-4 py-2 bg-red-500/10 text-red-400 rounded-lg hover:bg-red-500/20 transition-colors border border-red-500/20"
          >
            <HiOutlineTrash className="w-5 h-5" />
            <span className="font-medium">Clear All</span>
          </button>
        )}
      </div>

      {loading ? (
        <LoadingSpinner />
      ) : chats.length === 0 ? (
        <div className="text-center py-20 bg-slate-800/30 rounded-2xl border border-slate-700/50 border-dashed">
          <HiOutlineClock className="w-12 h-12 text-slate-500 mx-auto mb-4" />
          <h3 className="text-xl font-medium text-slate-300 mb-2">No history found</h3>
          <p className="text-slate-500 mb-6">You haven't started any conversations yet.</p>
          <button
            onClick={() => navigate('/chat')}
            className="px-6 py-2.5 bg-brand-600 hover:bg-brand-500 text-white rounded-xl transition-colors font-medium shadow-lg"
          >
            Start a New Chat
          </button>
        </div>
      ) : (
        <div className="grid gap-4 md:grid-cols-2 lg:grid-cols-3">
          {chats.map((chat) => (
            <div 
              key={chat.id}
              className="bg-slate-800/50 border border-slate-700/50 rounded-2xl p-5 hover:border-brand-500/50 hover:bg-slate-800 transition-all cursor-pointer group flex flex-col"
              onClick={() => navigate(`/chat?id=${chat.id}`)}
            >
              <div className="flex items-start justify-between mb-4">
                <div className="w-10 h-10 rounded-xl bg-brand-500/10 text-brand-400 flex items-center justify-center border border-brand-500/20">
                  <HiOutlineChatBubbleLeftRight className="w-5 h-5" />
                </div>
                <button
                  onClick={(e) => {
                    e.stopPropagation();
                    if (window.confirm('Delete this chat?')) {
                      deleteChat(chat.id);
                    }
                  }}
                  className="p-2 text-slate-500 hover:text-red-400 hover:bg-slate-700/50 rounded-lg transition-colors opacity-0 group-hover:opacity-100"
                  title="Delete chat"
                >
                  <HiOutlineTrash className="w-5 h-5" />
                </button>
              </div>
              
              <h3 className="text-lg font-semibold text-slate-200 mb-2 line-clamp-2 flex-1">
                {chat.title}
              </h3>
              
              <div className="flex items-center justify-between text-xs text-slate-500 mt-auto pt-4 border-t border-slate-700/50">
                <span>{formatDate(chat.updated_at)}</span>
              </div>
            </div>
          ))}
        </div>
      )}
    </div>
  );
};

export default History;
