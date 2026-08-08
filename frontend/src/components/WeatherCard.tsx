import { useLanguage } from '../context/LanguageContext';

interface WeatherCardProps {
  temperature: number;
  humidity: number;
  wind_speed: number;
  condition: string;
  rainfall: number;
}

export function WeatherCard({ temperature, humidity, wind_speed, condition, rainfall }: WeatherCardProps) {
  const { t } = useLanguage();

  return (
    <div className="bg-white/95 backdrop-blur-md border border-slate-200/90 rounded-2xl p-6 shadow-md hover:shadow-lg transition-all duration-300 relative overflow-hidden group">
      {/* Ambient sky decoration */}
      <div className="absolute top-0 right-0 -mr-8 -mt-8 w-36 h-36 rounded-full bg-blue-100/70 blur-3xl group-hover:bg-blue-200/70 transition-all pointer-events-none"></div>
      <div className="absolute bottom-0 left-0 -ml-8 -mb-8 w-36 h-36 rounded-full bg-teal-100/70 blur-3xl group-hover:bg-teal-200/70 transition-all pointer-events-none"></div>

      <h3 className="text-xl font-black text-slate-900 mb-6 relative z-10 flex items-center gap-2">
        <span className="bg-gradient-to-r from-blue-700 via-sky-600 to-teal-600 bg-clip-text text-transparent">{t('weather.title')}</span>
      </h3>
      
      <div className="grid grid-cols-2 sm:grid-cols-4 gap-4 relative z-10">
        <div className="flex items-center gap-4 bg-slate-50 rounded-xl p-3.5 border border-slate-200/80 hover:bg-slate-100/80 transition-colors">
          <div className="w-12 h-12 bg-gradient-to-br from-orange-400 to-red-500 rounded-xl flex items-center justify-center shadow-sm shrink-0">
            <span className="text-2xl drop-shadow-md">🌡️</span>
          </div>
          <div className="min-w-0">
            <p className="text-[11px] text-slate-500 uppercase tracking-wider font-semibold truncate">{t('weather.currentTemp')}</p>
            <p className="text-xl sm:text-2xl font-black text-slate-900 tracking-tight">{temperature}°C</p>
          </div>
        </div>

        <div className="flex items-center gap-4 bg-slate-50 rounded-xl p-3.5 border border-slate-200/80 hover:bg-slate-100/80 transition-colors">
          <div className="w-12 h-12 bg-gradient-to-br from-cyan-400 to-blue-500 rounded-xl flex items-center justify-center shadow-sm shrink-0">
            <span className="text-2xl drop-shadow-md">💧</span>
          </div>
          <div className="min-w-0">
            <p className="text-[11px] text-slate-500 uppercase tracking-wider font-semibold truncate">{t('weather.humidity')}</p>
            <p className="text-xl sm:text-2xl font-black text-slate-900 tracking-tight">{humidity}%</p>
          </div>
        </div>

        <div className="flex items-center gap-4 bg-slate-50 rounded-xl p-3.5 border border-slate-200/80 hover:bg-slate-100/80 transition-colors">
          <div className="w-12 h-12 bg-gradient-to-br from-teal-400 to-emerald-500 rounded-xl flex items-center justify-center shadow-sm shrink-0">
            <span className="text-2xl drop-shadow-md">💨</span>
          </div>
          <div className="min-w-0">
            <p className="text-[11px] text-slate-500 uppercase tracking-wider font-semibold truncate">{t('weather.windSpeed')}</p>
            <p className="text-xl sm:text-2xl font-black text-slate-900 tracking-tight">{wind_speed} <span className="text-xs font-semibold text-slate-600">km/h</span></p>
          </div>
        </div>

        <div className="flex items-center gap-4 bg-slate-50 rounded-xl p-3.5 border border-slate-200/80 hover:bg-slate-100/80 transition-colors">
          <div className="w-12 h-12 bg-gradient-to-br from-indigo-400 to-purple-500 rounded-xl flex items-center justify-center shadow-sm shrink-0">
            <span className="text-2xl drop-shadow-md">🌧️</span>
          </div>
          <div className="min-w-0">
            <p className="text-[11px] text-slate-500 uppercase tracking-wider font-semibold truncate">{t('weather.rainfall')}</p>
            <p className="text-xl sm:text-2xl font-black text-slate-900 tracking-tight">{rainfall} <span className="text-xs font-semibold text-slate-600">mm</span></p>
          </div>
        </div>
      </div>

      <div className="mt-6 pt-5 border-t border-slate-200/80 relative z-10 flex items-center justify-between">
        <div>
          <p className="text-xs text-slate-500 uppercase tracking-wider font-semibold">{t('weather.statusLabel')}</p>
          <p className="text-xl font-extrabold text-slate-900 tracking-tight mt-0.5">{condition}</p>
        </div>
        <div className="w-10 h-10 bg-blue-50 rounded-full flex items-center justify-center animate-pulse border border-blue-100">
          <span className="text-xl">🌤️</span>
        </div>
      </div>
    </div>
  );
}



