import { useState } from 'react';
import { CategoryCard } from '../components/CategoryCard';
import { GuideContent } from '../components/GuideContent';
import { categories, getGuidesByCategory, searchGuides, SurvivalGuide } from '../data/survivalGuides';
import { useLanguage } from '../context/LanguageContext';

type ViewState = 'categories' | 'category-detail' | 'guide-detail';

export function SurvivalPage() {
  const [viewState, setViewState] = useState<ViewState>('categories');
  const [selectedCategory, setSelectedCategory] = useState<string | null>(null);
  const [selectedGuide, setSelectedGuide] = useState<SurvivalGuide | null>(null);
  const [searchQuery, setSearchQuery] = useState('');
  const { t } = useLanguage();

  const handleCategoryClick = (categoryId: string) => {
    setSelectedCategory(categoryId);
    setViewState('category-detail');
  };

  const handleGuideClick = (guide: SurvivalGuide) => {
    setSelectedGuide(guide);
    setViewState('guide-detail');
  };

  const handleBack = () => {
    if (viewState === 'guide-detail') {
      setViewState('category-detail');
      setSelectedGuide(null);
    } else {
      setViewState('categories');
      setSelectedCategory(null);
    }
  };

  const filteredGuides = searchQuery ? searchGuides(searchQuery) : [];
  const categoryGuides = selectedCategory ? getGuidesByCategory(selectedCategory) : [];

  return (
    <div className="space-y-6">
      {/* Header */}
      <div>
        <h2 className="text-3xl font-black text-slate-900">{t('survival.title')}</h2>
        <p className="text-slate-500 mt-1 text-sm">{t('survival.subtitle')}</p>
      </div>

      {/* Search Bar */}
      <div className="relative">
        <input
          type="text"
          placeholder={t('survival.searchPlaceholder')}
          value={searchQuery}
          onChange={(e) => setSearchQuery(e.target.value)}
          className="w-full px-4 py-3.5 pl-11 bg-white text-slate-900 rounded-2xl border border-slate-200/90 focus:outline-none focus:ring-2 focus:ring-blue-500 focus:border-transparent placeholder-slate-400 shadow-sm transition-all font-medium"
        />
        <svg
          className="absolute left-4 top-4 w-5 h-5 text-slate-400"
          fill="none"
          stroke="currentColor"
          viewBox="0 0 24 24"
        >
          <path
            strokeLinecap="round"
            strokeLinejoin="round"
            strokeWidth={2}
            d="M21 21l-6-6m2-5a7 7 0 11-14 0 7 7 0 0114 0z"
          />
        </svg>
      </div>

      {/* Search Results */}
      {searchQuery && (
        <div className="space-y-3">
          <h3 className="font-bold text-slate-800">{t('survival.searchResults')} ({filteredGuides.length})</h3>
          {filteredGuides.length === 0 ? (
            <p className="text-slate-500 py-4 text-center bg-white rounded-xl border border-slate-200/90 shadow-xs">{t('survival.noResults')}</p>
          ) : (
            filteredGuides.map((guide) => (
              <button
                key={guide.id}
                onClick={() => handleGuideClick(guide)}
                className="w-full text-left bg-white/95 rounded-xl p-4 hover:bg-slate-50 transition-all border border-slate-200/90 hover:border-blue-400 shadow-xs hover:scale-[1.005]"
              >
                <div className="flex items-center gap-3.5">
                  <span className="text-3xl">{guide.icon}</span>
                  <div>
                    <p className="font-bold text-slate-900">{guide.title}</p>
                    <p className="text-sm text-slate-600 mt-0.5">{guide.description}</p>
                  </div>
                </div>
              </button>
            ))
          )}
        </div>
      )}

      {/* Categories View */}
      {!searchQuery && viewState === 'categories' && (
        <div className="grid grid-cols-1 sm:grid-cols-2 gap-4">
          {categories.map((category) => (
            <CategoryCard
              key={category.id}
              id={category.id}
              name={category.name}
              icon={category.icon}
              description={category.description}
              onClick={() => handleCategoryClick(category.id)}
            />
          ))}
        </div>
      )}

      {/* Category Detail View */}
      {!searchQuery && viewState === 'category-detail' && selectedCategory && (
        <div className="space-y-4">
          <button
            onClick={handleBack}
            className="flex items-center gap-2 text-slate-700 hover:text-slate-900 bg-white hover:bg-slate-50 px-4 py-2 rounded-xl text-sm font-semibold border border-slate-200 transition-all shadow-xs hover:scale-105 active:scale-95"
          >
            <svg className="w-4 h-4" fill="none" stroke="currentColor" viewBox="0 0 24 24">
              <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M15 19l-7-7 7-7" />
            </svg>
            <span>{t('survival.backToCat')}</span>
          </button>

          <h3 className="text-xl font-bold text-slate-900">
            {categories.find((c) => c.id === selectedCategory)?.name}
          </h3>

          <div className="space-y-3">
            {categoryGuides.map((guide) => (
              <button
                key={guide.id}
                onClick={() => handleGuideClick(guide)}
                className="w-full text-left bg-white/95 rounded-xl p-4 hover:bg-slate-50 transition-all border border-slate-200/90 hover:border-blue-400 shadow-xs hover:scale-[1.005]"
              >
                <div className="flex items-center gap-3.5">
                  <span className="text-3xl">{guide.icon}</span>
                  <div>
                    <p className="font-bold text-slate-900">{guide.title}</p>
                    <p className="text-sm text-slate-600 mt-0.5">{guide.description}</p>
                  </div>
                </div>
              </button>
            ))}
          </div>
        </div>
      )}

      {/* Guide Detail View */}
      {!searchQuery && viewState === 'guide-detail' && selectedGuide && (
        <GuideContent guide={selectedGuide} onBack={handleBack} />
      )}

      {/* Offline Indicator */}
      <div className="text-center text-xs text-slate-500 pt-4 border-t border-slate-200/80 font-medium">
        {t('survival.offlineNotice')}
      </div>
    </div>
  );
}



