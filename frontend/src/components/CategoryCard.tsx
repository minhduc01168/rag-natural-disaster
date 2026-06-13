interface CategoryCardProps {
  id: string;
  name: string;
  icon: string;
  description: string;
  onClick: () => void;
}

export function CategoryCard({ name, icon, description, onClick }: CategoryCardProps) {
  return (
    <button
      onClick={onClick}
      className="bg-white rounded-xl shadow-md p-6 hover:shadow-lg transition-all hover:scale-105 text-left w-full"
    >
      <div className="flex items-start gap-4">
        <div className="w-14 h-14 bg-blue-50 rounded-xl flex items-center justify-center flex-shrink-0">
          <span className="text-3xl">{icon}</span>
        </div>
        <div className="flex-1">
          <h3 className="text-lg font-semibold text-gray-900">{name}</h3>
          <p className="text-sm text-gray-600 mt-1">{description}</p>
        </div>
      </div>
    </button>
  );
}
