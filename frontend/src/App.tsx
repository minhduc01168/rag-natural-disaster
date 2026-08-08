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

  return (
    <div className="flex items-center gap-3 sm:gap-4">
      {/* Streamlined VI|EN Language Switcher Pill */}
      <div className="flex items-center rounded-xl bg-slate-200/80 p-1 border border-slate-300/80 shadow-xs text-xs font-semibold">
        <button
          onClick={() => setLang('vi')}
          className={`px-2.5 py-1 rounded-lg transition-all ${
            lang === 'vi'
              ? 'bg-blue-600 text-white shadow-sm shadow-blue-500/20 font-bold scale-105'
              : 'text-slate-600 hover:text-slate-900'
          }`}
        >
          VI
        </button>
        <span className="text-slate-300 px-0.5 font-normal">|</span>
        <button
          onClick={() => setLang('en')}
          className={`px-2.5 py-1 rounded-lg transition-all ${
            lang === 'en'
              ? 'bg-blue-600 text-white shadow-sm shadow-blue-500/20 font-bold scale-105'
              : 'text-slate-600 hover:text-slate-900'
          }`}
        >
          EN
        </button>
      </div>

      {isAuthenticated ? (
        <div className="flex items-center gap-4">
          <span className="text-sm font-medium text-slate-600 hidden sm:inline">
            {t('nav.hello')}, <span className="text-blue-600 font-bold">{user?.full_name}</span>
          </span>
          <button
            onClick={handleLogout}
            className="text-sm font-semibold text-red-600 hover:text-red-700 hover:bg-red-50 transition-colors px-2.5 py-1 rounded-lg"
          >
            {t('nav.logout')}
          </button>
        </div>
      ) : (
        <div className="flex items-center gap-3">
          <Link to="/login" className="text-sm font-medium text-slate-600 hover:text-slate-900 transition-colors px-2 py-1">
            {t('nav.login')}
          </Link>
          <Link
            to="/register"
            className="text-sm font-semibold bg-blue-600 hover:bg-blue-700 text-white px-4 py-1.5 rounded-xl shadow-md shadow-blue-500/20 hover:scale-105 active:scale-95 transition-all"
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
    <div className="min-h-screen bg-gradient-to-br from-slate-100 via-sky-50/60 to-blue-50/50 text-slate-800 flex flex-col">
      <header className="bg-white/90 backdrop-blur-md border-b border-slate-200/90 sticky top-0 z-50 shadow-sm">
        <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 flex items-center justify-between py-4">
          <div className="flex items-center gap-8">
            <h1 className="text-2xl font-black bg-gradient-to-r from-blue-600 via-sky-600 to-teal-500 bg-clip-text text-transparent drop-shadow-xs">
              <Link to="/">TerraAlert</Link>
            </h1>
            <nav className="hidden md:flex gap-6">
              <Link
                to="/"
                className={`text-sm font-medium transition-all duration-200 hover:-translate-y-0.5 ${
                  location.pathname === '/' ? 'text-blue-600 font-extrabold border-b-2 border-blue-600 pb-0.5' : 'text-slate-600 hover:text-blue-600'
                }`}
              >
                {t('nav.home')}
              </Link>
              <Link
                to="/research"
                className={`text-sm font-medium transition-all duration-200 hover:-translate-y-0.5 ${
                  location.pathname === '/research' ? 'text-blue-600 font-extrabold border-b-2 border-blue-600 pb-0.5' : 'text-slate-600 hover:text-blue-600'
                }`}
              >
                {t('nav.research')}
              </Link>
              <Link
                to="/alerts"
                className={`text-sm font-medium transition-all duration-200 hover:-translate-y-0.5 ${
                  location.pathname === '/alerts' ? 'text-blue-600 font-extrabold border-b-2 border-blue-600 pb-0.5' : 'text-slate-600 hover:text-blue-600'
                }`}
              >
                {t('nav.alerts')}
              </Link>
              <Link
                to="/survival"
                className={`text-sm font-medium transition-all duration-200 hover:-translate-y-0.5 ${
                  location.pathname === '/survival' ? 'text-blue-600 font-extrabold border-b-2 border-blue-600 pb-0.5' : 'text-slate-600 hover:text-blue-600'
                }`}
              >
                {t('nav.survival')}
              </Link>
              {user?.role === 'ADMIN' && (
                <Link
                  to="/admin"
                  className={`text-sm font-medium transition-all duration-200 hover:-translate-y-0.5 ${
                    location.pathname.startsWith('/admin') ? 'text-teal-600 font-bold border-b-2 border-teal-600 pb-0.5' : 'text-teal-600/80 hover:text-teal-700'
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
      <footer className="mt-auto py-8 text-center text-slate-500 text-sm border-t border-slate-200/90 bg-white/60">
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
        <h2 className="text-3xl font-black text-slate-900">{t('alerts.title')}</h2>
        <p className="text-slate-500 mt-1 text-sm">{t('alerts.subtitle')}</p>
      </div>
      <AlertList />
    </div>
  )
}

function Survival() {
  return <SurvivalPage />
}

function Offline() {
  const { t } = useLanguage();
  return (
    <div className="min-h-screen bg-slate-100 flex items-center justify-center text-slate-800">
      <div className="text-center p-8 max-w-md bg-white border border-slate-200 shadow-xl rounded-2xl">
        <div className="text-6xl mb-4 animate-bounce">📡</div>
        <h2 className="text-2xl font-bold text-slate-900">{t('common.offlineTitle')}</h2>
        <p className="mt-2 text-slate-500 text-sm">{t('common.offlineDesc')}</p>
        <Link
          to="/"
          className="mt-6 inline-block bg-blue-600 text-white px-6 py-2.5 rounded-xl text-sm font-semibold hover:bg-blue-700 transition-all shadow-md shadow-blue-500/20 hover:scale-105 active:scale-95"
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
              <Route path="/research" element={<ResearchPage />} />
              <Route path="/alerts" element={<Alerts />} />
              <Route path="/survival" element={<Survival />} />
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
