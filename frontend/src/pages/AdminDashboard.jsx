import React, { useState, useEffect } from 'react';
import { 
  HiOutlineUsers, 
  HiOutlineDocumentText, 
  HiOutlineChatBubbleLeftRight, 
  HiOutlineStar 
} from 'react-icons/hi2';
import api from '../api/axios';
import { formatDate } from '../utils/helpers';
import LoadingSpinner from '../components/Common/LoadingSpinner';

const AdminDashboard = () => {
  const [stats, setStats] = useState(null);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    const fetchDashboard = async () => {
      try {
        const { data } = await api.get('/admin/dashboard');
        setStats(data.data);
      } catch (error) {
        console.error('Failed to fetch dashboard', error);
      } finally {
        setLoading(false);
      }
    };
    fetchDashboard();
  }, []);

  if (loading) return <LoadingSpinner />;

  const statCards = [
    { title: 'Total Users', value: stats?.total_users || 0, icon: <HiOutlineUsers />, color: 'from-blue-500 to-cyan-500' },
    { title: 'Knowledge Base', value: stats?.total_documents || 0, icon: <HiOutlineDocumentText />, color: 'from-purple-500 to-pink-500' },
    { title: 'Total Chats', value: stats?.total_chats || 0, icon: <HiOutlineChatBubbleLeftRight />, color: 'from-emerald-500 to-teal-500' },
    { title: 'Avg Rating', value: stats?.avg_rating || '0.0', icon: <HiOutlineStar />, color: 'from-amber-500 to-orange-500' }
  ];

  return (
    <div className="p-6 md:p-8 max-w-7xl mx-auto w-full">
      <div className="mb-8">
        <h1 className="text-3xl font-bold text-white mb-2">Admin Dashboard</h1>
        <p className="text-slate-400">Overview of system metrics and activity</p>
      </div>

      <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-6 mb-8">
        {statCards.map((stat, idx) => (
          <div key={idx} className="bg-slate-800/50 border border-slate-700/50 rounded-2xl p-6 relative overflow-hidden group">
            <div className={`absolute top-0 right-0 p-4 opacity-10 transform translate-x-4 -translate-y-4 group-hover:scale-110 transition-transform duration-500`}>
              <div className={`w-24 h-24 text-white`}>
                {React.cloneElement(stat.icon, { className: "w-full h-full" })}
              </div>
            </div>
            
            <div className={`w-12 h-12 rounded-xl bg-gradient-to-br ${stat.color} flex items-center justify-center text-white mb-4 shadow-lg`}>
              {React.cloneElement(stat.icon, { className: "w-6 h-6" })}
            </div>
            <h3 className="text-slate-400 font-medium mb-1">{stat.title}</h3>
            <p className="text-3xl font-bold text-white">{stat.value}</p>
          </div>
        ))}
      </div>

      <div className="bg-slate-800/50 border border-slate-700/50 rounded-2xl overflow-hidden backdrop-blur-xl">
        <div className="p-6 border-b border-slate-700/50 flex justify-between items-center">
          <h2 className="text-xl font-bold text-white">Recent Activity</h2>
        </div>
        <div className="p-6">
          {stats?.recent_activity?.length > 0 ? (
            <div className="space-y-6">
              {stats.recent_activity.map((item, idx) => (
                <div key={idx} className="flex gap-4">
                  <div className="w-10 h-10 rounded-full bg-slate-700/50 flex items-center justify-center flex-shrink-0">
                    <HiOutlineStar className="w-5 h-5 text-amber-400" />
                  </div>
                  <div>
                    <p className="text-slate-200">{item.description}</p>
                    <p className="text-sm text-slate-500">{formatDate(item.timestamp)}</p>
                  </div>
                </div>
              ))}
            </div>
          ) : (
            <p className="text-slate-500 text-center py-8">No recent activity found</p>
          )}
        </div>
      </div>
    </div>
  );
};

export default AdminDashboard;
