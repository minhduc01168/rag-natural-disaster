import { useState } from 'react';
import { MapView } from '../components/map/MapView';
import { LSMLegend } from '../components/map/LSMLayer';
import { PrecipitationChart } from '../components/charts/PrecipitationChart';
import { useGeoJSON } from '../hooks/useGeoJSON';
import { useLanguage } from '../context/LanguageContext';

type DataLayer = 'elevation' | 'precipitation' | 'disasters' | 'lsm';

export function ResearchPage() {
  const [activeLayer, setActiveLayer] = useState<DataLayer>('lsm');
  const [riskFilter, setRiskFilter] = useState<string>('');
  const { t } = useLanguage();

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
        <h2 className="text-3xl font-bold text-white drop-shadow-sm">{t('research.title')}</h2>
        <p className="text-slate-300 mt-1 text-sm">{t('research.subtitle')}</p>
      </div>

      {/* Layer Controls */}
      <div className="flex flex-wrap gap-3">
        <button
          onClick={() => setActiveLayer('lsm')}
          className={`px-4 py-2.5 rounded-xl text-sm font-semibold transition-all shadow-sm ${
            activeLayer === 'lsm'
              ? 'bg-blue-600 text-white shadow-blue-500/20 scale-105'
              : 'bg-slate-800/80 text-slate-300 hover:bg-slate-700 hover:text-white border border-slate-700 hover:border-slate-500'
          }`}
        >
          {t('research.layerLsm')}
        </button>
        <button
          onClick={() => setActiveLayer('disasters')}
          className={`px-4 py-2.5 rounded-xl text-sm font-semibold transition-all shadow-sm ${
            activeLayer === 'disasters'
              ? 'bg-blue-600 text-white shadow-blue-500/20 scale-105'
              : 'bg-slate-800/80 text-slate-300 hover:bg-slate-700 hover:text-white border border-slate-700 hover:border-slate-500'
          }`}
        >
          {t('research.layerDisaster')}
        </button>
        <button
          onClick={() => setActiveLayer('elevation')}
          className={`px-4 py-2.5 rounded-xl text-sm font-semibold transition-all shadow-sm ${
            activeLayer === 'elevation'
              ? 'bg-blue-600 text-white shadow-blue-500/20 scale-105'
              : 'bg-slate-800/80 text-slate-300 hover:bg-slate-700 hover:text-white border border-slate-700 hover:border-slate-500'
          }`}
        >
          {t('research.layerElevation')}
        </button>
      </div>

      {/* Risk Filter for LSM */}
      {activeLayer === 'lsm' && (
        <div className="flex flex-wrap gap-2 pt-1">
          <button
            onClick={() => setRiskFilter('')}
            className={`px-3.5 py-1.5 rounded-xl text-xs font-semibold transition-all shadow-sm ${
              !riskFilter ? 'bg-slate-700 text-white scale-105 border border-slate-500' : 'bg-slate-800/80 text-slate-400 hover:bg-slate-700 hover:text-white border border-slate-700'
            }`}
          >
            {t('alerts.filterAll')}
          </button>
          <button
            onClick={() => setRiskFilter('low')}
            className={`px-3.5 py-1.5 rounded-xl text-xs font-semibold transition-all shadow-sm ${
              riskFilter === 'low' ? 'bg-emerald-600 text-white scale-105 border border-emerald-500' : 'bg-slate-800/80 text-slate-400 hover:bg-slate-700 hover:text-white border border-slate-700'
            }`}
          >
            {t('alerts.riskLow')}
          </button>
          <button
            onClick={() => setRiskFilter('medium')}
            className={`px-3.5 py-1.5 rounded-xl text-xs font-semibold transition-all shadow-sm ${
              riskFilter === 'medium' ? 'bg-amber-600 text-white scale-105 border border-amber-500' : 'bg-slate-800/80 text-slate-400 hover:bg-slate-700 hover:text-white border border-slate-700'
            }`}
          >
            {t('alerts.riskMedium')}
          </button>
          <button
            onClick={() => setRiskFilter('high')}
            className={`px-3.5 py-1.5 rounded-xl text-xs font-semibold transition-all shadow-sm ${
              riskFilter === 'high' ? 'bg-rose-600 text-white scale-105 border border-rose-500' : 'bg-slate-800/80 text-slate-400 hover:bg-slate-700 hover:text-white border border-slate-700'
            }`}
          >
            {t('alerts.riskHigh')}
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
          <div className="bg-slate-900/50 backdrop-blur-md border border-white/10 rounded-2xl shadow-lg p-5">
            <h4 className="font-semibold text-white mb-3 text-base flex items-center gap-2">
              <span>📊</span> {t('research.statsTitle')}
            </h4>
            <div className="space-y-2.5">
              <div className="flex justify-between items-center">
                <span className="text-sm text-slate-400">{t('research.totalPoints')}</span>
                <span className="text-sm font-bold text-blue-400 font-mono bg-blue-500/10 px-2 py-0.5 rounded-lg border border-blue-500/20">{currentData?.features?.length || 0}</span>
              </div>
              <div className="flex justify-between items-center">
                <span className="text-sm text-slate-400">{t('research.dataLayer')}</span>
                <span className="text-sm font-semibold text-slate-200 uppercase tracking-wider bg-slate-800 px-2 py-0.5 rounded-lg">{activeLayer}</span>
              </div>
            </div>
          </div>
        </div>
      </div>

      {/* Charts */}
      <div className="grid grid-cols-1 lg:grid-cols-2 gap-6">
        <PrecipitationChart />
        
        {/* Risk Distribution */}
        <div className="bg-slate-900/50 backdrop-blur-md border border-white/10 rounded-2xl shadow-lg p-6">
          <h3 className="text-lg font-bold text-white mb-4 flex items-center gap-2">
            <span>📈</span> {t('research.riskDist')}
          </h3>
          <div className="space-y-4">
            <div>
              <div className="flex justify-between mb-1">
                <span className="text-sm font-medium text-slate-300">{t('alerts.riskLow')}</span>
                <span className="text-sm font-bold text-emerald-400 font-mono">40%</span>
              </div>
              <div className="w-full bg-slate-800 rounded-full h-2.5 overflow-hidden border border-white/5">
                <div className="bg-gradient-to-r from-emerald-500 to-green-400 h-full rounded-full transition-all duration-500" style={{ width: '40%' }} />
              </div>
            </div>
            <div>
              <div className="flex justify-between mb-1">
                <span className="text-sm font-medium text-slate-300">{t('alerts.riskMedium')}</span>
                <span className="text-sm font-bold text-amber-400 font-mono">35%</span>
              </div>
              <div className="w-full bg-slate-800 rounded-full h-2.5 overflow-hidden border border-white/5">
                <div className="bg-gradient-to-r from-amber-500 to-yellow-400 h-full rounded-full transition-all duration-500" style={{ width: '35%' }} />
              </div>
            </div>
            <div>
              <div className="flex justify-between mb-1">
                <span className="text-sm font-medium text-slate-300">{t('alerts.riskHigh')}</span>
                <span className="text-sm font-bold text-rose-400 font-mono">25%</span>
              </div>
              <div className="w-full bg-slate-800 rounded-full h-2.5 overflow-hidden border border-white/5">
                <div className="bg-gradient-to-r from-rose-500 to-red-400 h-full rounded-full transition-all duration-500" style={{ width: '25%' }} />
              </div>
            </div>
          </div>
        </div>
      </div>
    </div>
  );
}
