import React, { useState } from 'react';
import { HiOutlineUser } from 'react-icons/hi2';
import { HiOutlineMail } from 'react-icons/hi';
import useAuth from '../hooks/useAuth';
import api from '../api/axios';
import { toast } from 'react-hot-toast';
import { formatDate } from '../utils/helpers';

const Profile = () => {
  const { user, fetchProfile } = useAuth();
  const [username, setUsername] = useState(user?.username || '');
  const [email, setEmail] = useState(user?.email || '');
  const [isSubmitting, setIsSubmitting] = useState(false);

  const handleSubmit = async (e) => {
    e.preventDefault();
    setIsSubmitting(true);
    try {
      await api.put('/users/profile', { username, email });
      toast.success('Profile updated successfully');
      await fetchProfile(); // refresh user data
    } catch (error) {
      toast.error(error.response?.data?.error?.message || 'Update failed');
    } finally {
      setIsSubmitting(false);
    }
  };

  return (
    <div className="p-6 md:p-8 max-w-3xl mx-auto w-full">
      <div className="mb-8">
        <h1 className="text-3xl font-bold text-white mb-2">My Profile</h1>
        <p className="text-slate-400">Manage your personal information</p>
      </div>

      <div className="bg-slate-800/50 border border-slate-700/50 rounded-2xl overflow-hidden backdrop-blur-xl">
        <div className="p-8 border-b border-slate-700/50 bg-slate-800/30 flex items-center gap-6">
          <div className="w-24 h-24 rounded-full bg-gradient-to-br from-brand-500 to-purple-600 flex items-center justify-center text-4xl font-bold text-white shadow-xl shadow-brand-500/20 border-4 border-slate-800">
            {user?.username?.charAt(0).toUpperCase()}
          </div>
          <div>
            <h2 className="text-2xl font-bold text-white">{user?.username}</h2>
            <div className="flex items-center gap-3 mt-2">
              <span className="px-3 py-1 bg-brand-500/10 text-brand-400 text-xs font-semibold rounded-full border border-brand-500/20 uppercase tracking-wider">
                {user?.role}
              </span>
              <span className="text-slate-400 text-sm">
                Joined {formatDate(user?.created_at)}
              </span>
            </div>
          </div>
        </div>

        <div className="p-8">
          <form onSubmit={handleSubmit} className="space-y-6">
            <div className="grid grid-cols-1 md:grid-cols-2 gap-6">
              <div>
                <label className="block text-sm font-medium text-slate-300 mb-2">Username</label>
                <div className="relative">
                  <div className="absolute inset-y-0 left-0 pl-3 flex items-center pointer-events-none">
                    <HiOutlineUser className="w-5 h-5 text-slate-500" />
                  </div>
                  <input
                    type="text"
                    value={username}
                    onChange={(e) => setUsername(e.target.value)}
                    className="w-full pl-10 pr-4 py-3 bg-slate-900/50 border border-slate-700/50 focus:border-brand-500 focus:ring-1 focus:ring-brand-500 transition-all text-slate-100 rounded-xl"
                  />
                </div>
              </div>
              
              <div>
                <label className="block text-sm font-medium text-slate-300 mb-2">Email Address</label>
                <div className="relative">
                  <div className="absolute inset-y-0 left-0 pl-3 flex items-center pointer-events-none">
                    <HiOutlineMail className="w-5 h-5 text-slate-500" />
                  </div>
                  <input
                    type="email"
                    value={email}
                    onChange={(e) => setEmail(e.target.value)}
                    className="w-full pl-10 pr-4 py-3 bg-slate-900/50 border border-slate-700/50 focus:border-brand-500 focus:ring-1 focus:ring-brand-500 transition-all text-slate-100 rounded-xl"
                  />
                </div>
              </div>
            </div>

            <div className="pt-4 flex justify-end">
              <button
                type="submit"
                disabled={isSubmitting || (username === user?.username && email === user?.email)}
                className="px-6 py-2.5 bg-brand-600 hover:bg-brand-500 text-white rounded-xl font-medium transition-all shadow-lg disabled:opacity-50 disabled:cursor-not-allowed flex items-center gap-2"
              >
                {isSubmitting && <div className="w-4 h-4 border-2 border-white/30 border-t-white rounded-full animate-spin"></div>}
                Save Changes
              </button>
            </div>
          </form>
        </div>
      </div>
    </div>
  );
};

export default Profile;
