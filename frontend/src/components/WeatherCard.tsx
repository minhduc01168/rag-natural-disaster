interface WeatherCardProps {
  temperature: number;
  humidity: number;
  wind_speed: number;
  condition: string;
  rainfall: number;
}

export function WeatherCard({ temperature, humidity, wind_speed, condition, rainfall }: WeatherCardProps) {
  return (
    <div className="bg-white/5 backdrop-blur-xl border border-white/10 rounded-2xl p-6 shadow-2xl relative overflow-hidden group hover:bg-white/10 transition-all duration-300">
      {/* Background decoration */}
      <div className="absolute top-0 right-0 -mr-8 -mt-8 w-32 h-32 rounded-full bg-blue-500/20 blur-2xl group-hover:bg-blue-400/30 transition-all"></div>
      <div className="absolute bottom-0 left-0 -ml-8 -mb-8 w-32 h-32 rounded-full bg-teal-500/20 blur-2xl group-hover:bg-teal-400/30 transition-all"></div>

      <h3 className="text-xl font-semibold text-white mb-6 relative z-10 flex items-center gap-2">
        <span className="bg-gradient-to-r from-blue-400 to-teal-300 bg-clip-text text-transparent">Thời tiết hiện tại</span>
      </h3>
      
      <div className="grid grid-cols-2 gap-4 relative z-10">
        <div className="flex items-center gap-4 bg-white/5 rounded-xl p-3 border border-white/5 hover:bg-white/10 transition-colors">
          <div className="w-12 h-12 bg-gradient-to-br from-orange-400 to-red-500 rounded-xl flex items-center justify-center shadow-lg">
            <span className="text-2xl drop-shadow-md">🌡️</span>
          </div>
          <div>
            <p className="text-xs text-slate-400 uppercase tracking-wider font-medium">Nhiệt độ</p>
            <p className="text-2xl font-bold text-white tracking-tight">{temperature}°C</p>
          </div>
        </div>

        <div className="flex items-center gap-4 bg-white/5 rounded-xl p-3 border border-white/5 hover:bg-white/10 transition-colors">
          <div className="w-12 h-12 bg-gradient-to-br from-cyan-400 to-blue-500 rounded-xl flex items-center justify-center shadow-lg">
            <span className="text-2xl drop-shadow-md">💧</span>
          </div>
          <div>
            <p className="text-xs text-slate-400 uppercase tracking-wider font-medium">Độ ẩm</p>
            <p className="text-2xl font-bold text-white tracking-tight">{humidity}%</p>
          </div>
        </div>

        <div className="flex items-center gap-4 bg-white/5 rounded-xl p-3 border border-white/5 hover:bg-white/10 transition-colors">
          <div className="w-12 h-12 bg-gradient-to-br from-teal-400 to-emerald-500 rounded-xl flex items-center justify-center shadow-lg">
            <span className="text-2xl drop-shadow-md">💨</span>
          </div>
          <div>
            <p className="text-xs text-slate-400 uppercase tracking-wider font-medium">Gió</p>
            <p className="text-2xl font-bold text-white tracking-tight">{wind_speed} km/h</p>
          </div>
        </div>

        <div className="flex items-center gap-4 bg-white/5 rounded-xl p-3 border border-white/5 hover:bg-white/10 transition-colors">
          <div className="w-12 h-12 bg-gradient-to-br from-indigo-400 to-purple-500 rounded-xl flex items-center justify-center shadow-lg">
            <span className="text-2xl drop-shadow-md">🌧️</span>
          </div>
          <div>
            <p className="text-xs text-slate-400 uppercase tracking-wider font-medium">Lượng mưa</p>
            <p className="text-2xl font-bold text-white tracking-tight">{rainfall} mm</p>
          </div>
        </div>
      </div>

      <div className="mt-6 pt-5 border-t border-white/10 relative z-10 flex items-center justify-between">
        <div>
          <p className="text-xs text-slate-400 uppercase tracking-wider font-medium">Tình trạng</p>
          <p className="text-xl font-bold text-white tracking-tight mt-1">{condition}</p>
        </div>
        <div className="w-10 h-10 bg-white/10 rounded-full flex items-center justify-center animate-pulse">
          <span className="text-xl">🌤️</span>
        </div>
      </div>
    </div>
  );
}
