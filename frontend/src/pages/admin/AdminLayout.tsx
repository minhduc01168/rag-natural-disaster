import { Outlet, Link, useLocation } from 'react-router-dom';
import { useLanguage } from '../../context/LanguageContext';

export function AdminLayout() {
  const location = useLocation();
  const { t } = useLanguage();

  const navItems = [
    { path: '/admin/kb', icon: '📚', label: t('admin.navUpload') },
    { path: '/admin/kb-docs', icon: '🗂️', label: t('admin.navManage') },
  ];

  return (
    <div className="flex flex-1 min-h-[calc(100vh-73px)] w-full">
      {/* Sidebar */}
      <aside className="w-64 bg-white/90 border-r border-slate-200/90 flex flex-col backdrop-blur-md shrink-0 shadow-xs">
        <div className="p-6 border-b border-slate-200/80">
          <h2 className="text-xl font-black bg-gradient-to-r from-blue-600 via-sky-600 to-teal-500 bg-clip-text text-transparent">
            {t('admin.title')}
          </h2>
          <p className="text-xs text-slate-500 mt-1 font-medium">{t('admin.subtitle')}</p>
        </div>
        <nav className="flex-1 py-4 space-y-1">
          {navItems.map((item) => {
            const isActive = location.pathname === item.path || 
                             (item.path !== '/admin' && location.pathname.startsWith(item.path));
            return (
              <Link
                key={item.path}
                to={item.path}
                className={`flex items-center gap-3 px-6 py-3.5 transition-all ${
                  isActive 
                    ? 'bg-blue-50 text-blue-700 border-r-4 border-blue-600 font-extrabold shadow-xs' 
                    : 'text-slate-600 hover:bg-slate-100/70 hover:text-slate-900 font-medium'
                }`}
              >
                <span className="text-xl">{item.icon}</span>
                <span>{item.label}</span>
              </Link>
            );
          })}
        </nav>
      </aside>

      {/* Main Content Area */}
      <main className="flex-1 overflow-auto bg-transparent p-6 sm:p-8">
        <div className="w-full max-w-none">
          <Outlet />
        </div>
      </main>
    </div>
  );
}

