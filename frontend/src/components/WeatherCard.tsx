interface WeatherCardProps {
  temperature: number;
  humidity: number;
  wind_speed: number;
  condition: string;
  rainfall: number;
}

export function WeatherCard({ temperature, humidity, wind_speed, condition, rainfall }: WeatherCardProps) {
  return (
    <div className="bg-white rounded-xl shadow-md p-6">
      <h3 className="text-lg font-semibold text-gray-900 mb-4">Thời tiết hiện tại</h3>
      
      <div className="grid grid-cols-2 gap-4">
        <div className="flex items-center gap-3">
          <div className="w-10 h-10 bg-blue-100 rounded-lg flex items-center justify-center">
            <span className="text-xl">🌡️</span>
          </div>
          <div>
            <p className="text-sm text-gray-500">Nhiệt độ</p>
            <p className="text-xl font-bold text-gray-900">{temperature}°C</p>
          </div>
        </div>

        <div className="flex items-center gap-3">
          <div className="w-10 h-10 bg-cyan-100 rounded-lg flex items-center justify-center">
            <span className="text-xl">💧</span>
          </div>
          <div>
            <p className="text-sm text-gray-500">Độ ẩm</p>
            <p className="text-xl font-bold text-gray-900">{humidity}%</p>
          </div>
        </div>

        <div className="flex items-center gap-3">
          <div className="w-10 h-10 bg-teal-100 rounded-lg flex items-center justify-center">
            <span className="text-xl">💨</span>
          </div>
          <div>
            <p className="text-sm text-gray-500">Gió</p>
            <p className="text-xl font-bold text-gray-900">{wind_speed} km/h</p>
          </div>
        </div>

        <div className="flex items-center gap-3">
          <div className="w-10 h-10 bg-purple-100 rounded-lg flex items-center justify-center">
            <span className="text-xl">🌧️</span>
          </div>
          <div>
            <p className="text-sm text-gray-500">Mưa</p>
            <p className="text-xl font-bold text-gray-900">{rainfall} mm</p>
          </div>
        </div>
      </div>

      <div className="mt-4 pt-4 border-t border-gray-100">
        <p className="text-sm text-gray-500">Tình trạng</p>
        <p className="text-lg font-medium text-gray-700">{condition}</p>
      </div>
    </div>
  );
}
