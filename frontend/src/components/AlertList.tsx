import { useState } from 'react';
import { AlertCard } from './AlertCard';
import { AlertFilter } from './AlertFilter';
import { useLanguage } from '../context/LanguageContext';

interface Alert {
  id: string;
  level: string;
  location: string;
  description: string;
  timestamp: string;
}

interface AlertListProps {
  alerts?: Alert[];
}

// Sample data for demonstration
const sampleAlerts: Alert[] = [
  {
    id: 'ALT-001',
    level: 'green',
    location: 'Hà Nội',
    description: 'Thời tiết bình thường, không có nguy hiểm / Normal weather conditions, no hazards detected',
    timestamp: '2026-05-23T10:00:00Z',
  },
  {
    id: 'ALT-002',
    level: 'yellow',
    location: 'Lào Cai',
    description: 'Mưa vừa, gió mạnh cấp 5-6 / Moderate rain, strong wind gusting level 5-6',
    timestamp: '2026-05-23T09:30:00Z',
  },
  {
    id: 'ALT-003',
    level: 'red',
    location: 'Yên Bái',
    description: 'Cảnh báo sạt lở đất, mưa lớn kéo dài / High landslide alert due to continuous heavy rainfall',
    timestamp: '2026-05-23T09:00:00Z',
  },
  {
    id: 'ALT-004',
    level: 'yellow',
    location: 'Sơn La',
    description: 'Nhiệt độ cao bất thường, nguy cơ cháy rừng / Abnormal high temperature, forest fire risk',
    timestamp: '2026-05-23T08:30:00Z',
  },
  {
    id: 'ALT-005',
    level: 'green',
    location: 'Đà Nẵng',
    description: 'Thời tiết tốt, biển lặng / Favorable weather, calm seas',
    timestamp: '2026-05-23T08:00:00Z',
  },
];

export function AlertList({ alerts = sampleAlerts }: AlertListProps) {
  const [filter, setFilter] = useState('all');
  const { t } = useLanguage();

  const filteredAlerts = filter === 'all'
    ? alerts
    : alerts.filter((alert) => alert.level === filter);

  return (
    <div className="space-y-6">
      <AlertFilter activeFilter={filter} onFilterChange={setFilter} />

      {filteredAlerts.length === 0 ? (
        <div className="text-center py-16 bg-white/95 border border-slate-200/90 rounded-2xl shadow-xs">
          <div className="text-5xl mb-4">📭</div>
          <p className="text-slate-800 font-bold text-base">{t('alerts.emptyTitle')}</p>
          <p className="text-sm text-slate-500 mt-1">{t('alerts.emptyDesc')}</p>
        </div>
      ) : (
        <div className="space-y-3">
          {filteredAlerts.map((alert) => (
            <AlertCard
              key={alert.id}
              id={alert.id}
              level={alert.level}
              location={alert.location}
              description={alert.description}
              timestamp={alert.timestamp}
            />
          ))}
        </div>
      )}

      <div className="text-center text-sm text-slate-500 pt-2 font-semibold">
        {t('alerts.showing')} {filteredAlerts.length} / {alerts.length}
      </div>



    </div>
  );
}
