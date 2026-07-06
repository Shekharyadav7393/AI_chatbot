import React, { useEffect, useState } from 'react';
import { useLocation, useNavigate } from 'react-router-dom';
import { HiOutlineUser, HiOutlineMail } from 'react-icons/hi2';
import { toast } from 'react-hot-toast';
import useChat from '../hooks/useChat';
import useAuth from '../hooks/useAuth';
import ChatWindow from '../components/Chat/ChatWindow';
import ChatInput from '../components/Chat/ChatInput';
import LoadingSpinner from '../components/Common/LoadingSpinner';

const Chat = () => {
  const { messages, loading, sendMessage, getChatDetail, setCurrentChatId, setMessages } = useChat();
  const { isAuthenticated, signup, login } = useAuth();
  const location = useLocation();
  const navigate = useNavigate();
  const [initDone, setInitDone] = useState(false);

  // Guest Form State
  const [guestName, setGuestName] = useState('');
  const [guestEmail, setGuestEmail] = useState('');
  const [guestLoading, setGuestLoading] = useState(false);

  useEffect(() => {
    const params = new URLSearchParams(location.search);
    const chatId = params.get('id');

    if (chatId && isAuthenticated) {
      getChatDetail(chatId).finally(() => setInitDone(true));
    } else {
      setCurrentChatId(null);
      setMessages([]);
      setInitDone(true);
    }
  }, [location.search, getChatDetail, setCurrentChatId, setMessages, isAuthenticated]);

  const handleSend = async (message) => {
    const params = new URLSearchParams(location.search);
    const chatId = params.get('id');
    const newChatId = await sendMessage(message, chatId);
    
    // If it was a new chat, update URL without reloading
    if (!chatId && newChatId) {
      navigate(`/chat?id=${newChatId}`, { replace: true });
    }
  };

  const handleStartChat = async (e) => {
    e.preventDefault();
    if (!guestName.trim() || !guestEmail.trim()) return;

    setGuestLoading(true);
    const defaultPassword = "GuestPassword123!";
    
    // Try to register new guest
    const success = await signup(guestEmail, guestName, defaultPassword);
    if (success) {
      toast.success(`Welcome ${guestName}!`);
    } else {
      // If fails (already registered), try silent login
      const loginSuccess = await login(guestEmail, defaultPassword);
      if (loginSuccess) {
        toast.success(`Welcome back ${guestName}!`);
      } else {
        toast.error("This email is registered with a password. Please click 'Sign In' at the top right.");
      }
    }
    setGuestLoading(false);
  };

  if (!initDone) return null;

  if (!isAuthenticated) {
    return (
      <div className="flex-1 flex items-center justify-center p-6 relative">
        <div className="w-full max-w-md p-8 glass-panel rounded-2xl relative overflow-hidden z-10">
          <div className="absolute top-0 inset-x-0 h-1 bg-gradient-to-r from-brand-500 to-purple-500"></div>
          <div className="text-center mb-6">
            <h2 className="text-2xl font-bold text-white mb-2">Start Conversation</h2>
            <p className="text-sm text-slate-400">Enter your details to connect with our support assistant.</p>
          </div>
          <form onSubmit={handleStartChat} className="space-y-4">
            <div>
              <label className="block text-sm font-medium text-slate-300 mb-1.5">Name</label>
              <div className="relative">
                <div className="absolute inset-y-0 left-0 pl-3 flex items-center pointer-events-none">
                  <HiOutlineUser className="h-5 w-5 text-slate-500" />
                </div>
                <input
                  type="text"
                  value={guestName}
                  onChange={(e) => setGuestName(e.target.value)}
                  className="w-full pl-10 pr-4 py-2.5 glass-input rounded-xl"
                  placeholder="John Doe"
                  required
                />
              </div>
            </div>
            <div>
              <label className="block text-sm font-medium text-slate-300 mb-1.5">Email Address</label>
              <div className="relative">
                <div className="absolute inset-y-0 left-0 pl-3 flex items-center pointer-events-none">
                  <HiOutlineMail className="h-5 w-5 text-slate-500" />
                </div>
                <input
                  type="email"
                  value={guestEmail}
                  onChange={(e) => setGuestEmail(e.target.value)}
                  className="w-full pl-10 pr-4 py-2.5 glass-input rounded-xl"
                  placeholder="john@example.com"
                  required
                />
              </div>
            </div>
            <button
              type="submit"
              disabled={guestLoading}
              className="w-full py-3 px-4 rounded-xl font-medium text-white bg-gradient-to-r from-brand-600 to-brand-500 hover:from-brand-500 hover:to-brand-400 focus:outline-none transition-all shadow-lg disabled:opacity-75 disabled:cursor-not-allowed flex justify-center items-center h-12"
            >
              {guestLoading ? <LoadingSpinner text="" /> : 'Start Chat'}
            </button>
          </form>
        </div>
      </div>
    );
  }

  return (
    <div className="flex flex-col h-full bg-transparent">
      <ChatWindow messages={messages} loading={loading} />
      <ChatInput onSend={handleSend} disabled={loading} />
    </div>
  );
};

export default Chat;
