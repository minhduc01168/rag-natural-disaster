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
      className="bg-white/95 backdrop-blur-md border border-slate-200/90 rounded-2xl shadow-sm hover:shadow-md p-6 hover:border-blue-400 transition-all hover:scale-[1.01] text-left w-full group"
    >
      <div className="flex items-start gap-4">
        <div className="w-14 h-14 bg-blue-50 rounded-xl flex items-center justify-center flex-shrink-0 border border-blue-100 shadow-xs group-hover:bg-blue-100/70 transition-all">
          <span className="text-3xl">{icon}</span>
        </div>
        <div className="flex-1">
          <h3 className="text-lg font-bold text-slate-900 group-hover:text-blue-600 transition-colors">{name}</h3>
          <p className="text-sm text-slate-600 mt-1 leading-relaxed">{description}</p>
        </div>
      </div>
    </button>
  );
}



