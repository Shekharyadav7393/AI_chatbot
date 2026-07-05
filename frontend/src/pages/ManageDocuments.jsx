import React, { useState, useEffect } from 'react';
import { 
  HiOutlineDocumentText, 
  HiOutlineTrash, 
  HiOutlineCheckCircle,
  HiOutlineXCircle,
  HiOutlineClock
} from 'react-icons/hi2';
import { HiOutlineCloudUpload } from 'react-icons/hi';
import api from '../api/axios';
import { formatFileSize, formatDate } from '../utils/helpers';
import { toast } from 'react-hot-toast';
import LoadingSpinner from '../components/Common/LoadingSpinner';

const ManageDocuments = () => {
  const [documents, setDocuments] = useState([]);
  const [loading, setLoading] = useState(true);
  const [uploading, setUploading] = useState(false);

  const fetchDocuments = async () => {
    try {
      const { data } = await api.get('/admin/documents');
      setDocuments(data.data.documents);
    } catch {
      toast.error('Failed to fetch knowledge base documents');
    } finally {
      setLoading(false);
    }
  };

  useEffect(() => {
    fetchDocuments();
    // Poll for status updates if any doc is processing
    const interval = setInterval(() => {
      setDocuments(prev => {
        if (prev.some(d => d.status === 'processing')) {
          fetchDocuments();
        }
        return prev;
      });
    }, 5000);
    return () => clearInterval(interval);
  }, []);

  const handleFileUpload = async (e) => {
    const file = e.target.files[0];
    if (!file) return;

    // Validate type
    const validTypes = ['application/pdf', 'application/vnd.openxmlformats-officedocument.wordprocessingml.document', 'text/plain'];
    if (!validTypes.includes(file.type)) {
      toast.error('Invalid file type. Please upload PDF, DOCX, or TXT.');
      return;
    }

    // Validate size (10MB)
    if (file.size > 10 * 1024 * 1024) {
      toast.error('File size exceeds 10MB limit.');
      return;
    }

    const formData = new FormData();
    formData.append('file', file);

    setUploading(true);
    try {
      await api.post('/admin/documents/upload', formData, {
        headers: { 'Content-Type': 'multipart/form-data' }
      });
      toast.success('Document uploaded to global knowledge base.');
      fetchDocuments();
    } catch (error) {
      toast.error(error.response?.data?.error?.message || 'Upload failed');
    } finally {
      setUploading(false);
      e.target.value = null; // reset input
    }
  };

  const handleDelete = async (id) => {
    if (!window.confirm('Are you sure you want to delete this document from the knowledge base?')) return;
    
    try {
      await api.delete(`/admin/documents/${id}`);
      setDocuments(prev => prev.filter(d => d.id !== id));
      toast.success('Document deleted');
    } catch {
      toast.error('Failed to delete document');
    }
  };

  const getStatusIcon = (status) => {
    switch (status) {
      case 'ready':
        return <HiOutlineCheckCircle className="w-5 h-5 text-emerald-500" />;
      case 'failed':
        return <HiOutlineXCircle className="w-5 h-5 text-red-500" />;
      case 'processing':
      default:
        return <HiOutlineClock className="w-5 h-5 text-amber-500 animate-pulse" />;
    }
  };

  return (
    <div className="p-6 md:p-8 max-w-6xl mx-auto w-full">
      <div className="flex flex-col md:flex-row md:items-center justify-between gap-4 mb-8">
        <div>
          <h1 className="text-3xl font-bold text-white mb-2">Knowledge Base</h1>
          <p className="text-slate-400">Manage documents used by the chatbot for answering queries</p>
        </div>
        
        <div>
          <input 
            type="file" 
            id="kb-file-upload" 
            className="hidden" 
            accept=".pdf,.docx,.txt"
            onChange={handleFileUpload}
            disabled={uploading}
          />
          <label 
            htmlFor="kb-file-upload"
            className={`flex items-center justify-center gap-2 px-5 py-2.5 bg-brand-600 text-white rounded-xl font-medium transition-all shadow-lg cursor-pointer ${uploading ? 'opacity-70 cursor-not-allowed bg-brand-700' : 'hover:bg-brand-500'}`}
          >
            {uploading ? (
              <LoadingSpinner text="" />
            ) : (
              <>
                <HiOutlineCloudUpload className="w-5 h-5" />
                <span>Upload to Knowledge Base</span>
              </>
            )}
          </label>
        </div>
      </div>

      {loading ? (
        <LoadingSpinner />
      ) : documents.length === 0 ? (
        <div className="text-center py-24 bg-slate-800/30 rounded-2xl border border-slate-700/50 border-dashed">
          <HiOutlineDocumentText className="w-16 h-16 text-slate-600 mx-auto mb-4" />
          <h3 className="text-xl font-medium text-slate-300 mb-2">No files uploaded yet</h3>
          <p className="text-slate-500 max-w-sm mx-auto">
            Upload policies, FAQs, manuals, or documents to allow the chatbot to retrieve information and answer users.
          </p>
        </div>
      ) : (
        <div className="bg-slate-800/50 rounded-2xl border border-slate-700/50 overflow-hidden backdrop-blur-xl">
          <div className="overflow-x-auto">
            <table className="w-full text-left border-collapse">
              <thead>
                <tr className="bg-slate-900/50 border-b border-slate-700/50">
                  <th className="p-4 font-semibold text-slate-300">File Name</th>
                  <th className="p-4 font-semibold text-slate-300 hidden sm:table-cell">Size</th>
                  <th className="p-4 font-semibold text-slate-300 hidden md:table-cell">Uploaded</th>
                  <th className="p-4 font-semibold text-slate-300">Status</th>
                  <th className="p-4 font-semibold text-slate-300 text-right">Actions</th>
                </tr>
              </thead>
              <tbody className="divide-y divide-slate-700/50">
                {documents.map(doc => (
                  <tr key={doc.id} className="hover:bg-slate-800/80 transition-colors group">
                    <td className="p-4">
                      <div className="flex items-center gap-3">
                        <div className="w-10 h-10 rounded-lg bg-slate-700/50 flex items-center justify-center text-slate-300">
                          <span className="text-xs font-bold uppercase">{doc.file_type}</span>
                        </div>
                        <span className="font-medium text-slate-200 truncate max-w-[200px] sm:max-w-[300px]" title={doc.filename}>
                          {doc.filename}
                        </span>
                      </div>
                    </td>
                    <td className="p-4 text-slate-400 hidden sm:table-cell whitespace-nowrap text-sm">
                      {formatFileSize(doc.file_size)}
                    </td>
                    <td className="p-4 text-slate-400 hidden md:table-cell whitespace-nowrap text-sm">
                      {formatDate(doc.created_at)}
                    </td>
                    <td className="p-4">
                      <div className="flex items-center gap-2">
                        {getStatusIcon(doc.status)}
                        <span className="text-sm capitalize text-slate-300">{doc.status}</span>
                      </div>
                    </td>
                    <td className="p-4 text-right">
                      <button 
                        onClick={() => handleDelete(doc.id)}
                        className="p-2 text-slate-500 hover:text-red-400 hover:bg-slate-700/50 rounded-lg transition-colors opacity-0 group-hover:opacity-100 cursor-pointer"
                        title="Delete Document"
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

export default ManageDocuments;
