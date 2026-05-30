interface LSMLegendProps {
  className?: string;
}

export function LSMLegend({ className }: LSMLegendProps) {
  return (
    <div className={`bg-white rounded-lg shadow-md p-4 ${className}`}>
      <h4 className="font-semibold text-gray-900 mb-3">Mức độ nhạy cảm sạt lở</h4>
      <div className="space-y-2">
        <div className="flex items-center gap-2">
          <div className="w-4 h-4 rounded" style={{ backgroundColor: '#22c55e' }} />
          <span className="text-sm text-gray-700">Thấp (0 - 0.4)</span>
        </div>
        <div className="flex items-center gap-2">
          <div className="w-4 h-4 rounded" style={{ backgroundColor: '#eab308' }} />
          <span className="text-sm text-gray-700">Trung bình (0.4 - 0.7)</span>
        </div>
        <div className="flex items-center gap-2">
          <div className="w-4 h-4 rounded" style={{ backgroundColor: '#ef4444' }} />
          <span className="text-sm text-gray-700">Cao (0.7 - 1.0)</span>
        </div>
      </div>
    </div>
  );
}
