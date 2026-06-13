import { useWeather } from '../hooks/useWeather';
import { WeatherCard } from './WeatherCard';
import { AlertStatus } from './AlertStatus';

export function Dashboard() {
  const { weather, alert, loading, error, refetch } = useWeather();

  if (loading) {
    return (
      <div className="flex items-center justify-center min-h-[400px]">
        <div className="text-center">
          <div className="animate-spin rounded-full h-12 w-12 border-b-2 border-blue-500 mx-auto"></div>
          <p className="mt-4 text-slate-300">Đang tải dữ liệu thời tiết...</p>
        </div>
      </div>
    );
  }

  return (
    <div className="space-y-6">
      {/* Header */}
      <div className="flex items-center justify-between">
        <div>
          <h2 className="text-3xl font-bold text-white drop-shadow-sm">Dashboard</h2>
          <p className="text-slate-300 mt-1">{weather?.location_name || 'Đang tải...'}</p>
        </div>
        <button
          onClick={refetch}
          className="p-2 text-slate-300 hover:text-white hover:bg-white/10 rounded-lg transition-all"
          title="Làm mới"
        >
          <svg className="w-6 h-6" fill="none" stroke="currentColor" viewBox="0 0 24 24">
            <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M4 4v5h.582m15.356 2A8.001 8.001 0 004.582 9m0 0H9m11 11v-5h-.581m0 0a8.003 8.003 0 01-15.357-2m15.357 2H15" />
          </svg>
        </button>
      </div>

      {/* Error message */}
      {error && (
        <div className="bg-red-500/10 backdrop-blur-md border border-red-500/20 rounded-xl p-4">
          <p className="text-red-400 text-sm">⚠️ {error} - Đang hiển thị dữ liệu mẫu</p>
        </div>
      )}



      {/* Alert Status */}
      {alert && (
        <AlertStatus
          level={alert.level}
          name={alert.name}
          description={alert.description}
          recommendations={alert.recommendations}
        />
      )}

      {/* Weather Card */}
      {weather && (
        <WeatherCard
          temperature={weather.temperature}
          humidity={weather.humidity}
          wind_speed={weather.wind_speed}
          condition={weather.condition}
          rainfall={weather.rainfall}
        />
      )}


    </div>
  );
}
