import { BrowserRouter as Router, Routes, Route, Link, useLocation, useNavigate } from 'react-router-dom'
import { Dashboard } from './components/Dashboard'
import { AlertList } from './components/AlertList'
import { SurvivalPage } from './pages/SurvivalPage'
import { ResearchPage } from './pages/ResearchPage'
import { LoginPage } from './pages/auth/LoginPage'
import { RegisterPage } from './pages/auth/RegisterPage'
import { AuthProvider, useAuth } from './context/AuthContext'
import { ProtectedRoute } from './components/ProtectedRoute'
import { TerraBotWidget } from './components/TerraBotWidget'
import { AdminLayout } from './pages/admin/AdminLayout'
import { KnowledgeBasePage } from './pages/admin/KnowledgeBasePage'

function HeaderAuth() {
  const { isAuthenticated, user, logout } = useAuth();
  const navigate = useNavigate();

  const handleLogout = () => {
    logout();
    navigate('/login');
  };

  if (isAuthenticated) {
    return (
      <div className="flex items-center gap-4">
        <span className="text-sm text-slate-300">Chào, {user?.full_name}</span>
        <button onClick={handleLogout} className="text-sm text-red-400 hover:text-red-300 transition-colors">
          Đăng xuất
        </button>
      </div>
    );
  }

  return (
    <div className="flex items-center gap-4">
      <Link to="/login" className="text-sm text-slate-300 hover:text-white transition-colors">Đăng nhập</Link>
      <Link to="/register" className="text-sm bg-blue-500 hover:bg-blue-600 text-white px-4 py-1.5 rounded-lg shadow-lg shadow-blue-500/20 transition-all">
        Đăng ký
      </Link>
    </div>
  );
}

function Layout({ children }: { children: React.ReactNode }) {
  const location = useLocation()
  const { user } = useAuth()
  const isOffline = location.pathname === '/offline'
  const isAuthPage = location.pathname === '/login' || location.pathname === '/register'

  if (isOffline || isAuthPage) {
    return <>{children}</>
  }

  return (
    <div className="min-h-screen bg-gradient-to-br from-slate-900 via-indigo-950 to-slate-900 text-slate-100">
      <header className="bg-slate-900/50 backdrop-blur-md border-b border-white/10 sticky top-0 z-50">
        <div className="w-full px-4 sm:px-6 lg:px-8 flex items-center justify-between py-4">
          <div className="flex items-center gap-8">
            <h1 className="text-2xl font-bold bg-gradient-to-r from-blue-400 to-indigo-400 bg-clip-text text-transparent drop-shadow-sm">
              <Link to="/">TerraAlert</Link>
            </h1>
            <nav className="hidden md:flex gap-6">
              <Link to="/" className={`transition-all duration-300 hover:-translate-y-0.5 ${location.pathname === '/' ? 'text-blue-400 font-semibold drop-shadow-md' : 'text-slate-300 hover:text-blue-300'}`}>Trang chủ</Link>
              <Link to="/alerts" className={`transition-all duration-300 hover:-translate-y-0.5 ${location.pathname === '/alerts' ? 'text-blue-400 font-semibold drop-shadow-md' : 'text-slate-300 hover:text-blue-300'}`}>Cảnh báo</Link>
              <Link to="/survival" className={`transition-all duration-300 hover:-translate-y-0.5 ${location.pathname === '/survival' ? 'text-blue-400 font-semibold drop-shadow-md' : 'text-slate-300 hover:text-blue-300'}`}>Cẩm nang</Link>
              <Link to="/research" className={`transition-all duration-300 hover:-translate-y-0.5 ${location.pathname === '/research' ? 'text-blue-400 font-semibold drop-shadow-md' : 'text-slate-300 hover:text-blue-300'}`}>📊 Research</Link>
              {user?.role === 'ADMIN' && (
                <Link to="/admin" className={`transition-all duration-300 hover:-translate-y-0.5 ${location.pathname.startsWith('/admin') ? 'text-teal-400 font-semibold drop-shadow-md' : 'text-teal-500/80 hover:text-teal-400'}`}>⚙️ Quản trị</Link>
              )}
            </nav>
          </div>
          <HeaderAuth />
        </div>
      </header>
      <main className="w-full px-4 py-12 sm:px-6 lg:px-8">
        {children}
      </main>
      <TerraBotWidget />
      <footer className="mt-12 py-8 text-center text-slate-500 text-sm border-t border-white/5">
        <p>TerraAlert - Hệ thống Cảnh báo Thiên tai Thông minh</p>
      </footer>
    </div>
  )
}

function Home() {
  return <Dashboard />
}

function Alerts() {
  return (
    <div className="space-y-6">
      <div>
        <h2 className="text-2xl font-bold text-gray-900">Trung tâm Cảnh báo</h2>
        <p className="text-gray-600 mt-1">Danh sách cảnh báo thời tiết theo thời gian thực</p>
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
  return (
    <div className="min-h-screen bg-gray-100 flex items-center justify-center">
      <div className="text-center p-8">
        <div className="text-6xl mb-4">📡</div>
        <h2 className="text-2xl font-bold text-gray-900">Không có kết nối</h2>
        <p className="mt-2 text-gray-600">Vui lòng kiểm tra mạng và thử lại</p>
        <Link to="/" className="mt-4 inline-block bg-primary-600 text-white px-6 py-2 rounded-lg hover:bg-primary-700 transition-colors">
          Thử lại
        </Link>
      </div>
    </div>
  )
}

function AdminDashboardPlaceholder() {
  return (
    <div className="text-center py-20">
      <h2 className="text-2xl font-bold text-white mb-4">Dashboard Tổng quan</h2>
      <p className="text-slate-400">Các biểu đồ thống kê sẽ hiển thị tại đây.</p>
    </div>
  );
}

function App() {
  return (
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
                <Route index element={<AdminDashboardPlaceholder />} />
                <Route path="kb" element={<KnowledgeBasePage />} />
                <Route path="*" element={<AdminDashboardPlaceholder />} />
              </Route>
            </Route>
          </Routes>
        </Layout>
      </Router>
    </AuthProvider>
  )
}

export default App
