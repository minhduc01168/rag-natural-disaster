interface AlertFilterProps {
  activeFilter: string;
  onFilterChange: (filter: string) => void;
}

const filters = [
  { key: 'all', label: 'Tất cả' },
  { key: 'green', label: 'An toàn' },
  { key: 'yellow', label: 'Cảnh giác' },
  { key: 'red', label: 'Nguy hiểm' },
];

export function AlertFilter({ activeFilter, onFilterChange }: AlertFilterProps) {
  return (
    <div className="flex flex-wrap gap-2">
      {filters.map((filter) => (
        <button
          key={filter.key}
          onClick={() => onFilterChange(filter.key)}
          className={`px-4 py-2 rounded-lg text-sm font-medium transition-colors ${
            activeFilter === filter.key
              ? 'bg-primary-600 text-white'
              : 'bg-white text-gray-700 hover:bg-gray-100 border border-gray-200'
          }`}
        >
          {filter.label}
        </button>
      ))}
    </div>
  );
}
