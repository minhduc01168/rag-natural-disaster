import { useState, useEffect, useCallback } from 'react';
import { useAuth } from '../../context/AuthContext';
import { useLanguage } from '../../context/LanguageContext';

// ─── Types ───────────────────────────────────────────────────────────────────

interface DocumentInfo {
  filename: string;
  chunk_count: number;
  status?: 'ready' | 'processing' | 'failed';
}

interface ChunkData {
  id?: string;
  text: string;
  metadata: Record<string, any>;
}

// ─── Helpers ─────────────────────────────────────────────────────────────────

const API = 'http://localhost:8000/api/v1/admin/rag';

function fileIcon(name: string) {
  if (name.endsWith('.pdf'))  return '📄';
  if (name.endsWith('.md'))   return '📋';
  if (/\.docx?$/.test(name)) return '📝';
  if (name.endsWith('.txt'))  return '📃';
  return '📁';
}

function fileExt(name: string) {
  return name.split('.').pop()?.toUpperCase() ?? 'FILE';
}


// ─── Sub-components ──────────────────────────────────────────────────────────

function Spinner() {
  const { t } = useLanguage();
  return (
    <div className="flex items-center justify-center gap-2 py-8 text-slate-400">
      <div className="w-5 h-5 border-2 border-blue-500 border-t-transparent rounded-full animate-spin" />
      <span className="text-sm">{t('admin.loading')}</span>
    </div>
  );
}

function EmptyState({ message }: { message: string }) {
  return (
    <div className="flex flex-col items-center justify-center py-20 text-slate-500">
      <div className="text-5xl mb-4">🗂️</div>
      <p className="text-sm">{message}</p>
    </div>
  );
}

// ─── Chunk Detail Slide-over Panel ───────────────────────────────────────────

interface ChunkPanelProps {
  filename: string;
  chunks: ChunkData[];
  loading: boolean;
  onClose: () => void;
}

function ChunkPanel({ filename, chunks, loading, onClose }: ChunkPanelProps) {
  const [expanded, setExpanded] = useState<Set<number>>(new Set());

  const toggle = (i: number) =>
    setExpanded(prev => {
      const s = new Set(prev);
      s.has(i) ? s.delete(i) : s.add(i);
      return s;
    });

  return (
    <>
      {/* Backdrop */}
      <div
        className="fixed inset-0 z-40 bg-slate-900/30 backdrop-blur-xs"
        onClick={onClose}
      />

      {/* Panel */}
      <aside
        className="
          fixed right-0 top-0 bottom-0 z-50
          w-full sm:w-[560px] lg:w-[640px]
          bg-white border-l border-slate-200/90
          flex flex-col shadow-2xl
          animate-in slide-in-from-right duration-250
        "
      >
        {/* Header */}
        <div className="flex items-center justify-between px-6 py-4 border-b border-slate-200 bg-slate-50/80 shrink-0">
          <div className="min-w-0 flex-1">
            <div className="flex items-center gap-2">
              <span className="text-2xl">{fileIcon(filename)}</span>
              <div className="min-w-0">
                <p className="font-extrabold text-slate-900 truncate">{filename}</p>
                <p className="text-xs text-slate-500 mt-0.5 font-medium">
                  {loading ? '...' : `${chunks.length} chunks`}
                </p>
              </div>
            </div>
          </div>
          <button
            onClick={onClose}
            className="ml-4 w-8 h-8 flex items-center justify-center rounded-lg text-slate-400 hover:text-slate-700 hover:bg-slate-200/60 transition-all shrink-0 font-bold"
          >
            ✕
          </button>
        </div>

        {/* Body */}
        <div className="flex-1 overflow-y-auto">
          {loading ? (
            <Spinner />
          ) : chunks.length === 0 ? (
            <EmptyState message="Không có chunks nào." />
          ) : (
            <div className="p-4 space-y-3">
              {chunks.map((chunk, i) => {
                const isOpen = expanded.has(i);
                const charCount = chunk.text.length;
                const tokenEst = Math.round(charCount / 4);
                return (
                  <div
                    key={chunk.id ?? i}
                    className="bg-slate-50 border border-slate-200/90 rounded-xl overflow-hidden hover:border-slate-300 transition-colors"
                  >
                    {/* Chunk header */}
                    <button
                      onClick={() => toggle(i)}
                      className="w-full flex items-center justify-between px-4 py-3 text-left group"
                    >
                      <div className="flex items-center gap-3">
                        <span className="w-7 h-7 flex items-center justify-center rounded-lg bg-blue-100 text-blue-700 text-xs font-bold shrink-0">
                          {i + 1}
                        </span>
                        <div>
                          <p className="text-sm text-slate-900 font-semibold line-clamp-1">
                            {chunk.text.slice(0, 80)}{chunk.text.length > 80 ? '…' : ''}
                          </p>
                          <p className="text-[11px] text-slate-500 mt-0.5 font-medium">
                            ~{tokenEst} tokens · {charCount} ký tự
                            {chunk.metadata?.['Header 1'] && (
                              <span className="ml-2 text-indigo-600 font-semibold">§ {chunk.metadata['Header 1']}</span>
                            )}
                          </p>
                        </div>
                      </div>
                      <span className={`text-slate-400 transition-transform duration-200 shrink-0 ml-2 ${isOpen ? 'rotate-180' : ''}`}>
                        ▾
                      </span>
                    </button>

                    {/* Chunk content */}
                    {isOpen && (
                      <div className="border-t border-slate-200/80 bg-white">
                        <pre className="px-4 py-3 text-[12px] text-slate-800 whitespace-pre-wrap font-mono leading-relaxed max-h-72 overflow-y-auto">
                          {chunk.text}
                        </pre>
                        {Object.keys(chunk.metadata).length > 0 && (
                          <div className="px-4 py-2 border-t border-slate-200/60 bg-slate-50 flex flex-wrap gap-2">
                            {Object.entries(chunk.metadata)
                              .filter(([k]) => k !== 'source_file')
                              .map(([k, v]) => (
                                <span key={k} className="text-[10px] bg-slate-200 text-slate-700 px-2 py-0.5 rounded-md font-medium">
                                  <span className="text-slate-500">{k}:</span> {String(v)}
                                </span>
                              ))}
                          </div>
                        )}
                      </div>
                    )}
                  </div>
                );
              })}
            </div>
          )}
        </div>
      </aside>
    </>
  );
}

