import { SurvivalGuide } from '../data/survivalGuides';
import { useLanguage } from '../context/LanguageContext';

interface GuideContentProps {
  guide: SurvivalGuide;
  onBack: () => void;
}

export function GuideContent({ guide, onBack }: GuideContentProps) {
  const { t } = useLanguage();

  return (
    <div className="bg-slate-800/80 backdrop-blur-xl border border-slate-700 rounded-2xl shadow-2xl p-6 text-slate-100">
      <button
        onClick={onBack}
        className="flex items-center gap-2 text-slate-300 hover:text-white bg-slate-900/60 hover:bg-slate-700 px-4 py-2 rounded-xl text-sm font-semibold border border-slate-700 transition-all shadow-sm hover:scale-105 active:scale-95 mb-6"
      >
        <svg className="w-4 h-4" fill="none" stroke="currentColor" viewBox="0 0 24 24">
          <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M15 19l-7-7 7-7" />
        </svg>
        <span>{t('survival.back')}</span>
      </button>

      <div className="flex items-center gap-4 mb-6 pb-6 border-b border-white/10">
        <span className="text-4xl p-3 bg-blue-500/10 rounded-2xl border border-blue-500/20">{guide.icon}</span>
        <div>
          <h2 className="text-2xl font-bold text-white drop-shadow-sm">{guide.title}</h2>
          <p className="text-slate-300 mt-1 text-sm">{guide.description}</p>
        </div>
      </div>

      <div>
        <h3 className="font-semibold text-blue-400 mb-4 text-base flex items-center gap-2">
          <span>📌</span> {t('survival.guideLabel')}
        </h3>
        <ol className="space-y-4">
          {guide.content.map((step, index) => (
            <li key={index} className="flex items-start gap-3.5 bg-slate-900/40 p-4 rounded-xl border border-white/5">
              <span className="w-7 h-7 bg-blue-600 text-white rounded-full flex items-center justify-center text-sm font-bold shrink-0 shadow-md">
                {index + 1}
              </span>
              <span className="text-slate-200 text-base leading-relaxed pt-0.5">{step.replace(/^\d+\.\s*/, '')}</span>
            </li>
          ))}
        </ol>
      </div>

      <div className="mt-8 p-4 bg-amber-500/10 rounded-xl border border-amber-500/30 flex items-start gap-3">
        <span className="text-2xl shrink-0">⚠️</span>
        <p className="text-sm text-amber-300 leading-relaxed pt-0.5">
          <strong>{t('survival.warningNote')}:</strong> {guide.title} - Trong trường hợp khẩn cấp, hãy liên hệ ngay số khẩn cấp cứu hộ cứu nạn quốc gia (112 / 115).
        </p>
      </div>
    </div>
  );
}
