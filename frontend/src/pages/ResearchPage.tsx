import { useState, useEffect } from 'react';

import { MapContainer, TileLayer, Marker, Popup, Circle } from 'react-leaflet';
import { BarChart, Bar, XAxis, YAxis, CartesianGrid, Tooltip, Legend, ResponsiveContainer } from 'recharts';
import L from 'leaflet';

import 'leaflet/dist/leaflet.css';

// Custom Leaflet Markers
const landslideRedIcon = L.divIcon({
  className: 'custom-leaflet-marker-red',
  html: `<div style="background-color: #ef4444; width: 18px; height: 18px; border-radius: 50%; border: 3px solid white; box-shadow: 0 0 10px rgba(239,68,68,0.8); animate: pulse;"></div>`,
  iconSize: [18, 18],
  iconAnchor: [9, 9],
});

const landslideYellowIcon = L.divIcon({
  className: 'custom-leaflet-marker-yellow',
  html: `<div style="background-color: #f59e0b; width: 16px; height: 16px; border-radius: 50%; border: 2.5px solid white; box-shadow: 0 0 8px rgba(245,158,11,0.7);"></div>`,
  iconSize: [16, 16],
  iconAnchor: [8, 8],
});

const stationBlueIcon = L.divIcon({
  className: 'custom-leaflet-marker-blue',
  html: `<div style="background-color: #0284c7; width: 22px; height: 22px; border-radius: 50%; border: 3px solid white; box-shadow: 0 0 10px rgba(2,132,199,0.8); display: flex; align-items: center; justify-content: center; color: white; font-size: 10px;">🌧️</div>`,
  iconSize: [22, 22],
  iconAnchor: [11, 11],
});

import disasterData from '../data/disaster_data.json';
import { fetchAllStationsLive, WeatherStation } from '../services/weatherService';

const HDX_LANDSLIDE_HOTSPOTS = disasterData.hdx_landslide_hotspots;

