import { useLanguage } from '../context/LanguageContext';

interface AlertCardProps {
  id: string;
  level: string;
  location: string;
  description: string;
  timestamp: string;
}

const levelColors: Record<string, { bg: string; border: string; text: string; badge: string }> = {
  green: {
    bg: 'bg-emerald-950/40',
    border: 'border-emerald-500',
    text: 'text-emerald-400',
    badge: 'bg-emerald-500/10 border-emerald-500/20 text-emerald-400',
  },
  yellow: {
    bg: 'bg-amber-950/40',
    border: 'border-amber-500',
    text: 'text-amber-400',
    badge: 'bg-amber-500/10 border-amber-500/20 text-amber-400',
  },
  red: {
    bg: 'bg-rose-950/40',
    border: 'border-rose-500',
    text: 'text-rose-400',
    badge: 'bg-rose-500/10 border-rose-500/20 text-rose-400',
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
    <div className={`${colors.bg} border-l-4 ${colors.border} border border-white/8 rounded-2xl p-5 backdrop-blur-md shadow-lg hover:border-slate-600 transition-all duration-200`}>
      <div className="flex flex-col sm:flex-row sm:items-start justify-between gap-2">
        <div className="flex-1 min-w-0">
          <div className="flex items-center gap-2 mb-2 flex-wrap">
            <span className={`text-xs font-bold px-2.5 py-0.5 rounded-full border ${colors.badge}`}>
              {getLabel(level)}
            </span>
            <span className="text-xs text-slate-400 font-mono">#{id}</span>
          </div>
          <p className="text-white font-semibold text-base">{location}</p>
          <p className="text-sm text-slate-300 mt-1 leading-relaxed">{description}</p>
        </div>
        <span className="text-xs text-slate-400 whitespace-nowrap sm:ml-4 font-mono self-end sm:self-auto mt-2 sm:mt-0">
          {new Date(timestamp).toLocaleString(lang === 'en' ? 'en-US' : 'vi-VN')}
        </span>
      </div>
    </div>
  );
}
