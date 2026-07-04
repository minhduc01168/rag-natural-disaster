import { BrowserRouter as Router, Routes, Route, Link, useLocation, useNavigate } from 'react-router-dom'
import { Dashboard } from './components/Dashboard'
import { AlertList } from './components/AlertList'
import { SurvivalPage } from './pages/SurvivalPage'
import { ResearchPage } from './pages/ResearchPage'
import { LoginPage } from './pages/auth/LoginPage'
import { RegisterPage } from './pages/auth/RegisterPage'
import { AuthProvider, useAuth } from './context/AuthContext'
import { LanguageProvider, useLanguage } from './context/LanguageContext'
import { ProtectedRoute } from './components/ProtectedRoute'
import { TerraBotWidget } from './components/TerraBotWidget'
import { AdminLayout } from './pages/admin/AdminLayout'
import { KnowledgeBasePage } from './pages/admin/KnowledgeBasePage'
import { KBDocumentsPage } from './pages/admin/KBDocumentsPage'

function HeaderAuth() {
  const { isAuthenticated, user, logout } = useAuth();
  const { t, lang, setLang } = useLanguage();
  const navigate = useNavigate();

  const handleLogout = () => {
    logout();
    navigate('/login');
  };

  const toggleLanguage = () => {
    setLang(lang === 'vi' ? 'en' : 'vi');
  };

  return (
    <div className="flex items-center gap-3 sm:gap-4">
      {/* Language Switcher Toggle */}
      <button
        onClick={toggleLanguage}
        className="px-3 py-1.5 rounded-xl bg-slate-800/80 hover:bg-slate-700 border border-slate-700 hover:border-slate-500 text-xs font-semibold text-slate-200 transition-all hover:scale-105 active:scale-95 flex items-center gap-1.5 shadow-sm"
        title={lang === 'vi' ? 'Switch to English' : 'Chuyển sang Tiếng Việt'}
      >
        <span>{lang === 'vi' ? '🇻🇳 VI' : '🇬🇧 EN'}</span>
      </button>

      {isAuthenticated ? (
        <div className="flex items-center gap-4">
          <span className="text-sm font-medium text-slate-300 hidden sm:inline">
            {t('nav.hello')}, <span className="text-blue-400">{user?.full_name}</span>
          </span>
          <button
            onClick={handleLogout}
            className="text-sm font-medium text-red-400 hover:text-red-300 transition-colors px-2 py-1 rounded-lg hover:bg-red-500/10"
          >
            {t('nav.logout')}
          </button>
        </div>
      ) : (
        <div className="flex items-center gap-3">
          <Link to="/login" className="text-sm font-medium text-slate-300 hover:text-white transition-colors px-2 py-1">
            {t('nav.login')}
          </Link>
          <Link
            to="/register"
            className="text-sm font-semibold bg-blue-600 hover:bg-blue-500 text-white px-4 py-1.5 rounded-xl shadow-md shadow-blue-500/20 hover:scale-105 active:scale-95 transition-all"
          >
            {t('nav.register')}
          </Link>
        </div>
      )}
    </div>
  );
}

