import React from 'react';
import SignupForm from '../components/Auth/SignupForm';

const Signup = () => {
  return (
    <div className="min-h-screen bg-[#0b1120] flex items-center justify-center p-4 relative overflow-hidden">
      {/* Background gradients */}
      <div className="absolute inset-0 z-0 pointer-events-none overflow-hidden">
        <div className="absolute top-[-20%] left-[-10%] w-[50%] h-[50%] rounded-full bg-purple-900/20 blur-[120px]"></div>
        <div className="absolute bottom-[-20%] right-[-10%] w-[50%] h-[50%] rounded-full bg-brand-900/20 blur-[120px]"></div>
      </div>
      
      <div className="z-10 w-full flex justify-center">
        <SignupForm />
      </div>
    </div>
  );
};

export default Signup;
