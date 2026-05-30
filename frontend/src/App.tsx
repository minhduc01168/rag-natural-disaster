import { BrowserRouter as Router, Routes, Route, Link, useLocation } from 'react-router-dom'
import { Dashboard } from './components/Dashboard'
import { AlertList } from './components/AlertList'
import { SurvivalPage } from './pages/SurvivalPage'
import { TerraBotPage } from './pages/TerraBotPage'
import { ResearchPage } from './pages/ResearchPage'

function Layout({ children }: { children: React.ReactNode }) {
  const location = useLocation()
  const isOffline = location.pathname === '/offline'

  if (isOffline) {
    return <>{children}</>
  }

  return (
    <div className="min-h-screen bg-gradient-to-br from-blue-50 to-indigo-100">
      <header className="bg-white shadow-sm">
        <div className="max-w-7xl mx-auto px-4 py-4 sm:px-6 lg:px-8 flex items-center justify-between">
          <h1 className="text-2xl font-bold text-primary-700">
            <Link to="/">TerraAlert</Link>
          </h1>
          <nav className="flex gap-4">
            <Link
              to="/"
              className={`transition-colors ${location.pathname === '/' ? 'text-primary-600 font-medium' : 'text-gray-600 hover:text-primary-600'}`}
            >
              Trang chủ
            </Link>
            <Link
              to="/alerts"
              className={`transition-colors ${location.pathname === '/alerts' ? 'text-primary-600 font-medium' : 'text-gray-600 hover:text-primary-600'}`}
            >
              Cảnh báo
            </Link>
            <Link
              to="/survival"
              className={`transition-colors ${location.pathname === '/survival' ? 'text-primary-600 font-medium' : 'text-gray-600 hover:text-primary-600'}`}
            >
              Cẩm nang
            </Link>
            <Link
              to="/terrabot"
              className={`transition-colors ${location.pathname === '/terrabot' ? 'text-primary-600 font-medium' : 'text-gray-600 hover:text-primary-600'}`}
            >
              🤖 TerraBot
            </Link>
            <Link
              to="/research"
              className={`transition-colors ${location.pathname === '/research' ? 'text-primary-600 font-medium' : 'text-gray-600 hover:text-primary-600'}`}
            >
              📊 Research
            </Link>
          </nav>
        </div>
      </header>
      <main className="max-w-7xl mx-auto px-4 py-12 sm:px-6 lg:px-8">
        {children}
      </main>
      <footer className="bg-white mt-12 py-6 text-center text-gray-500 text-sm">
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

function TerraBot() {
  return <TerraBotPage />
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

function App() {
  return (
    <Router>
      <Layout>
        <Routes>
          <Route path="/" element={<Home />} />
          <Route path="/alerts" element={<Alerts />} />
          <Route path="/survival" element={<Survival />} />
          <Route path="/terrabot" element={<TerraBot />} />
          <Route path="/research" element={<Research />} />
          <Route path="/offline" element={<Offline />} />
        </Routes>
      </Layout>
    </Router>
  )
}

export default App
