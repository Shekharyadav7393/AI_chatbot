import { useState, useCallback } from 'react';
import api from '../api/axios';
import { toast } from 'react-hot-toast';

const useChat = () => {
  const [messages, setMessages] = useState([]);
  const [chats, setChats] = useState([]);
  const [currentChatId, setCurrentChatId] = useState(null);
  const [loading, setLoading] = useState(false);

  const sendMessage = async (message, chatId = null) => {
    const tempId = 'temp-' + Date.now();
    const userMsg = {
      id: tempId,
      role: 'user',
      content: message,
      created_at: new Date().toISOString()
    };
    
    // Optimistic UI update
    setMessages(prev => [...prev, userMsg]);
    setLoading(true);
    
    try {
      const { data } = await api.post('/chat', { message, chat_id: chatId });
      const { chat_id, message: assistantMsg } = data.data;
      
      setCurrentChatId(chat_id);
      
      setMessages(prev => [...prev, assistantMsg]);
      return chat_id;
    } catch {
      setMessages(prev => prev.filter(m => m.id !== tempId));
      toast.error('Failed to send message');
      return null;
    } finally {
      setLoading(false);
    }
  };

  const getHistory = useCallback(async (skip = 0, limit = 20) => {
    setLoading(true);
    try {
      const { data } = await api.get(`/chat/history?skip=${skip}&limit=${limit}`);
      setChats(data.data.chats);
    } catch {
      toast.error('Failed to load chat history');
    } finally {
      setLoading(false);
    }
  }, []);

  const getChatDetail = useCallback(async (chatId) => {
    setLoading(true);
    try {
      const { data } = await api.get(`/chat/${chatId}`);
      setCurrentChatId(data.data.id);
      setMessages(data.data.messages);
    } catch {
      toast.error('Failed to load chat');
    } finally {
      setLoading(false);
    }
  }, []);

  const deleteChat = async (chatId) => {
    try {
      await api.delete(`/chat/${chatId}`);
      setChats(prev => prev.filter(c => c.id !== chatId));
      if (currentChatId === chatId) {
        setCurrentChatId(null);
        setMessages([]);
      }
      toast.success('Chat deleted');
    } catch {
      toast.error('Failed to delete chat');
    }
  };

  const deleteAllHistory = async () => {
    try {
      await api.delete('/chat/history/all');
      setChats([]);
      setCurrentChatId(null);
      setMessages([]);
      toast.success('All history deleted');
    } catch {
      toast.error('Failed to delete history');
    }
  };

  return {
    messages,
    chats,
    currentChatId,
    setCurrentChatId,
    setMessages,
    loading,
    sendMessage,
    getHistory,
    getChatDetail,
    deleteChat,
    deleteAllHistory
  };
};

export default useChat;
