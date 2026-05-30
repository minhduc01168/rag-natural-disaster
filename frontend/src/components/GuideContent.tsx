import { SurvivalGuide } from '../data/survivalGuides';

interface GuideContentProps {
  guide: SurvivalGuide;
  onBack: () => void;
}

export function GuideContent({ guide, onBack }: GuideContentProps) {
  return (
    <div className="bg-white rounded-xl shadow-md p-6">
      <button
        onClick={onBack}
        className="flex items-center gap-2 text-gray-600 hover:text-gray-900 mb-4"
      >
        <svg className="w-5 h-5" fill="none" stroke="currentColor" viewBox="0 0 24 24">
          <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M15 19l-7-7 7-7" />
        </svg>
        Quay lại
      </button>

      <div className="flex items-center gap-3 mb-4">
        <span className="text-3xl">{guide.icon}</span>
        <div>
          <h2 className="text-xl font-bold text-gray-900">{guide.title}</h2>
          <p className="text-gray-600">{guide.description}</p>
        </div>
      </div>

      <div className="border-t border-gray-100 pt-4">
        <h3 className="font-semibold text-gray-900 mb-3">Hướng dẫn:</h3>
        <ol className="space-y-3">
          {guide.content.map((step, index) => (
            <li key={index} className="flex items-start gap-3">
              <span className="w-7 h-7 bg-blue-100 text-blue-700 rounded-full flex items-center justify-center text-sm font-medium flex-shrink-0">
                {index + 1}
              </span>
              <span className="text-gray-700">{step.replace(/^\d+\.\s*/, '')}</span>
            </li>
          ))}
        </ol>
      </div>

      <div className="mt-6 p-4 bg-yellow-50 rounded-lg border border-yellow-200">
        <p className="text-sm text-yellow-800">
          ⚠️ <strong>Lưu ý:</strong> Đây là hướng dẫn cơ bản. Trong trường hợp khẩn cấp, hãy gọi ngay cấp cứu 115.
        </p>
      </div>
    </div>
  );
}
