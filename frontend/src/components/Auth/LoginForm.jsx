import React, { useState } from 'react';
import { useNavigate, Link } from 'react-router-dom';

import { HiOutlineLockClosed as LockIcon, HiEye as EyeIcon, HiEyeSlash as EyeSlashIcon } from 'react-icons/hi2';
import { HiOutlineMail } from 'react-icons/hi';
import useAuth from '../../hooks/useAuth';
import LoadingSpinner from '../Common/LoadingSpinner';
import { toast } from 'react-hot-toast';

const LoginForm = ({ isAdminPortal = false }) => {
  const [email, setEmail] = useState('');
  const [password, setPassword] = useState('');
  const [showPassword, setShowPassword] = useState(false);
  const [isSubmitting, setIsSubmitting] = useState(false);
  const { login, logout, fetchProfile } = useAuth();
  const navigate = useNavigate();

  const handleSubmit = async (e) => {
    e.preventDefault();
    setIsSubmitting(true);
    
    const loggedInUser = await login(email, password);
    if (loggedInUser) {
      if (isAdminPortal) {
        if (loggedInUser.role !== 'admin') {
          toast.error('Access denied. Only administrators are allowed here.');
          await logout();
          setIsSubmitting(false);
          return;
        }
        toast.success('Welcome to Admin Panel!');
        navigate('/admin');
      } else {
        if (loggedInUser.role === 'admin') {
          toast.error('Admins must log in through the Admin Portal.');
          await logout();
          setIsSubmitting(false);
          return;
        }
        toast.success('Logged in successfully!');
        navigate('/chat');
      }
    }
    setIsSubmitting(false);
  };

  return (
    <div className="w-full max-w-md p-8 glass-panel rounded-2xl relative overflow-hidden">
      <div className="absolute top-0 inset-x-0 h-1 bg-gradient-to-r from-brand-500 via-purple-500 to-brand-500"></div>
      
      <div className="text-center mb-8">
        <h2 className="text-3xl font-bold text-white mb-2">
          {isAdminPortal ? 'Admin Portal' : 'Welcome Back'}
        </h2>
        <p className="text-slate-400">
          {isAdminPortal ? 'Sign in to access control panel' : 'Sign in to continue to SupportDesk'}
        </p>
      </div>

      <form onSubmit={handleSubmit} className="space-y-5">
        <div>
          <label className="block text-sm font-medium text-slate-300 mb-1.5">Email Address</label>
          <div className="relative">
            <div className="absolute inset-y-0 left-0 pl-3 flex items-center pointer-events-none">
              <HiOutlineMail className="h-5 w-5 text-slate-500" />
            </div>
            <input
              type="email"
              value={email}
              onChange={(e) => setEmail(e.target.value)}
              className="w-full pl-10 pr-4 py-2.5 glass-input rounded-xl text-sm"
              placeholder="you@company.com"
              required
            />
          </div>
        </div>

        <div>
          <label className="block text-sm font-medium text-slate-300 mb-1.5">Password</label>
          <div className="relative">
            <div className="absolute inset-y-0 left-0 pl-3 flex items-center pointer-events-none">
              <LockIcon className="h-5 w-5 text-slate-500" />
            </div>
            <input
              type={showPassword ? 'text' : 'password'}
              value={password}
              onChange={(e) => setPassword(e.target.value)}
              className="w-full pl-10 pr-10 py-2.5 glass-input rounded-xl text-sm"
              placeholder="••••••••"
              required
            />
            <button
              type="button"
              className="absolute inset-y-0 right-0 pr-3 flex items-center text-slate-500 hover:text-slate-300 transition-colors"
              onClick={() => setShowPassword(!showPassword)}
            >
              {showPassword ? <EyeSlashIcon className="h-5 w-5" /> : <EyeIcon className="h-5 w-5" />}
            </button>
          </div>
        </div>

        <button
          type="submit"
          disabled={isSubmitting}
          className="w-full py-3 px-4 rounded-xl font-medium text-white bg-gradient-to-r from-brand-600 to-brand-500 hover:from-brand-500 hover:to-brand-400 focus:outline-none focus:ring-2 focus:ring-brand-500 focus:ring-offset-2 focus:ring-offset-slate-900 transition-all shadow-lg shadow-brand-500/25 disabled:opacity-70 disabled:cursor-not-allowed flex justify-center items-center h-12 text-sm cursor-pointer"
        >
          {isSubmitting ? <LoadingSpinner text="" /> : 'Sign In'}
        </button>
      </form>

      {!isAdminPortal && (
        <p className="mt-8 text-center text-sm text-slate-400">
          Don't have an account?{' '}
          <Link to="/signup" className="text-brand-400 hover:text-brand-300 font-medium transition-colors hover:underline">
            Sign up
          </Link>
        </p>
      )}
    </div>
  );
};

export default LoginForm;
