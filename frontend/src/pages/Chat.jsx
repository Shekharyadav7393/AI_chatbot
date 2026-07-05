import React, { useEffect, useState } from 'react';
import { useLocation, useNavigate } from 'react-router-dom';
import useChat from '../hooks/useChat';
import ChatWindow from '../components/Chat/ChatWindow';
import ChatInput from '../components/Chat/ChatInput';

const Chat = () => {
  const { messages, loading, sendMessage, getChatDetail, setCurrentChatId, setMessages } = useChat();
  const location = useLocation();
  const navigate = useNavigate();
  const [initDone, setInitDone] = useState(false);

  useEffect(() => {
    const params = new URLSearchParams(location.search);
    const chatId = params.get('id');

    if (chatId) {
      getChatDetail(chatId).finally(() => setInitDone(true));
    } else {
      setCurrentChatId(null);
      setMessages([]);
      setInitDone(true);
    }
  }, [location.search, getChatDetail, setCurrentChatId, setMessages]);

  const handleSend = async (message) => {
    const params = new URLSearchParams(location.search);
    const chatId = params.get('id');
    const newChatId = await sendMessage(message, chatId);
    
    // If it was a new chat, update URL without reloading
    if (!chatId && newChatId) {
      navigate(`/chat?id=${newChatId}`, { replace: true });
    }
  };

  if (!initDone) return null;

  return (
    <div className="flex flex-col h-full bg-transparent">
      <ChatWindow messages={messages} loading={loading} />
      <ChatInput onSend={handleSend} disabled={loading} />
    </div>
  );
};

export default Chat;