export function ResearchPage() {
  const [selectedProvince, setSelectedProvince] = useState<string>('All');
  const [selectedRisk, setSelectedRisk] = useState<string>('All');
  const [stations, setStations] = useState<WeatherStation[]>(disasterData.vrain_stations as WeatherStation[]);
  const [isLoadingLive, setIsLoadingLive] = useState<boolean>(false);
  const [isLive, setIsLive] = useState<boolean>(true);
  const [lastUpdated, setLastUpdated] = useState<string>(new Date().toLocaleTimeString('vi-VN'));

  const loadLiveData = async () => {
    setIsLoadingLive(true);
    try {
      const liveData = await fetchAllStationsLive();
      setStations(liveData);
      setLastUpdated(new Date().toLocaleTimeString('vi-VN'));
    } catch (e) {
      console.warn('Failed to load live data:', e);
    } finally {
      setIsLoadingLive(false);
    }
  };

  // Real-time Auto Refresh Polling (Refresh every 30 seconds from Open-Meteo API)
  useEffect(() => {
    loadLiveData();
    if (!isLive) return;
    const interval = setInterval(() => {
      loadLiveData();
    }, 30000);
    return () => clearInterval(interval);
  }, [isLive]);

  const filteredHotspots = HDX_LANDSLIDE_HOTSPOTS.filter(h => {
    const matchProv = selectedProvince === 'All' || h.province === selectedProvince;
    const matchRisk = selectedRisk === 'All' || h.riskLevel === selectedRisk;
    return matchProv && matchRisk;
  });

  const filteredStations = stations.filter(s => {
    return selectedProvince === 'All' || s.province === selectedProvince;
  });

  const chartData = stations.map(s => ({
    name: s.name.replace('Trạm ', ''),
    'Lượng mưa 24h (mm)': s.rainfall24h,
    'Lượng mưa tích lũy 72h (mm)': s.rainfall72h,
  }));


  return (
    <div className="space-y-6">
      {/* Header */}
      <div className="flex flex-col md:flex-row md:items-center justify-between gap-4">
        <div>
          <h2 className="text-3xl font-black text-slate-900 tracking-tight">Research Dashboard</h2>
          <p className="text-slate-500 mt-1 text-sm font-medium">
            Số hóa bản đồ nguy cơ sạt lở đất (HDX/Bộ TN&MT) và phân tích lượng mưa tích lũy trạm quan trắc (VRAIN)
          </p>
        </div>

        {/* Live Realtime Indicator Pill */}
        <div className="flex items-center gap-3 bg-white/90 border border-slate-200/90 px-4 py-2 rounded-2xl shadow-xs shrink-0 self-start md:self-auto">
          <button
            onClick={() => setIsLive(!isLive)}
            className={`flex items-center gap-2 px-3 py-1 rounded-xl text-xs font-extrabold transition-all ${
              isLive
                ? 'bg-rose-50 text-rose-700 border border-rose-200'
                : 'bg-slate-100 text-slate-600 border border-slate-200'
            }`}
          >
            <span className={`w-2.5 h-2.5 rounded-full ${isLive ? 'bg-rose-600 animate-ping' : 'bg-slate-400'}`}></span>
            {isLive ? '🔴 LIVE OPEN-METEO (ON)' : '⚪ TẮT AUTO REFRESH'}
          </button>

          <button
            onClick={loadLiveData}
            disabled={isLoadingLive}
            className="p-1.5 bg-slate-100 hover:bg-slate-200 rounded-lg text-slate-600 transition-all disabled:opacity-50"
            title="Làm mới dữ liệu từ Open-Meteo API"
          >
            <span className={`inline-block ${isLoadingLive ? 'animate-spin' : ''}`}>🔄</span>
          </button>

          <span className="text-xs text-slate-500 font-semibold">Cập nhật: {lastUpdated}</span>
        </div>
      </div>



      {/* Filter Bar */}
      <div className="bg-white/95 backdrop-blur-md border border-slate-200/90 rounded-2xl p-4 shadow-sm flex flex-col sm:flex-row sm:items-center justify-between gap-4">
        <div className="flex items-center gap-3 flex-wrap">
          <span className="text-xs font-bold uppercase tracking-wider text-slate-500">Lọc theo Tỉnh:</span>
          {['All', 'Lào Cai', 'Yên Bái', 'Hà Giang', 'Sơn La', 'Cao Bằng'].map((prov) => (
            <button
              key={prov}
              onClick={() => setSelectedProvince(prov)}
              className={`px-3 py-1.5 rounded-xl text-xs font-bold transition-all ${
                selectedProvince === prov
                  ? 'bg-blue-600 text-white shadow-xs scale-105'
                  : 'bg-slate-100 text-slate-700 hover:bg-slate-200 border border-slate-200/80'
              }`}
            >
              {prov === 'All' ? 'Tất cả các tỉnh' : prov}
            </button>
          ))}
        </div>

        <div className="flex items-center gap-2">
          <span className="text-xs font-bold uppercase tracking-wider text-slate-500">Nguy cơ:</span>
          {['All', 'Danger', 'Alert'].map((risk) => (
            <button
              key={risk}
              onClick={() => setSelectedRisk(risk)}
              className={`px-3 py-1.5 rounded-xl text-xs font-bold transition-all ${
                selectedRisk === risk
                  ? risk === 'Danger'
                    ? 'bg-rose-600 text-white shadow-xs'
                    : risk === 'Alert'
                    ? 'bg-amber-600 text-white shadow-xs'
                    : 'bg-blue-600 text-white shadow-xs'
                  : 'bg-slate-100 text-slate-700 hover:bg-slate-200 border border-slate-200/80'
              }`}
            >
              {risk === 'All' ? 'Tất cả' : risk === 'Danger' ? '🔴 Nguy hiểm' : '🟡 Cảnh giác'}
            </button>
          ))}
        </div>
      </div>

      {/* Main Map & Legend Section */}
      <div className="grid grid-cols-1 lg:grid-cols-4 gap-6">
        {/* Leaflet Map (3 cols) */}
        <div className="lg:col-span-3 bg-white/95 backdrop-blur-md border border-slate-200/90 rounded-2xl p-4 shadow-md flex flex-col">
          <div className="flex items-center justify-between mb-3 px-2">
            <h3 className="text-lg font-black text-slate-900 flex items-center gap-2">
              <span>🗺️</span> Bản đồ Khoanh vùng Nguy cơ Sạt lở (GIS Leaflet)
            </h3>
            <span className="text-xs bg-blue-50 text-blue-700 border border-blue-200 px-2.5 py-1 rounded-full font-bold">
              Hiển thị: {filteredHotspots.length} Điểm nóng sạt lở & {filteredStations.length} Trạm VRAIN
            </span>
          </div>

          <div className="w-full h-[480px] rounded-xl overflow-hidden border border-slate-200 shadow-inner relative z-0">
            <MapContainer
              center={[22.1, 104.5]}
              zoom={8}
              scrollWheelZoom={false}
              className="w-full h-full"
            >
              <TileLayer
                attribution='&copy; <a href="https://www.openstreetmap.org/copyright">OpenStreetMap</a> contributors'
                url="https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png"
              />

              {/* VRAIN Rain Gauge Station Markers */}
              {filteredStations.map((station) => (
                <Marker
                  key={station.id}
                  position={[station.lat, station.lng]}
                  icon={stationBlueIcon}
                >
                  <Popup>
                    <div className="p-1 text-slate-900">
                      <p className="font-bold text-sm text-blue-700">🌧️ {station.name}</p>
                      <p className="text-xs text-slate-600 mt-1 font-medium">Tỉnh: {station.province}</p>
                      <div className="mt-2 pt-2 border-t border-slate-200 text-xs font-semibold space-y-1">
                        <p className="text-slate-800">Lượng mưa 24h: <span className="font-extrabold text-blue-600">{station.rainfall24h} mm</span></p>
                        <p className="text-slate-800">Tích lũy 72h: <span className="font-extrabold text-indigo-600">{station.rainfall72h} mm</span></p>
                      </div>
                    </div>
                  </Popup>
                </Marker>
              ))}

              {/* HDX Landslide Hotspots & Buffer Risk Polygons (Circle Overlays) */}
              {filteredHotspots.map((hotspot) => (
                <div key={hotspot.id}>
                  {/* Circle Buffer Overlay (Khoanh vùng nguy cơ sạt lở 1.8km - 3.5km) */}
                  <Circle
                    center={[hotspot.lat, hotspot.lng]}
                    radius={hotspot.radiusMeters}
                    pathOptions={{
                      color: hotspot.riskLevel === 'Danger' ? '#ef4444' : '#f59e0b',
                      fillColor: hotspot.riskLevel === 'Danger' ? '#ef4444' : '#f59e0b',
                      fillOpacity: 0.25,
                      weight: 2,
                      dashArray: '6, 6',
                    }}
                  />
                  {/* Point Marker */}
                  <Marker
                    position={[hotspot.lat, hotspot.lng]}
                    icon={hotspot.riskLevel === 'Danger' ? landslideRedIcon : landslideYellowIcon}
                  >
                    <Popup>
                      <div className="p-1 text-slate-900">
                        <div className="flex items-center gap-1.5 mb-1">
                          <span className={`text-[10px] px-2 py-0.5 rounded font-extrabold text-white ${hotspot.riskLevel === 'Danger' ? 'bg-rose-600' : 'bg-amber-600'}`}>
                            {hotspot.riskLevel === 'Danger' ? '🔴 NGUY HIỂM' : '🟡 CẢNH GIÁC'}
                          </span>
                          <span className="text-xs font-bold text-slate-500">{hotspot.date}</span>
                        </div>
                        <p className="font-extrabold text-sm text-slate-900">{hotspot.location}</p>
                        <p className="text-xs text-slate-600 mt-1 font-medium leading-relaxed">{hotspot.details}</p>
                        <p className="text-[11px] text-rose-700 mt-2 font-bold bg-rose-50 p-1.5 rounded border border-rose-200">
                          ⚠️ Bán kính nguy cơ sạt trượt bão hòa đất: {(hotspot.radiusMeters / 1000).toFixed(1)} km
                        </p>
                      </div>
                    </Popup>
                  </Marker>
                </div>
              ))}
            </MapContainer>
          </div>
        </div>

        {/* Legend & Statistics Sidebar (1 col) */}
        <div className="space-y-4">
          <div className="bg-white/95 backdrop-blur-md border border-slate-200/90 rounded-2xl p-5 shadow-sm">
            <h4 className="font-black text-slate-900 text-sm mb-3 uppercase tracking-wider">📌 Chú giải Bản đồ GIS</h4>
            <div className="space-y-3 text-xs">
              <div className="flex items-start gap-2.5">
                <div className="w-4 h-4 rounded-full bg-rose-500 border-2 border-white shadow-xs shrink-0 mt-0.5"></div>
                <div>
                  <p className="font-bold text-slate-900">🔴 Tâm sạt lở nguy hiểm (HDX)</p>
                  <p className="text-slate-500">Vùng có hiện trạng sạt trượt & nứt đất lớn</p>
                </div>
              </div>

              <div className="flex items-start gap-2.5">
                <div className="w-4 h-4 rounded-full bg-amber-500 border-2 border-white shadow-xs shrink-0 mt-0.5"></div>
                <div>
                  <p className="font-bold text-slate-900">🟡 Tâm sạt lở cảnh giác</p>
                  <p className="text-slate-500">Mái taluy đường & khe suối dốc cao</p>
                </div>
              </div>

              <div className="flex items-start gap-2.5">
                <div className="w-4 h-4 rounded-full bg-rose-500/20 border border-rose-500 border-dashed shrink-0 mt-0.5"></div>
                <div>
                  <p className="font-bold text-slate-900">⭕ Vùng khoanh nguy cơ (1-3km)</p>
                  <p className="text-slate-500">Diện tích bão hòa nước có rủi ro trượt lở lan tỏa</p>
                </div>
              </div>

              <div className="flex items-start gap-2.5">
                <div className="w-4 h-4 rounded-full bg-sky-600 border-2 border-white shadow-xs shrink-0 mt-0.5"></div>
                <div>
                  <p className="font-bold text-slate-900">🌧️ Trạm quan trắc mưa (VRAIN)</p>
                  <p className="text-slate-500">Đo lượng mưa tự động thời gian thực</p>
                </div>
              </div>
            </div>
          </div>

          <div className="bg-white/95 backdrop-blur-md border border-slate-200/90 rounded-2xl p-5 shadow-sm">
            <h4 className="font-black text-slate-900 text-sm mb-3 uppercase tracking-wider">📊 Phân tích Ngưỡng mưa</h4>
            <div className="space-y-2.5 text-xs font-medium">
              <div className="bg-slate-50 p-2.5 rounded-xl border border-slate-200/80">
                <p className="text-slate-900 font-bold">🟢 Mức An toàn (&lt;50mm/24h):</p>
                <p className="text-slate-600 mt-0.5">Đất chưa bão hòa nước. Rủi ro thấp.</p>
              </div>

              <div className="bg-amber-50 p-2.5 rounded-xl border border-amber-200">
                <p className="text-amber-900 font-bold">🟡 Mức Cảnh giác (50-150mm/24h):</p>
                <p className="text-amber-800 mt-0.5">Mưa tích lũy 72h &gt;200mm. Nguy cơ trượt taluy.</p>
              </div>

              <div className="bg-rose-50 p-2.5 rounded-xl border border-rose-200">
                <p className="text-rose-950 font-bold">🔴 Mức Khẩn cấp (&gt;150mm/24h):</p>
                <p className="text-rose-900 mt-0.5">Mưa tích lũy 72h &gt;300mm. Kích hoạt sơ tán ngay!</p>
              </div>
            </div>
          </div>
        </div>
      </div>

      {/* Precipitation Bar Chart Section */}
      <div className="bg-white/95 backdrop-blur-md border border-slate-200/90 rounded-2xl p-6 shadow-md">
        <h3 className="text-xl font-black text-slate-900 mb-2 flex items-center gap-2">
          <span>📈</span> Biểu đồ Lượng mưa Tích lũy Trạm Quan trắc VRAIN
        </h3>
        <p className="text-xs text-slate-500 mb-6 font-medium">
          So sánh lượng mưa 24 giờ và lượng mưa tích lũy 72 giờ tại các trạm trọng điểm vùng cao
        </p>

        <div className="w-full h-80">
          <ResponsiveContainer width="100%" height="100%">
            <BarChart data={chartData} margin={{ top: 10, right: 30, left: 0, bottom: 0 }}>
              <CartesianGrid strokeDasharray="3 3" stroke="#e2e8f0" />
              <XAxis dataKey="name" stroke="#64748b" fontSize={12} tickLine={false} />
              <YAxis stroke="#64748b" fontSize={12} unit=" mm" />
              <Tooltip
                contentStyle={{ backgroundColor: '#ffffff', borderRadius: '12px', border: '1px solid #cbd5e1', boxShadow: '0 4px 12px rgba(0,0,0,0.1)' }}
              />
              <Legend wrapperStyle={{ paddingTop: '10px' }} />
              <Bar dataKey="Lượng mưa 24h (mm)" fill="#0284c7" radius={[6, 6, 0, 0]} />
              <Bar dataKey="Lượng mưa tích lũy 72h (mm)" fill="#4f46e5" radius={[6, 6, 0, 0]} />
            </BarChart>
          </ResponsiveContainer>
        </div>
      </div>
    </div>
  );
}
