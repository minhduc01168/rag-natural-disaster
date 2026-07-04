import { useLanguage } from '../context/LanguageContext';

interface AlertFilterProps {
  activeFilter: string;
  onFilterChange: (filter: string) => void;
}

export function AlertFilter({ activeFilter, onFilterChange }: AlertFilterProps) {
  const { t } = useLanguage();

  const filters = [
    { key: 'all', label: t('alerts.filterAll') },
    { key: 'green', label: t('alerts.riskLow') },
    { key: 'yellow', label: t('alerts.riskMedium') },
    { key: 'red', label: t('alerts.riskHigh') },
  ];

  return (
    <div className="flex flex-wrap gap-2">
      {filters.map((filter) => (
        <button
          key={filter.key}
          onClick={() => onFilterChange(filter.key)}
          className={`px-4 py-2 rounded-xl text-sm font-semibold transition-all shadow-sm ${
            activeFilter === filter.key
              ? 'bg-blue-600 text-white shadow-blue-500/20 scale-105'
              : 'bg-slate-800/80 text-slate-300 hover:bg-slate-700 hover:text-white border border-slate-700 hover:border-slate-500'
          }`}
        >
          {filter.label}
        </button>
      ))}
    </div>
  );
}