// ─── Main Page ────────────────────────────────────────────────────────────────

export function KBDocumentsPage() {
  const { token } = useAuth();
  const { t } = useLanguage();
  const [docs, setDocs] = useState<DocumentInfo[]>([]);
  const [loadingDocs, setLoadingDocs] = useState(true);
  const [error, setError] = useState('');

  // Slide-over state
  const [selectedFile, setSelectedFile] = useState<string | null>(null);
  const [chunks, setChunks] = useState<ChunkData[]>([]);
  const [loadingChunks, setLoadingChunks] = useState(false);

  // Delete state
  const [deleting, setDeleting] = useState<string | null>(null);
  const [confirmDelete, setConfirmDelete] = useState<string | null>(null);

  // ── Fetch document list ──
  const fetchDocs = useCallback(async () => {
    setLoadingDocs(true);
    setError('');
    try {
      const res = await fetch(`${API}/documents`, {
        headers: { Authorization: `Bearer ${token}` },
      });
      if (!res.ok) throw new Error(`HTTP ${res.status}`);
      setDocs(await res.json());
    } catch (e: any) {
      setError(e.message ?? 'Không thể tải danh sách tài liệu.');
    } finally {
      setLoadingDocs(false);
    }
  }, [token]);

  useEffect(() => { fetchDocs(); }, [fetchDocs]);

  // ── Open chunk panel ──
  const openChunks = async (filename: string) => {
    setSelectedFile(filename);
    setChunks([]);
    setLoadingChunks(true);
    try {
      const res = await fetch(
        `${API}/documents/${encodeURIComponent(filename)}/chunks`,
        { headers: { Authorization: `Bearer ${token}` } },
      );
      if (!res.ok) throw new Error(`HTTP ${res.status}`);
      setChunks(await res.json());
    } catch (e: any) {
      setChunks([]);
    } finally {
      setLoadingChunks(false);
    }
  };

  // ── Delete document ──
  const handleDelete = async (filename: string) => {
    setDeleting(filename);
    try {
      const res = await fetch(
        `${API}/documents/${encodeURIComponent(filename)}`,
        { method: 'DELETE', headers: { Authorization: `Bearer ${token}` } },
      );
      if (!res.ok) throw new Error(`HTTP ${res.status}`);
      setDocs(prev => prev.filter(d => d.filename !== filename));
      if (selectedFile === filename) setSelectedFile(null);
      setConfirmDelete(null);
    } catch (e: any) {
      setError(e.message ?? 'Xóa thất bại.');
    } finally {
      setDeleting(null);
    }
  };

  // ─────────────────────────────────────────────────────────────────
  return (
    <div className="space-y-6">
      {/* Page header */}
      <div className="flex items-end justify-between">
        <div>
          <h1 className="text-3xl font-black text-slate-900">{t('admin.docsTitle')}</h1>
          <p className="text-slate-500 mt-1 text-sm">
            {t('admin.docsSubtitle')}
          </p>
        </div>
        <button
          onClick={fetchDocs}
          disabled={loadingDocs}
          className="flex items-center gap-2 px-4 py-2.5 bg-white hover:bg-slate-50 border border-slate-200/90 rounded-xl text-sm font-semibold text-slate-700 hover:text-slate-900 transition-all disabled:opacity-50 shadow-xs hover:scale-105 active:scale-95"
        >
          <span className={loadingDocs ? 'animate-spin' : ''}>🔄</span>
          <span>{t('admin.refresh')}</span>
        </button>
      </div>

      {/* Error */}
      {error && (
        <div className="bg-red-50 border border-red-200 text-red-700 p-4 rounded-xl text-sm font-medium shadow-xs">
          {error}
        </div>
      )}

      {/* Stats bar */}
      {!loadingDocs && docs.length > 0 && (
        <div className="grid grid-cols-2 sm:grid-cols-3 gap-4">
          {[
            { label: t('admin.totalDocs'), value: docs.length, icon: '📁' },
            { label: t('admin.totalChunks'), value: docs.reduce((a, d) => a + d.chunk_count, 0), icon: '🧩' },
            { label: t('admin.avgChunks'), value: Math.round(docs.reduce((a,d)=>a+d.chunk_count,0)/docs.length), icon: '📊' },
          ].map(stat => (
            <div key={stat.label} className="bg-white/95 border border-slate-200/90 rounded-2xl p-4 shadow-sm">
              <p className="text-2xl mb-1">{stat.icon}</p>
              <p className="text-2xl font-black text-slate-900">{stat.value}</p>
              <p className="text-xs text-slate-500 mt-0.5 font-medium">{stat.label}</p>
            </div>
          ))}
        </div>
      )}

      {/* Document grid */}
      {loadingDocs ? (
        <Spinner />
      ) : docs.length === 0 ? (
        <div className="bg-white/95 border border-slate-200/90 rounded-2xl shadow-xs">
          <EmptyState message={t('admin.emptyDocs')} />
        </div>
      ) : (
        <div className="flex flex-col gap-3">
          {docs.map(doc => {
            const isSelected = selectedFile === doc.filename;
            const maxChunks = Math.max(...docs.map(d => d.chunk_count), 1);
            const progressPct = Math.min(100, Math.round((doc.chunk_count / maxChunks) * 100));

            return (
              <div
                key={doc.filename}
                className={`
                  group relative bg-white/95 border rounded-2xl p-4 sm:px-6 sm:py-4
                  transition-all duration-200
                  flex flex-col sm:flex-row items-start sm:items-center justify-between gap-4
                  ${isSelected
                    ? 'border-blue-500 shadow-md shadow-blue-500/10 bg-blue-50/30'
                    : 'border-slate-200/90 hover:border-blue-400 hover:shadow-sm'}
                `}
              >
                {/* Row body — clickable */}
                <button
                  onClick={() => openChunks(doc.filename)}
                  className="flex-1 w-full sm:w-auto text-left flex flex-col md:flex-row md:items-center justify-between gap-4 min-w-0"
                >
                  {/* Left: Icon + Filename + Badges */}
                  <div className="flex items-center gap-4 min-w-0 flex-1">
                    <span className="text-3xl sm:text-4xl shrink-0 p-2 bg-blue-50 rounded-xl border border-blue-100">
                      {fileIcon(doc.filename)}
                    </span>
                    <div className="min-w-0 flex-1">
                      <p className="font-bold text-slate-900 text-sm sm:text-base leading-snug truncate hover:text-blue-600 transition-colors">
                        {doc.filename}
                      </p>
                      <div className="flex items-center gap-2 mt-1.5 flex-wrap">
                        <span className="text-[10px] font-bold bg-slate-100 text-slate-700 px-2.5 py-0.5 rounded-md border border-slate-200">
                          {fileExt(doc.filename)}
                        </span>
                        <span className="text-[10px] font-bold bg-blue-50 text-blue-700 px-2.5 py-0.5 rounded-md border border-blue-200/80">
                          🧩 {doc.chunk_count} {t('admin.chunks')}
                        </span>
                        <span 
                          className={`inline-flex items-center gap-1 text-[10px] font-bold px-2.5 py-0.5 rounded-md border ${
                            (!doc.status || doc.status === 'ready')
                              ? 'bg-emerald-50 text-emerald-800 border-emerald-200'
                              : doc.status === 'processing'
                              ? 'bg-amber-50 text-amber-800 border-amber-200 animate-pulse'
                              : 'bg-rose-50 text-rose-800 border-rose-200'
                          }`}
                          title={(!doc.status || doc.status === 'ready') ? t('admin.statusReadyDesc') : t('admin.statusProcessingDesc')}
                        >
                          <span className={`w-1.5 h-1.5 rounded-full ${(!doc.status || doc.status === 'ready') ? 'bg-emerald-500' : doc.status === 'processing' ? 'bg-amber-500 animate-ping' : 'bg-rose-500'}`} />
                          {(!doc.status || doc.status === 'ready') ? t('admin.statusReady') : doc.status === 'processing' ? t('admin.statusProcessing') : t('admin.statusFailed')}
                        </span>
                      </div>
                    </div>
                  </div>

                  {/* Middle/Right: Progress bar & Status */}
                  <div className="w-full md:w-56 shrink-0 flex flex-col justify-center">
                    <div className="flex items-center justify-between text-[11px] text-slate-500 mb-1.5 font-semibold">
                      <span>{isSelected ? t('admin.viewingChunks') : t('admin.viewChunks')}</span>
                      <span className="text-slate-600">{progressPct}%</span>
                    </div>
                    <div className="w-full h-1.5 bg-slate-100 rounded-full overflow-hidden border border-slate-200/60">
                      <div
                        className="h-full bg-gradient-to-r from-blue-500 via-sky-500 to-teal-500 rounded-full transition-all duration-300"
                        style={{ width: `${progressPct}%` }}
                      />
                    </div>
                  </div>
                </button>

                {/* Right: Actions */}
                <div className="shrink-0 self-end sm:self-center border-t sm:border-t-0 pt-3 sm:pt-0 w-full sm:w-auto border-slate-100 flex justify-end">
                  {confirmDelete === doc.filename ? (
                    <div className="flex items-center gap-2">
                      <span className="text-xs text-rose-600 font-bold mr-1">{t('admin.confirmDelete')}</span>
                      <button
                        onClick={() => handleDelete(doc.filename)}
                        disabled={deleting === doc.filename}
                        className="text-xs px-3 py-1.5 bg-rose-600 hover:bg-rose-700 text-white font-bold rounded-xl transition-all disabled:opacity-50 shadow-xs hover:scale-105"
                      >
                        {deleting === doc.filename ? '...' : t('admin.delete')}
                      </button>
                      <button
                        onClick={() => setConfirmDelete(null)}
                        className="text-xs px-3 py-1.5 bg-slate-200 hover:bg-slate-300 text-slate-700 font-semibold rounded-xl transition-all shadow-xs"
                      >
                        {t('admin.cancel')}
                      </button>
                    </div>
                  ) : (
                    <button
                      onClick={(e) => { e.stopPropagation(); setConfirmDelete(doc.filename); }}
                      className="
                        w-9 h-9 flex items-center justify-center
                        rounded-xl text-slate-400 hover:text-rose-600 hover:bg-rose-50
                        transition-all border border-transparent hover:border-rose-200 shadow-xs
                      "
                      title={t('admin.delete')}
                    >
                      🗑
                    </button>
                  )}
                </div>
              </div>
            );
          })}
        </div>
      )}

      {/* Chunk slide-over panel */}
      {selectedFile && (
        <ChunkPanel
          filename={selectedFile}
          chunks={chunks}
          loading={loadingChunks}
          onClose={() => setSelectedFile(null)}
        />
      )}
    </div>
  );
}

