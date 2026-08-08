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
          <div className="animate-spin rounded-full h-12 w-12 border-b-2 border-blue-600 mx-auto"></div>
          <p className="mt-4 text-slate-600 font-medium">{t('common.loading')}</p>
        </div>
      </div>
    );
  }

  return (
    <div className="space-y-6">
      {/* Header */}
      <div className="flex flex-col sm:flex-row sm:items-center justify-between gap-4">
        <div>
          <h2 className="text-3xl font-black text-slate-900 tracking-tight">{t('home.title')}</h2>
          <div className="flex items-center gap-2 mt-1">
            <span className="text-xs bg-blue-100 text-blue-800 border border-blue-200/80 px-3 py-1 rounded-full font-semibold shadow-xs">
              📍 {weather?.location_name || t('weather.location')}
            </span>
            <span className="text-slate-500 text-sm hidden sm:inline">· {t('home.subtitle')}</span>
          </div>
        </div>
        <button
          onClick={refetch}
          className="flex items-center gap-2 px-4 py-2.5 bg-white hover:bg-slate-50 border border-slate-200/90 hover:border-slate-300 rounded-xl text-sm font-semibold text-slate-700 hover:text-slate-900 transition-all shadow-xs hover:scale-105 active:scale-95 shrink-0 self-start sm:self-auto"
          title={t('common.refresh')}
        >
          <svg className="w-4 h-4 text-blue-600" fill="none" stroke="currentColor" viewBox="0 0 24 24">
            <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M4 4v5h.582m15.356 2A8.001 8.001 0 004.582 9m0 0H9m11 11v-5h-.581m0 0a8.003 8.003 0 01-15.357-2m15.357 2H15" />
          </svg>
          <span>{t('common.refresh')}</span>
        </button>
      </div>

      {/* Error message */}
      {error && (
        <div className="bg-amber-50 border border-amber-200/90 rounded-2xl p-4 shadow-xs">
          <p className="text-amber-800 text-sm font-medium">⚠️ {error} - Đang hiển thị dữ liệu mẫu</p>
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



