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
    <div className={`bg-white/5 backdrop-blur-xl border border-white/10 rounded-2xl p-6 shadow-2xl relative overflow-hidden group hover:bg-white/10 transition-all duration-300 ${className}`}>
      <h3 className="text-xl font-semibold text-white mb-6 flex items-center gap-2">
        <span className="bg-gradient-to-r from-blue-400 to-teal-300 bg-clip-text text-transparent">Lượng mưa theo thời gian</span>
      </h3>
      
      <div className="relative z-10">
        <ResponsiveContainer width="100%" height={300}>
          <LineChart data={data}>
            <CartesianGrid strokeDasharray="3 3" stroke="#ffffff1a" vertical={false} />
            <XAxis
              dataKey="date"
              tick={{ fill: '#94a3b8', fontSize: 12 }}
              tickFormatter={(value) => value.split('-')[2]}
              axisLine={{ stroke: '#ffffff1a' }}
              tickLine={{ stroke: '#ffffff1a' }}
            />
            <YAxis
              tick={{ fill: '#94a3b8', fontSize: 12 }}
              axisLine={{ stroke: '#ffffff1a' }}
              tickLine={{ stroke: '#ffffff1a' }}
              label={{ value: 'mm', angle: -90, position: 'insideLeft', fill: '#94a3b8' }}
            />
            <Tooltip
              contentStyle={{ backgroundColor: 'rgba(15, 23, 42, 0.9)', borderColor: 'rgba(255,255,255,0.1)', borderRadius: '12px', color: '#fff' }}
              labelFormatter={(value) => `Ngày: ${value}`}
              formatter={(value: any) => [`${Number(value).toFixed(1)} mm`, 'Lượng mưa']}
            />
            <Legend wrapperStyle={{ paddingTop: '20px', color: '#94a3b8' }} />
            <Line
              type="monotone"
              dataKey="amount"
              name="Lượng mưa"
              stroke="#2dd4bf"
              strokeWidth={3}
              dot={{ r: 4, fill: '#0f172a', stroke: '#2dd4bf', strokeWidth: 2 }}
              activeDot={{ r: 6, fill: '#2dd4bf', stroke: '#fff', strokeWidth: 2 }}
              animationDuration={1500}
            />
          </LineChart>
        </ResponsiveContainer>
      </div>
    </div>
  );
}
