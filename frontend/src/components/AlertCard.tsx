import { useLanguage } from '../context/LanguageContext';

interface AlertCardProps {
  id: string;
  level: string;
  location: string;
  description: string;
  timestamp: string;
}

const levelColors: Record<string, { bg: string; border: string; text: string; badge: string; desc: string }> = {
  green: {
    bg: 'bg-emerald-50/90',
    border: 'border-emerald-500',
    text: 'text-emerald-950',
    desc: 'text-emerald-900',
    badge: 'bg-emerald-100 border-emerald-300 text-emerald-800 font-bold',
  },
  yellow: {
    bg: 'bg-amber-50/90',
    border: 'border-amber-500',
    text: 'text-amber-950',
    desc: 'text-amber-900',
    badge: 'bg-amber-100 border-amber-300 text-amber-800 font-bold',
  },
  red: {
    bg: 'bg-rose-50/90',
    border: 'border-rose-500',
    text: 'text-rose-950',
    desc: 'text-rose-900',
    badge: 'bg-rose-100 border-rose-300 text-rose-800 font-bold',
  },
};

export function AlertCard({ id, level, location, description, timestamp }: AlertCardProps) {
  const { t, lang } = useLanguage();
  const colors = levelColors[level] || levelColors.green;

  const getLabel = (lvl: string) => {
    if (lvl === 'red') return t('alerts.riskHigh');
    if (lvl === 'yellow') return t('alerts.riskMedium');
    return t('alerts.riskLow');
  };

  return (
    <div className={`${colors.bg} border-l-4 ${colors.border} border border-slate-200/90 rounded-2xl p-5 shadow-sm hover:shadow-md transition-all duration-200`}>
      <div className="flex flex-col sm:flex-row sm:items-start justify-between gap-2">
        <div className="flex-1 min-w-0">
          <div className="flex items-center gap-2 mb-2 flex-wrap">
            <span className={`text-xs px-2.5 py-0.5 rounded-full border ${colors.badge}`}>
              {getLabel(level)}
            </span>
            <span className="text-xs text-slate-400 font-mono font-semibold">#{id}</span>
          </div>
          <p className={`${colors.text} font-black text-base tracking-tight`}>{location}</p>
          <p className={`text-sm ${colors.desc} mt-1 leading-relaxed font-medium`}>{description}</p>
        </div>
        <span className="text-xs text-slate-500 whitespace-nowrap sm:ml-4 font-mono self-end sm:self-auto mt-2 sm:mt-0 font-medium">
          {new Date(timestamp).toLocaleString(lang === 'en' ? 'en-US' : 'vi-VN')}
        </span>
      </div>
    </div>
  );
}



