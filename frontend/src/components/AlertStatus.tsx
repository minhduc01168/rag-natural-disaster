interface AlertStatusProps {
  level: string;
  name: string;
  description: string;
  recommendations: string[];
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

const levelIcons: Record<string, string> = {
  green: '✅',
  yellow: '⚠️',
  red: '🚨',
};

export function AlertStatus({ level, name, description, recommendations }: AlertStatusProps) {
  const colors = levelColors[level] || levelColors.green;
  const icon = levelIcons[level] || '❓';

  return (
    <div className={`${colors.bg} border-l-4 ${colors.border} rounded-xl p-6`}>
      <div className="flex items-center gap-3 mb-3">
        <span className="text-2xl">{icon}</span>
        <div>
          <h3 className={`text-lg font-semibold ${colors.text}`}>{name}</h3>
          <p className="text-sm text-gray-600">{description}</p>
        </div>
      </div>

      {recommendations.length > 0 && (
        <div className="mt-4">
          <p className="text-sm font-medium text-gray-700 mb-2">Khuyến nghị:</p>
          <ul className="space-y-1">
            {recommendations.map((rec, index) => (
              <li key={index} className="text-sm text-gray-600 flex items-start gap-2">
                <span className="text-gray-400">•</span>
                {rec}
              </li>
            ))}
          </ul>
        </div>
      )}
    </div>
  );
}
