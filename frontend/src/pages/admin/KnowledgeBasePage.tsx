import { useState, useRef } from 'react';

interface ChunkData {
  text: string;
  metadata: Record<string, any>;
}

export function KnowledgeBasePage() {
  const [file, setFile] = useState<File | null>(null);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState('');
  const [chunks, setChunks] = useState<ChunkData[] | null>(null);
  const [committing, setCommitting] = useState(false);
  const [success, setSuccess] = useState('');
  const fileInputRef = useRef<HTMLInputElement>(null);

  const handleFileChange = (e: React.ChangeEvent<HTMLInputElement>) => {
    if (e.target.files && e.target.files[0]) {
      setFile(e.target.files[0]);
      setChunks(null);
      setError('');
      setSuccess('');
    }
  };

  const handleDryRun = async () => {
    if (!file) return;
    setLoading(true);
    setError('');
    
    const formData = new FormData();
    formData.append('file', file);

    try {
      const token = localStorage.getItem('token');
      const response = await fetch('/api/v1/admin/rag/dry-run', {
        method: 'POST',
        headers: {
          'Authorization': `Bearer ${token}`
        },
        body: formData
      });

      if (!response.ok) {
        throw new Error('Lỗi khi phân tích tài liệu');
      }

      const data = await response.json();
      setChunks(data);
    } catch (err: any) {
      setError(err.message || 'Đã có lỗi xảy ra');
    } finally {
      setLoading(false);
    }
  };

  const handleCommit = async () => {
    if (!chunks) return;
    setCommitting(true);
    setError('');

    try {
      const token = localStorage.getItem('token');
      const response = await fetch('/api/v1/admin/rag/commit', {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
          'Authorization': `Bearer ${token}`
        },
        body: JSON.stringify({ chunks })
      });

      if (!response.ok) {
        throw new Error('Lỗi khi lưu vào CSDL');
      }

      setSuccess(`Đã lưu thành công ${chunks.length} phân đoạn vào Knowledge Base.`);
      setChunks(null);
      setFile(null);
      if (fileInputRef.current) fileInputRef.current.value = '';
    } catch (err: any) {
      setError(err.message || 'Đã có lỗi xảy ra');
    } finally {
      setCommitting(false);
    }
  };

  return (
    <div className="space-y-6">
      <div className="flex justify-between items-end">
        <div>
          <h1 className="text-3xl font-bold text-white drop-shadow-sm">Quản lý Knowledge Base</h1>
          <p className="text-slate-400 mt-2">Tải lên và kiểm duyệt tài liệu AI RAG (Two-Phase Ingestion)</p>
        </div>
      </div>

      {error && (
        <div className="bg-red-500/10 border border-red-500/30 text-red-400 p-4 rounded-xl">
          {error}
        </div>
      )}

      {success && (
        <div className="bg-green-500/10 border border-green-500/30 text-green-400 p-4 rounded-xl">
          {success}
        </div>
      )}

      <div className="bg-slate-900/50 border border-white/10 p-6 rounded-2xl backdrop-blur-md shadow-xl">
        <h2 className="text-xl font-semibold mb-4 text-slate-200">1. Upload Tài liệu</h2>
        <div className="flex items-center gap-4">
          <input 
            type="file" 
            ref={fileInputRef}
            onChange={handleFileChange}
            accept=".pdf,.docx,.txt,.md"
            className="block w-full text-sm text-slate-400
              file:mr-4 file:py-2 file:px-4
              file:rounded-full file:border-0
              file:text-sm file:font-semibold
              file:bg-blue-500/10 file:text-blue-400
              hover:file:bg-blue-500/20 transition-all cursor-pointer"
          />
          <button 
            onClick={handleDryRun}
            disabled={!file || loading}
            className="bg-blue-600 hover:bg-blue-500 disabled:opacity-50 disabled:cursor-not-allowed text-white px-6 py-2 rounded-xl whitespace-nowrap shadow-lg shadow-blue-500/20 font-medium transition-all"
          >
            {loading ? 'Đang phân tích...' : 'Phân tích thử (Dry Run)'}
          </button>
        </div>
        <p className="text-xs text-slate-500 mt-3">Hỗ trợ: PDF, DOCX, TXT. Hệ thống sẽ bóc tách văn bản và chia nhỏ (chunk) nhưng chưa lưu vào Database.</p>
      </div>

      {chunks && (
        <div className="bg-slate-900/50 border border-white/10 p-6 rounded-2xl backdrop-blur-md shadow-xl animate-in fade-in slide-in-from-bottom-4">
          <div className="flex justify-between items-center mb-6">
            <h2 className="text-xl font-semibold text-slate-200">2. Chunking Inspector (Kiểm duyệt)</h2>
            <button 
              onClick={handleCommit}
              disabled={committing}
              className="bg-green-600 hover:bg-green-500 disabled:opacity-50 text-white px-6 py-2 rounded-xl shadow-lg shadow-green-500/20 font-medium transition-all"
            >
              {committing ? 'Đang lưu...' : `Phê duyệt & Nạp ${chunks.length} Chunks`}
            </button>
          </div>

          <div className="grid grid-cols-1 lg:grid-cols-2 gap-4 max-h-[600px] overflow-y-auto pr-2 custom-scrollbar">
            {chunks.map((chunk, idx) => (
              <div key={idx} className="bg-slate-800/80 border border-slate-700 rounded-xl p-4 flex flex-col group hover:border-slate-500 transition-colors">
                <div className="flex justify-between items-start mb-2">
                  <span className="text-xs font-semibold bg-slate-700 text-slate-300 px-2 py-1 rounded">
                    Chunk #{idx + 1}
                  </span>
                  <span className="text-xs text-slate-400" title="Kích thước ước tính">
                    ~{Math.round(chunk.text.length / 4)} tokens
                  </span>
                </div>
                <div className="text-sm text-slate-300 flex-1 whitespace-pre-wrap font-mono bg-slate-950/50 p-3 rounded-lg overflow-y-auto max-h-48">
                  {chunk.text}
                </div>
              </div>
            ))}
          </div>
        </div>
      )}
    </div>
  );
}
