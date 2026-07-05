import { Toaster } from 'react-hot-toast';

const Toast = () => {
  return (
    <Toaster
      position="top-right"
      toastOptions={{
        className: '',
        style: {
          background: '#1e293b', // slate-800
          color: '#f1f5f9', // slate-100
          border: '1px solid rgba(51, 65, 85, 0.5)', // slate-700/50
          backdropFilter: 'blur(12px)',
        },
        success: {
          iconTheme: {
            primary: '#10b981', // emerald-500
            secondary: '#1e293b',
          },
        },
        error: {
          iconTheme: {
            primary: '#ef4444', // red-500
            secondary: '#1e293b',
          },
        },
      }}
    />
  );
};

export default Toast;
