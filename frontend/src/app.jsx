import { BrowserRouter, Routes, Route, Navigate } from 'react-router-dom'
import Navbar    from './components/Navbar.jsx'
import Dashboard from './pages/Dashboard.jsx'
import SOCChat   from './pages/SOCChat.jsx'
import Reports   from './pages/Reports.jsx'

export default function App() {
  return (
    <BrowserRouter>
      <div className="app-layout">
        <Navbar alertCount={7} />
        <div className="main-content">
          <Routes>
            <Route path="/"        element={<Dashboard />} />
            <Route path="/chat"    element={
              <div style={{ display: 'flex', flexDirection: 'column', height: '100%', overflow: 'hidden' }}>
                <SOCChat />
              </div>
            } />
            <Route path="/reports" element={<Reports />} />
            <Route path="*"        element={<Navigate to="/" replace />} />
          </Routes>
        </div>
      </div>
    </BrowserRouter>
  )
}
