import {
  LineChart,
  Line,
  XAxis,
  YAxis,
  CartesianGrid,
  Tooltip,
  Legend,
  ResponsiveContainer,
} from 'recharts';

interface PrecipitationData {
  date: string;
  amount: number;
}

interface PrecipitationChartProps {
  data?: PrecipitationData[];
  className?: string;
}

// Mock data for demonstration
const mockData: PrecipitationData[] = Array.from({ length: 30 }, (_, i) => ({
  date: `2026-01-${(i + 1).toString().padStart(2, '0')}`,
  amount: Math.random() * 50 + 5,
}));

export function PrecipitationChart({ data = mockData, className }: PrecipitationChartProps) {
  return (
    <div className={`bg-white rounded-xl shadow-md p-6 ${className}`}>
      <h3 className="text-lg font-semibold text-gray-900 mb-4">Lượng mưa theo thời gian</h3>
      
      <ResponsiveContainer width="100%" height={300}>
        <LineChart data={data}>
          <CartesianGrid strokeDasharray="3 3" />
          <XAxis
            dataKey="date"
            tick={{ fontSize: 12 }}
            tickFormatter={(value) => value.split('-')[2]}
          />
          <YAxis
            label={{ value: 'mm', angle: -90, position: 'insideLeft' }}
          />
          <Tooltip
            labelFormatter={(value) => `Ngày: ${value}`}
            formatter={(value: number) => [`${value.toFixed(1)} mm`, 'Lượng mưa']}
          />
          <Legend />
          <Line
            type="monotone"
            dataKey="amount"
            name="Lượng mưa"
            stroke="#3b82f6"
            strokeWidth={2}
            dot={{ r: 3 }}
            activeDot={{ r: 5 }}
          />
        </LineChart>
      </ResponsiveContainer>
    </div>
  );
}
