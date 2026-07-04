import { useWeather } from '../hooks/useWeather';
import { WeatherCard } from './WeatherCard';
import { AlertStatus } from './AlertStatus';
import { useLanguage } from '../context/LanguageContext';

export function Dashboard() {
  const { weather, alert, loading, error, refetch } = useWeather();
  const { t } = useLanguage();

  if (loading) {
    return (
      <div className="flex items-center justify-center min-h-[400px]">
        <div className="text-center">
          <div className="animate-spin rounded-full h-12 w-12 border-b-2 border-blue-500 mx-auto"></div>
          <p className="mt-4 text-slate-300">{t('common.loading')}</p>
        </div>
      </div>
    );
  }

  return (
    <div className="space-y-6">
      {/* Header */}
      <div className="flex flex-col sm:flex-row sm:items-center justify-between gap-4">
        <div>
          <h2 className="text-3xl font-bold text-white drop-shadow-sm">{t('home.title')}</h2>
          <div className="flex items-center gap-2 mt-1">
            <span className="text-xs bg-blue-500/10 text-blue-400 border border-blue-500/20 px-2.5 py-0.5 rounded-full font-medium">
              📍 {weather?.location_name || t('weather.location')}
            </span>
            <span className="text-slate-400 text-sm hidden sm:inline">· {t('home.subtitle')}</span>
          </div>
        </div>
        <button
          onClick={refetch}
          className="flex items-center gap-2 px-4 py-2.5 bg-slate-800/80 hover:bg-slate-700 border border-slate-700 hover:border-slate-500 rounded-xl text-sm font-semibold text-slate-200 hover:text-white transition-all shadow-sm hover:scale-105 active:scale-95 shrink-0 self-start sm:self-auto"
          title={t('common.refresh')}
        >
          <svg className="w-4 h-4" fill="none" stroke="currentColor" viewBox="0 0 24 24">
            <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M4 4v5h.582m15.356 2A8.001 8.001 0 004.582 9m0 0H9m11 11v-5h-.581m0 0a8.003 8.003 0 01-15.357-2m15.357 2H15" />
          </svg>
          <span>{t('common.refresh')}</span>
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
