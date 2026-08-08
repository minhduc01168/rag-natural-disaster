import disasterData from '../data/disaster_data.json';

export interface WeatherStation {
  id: string;
  name: string;
  province: string;
  lat: number;
  lng: number;
  rainfall24h: number;
  rainfall72h: number;
  status: 'Safe' | 'Alert' | 'Danger';
  lastUpdated?: string;
  isLive?: boolean;
}

export interface LandslideHotspot {
  id: string;
  location: string;
  province: string;
  lat: number;
  lng: number;
  riskLevel: 'Safe' | 'Alert' | 'Danger';
  radiusMeters: number;
  date: string;
  details: string;
}

/**
  * Calculate risk status based on 24h & 72h accumulated rainfall threshold matrix:
  * - Danger (Red): 24h > 150mm OR 72h > 300mm
  * - Alert (Yellow): 24h >= 50mm OR 72h >= 200mm
  * - Safe (Green): 24h < 50mm
  */
export function calculateRiskStatus(rainfall24h: number, rainfall72h: number): 'Safe' | 'Alert' | 'Danger' {
  if (rainfall24h > 150 || rainfall72h > 300) return 'Danger';
  if (rainfall24h >= 50 || rainfall72h >= 200) return 'Alert';
  return 'Safe';
}

/**
  * Fetch live weather & precipitation data from Open-Meteo API for a specific station coordinates
  */
export async function fetchLiveStationPrecipitation(station: typeof disasterData.vrain_stations[0]): Promise<WeatherStation> {
  try {
    const url = `https://api.open-meteo.com/v1/forecast?latitude=${station.lat}&longitude=${station.lng}&current=precipitation,rain&daily=precipitation_sum&timezone=Asia%2FBangkok`;
    const response = await fetch(url);
    
    if (!response.ok) {
      throw new Error(`Open-Meteo API error: ${response.statusText}`);
    }

    const data = await response.json();
    const dailySums: number[] = data.daily?.precipitation_sum || [];
    
    // Day 0 = today (24h), Sum of Day 0..2 = 72h accumulation
    const rain24h = Math.round((dailySums[0] || station.rainfall24h) * 10) / 10;
    const rain72h = Math.round((dailySums.slice(0, 3).reduce((acc, val) => acc + val, 0) || station.rainfall72h) * 10) / 10;
    const computedStatus = calculateRiskStatus(rain24h, rain72h);

    return {
      ...station,
      status: computedStatus as 'Safe' | 'Alert' | 'Danger',
      rainfall24h: rain24h > 0 ? rain24h : station.rainfall24h,
      rainfall72h: rain72h > 0 ? rain72h : station.rainfall72h,
      lastUpdated: new Date().toLocaleTimeString('vi-VN'),
      isLive: true,
    };
  } catch (error) {
    console.warn(`[Open-Meteo] Fallback to local schema for station ${station.name}:`, error);
    return {
      ...station,
      status: station.status as 'Safe' | 'Alert' | 'Danger',
      lastUpdated: new Date().toLocaleTimeString('vi-VN') + ' (Local Fallback)',
      isLive: false,
    };
  }
}

/**
  * Fetch live precipitation data for all stations in parallel
  */
export async function fetchAllStationsLive(): Promise<WeatherStation[]> {
  const promises = disasterData.vrain_stations.map(station => fetchLiveStationPrecipitation(station));
  return Promise.all(promises);
}
