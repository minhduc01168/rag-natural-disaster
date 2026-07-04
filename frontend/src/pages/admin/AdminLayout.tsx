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
      <aside className="w-64 bg-slate-900/80 border-r border-white/10 flex flex-col backdrop-blur-xl shrink-0">
        <div className="p-6 border-b border-white/5">
          <h2 className="text-xl font-bold bg-gradient-to-r from-blue-400 to-indigo-400 bg-clip-text text-transparent">
            {t('admin.title')}
          </h2>
          <p className="text-xs text-slate-400 mt-1">{t('admin.subtitle')}</p>
        </div>
        <nav className="flex-1 py-4 space-y-1">
          {navItems.map((item) => {
            const isActive = location.pathname === item.path || 
                             (item.path !== '/admin' && location.pathname.startsWith(item.path));
            return (
              <Link
                key={item.path}
                to={item.path}
                className={`flex items-center gap-3 px-6 py-3 transition-colors ${
                  isActive 
                    ? 'bg-blue-500/10 text-blue-400 border-r-2 border-blue-500 font-semibold' 
                    : 'text-slate-400 hover:bg-white/5 hover:text-slate-200'
                }`}
              >
                <span className="text-xl">{item.icon}</span>
                <span className="font-medium">{item.label}</span>
              </Link>
            );
          })}
        </nav>
      </aside>

      {/* Main Content Area */}
      <main className="flex-1 overflow-auto bg-slate-950/50 p-6 sm:p-8">
        <div className="w-full max-w-none">
          <Outlet />
        </div>
      </main>
    </div>
  );
}
