import { useState } from 'react';
import { CategoryCard } from '../components/CategoryCard';
import { GuideContent } from '../components/GuideContent';
import { categories, getGuidesByCategory, searchGuides, SurvivalGuide } from '../data/survivalGuides';

type ViewState = 'categories' | 'category-detail' | 'guide-detail';

export function SurvivalPage() {
  const [viewState, setViewState] = useState<ViewState>('categories');
  const [selectedCategory, setSelectedCategory] = useState<string | null>(null);
  const [selectedGuide, setSelectedGuide] = useState<SurvivalGuide | null>(null);
  const [searchQuery, setSearchQuery] = useState('');

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
        <h2 className="text-2xl font-bold text-gray-900">Cẩm nang Sinh tồn</h2>
        <p className="text-gray-600 mt-1">Kiến thức sinh tồn cơ bản - hoạt động offline</p>
      </div>

      {/* Search Bar */}
      <div className="relative">
        <input
          type="text"
          placeholder="Tìm kiếm cẩm nang..."
          value={searchQuery}
          onChange={(e) => setSearchQuery(e.target.value)}
          className="w-full px-4 py-3 pl-10 bg-white rounded-xl border border-gray-200 focus:outline-none focus:ring-2 focus:ring-primary-500 focus:border-transparent"
        />
        <svg
          className="absolute left-3 top-3.5 w-5 h-5 text-gray-400"
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
          <h3 className="font-semibold text-gray-700">Kết quả tìm kiếm ({filteredGuides.length})</h3>
          {filteredGuides.length === 0 ? (
            <p className="text-gray-500">Không tìm thấy kết quả</p>
          ) : (
            filteredGuides.map((guide) => (
              <button
                key={guide.id}
                onClick={() => handleGuideClick(guide)}
                className="w-full text-left bg-white rounded-lg p-4 hover:bg-gray-50 transition-colors border border-gray-100"
              >
                <div className="flex items-center gap-3">
                  <span className="text-2xl">{guide.icon}</span>
                  <div>
                    <p className="font-medium text-gray-900">{guide.title}</p>
                    <p className="text-sm text-gray-600">{guide.description}</p>
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
            className="flex items-center gap-2 text-gray-600 hover:text-gray-900"
          >
            <svg className="w-5 h-5" fill="none" stroke="currentColor" viewBox="0 0 24 24">
              <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M15 19l-7-7 7-7" />
            </svg>
            Quay lại danh mục
          </button>

          <h3 className="text-lg font-semibold text-gray-900">
            {categories.find((c) => c.id === selectedCategory)?.name}
          </h3>

          <div className="space-y-3">
            {categoryGuides.map((guide) => (
              <button
                key={guide.id}
                onClick={() => handleGuideClick(guide)}
                className="w-full text-left bg-white rounded-xl shadow-sm p-4 hover:shadow-md transition-shadow"
              >
                <div className="flex items-center gap-3">
                  <span className="text-2xl">{guide.icon}</span>
                  <div>
                    <p className="font-medium text-gray-900">{guide.title}</p>
                    <p className="text-sm text-gray-600">{guide.description}</p>
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
      <div className="text-center text-sm text-gray-400 pt-4 border-t border-gray-100">
        📱 Nội dung này hoạt động offline
      </div>
    </div>
  );
}
