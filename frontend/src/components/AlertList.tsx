import { useState } from 'react';
import { AlertCard } from './AlertCard';
import { AlertFilter } from './AlertFilter';

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
    description: 'Thời tiết bình thường, không có nguy hiểm',
    timestamp: '2026-05-23T10:00:00Z',
  },
  {
    id: 'ALT-002',
    level: 'yellow',
    location: 'Lào Cai',
    description: 'Mưa vừa, gió mạnh cấp 5-6',
    timestamp: '2026-05-23T09:30:00Z',
  },
  {
    id: 'ALT-003',
    level: 'red',
    location: 'Yên Bái',
    description: 'Cảnh báo sạt lở đất, mưa lớn kéo dài',
    timestamp: '2026-05-23T09:00:00Z',
  },
  {
    id: 'ALT-004',
    level: 'yellow',
    location: 'Sơn La',
    description: 'Nhiệt độ cao bất thường, nguy cơ cháy rừng',
    timestamp: '2026-05-23T08:30:00Z',
  },
  {
    id: 'ALT-005',
    level: 'green',
    location: 'Đà Nẵng',
    description: 'Thời tiết tốt, biển lặng',
    timestamp: '2026-05-23T08:00:00Z',
  },
];

export function AlertList({ alerts = sampleAlerts }: AlertListProps) {
  const [filter, setFilter] = useState('all');

  const filteredAlerts = filter === 'all'
    ? alerts
    : alerts.filter((alert) => alert.level === filter);

  return (
    <div className="space-y-4">
      <AlertFilter activeFilter={filter} onFilterChange={setFilter} />

      {filteredAlerts.length === 0 ? (
        <div className="text-center py-12">
          <div className="text-4xl mb-4">📭</div>
          <p className="text-gray-500">Không có cảnh báo nào</p>
          <p className="text-sm text-gray-400 mt-1">Hệ thống đang theo dõi thời tiết...</p>
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

      <div className="text-center text-sm text-gray-400 pt-4">
        Hiển thị {filteredAlerts.length} / {alerts.length} cảnh báo
      </div>
    </div>
  );
}
