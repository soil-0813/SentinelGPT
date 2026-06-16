import { NavLink, useLocation } from 'react-router-dom'
import {
  LayoutDashboard, MessageSquare, FileText,
  Shield, Activity, Bell, Settings, ChevronRight
} from 'lucide-react'

const NAV_ITEMS = [
  { to: '/',        icon: LayoutDashboard, label: 'Dashboard'    },
  { to: '/chat',    icon: MessageSquare,   label: 'SOC Chat'     },
  { to: '/reports', icon: FileText,        label: 'Reports'      },
]

export default function Navbar({ alertCount = 3 }) {
  return (
    <aside style={{
      position: 'fixed', top: 0, left: 0, bottom: 0,
      width: 'var(--sidebar-w)',
      background: 'var(--bg-deep)',
      borderRight: '1px solid var(--border)',
      display: 'flex', flexDirection: 'column',
      zIndex: 100,
    }}>
      {/* Logo */}
      <div style={{
        padding: '22px 20px 18px',
        borderBottom: '1px solid var(--border)',
        display: 'flex', alignItems: 'center', gap: 12,
      }}>
        <div style={{
          width: 38, height: 38,
          borderRadius: 10,
          background: 'linear-gradient(135deg, #0099cc, #00c8ff)',
          display: 'flex', alignItems: 'center', justifyContent: 'center',
          boxShadow: '0 0 20px rgba(0,200,255,0.35)',
          flexShrink: 0,
        }}>
          <Shield size={20} color="#000" strokeWidth={2.5} />
        </div>
        <div>
          <div style={{ fontSize: '1rem', fontWeight: 700, color: 'var(--text-primary)', letterSpacing: '-0.01em' }}>
            Sentinel<span style={{ color: 'var(--cyan)' }}>GPT</span>
          </div>
          <div style={{ fontSize: '0.66rem', color: 'var(--text-muted)', textTransform: 'uppercase', letterSpacing: '0.08em', marginTop: 1 }}>
            SOC Intelligence
          </div>
        </div>
      </div>

      {/* Nav section label */}
      <div style={{ padding: '20px 20px 8px', fontSize: '0.67rem', color: 'var(--text-dim)', textTransform: 'uppercase', letterSpacing: '0.1em', fontWeight: 600 }}>
        Navigation
      </div>

      {/* Nav links */}
      <nav style={{ flex: 1, padding: '0 10px', display: 'flex', flexDirection: 'column', gap: 3 }}>
        {NAV_ITEMS.map(({ to, icon: Icon, label }) => (
          <NavLink
            key={to}
            to={to}
            end={to === '/'}
            style={({ isActive }) => ({
              display: 'flex', alignItems: 'center', gap: 12,
              padding: '10px 12px',
              borderRadius: 'var(--radius-md)',
              textDecoration: 'none',
              transition: 'var(--transition)',
              fontSize: '0.875rem',
              fontWeight: 500,
              position: 'relative',
              background: isActive ? 'linear-gradient(135deg, rgba(0,200,255,0.12), rgba(0,150,200,0.06))' : 'transparent',
              color: isActive ? 'var(--cyan)' : 'var(--text-muted)',
              border: isActive ? '1px solid rgba(0,200,255,0.2)' : '1px solid transparent',
            })}
          >
            {({ isActive }) => (
              <>
                <Icon size={17} strokeWidth={isActive ? 2.2 : 1.8} />
                <span style={{ flex: 1 }}>{label}</span>
                {isActive && <ChevronRight size={13} style={{ opacity: 0.5 }} />}
              </>
            )}
          </NavLink>
        ))}
      </nav>

      {/* Alert count */}
      <div style={{ padding: '12px 10px' }}>
        <div style={{
          display: 'flex', alignItems: 'center', gap: 10,
          padding: '10px 12px',
          background: 'rgba(255,59,92,0.08)',
          border: '1px solid rgba(255,59,92,0.2)',
          borderRadius: 'var(--radius-md)',
        }}>
          <Bell size={16} color="var(--red)" />
          <span style={{ flex: 1, fontSize: '0.82rem', color: 'var(--text-secondary)' }}>Active Alerts</span>
          <span style={{
            background: 'var(--red)', color: '#fff',
            fontSize: '0.7rem', fontWeight: 700,
            padding: '2px 7px', borderRadius: 10,
            fontFamily: 'var(--font-mono)',
          }}>{alertCount}</span>
        </div>
      </div>

      {/* Footer */}
      <div style={{
        padding: '14px 20px',
        borderTop: '1px solid var(--border)',
        display: 'flex', alignItems: 'center', gap: 10,
      }}>
        <div style={{
          width: 30, height: 30, borderRadius: '50%',
          background: 'linear-gradient(135deg, var(--cyan-dim), var(--purple))',
          display: 'flex', alignItems: 'center', justifyContent: 'center',
          fontSize: '0.72rem', fontWeight: 700, color: '#fff',
          flexShrink: 0,
        }}>AB</div>
        <div style={{ flex: 1, minWidth: 0 }}>
          <div style={{ fontSize: '0.8rem', fontWeight: 600, color: 'var(--text-primary)', whiteSpace: 'nowrap', overflow: 'hidden', textOverflow: 'ellipsis' }}>Aritra B.</div>
          <div style={{ fontSize: '0.68rem', color: 'var(--text-muted)' }}>Dashboard Engineer</div>
        </div>
        <Settings size={14} color="var(--text-dim)" style={{ cursor: 'pointer' }} />
      </div>
    </aside>
  )
}
