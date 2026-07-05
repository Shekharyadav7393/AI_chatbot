import React, { useState, useEffect } from 'react';
import { HiOutlineUsers, HiOutlineTrash, HiOutlineUserCircle } from 'react-icons/hi2';
import api from '../api/axios';
import { formatDate } from '../utils/helpers';
import { toast } from 'react-hot-toast';
import LoadingSpinner from '../components/Common/LoadingSpinner';

const ManageUsers = () => {
  const [users, setUsers] = useState([]);
  const [loading, setLoading] = useState(true);

  const fetchUsers = async () => {
    try {
      const { data } = await api.get('/admin/users');
      setUsers(data.data.users);
    } catch {
      toast.error('Failed to load users list');
    } finally {
      setLoading(false);
    }
  };

  useEffect(() => {
    fetchUsers();
  }, []);

  const handleRoleChange = async (userId, currentRole) => {
    const newRole = currentRole === 'admin' ? 'user' : 'admin';
    try {
      await api.put(`/admin/users/${userId}`, { role: newRole });
      toast.success(`Role updated to ${newRole}`);
      fetchUsers();
    } catch (error) {
      toast.error(error.response?.data?.error?.message || 'Failed to update role');
    }
  };

  const handleStatusToggle = async (userId, currentStatus) => {
    try {
      await api.put(`/admin/users/${userId}`, { is_active: !currentStatus });
      toast.success(`User status updated`);
      fetchUsers();
    } catch (error) {
      toast.error(error.response?.data?.error?.message || 'Failed to update user status');
    }
  };

  const handleDeleteUser = async (userId) => {
    if (!window.confirm('Are you sure you want to delete this user? All their chat history will be lost.')) return;
    try {
      await api.delete(`/admin/users/${userId}`);
      toast.success('User deleted successfully');
      setUsers(prev => prev.filter(u => u.id !== userId));
    } catch {
      toast.error('Failed to delete user');
    }
  };

  return (
    <div className="p-6 md:p-8 max-w-6xl mx-auto w-full">
      <div className="mb-8">
        <h1 className="text-3xl font-bold text-white mb-2">Manage Users</h1>
        <p className="text-slate-400">View and manage registered accounts, roles, and status</p>
      </div>

      {loading ? (
        <LoadingSpinner />
      ) : users.length === 0 ? (
        <div className="text-center py-24 bg-slate-800/30 rounded-2xl border border-slate-700/50">
          <HiOutlineUsers className="w-16 h-16 text-slate-600 mx-auto mb-4" />
          <h3 className="text-xl font-medium text-slate-300">No users found</h3>
        </div>
      ) : (
        <div className="bg-slate-800/50 rounded-2xl border border-slate-700/50 overflow-hidden backdrop-blur-xl">
          <div className="overflow-x-auto">
            <table className="w-full text-left border-collapse">
              <thead>
                <tr className="bg-slate-900/50 border-b border-slate-700/50">
                  <th className="p-4 font-semibold text-slate-300">User Details</th>
                  <th className="p-4 font-semibold text-slate-300">Role</th>
                  <th className="p-4 font-semibold text-slate-300">Status</th>
                  <th className="p-4 font-semibold text-slate-300 hidden sm:table-cell">Joined</th>
                  <th className="p-4 font-semibold text-slate-300 text-right">Actions</th>
                </tr>
              </thead>
              <tbody className="divide-y divide-slate-700/50">
                {users.map(u => (
                  <tr key={u.id} className="hover:bg-slate-800/80 transition-colors group">
                    <td className="p-4">
                      <div className="flex items-center gap-3">
                        <div className="w-10 h-10 rounded-full bg-slate-700/50 flex items-center justify-center border border-slate-600">
                          <HiOutlineUserCircle className="w-6 h-6 text-slate-300" />
                        </div>
                        <div>
                          <p className="font-semibold text-slate-200">{u.username}</p>
                          <p className="text-xs text-slate-400">{u.email}</p>
                        </div>
                      </div>
                    </td>
                    <td className="p-4">
                      <button 
                        onClick={() => handleRoleChange(u.id, u.role)}
                        className={`px-3 py-1 text-xs font-semibold rounded-full border transition-all cursor-pointer capitalize
                          ${u.role === 'admin' 
                            ? 'bg-purple-500/10 text-purple-400 border-purple-500/20 hover:bg-purple-500/20' 
                            : 'bg-blue-500/10 text-blue-400 border-blue-500/20 hover:bg-blue-500/20'}`}
                        title="Click to toggle role"
                      >
                        {u.role}
                      </button>
                    </td>
                    <td className="p-4">
                      <button
                        onClick={() => handleStatusToggle(u.id, u.is_active)}
                        className={`px-3 py-1 text-xs font-semibold rounded-full border transition-all cursor-pointer
                          ${u.is_active 
                            ? 'bg-emerald-500/10 text-emerald-400 border-emerald-500/20 hover:bg-emerald-500/20' 
                            : 'bg-red-500/10 text-red-400 border-red-500/20 hover:bg-red-500/20'}`}
                        title="Click to toggle status"
                      >
                        {u.is_active ? 'Active' : 'Suspended'}
                      </button>
                    </td>
                    <td className="p-4 text-slate-400 hidden sm:table-cell whitespace-nowrap text-sm">
                      {formatDate(u.created_at)}
                    </td>
                    <td className="p-4 text-right">
                      <button 
                        onClick={() => handleDeleteUser(u.id)}
                        className="p-2 text-slate-500 hover:text-red-450 hover:bg-slate-700/50 rounded-lg transition-colors opacity-0 group-hover:opacity-100 cursor-pointer"
                        title="Delete Account"
                      >
                        <HiOutlineTrash className="w-5 h-5 text-red-500" />
                      </button>
                    </td>
                  </tr>
                ))}
              </tbody>
            </table>
          </div>
        </div>
      )}
    </div>
  );
};

export default ManageUsers;
