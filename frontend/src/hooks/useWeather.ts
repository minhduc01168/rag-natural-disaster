import { useState, useEffect, useCallback } from 'react';
import { apiUrl } from '../config/api';

interface WeatherData {
  temperature: number;
  humidity: number;
  wind_speed: number;
  condition: string;
  location_name: string;
  rainfall: number;
}

interface AlertData {
  level: string;
  name: string;
  description: string;
  recommendations: string[];
}

interface UseWeatherReturn {
  weather: WeatherData | null;
  alert: AlertData | null;
  loading: boolean;
  error: string | null;
  refetch: () => void;
}

export function useWeather(lat: number = 21.0285, lon: number = 105.8542): UseWeatherReturn {
  const [weather, setWeather] = useState<WeatherData | null>(null);
  const [alert, setAlert] = useState<AlertData | null>(null);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState<string | null>(null);

  const fetchWeather = useCallback(async () => {
    setLoading(true);
    setError(null);

    try {
      const response = await fetch(apiUrl(`/api/v1/fast-lane/weather/${lat}/${lon}`));
      if (!response.ok) {
        throw new Error('Failed to fetch weather data');
      }

      const data = await response.json();
      if (data.status === 'success') {
        setWeather(data.data);
        setAlert(data.alert);
      } else {
        throw new Error(data.message || 'Unknown error');
      }
    } catch (err) {
      setError(err instanceof Error ? err.message : 'Network error');
      // Set fallback data
      setWeather({
        temperature: 28.5,
        humidity: 75,
        wind_speed: 12,
        condition: 'Nhiều mây',
        location_name: `Vị trí (${lat.toFixed(2)}, ${lon.toFixed(2)})`,
        rainfall: 0,
      });
      setAlert({
        level: 'green',
        name: 'An toàn',
        description: 'Thời tiết bình thường',
        recommendations: ['Thời tiết thuận lợi'],
      });
    } finally {
      setLoading(false);
    }
  }, [lat, lon]);

  useEffect(() => {
    fetchWeather();
  }, [fetchWeather]);

  return { weather, alert, loading, error, refetch: fetchWeather };
}
