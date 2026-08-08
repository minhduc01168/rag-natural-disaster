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
          className={`px-4 py-2 rounded-xl text-sm font-semibold transition-all shadow-xs ${
            activeFilter === filter.key
              ? 'bg-blue-600 text-white shadow-md shadow-blue-500/20 scale-105 font-bold'
              : 'bg-white text-slate-700 hover:bg-slate-50 hover:text-slate-900 border border-slate-200/90'
          }`}
        >
          {filter.label}
        </button>
      ))}
    </div>
  );
}



