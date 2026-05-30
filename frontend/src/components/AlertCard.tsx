interface AlertCardProps {
  id: string;
  level: string;
  location: string;
  description: string;
  timestamp: string;
}

const levelColors: Record<string, { bg: string; border: string; text: string }> = {
  green: {
    bg: 'bg-green-50',
    border: 'border-green-500',
    text: 'text-green-700',
  },
  yellow: {
    bg: 'bg-yellow-50',
    border: 'border-yellow-500',
    text: 'text-yellow-700',
  },
  red: {
    bg: 'bg-red-50',
    border: 'border-red-500',
    text: 'text-red-700',
  },
};

const levelLabels: Record<string, string> = {
  green: 'An toàn',
  yellow: 'Cảnh giác',
  red: 'Nguy hiểm',
};

export function AlertCard({ id, level, location, description, timestamp }: AlertCardProps) {
  const colors = levelColors[level] || levelColors.green;
  const label = levelLabels[level] || 'Unknown';

  return (
    <div className={`${colors.bg} border-l-4 ${colors.border} rounded-lg p-4`}>
      <div className="flex items-start justify-between">
        <div className="flex-1">
          <div className="flex items-center gap-2 mb-1">
            <span className={`text-sm font-medium ${colors.text}`}>{label}</span>
            <span className="text-xs text-gray-400">#{id}</span>
          </div>
          <p className="text-gray-900 font-medium">{location}</p>
          <p className="text-sm text-gray-600 mt-1">{description}</p>
        </div>
        <span className="text-xs text-gray-400 whitespace-nowrap ml-4">
          {new Date(timestamp).toLocaleString('vi-VN')}
        </span>
      </div>
    </div>
  );
}
