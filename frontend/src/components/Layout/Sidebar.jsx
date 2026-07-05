import React from 'react';
import { NavLink } from 'react-router-dom';
import { 
  HiOutlineChatBubbleLeftRight, 
  HiOutlineClock, 
  HiOutlineDocumentText, 
  HiOutlineUser,
  HiOutlineSquares2X2,
  HiOutlineUsers,
  HiOutlinePlus
} from 'react-icons/hi2';
import useAuth from '../../hooks/useAuth';

const Sidebar = () => {
  const { user } = useAuth();
  
  const navLinkClass = ({ isActive }) => 
    `flex items-center gap-3 px-4 py-3 rounded-xl transition-all duration-200 ${
      isActive 
        ? 'bg-brand-500/10 text-brand-400 border border-brand-500/20' 
        : 'text-slate-400 hover:bg-slate-800 hover:text-slate-200'
    }`;

  return (
    <aside className="w-64 border-r border-slate-700/50 bg-slate-900/50 hidden md:flex flex-col h-[calc(100vh-4rem)] sticky top-16">
      <div className="p-4">
        <NavLink 
          to="/chat" 
          end
          className="flex items-center justify-center gap-2 w-full bg-gradient-to-r from-brand-600 to-brand-500 hover:from-brand-500 hover:to-brand-400 text-white px-4 py-3 rounded-xl font-medium transition-all shadow-lg shadow-brand-500/20"
        >
          <HiOutlinePlus className="w-5 h-5" />
          <span>New Chat</span>
        </NavLink>
      </div>

      <div className="flex-1 overflow-y-auto px-3 py-2 space-y-1">
        <div className="text-xs font-semibold text-slate-500 uppercase tracking-wider mb-3 px-4">Menu</div>
        
        <NavLink to="/chat" end className={navLinkClass}>
          <HiOutlineChatBubbleLeftRight className="w-5 h-5" />
          <span>Current Chat</span>
        </NavLink>
        
        <NavLink to="/history" className={navLinkClass}>
          <HiOutlineClock className="w-5 h-5" />
          <span>History</span>
        </NavLink>
        
        <NavLink to="/profile" className={navLinkClass}>
          <HiOutlineUser className="w-5 h-5" />
          <span>Profile</span>
        </NavLink>

        {user?.role === 'admin' && (
          <>
            <div className="text-xs font-semibold text-brand-400/70 uppercase tracking-wider mt-8 mb-3 px-4 flex items-center gap-2">
              <div className="h-px bg-brand-500/20 flex-1"></div>
              <span>Admin</span>
              <div className="h-px bg-brand-500/20 flex-1"></div>
            </div>
            
            <NavLink to="/admin" end className={navLinkClass}>
              <HiOutlineSquares2X2 className="w-5 h-5" />
              <span>Dashboard</span>
            </NavLink>
            
            <NavLink to="/admin/users" className={navLinkClass}>
              <HiOutlineUsers className="w-5 h-5" />
              <span>Manage Users</span>
            </NavLink>
            
            <NavLink to="/admin/documents" className={navLinkClass}>
              <HiOutlineDocumentText className="w-5 h-5" />
              <span>Knowledge Base</span>
            </NavLink>
          </>
        )}
      </div>
    </aside>
  );
};

export default Sidebar;
