import { useState } from 'react';
import { MapView } from '../components/map/MapView';
import { LSMLegend } from '../components/map/LSMLayer';
import { PrecipitationChart } from '../components/charts/PrecipitationChart';
import { useGeoJSON } from '../hooks/useGeoJSON';

type DataLayer = 'elevation' | 'precipitation' | 'disasters' | 'lsm';

export function ResearchPage() {
  const [activeLayer, setActiveLayer] = useState<DataLayer>('lsm');
  const [riskFilter, setRiskFilter] = useState<string>('');

  const { data: lsmData } = useGeoJSON('lsm', riskFilter ? { risk_level: riskFilter } : undefined);
  const { data: disasterData } = useGeoJSON('disasters');
  const { data: elevationData } = useGeoJSON('elevation');

  const currentData = activeLayer === 'lsm' ? lsmData : 
                      activeLayer === 'disasters' ? disasterData : 
                      elevationData;

  return (
    <div className="space-y-6">
      {/* Header */}
      <div>
        <h2 className="text-2xl font-bold text-white drop-shadow-sm">Research Dashboard</h2>
        <p className="text-slate-300 mt-1">Phân tích dữ liệu GIS và bản đồ nhạy cảm sạt lở</p>
      </div>

      {/* Layer Controls */}
      <div className="flex flex-wrap gap-3">
        <button
          onClick={() => setActiveLayer('lsm')}
          className={`px-4 py-2 rounded-lg text-sm font-medium transition-colors ${
            activeLayer === 'lsm'
              ? 'bg-blue-600 text-white shadow-lg shadow-blue-500/20'
              : 'bg-slate-800/80 text-slate-300 hover:bg-slate-700 border border-white/10'
          }`}
        >
          🗺️ Bản đồ LSM
        </button>
        <button
          onClick={() => setActiveLayer('disasters')}
          className={`px-4 py-2 rounded-lg text-sm font-medium transition-colors ${
            activeLayer === 'disasters'
              ? 'bg-blue-600 text-white shadow-lg shadow-blue-500/20'
              : 'bg-slate-800/80 text-slate-300 hover:bg-slate-700 border border-white/10'
          }`}
        >
          ⚠️ Thiên tai
        </button>
        <button
          onClick={() => setActiveLayer('elevation')}
          className={`px-4 py-2 rounded-lg text-sm font-medium transition-colors ${
            activeLayer === 'elevation'
              ? 'bg-blue-600 text-white shadow-lg shadow-blue-500/20'
              : 'bg-slate-800/80 text-slate-300 hover:bg-slate-700 border border-white/10'
          }`}
        >
          ⛰️ Cao độ
        </button>
      </div>

      {/* Risk Filter for LSM */}
      {activeLayer === 'lsm' && (
        <div className="flex gap-2">
          <button
            onClick={() => setRiskFilter('')}
            className={`px-3 py-1.5 rounded-lg text-sm transition-colors ${
              !riskFilter ? 'bg-slate-700 text-white' : 'bg-slate-800/80 text-slate-400 hover:bg-slate-700 border border-white/10'
            }`}
          >
            Tất cả
          </button>
          <button
            onClick={() => setRiskFilter('low')}
            className={`px-3 py-1.5 rounded-lg text-sm transition-colors ${
              riskFilter === 'low' ? 'bg-green-600 text-white' : 'bg-slate-800/80 text-slate-400 hover:bg-slate-700 border border-white/10'
            }`}
          >
            Thấp
          </button>
          <button
            onClick={() => setRiskFilter('medium')}
            className={`px-3 py-1.5 rounded-lg text-sm transition-colors ${
              riskFilter === 'medium' ? 'bg-yellow-600 text-white' : 'bg-slate-800/80 text-slate-400 hover:bg-slate-700 border border-white/10'
            }`}
          >
            Trung bình
          </button>
          <button
            onClick={() => setRiskFilter('high')}
            className={`px-3 py-1.5 rounded-lg text-sm transition-colors ${
              riskFilter === 'high' ? 'bg-red-600 text-white' : 'bg-slate-800/80 text-slate-400 hover:bg-slate-700 border border-white/10'
            }`}
          >
            Cao
          </button>
        </div>
      )}

      {/* Map and Legend */}
      <div className="grid grid-cols-1 lg:grid-cols-4 gap-6">
        <div className="lg:col-span-3">
          <MapView
            geojson={currentData}
            onFeatureClick={(feature) => console.log('Feature clicked:', feature)}
          />
        </div>
        <div className="space-y-4">
          <LSMLegend />
          
          {/* Summary Stats */}
          <div className="bg-slate-900/50 backdrop-blur-md border border-white/10 rounded-xl shadow-lg p-4">
            <h4 className="font-semibold text-slate-100 mb-3">Thống kê</h4>
            <div className="space-y-2">
              <div className="flex justify-between">
                <span className="text-sm text-slate-400">Tổng điểm dữ liệu:</span>
                <span className="text-sm font-medium text-slate-200">{currentData?.features?.length || 0}</span>
              </div>
              <div className="flex justify-between">
                <span className="text-sm text-slate-400">Lớp dữ liệu:</span>
                <span className="text-sm font-medium text-slate-200 capitalize">{activeLayer}</span>
              </div>
            </div>
          </div>
        </div>
      </div>

      {/* Charts */}
      <div className="grid grid-cols-1 lg:grid-cols-2 gap-6">
        <PrecipitationChart />
        
        {/* Risk Distribution */}
        <div className="bg-slate-900/50 backdrop-blur-md border border-white/10 rounded-xl shadow-lg p-6">
          <h3 className="text-lg font-semibold text-slate-100 mb-4">Phân bố rủi ro</h3>
          <div className="space-y-4">
            <div>
              <div className="flex justify-between mb-1">
                <span className="text-sm text-slate-300">Thấp</span>
                <span className="text-sm text-green-400">40%</span>
              </div>
              <div className="w-full bg-slate-800 rounded-full h-2">
                <div className="bg-green-500 h-2 rounded-full" style={{ width: '40%' }} />
              </div>
            </div>
            <div>
              <div className="flex justify-between mb-1">
                <span className="text-sm text-slate-300">Trung bình</span>
                <span className="text-sm text-yellow-400">35%</span>
              </div>
              <div className="w-full bg-slate-800 rounded-full h-2">
                <div className="bg-yellow-500 h-2 rounded-full" style={{ width: '35%' }} />
              </div>
            </div>
            <div>
              <div className="flex justify-between mb-1">
                <span className="text-sm text-slate-300">Cao</span>
                <span className="text-sm text-red-400">25%</span>
              </div>
              <div className="w-full bg-slate-800 rounded-full h-2">
                <div className="bg-red-500 h-2 rounded-full" style={{ width: '25%' }} />
              </div>
            </div>
          </div>
        </div>
      </div>
    </div>
  );
}
