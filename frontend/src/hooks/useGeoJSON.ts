import { useState, useEffect, useCallback } from 'react';

interface GeoJSONFeature {
  type: string;
  geometry: {
    type: string;
    coordinates: number[] | number[][] | number[][][];
  };
  properties: Record<string, any>;
}

interface GeoJSONData {
  type: string;
  features: GeoJSONFeature[];
  metadata?: Record<string, any>;
}

interface UseGeoJSONReturn {
  data: GeoJSONData | null;
  loading: boolean;
  error: string | null;
  refetch: () => void;
}

const API_BASE_URL = 'http://localhost:8000';

export function useGeoJSON(endpoint: string, params?: Record<string, string>): UseGeoJSONReturn {
  const [data, setData] = useState<GeoJSONData | null>(null);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState<string | null>(null);

  const fetchData = useCallback(async () => {
    setLoading(true);
    setError(null);

    try {
      const url = new URL(`${API_BASE_URL}/api/v1/gis/${endpoint}`);
      if (params) {
        Object.entries(params).forEach(([key, value]) => {
          if (value) url.searchParams.append(key, value);
        });
      }

      const response = await fetch(url.toString());
      if (!response.ok) {
        throw new Error(`Failed to fetch: ${response.statusText}`);
      }

      const result = await response.json();
      setData(result);
    } catch (err) {
      setError(err instanceof Error ? err.message : 'Unknown error');
      // Set empty GeoJSON as fallback
      setData({
        type: 'FeatureCollection',
        features: [],
      });
    } finally {
      setLoading(false);
    }
  }, [endpoint, params]);

  useEffect(() => {
    fetchData();
  }, [fetchData]);

  return { data, loading, error, refetch: fetchData };
}
