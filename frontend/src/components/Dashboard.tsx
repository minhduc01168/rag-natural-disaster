import { useWeather } from '../hooks/useWeather';
import { WeatherCard } from './WeatherCard';
import { AlertStatus } from './AlertStatus';
import { SOSButton } from './SOSButton';

export function Dashboard() {
  const { weather, alert, loading, error, refetch } = useWeather();

  if (loading) {
    return (
      <div className="flex items-center justify-center min-h-[400px]">
        <div className="text-center">
          <div className="animate-spin rounded-full h-12 w-12 border-b-2 border-primary-600 mx-auto"></div>
          <p className="mt-4 text-gray-600">Đang tải dữ liệu thời tiết...</p>
        </div>
      </div>
    );
  }

  return (
    <div className="space-y-6">
      {/* Header */}
      <div className="flex items-center justify-between">
        <div>
          <h2 className="text-2xl font-bold text-gray-900">Dashboard</h2>
          <p className="text-gray-600">{weather?.location_name || 'Đang tải...'}</p>
        </div>
        <button
          onClick={refetch}
          className="p-2 text-gray-500 hover:text-gray-700 hover:bg-gray-100 rounded-lg transition-colors"
          title="Làm mới"
        >
          <svg className="w-5 h-5" fill="none" stroke="currentColor" viewBox="0 0 24 24">
            <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M4 4v5h.582m15.356 2A8.001 8.001 0 004.582 9m0 0H9m11 11v-5h-.581m0 0a8.003 8.003 0 01-15.357-2m15.357 2H15" />
          </svg>
        </button>
      </div>

      {/* Error message */}
      {error && (
        <div className="bg-yellow-50 border border-yellow-200 rounded-lg p-4">
          <p className="text-yellow-700 text-sm">⚠️ {error} - Hiển thị dữ liệu mẫu</p>
        </div>
      )}

      {/* SOS Button */}
      <SOSButton />

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

      {/* Quick Actions */}
      <div className="grid grid-cols-2 gap-4">
        <a
          href="/alerts"
          className="bg-white rounded-xl shadow-md p-4 hover:shadow-lg transition-shadow text-center"
        >
          <span className="text-2xl">📢</span>
          <p className="mt-2 font-medium text-gray-900">Cảnh báo</p>
        </a>
        <a
          href="/survival"
          className="bg-white rounded-xl shadow-md p-4 hover:shadow-lg transition-shadow text-center"
        >
          <span className="text-2xl">📖</span>
          <p className="mt-2 font-medium text-gray-900">Cẩm nang</p>
        </a>
      </div>
    </div>
  );
}
