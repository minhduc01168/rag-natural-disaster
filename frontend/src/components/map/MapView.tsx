import { useEffect } from 'react';
import { MapContainer, TileLayer, GeoJSON, useMap } from 'react-leaflet';
import L from 'leaflet';
import 'leaflet/dist/leaflet.css';

// Automatically resize Leaflet map on mount
function MapResizer() {
  const map = useMap();
  useEffect(() => {
    map.invalidateSize();
    const timer = setTimeout(() => {
      map.invalidateSize();
    }, 250);
    return () => clearTimeout(timer);
  }, [map]);
  return null;
}

// Fix Leaflet default icon issue
delete (L.Icon.Default.prototype as any)._getIconUrl;
L.Icon.Default.mergeOptions({
  iconRetinaUrl: 'https://cdnjs.cloudflare.com/ajax/libs/leaflet/1.7.1/images/marker-icon-2x.png',
  iconUrl: 'https://cdnjs.cloudflare.com/ajax/libs/leaflet/1.7.1/images/marker-icon.png',
  shadowUrl: 'https://cdnjs.cloudflare.com/ajax/libs/leaflet/1.7.1/images/marker-shadow.png',
});

interface GeoJSONData {
  type: string;
  features: any[];
}

interface MapViewProps {
  center?: [number, number];
  zoom?: number;
  geojson?: GeoJSONData | null;
  onFeatureClick?: (feature: any) => void;
}

const riskColors: Record<string, string> = {
  low: '#22c55e',
  medium: '#eab308',
  high: '#ef4444',
};

export function MapView({ center = [21.0285, 105.8542], zoom = 10, geojson, onFeatureClick }: MapViewProps) {
  const geoJsonStyle = (feature: any) => {
    const riskLevel = feature.properties?.risk_level;
    return {
      fillColor: riskColors[riskLevel] || '#3b82f6',
      weight: 2,
      opacity: 1,
      color: 'white',
      fillOpacity: 0.7,
    };
  };

  const onEachFeature = (feature: any, layer: L.Layer) => {
    if (feature.properties) {
      const popupContent = Object.entries(feature.properties)
        .map(([key, value]) => `<strong>${key}:</strong> ${value}`)
        .join('<br/>');
      
      layer.bindPopup(popupContent);
    }

    layer.on('click', () => {
      if (onFeatureClick) {
        onFeatureClick(feature);
      }
    });
  };

  return (
    <MapContainer
      center={center}
      zoom={zoom}
      className="w-full h-[500px] rounded-xl overflow-hidden"
      style={{ width: '100%', height: '500px' }}
    >
      <MapResizer />
      <TileLayer
        attribution='Tiles &copy; Esri &mdash; Esri, USGS, NOAA'
        url="https://server.arcgisonline.com/ArcGIS/rest/services/World_Topo_Map/MapServer/tile/{z}/{y}/{x}"
        maxZoom={18}
      />
      
      {geojson && geojson.features.length > 0 && (
        <GeoJSON
          key={JSON.stringify(geojson)}
          data={geojson as any}
          style={geoJsonStyle}
          onEachFeature={onEachFeature}
        />
      )}
    </MapContainer>
  );
}
