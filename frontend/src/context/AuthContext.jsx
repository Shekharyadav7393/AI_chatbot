import { useState, useEffect } from 'react';
import api from '../api/axios';
import { toast } from 'react-hot-toast';
import { AuthContext } from './AuthContextCore';

export const AuthProvider = ({ children }) => {
  const [user, setUser] = useState(null);
  const [loading, setLoading] = useState(true);
  const [isAuthenticated, setIsAuthenticated] = useState(false);

  const fetchProfile = async () => {
    try {
      const { data } = await api.get('/users/profile');
      setUser(data.data);
      setIsAuthenticated(true);
    } catch {
      setUser(null);
      setIsAuthenticated(false);
      localStorage.removeItem('access_token');
      localStorage.removeItem('refresh_token');
    } finally {
      setLoading(false);
    }
  };

  useEffect(() => {
    const token = localStorage.getItem('access_token');
    if (token) {
      fetchProfile();
    } else {
      setLoading(false);
    }
  }, []);

  const login = async (email, password) => {
    try {
      const { data } = await api.post('/auth/login', { email, password });
      localStorage.setItem('access_token', data.data.access_token);
      localStorage.setItem('refresh_token', data.data.refresh_token);
      
      const profileRes = await api.get('/users/profile');
      const userProfile = profileRes.data.data;
      setUser(userProfile);
      setIsAuthenticated(true);
      setLoading(false);
      return userProfile;
    } catch (error) {
      toast.error(error.response?.data?.error?.message || 'Login failed');
      return null;
    }
  };

  const signup = async (email, username, password) => {
    try {
      const { data } = await api.post('/auth/signup', { email, username, password });
      localStorage.setItem('access_token', data.data.access_token);
      localStorage.setItem('refresh_token', data.data.refresh_token);
      await fetchProfile();
      return true;
    } catch (error) {
      toast.error(error.response?.data?.error?.message || 'Signup failed');
      return false;
    }
  };

  const logout = async () => {
    try {
      const refresh_token = localStorage.getItem('refresh_token');
      if (refresh_token) {
        await api.post('/auth/logout', { refresh_token });
      }
    } catch (error) {
      console.error('Logout error', error);
    } finally {
      localStorage.removeItem('access_token');
      localStorage.removeItem('refresh_token');
      setUser(null);
      setIsAuthenticated(false);
    }
  };

  return (
    <AuthContext.Provider value={{ user, loading, isAuthenticated, login, signup, logout, fetchProfile }}>
      {children}
    </AuthContext.Provider>
  );
};