function Layout({ children }: { children: React.ReactNode }) {
  const location = useLocation()
  const { user } = useAuth()
  const { t } = useLanguage()
  const isOffline = location.pathname === '/offline'
  const isAuthPage = location.pathname === '/login' || location.pathname === '/register'
  const isAdminPage = location.pathname.startsWith('/admin')

  if (isOffline || isAuthPage) {
    return <>{children}</>
  }

  return (
    <div className="min-h-screen bg-gradient-to-br from-slate-900 via-indigo-950 to-slate-900 text-slate-100 flex flex-col">
      <header className="bg-slate-900/60 backdrop-blur-md border-b border-white/10 sticky top-0 z-50">
        <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 flex items-center justify-between py-4">
          <div className="flex items-center gap-8">
            <h1 className="text-2xl font-bold bg-gradient-to-r from-blue-400 to-indigo-400 bg-clip-text text-transparent drop-shadow-sm">
              <Link to="/">TerraAlert</Link>
            </h1>
            <nav className="hidden md:flex gap-6">
              <Link
                to="/"
                className={`text-sm font-medium transition-all duration-200 hover:-translate-y-0.5 ${
                  location.pathname === '/' ? 'text-blue-400 font-semibold drop-shadow-md' : 'text-slate-300 hover:text-blue-300'
                }`}
              >
                {t('nav.home')}
              </Link>
              <Link
                to="/alerts"
                className={`text-sm font-medium transition-all duration-200 hover:-translate-y-0.5 ${
                  location.pathname === '/alerts' ? 'text-blue-400 font-semibold drop-shadow-md' : 'text-slate-300 hover:text-blue-300'
                }`}
              >
                {t('nav.alerts')}
              </Link>
              <Link
                to="/survival"
                className={`text-sm font-medium transition-all duration-200 hover:-translate-y-0.5 ${
                  location.pathname === '/survival' ? 'text-blue-400 font-semibold drop-shadow-md' : 'text-slate-300 hover:text-blue-300'
                }`}
              >
                {t('nav.survival')}
              </Link>
              <Link
                to="/research"
                className={`text-sm font-medium transition-all duration-200 hover:-translate-y-0.5 ${
                  location.pathname === '/research' ? 'text-blue-400 font-semibold drop-shadow-md' : 'text-slate-300 hover:text-blue-300'
                }`}
              >
                {t('nav.research')}
              </Link>
              {user?.role === 'ADMIN' && (
                <Link
                  to="/admin"
                  className={`text-sm font-medium transition-all duration-200 hover:-translate-y-0.5 ${
                    location.pathname.startsWith('/admin') ? 'text-teal-400 font-semibold drop-shadow-md' : 'text-teal-500/80 hover:text-teal-400'
                  }`}
                >
                  {t('nav.admin')}
                </Link>
              )}
            </nav>
          </div>
          <HeaderAuth />
        </div>
      </header>
      <main className={isAdminPage ? "flex-1 w-full flex flex-col" : "flex-1 w-full max-w-7xl mx-auto px-4 py-8 sm:px-6 lg:px-8"}>
        {children}
      </main>
      <TerraBotWidget />
      <footer className="mt-auto py-8 text-center text-slate-500 text-sm border-t border-white/5">
        <p>{t('common.footerText')}</p>
      </footer>
    </div>
  )
}

function Home() {
  return <Dashboard />
}

function Alerts() {
  const { t } = useLanguage();
  return (
    <div className="space-y-6">
      <div>
        <h2 className="text-3xl font-bold text-white drop-shadow-sm">{t('alerts.title')}</h2>
        <p className="text-slate-400 mt-1 text-sm">{t('alerts.subtitle')}</p>
      </div>
      <AlertList />
    </div>
  )
}

function Survival() {
  return <SurvivalPage />
}

function Research() {
  return <ResearchPage />
}

function Offline() {
  const { t } = useLanguage();
  return (
    <div className="min-h-screen bg-slate-900 flex items-center justify-center text-slate-100">
      <div className="text-center p-8 max-w-md bg-slate-800/50 border border-slate-700 rounded-2xl backdrop-blur-md">
        <div className="text-6xl mb-4 animate-bounce">📡</div>
        <h2 className="text-2xl font-bold text-white">{t('common.offlineTitle')}</h2>
        <p className="mt-2 text-slate-400 text-sm">{t('common.offlineDesc')}</p>
        <Link
          to="/"
          className="mt-6 inline-block bg-blue-600 text-white px-6 py-2.5 rounded-xl text-sm font-semibold hover:bg-blue-500 transition-all shadow-md shadow-blue-500/20 hover:scale-105 active:scale-95"
        >
          {t('common.retry')}
        </Link>
      </div>
    </div>
  )
}

function App() {
  return (
    <LanguageProvider>
      <AuthProvider>
        <Router>
          <Layout>
            <Routes>
              <Route path="/" element={<Home />} />
              <Route path="/alerts" element={<Alerts />} />
              <Route path="/survival" element={<Survival />} />
              <Route path="/research" element={<Research />} />
              <Route path="/login" element={<LoginPage />} />
              <Route path="/register" element={<RegisterPage />} />
              <Route path="/offline" element={<Offline />} />
              
              {/* Protected Admin Routes */}
              <Route element={<ProtectedRoute requiredRole="ADMIN" />}>
                <Route path="/admin" element={<AdminLayout />}>
                  <Route index element={<KnowledgeBasePage />} />
                  <Route path="kb" element={<KnowledgeBasePage />} />
                  <Route path="kb-docs" element={<KBDocumentsPage />} />
                  <Route path="*" element={<KnowledgeBasePage />} />
                </Route>
              </Route>
            </Routes>
          </Layout>
        </Router>
      </AuthProvider>
    </LanguageProvider>
  )
}

export default App
