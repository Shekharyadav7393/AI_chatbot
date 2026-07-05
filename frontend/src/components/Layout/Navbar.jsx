import React from 'react';
import { HiOutlineUserCircle, HiArrowRightOnRectangle } from 'react-icons/hi2';
import useAuth from '../../hooks/useAuth';

const Navbar = () => {
  const { user, logout } = useAuth();

  return (
    <nav className="h-16 border-b border-slate-700/50 bg-slate-900/80 backdrop-blur-xl sticky top-0 z-40 flex items-center justify-between px-6">
      <div className="flex items-center gap-3">
        <div className="w-8 h-8 rounded-lg bg-gradient-to-br from-brand-500 to-purple-600 flex items-center justify-center">
          <span className="text-white font-bold text-sm">AI</span>
        </div>
        <span className="font-semibold text-lg bg-clip-text text-transparent bg-gradient-to-r from-slate-100 to-slate-400">
          SupportDesk
        </span>
      </div>

      <div className="flex items-center gap-4">
        {user && (
          <div className="flex items-center gap-4">
            <div className="flex items-center gap-2">
              <div className="w-8 h-8 rounded-full bg-slate-800 flex items-center justify-center border border-slate-700">
                <HiOutlineUserCircle className="w-5 h-5 text-slate-400" />
              </div>
              <div className="hidden md:block text-sm">
                <p className="font-medium text-slate-200">{user.username}</p>
                <p className="text-xs text-slate-400 capitalize">{user.role}</p>
              </div>
            </div>
            
            <div className="h-6 w-px bg-slate-700"></div>
            
            <button 
              onClick={logout}
              className="text-slate-400 hover:text-red-400 transition-colors p-2 rounded-lg hover:bg-slate-800"
              title="Logout"
            >
              <HiArrowRightOnRectangle className="w-5 h-5" />
            </button>
          </div>
        )}
      </div>
    </nav>
  );
};

export default Navbar;
