import React from 'react';
import { Outlet } from 'react-router-dom';
import Navbar from './Navbar';
import Sidebar from './Sidebar';

const AppLayout = () => {
  return (
    <div className="min-h-screen bg-[#0a0a1a] text-slate-200 font-sans selection:bg-brand-500/30 selection:text-brand-100 flex flex-col">
      {/* Animated background gradients */}
      <div className="fixed inset-0 z-0 pointer-events-none overflow-hidden">
        <div className="absolute top-[-20%] left-[-15%] w-[50%] h-[50%] rounded-full bg-gradient-to-br from-violet-600/15 to-indigo-900/10 blur-[140px] animate-pulse" style={{ animationDuration: '8s' }}></div>
        <div className="absolute bottom-[-20%] right-[-15%] w-[50%] h-[50%] rounded-full bg-gradient-to-tl from-cyan-600/10 to-blue-900/10 blur-[140px] animate-pulse" style={{ animationDuration: '10s' }}></div>
        <div className="absolute top-[40%] left-[50%] -translate-x-1/2 w-[30%] h-[30%] rounded-full bg-gradient-to-r from-fuchsia-600/5 to-rose-600/5 blur-[120px] animate-pulse" style={{ animationDuration: '12s' }}></div>
        {/* Subtle grid overlay */}
        <div className="absolute inset-0 opacity-[0.03]" style={{ backgroundImage: 'radial-gradient(circle at 1px 1px, rgba(255,255,255,0.3) 1px, transparent 0)', backgroundSize: '40px 40px' }}></div>
      </div>

      {/* Main Content Wrapper */}
      <div className="relative z-10 flex flex-col min-h-screen">
        <Navbar />
        
        <div className="flex flex-1 overflow-hidden">
          <Sidebar />
          
          <main className="flex-1 flex flex-col w-full h-[calc(100vh-4rem)] overflow-hidden">
            <Outlet />
          </main>
        </div>
      </div>
    </div>
  );
};

export default AppLayout;
