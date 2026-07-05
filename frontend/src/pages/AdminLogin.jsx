import React from 'react';
import LoginForm from '../components/Auth/LoginForm';

const AdminLogin = () => {
  return (
    <div className="min-h-screen bg-[#060613] flex items-center justify-center p-4 relative overflow-hidden">
      {/* Dynamic background gradients for Admin Portal */}
      <div className="absolute inset-0 z-0 pointer-events-none overflow-hidden">
        <div className="absolute top-[-20%] left-[-10%] w-[50%] h-[50%] rounded-full bg-purple-900/15 blur-[130px] animate-pulse" style={{ animationDuration: '6s' }}></div>
        <div className="absolute bottom-[-20%] right-[-10%] w-[50%] h-[50%] rounded-full bg-indigo-900/15 blur-[130px] animate-pulse" style={{ animationDuration: '8s' }}></div>
      </div>
      
      <div className="z-10 w-full flex justify-center">
        <LoginForm isAdminPortal={true} />
      </div>
    </div>
  );
};

export default AdminLogin;
