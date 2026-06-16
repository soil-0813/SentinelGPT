import { AlertTriangle, Flame, Shield, Info } from 'lucide-react'

const ICONS = {
  critical: <Flame size={15} />,
  high:     <AlertTriangle size={15} />,
  medium:   <Shield size={15} />,
  low:      <Info size={15} />,
}

function timeAgo(isoString) {
  const diff = Math.floor((Date.now() - new Date(isoString)) / 1000)
  if (diff < 60)  return `${diff}s ago`
  if (diff < 3600) return `${Math.floor(diff / 60)}m ago`
  return `${Math.floor(diff / 3600)}h ago`
}

export default function AlertCard({ alert, onClick }) {
  const { title, description, severity, source, ip, mitre, timestamp, status } = alert

  return (
    <div
      className={`alert-card ${severity}`}
      onClick={() => onClick?.(alert)}
      role="button"
      tabIndex={0}
    >
      <div className={`alert-icon severity-badge ${severity}`} style={{ padding: 0, width: 28, height: 28, display: 'flex', alignItems: 'center', justifyContent: 'center', borderRadius: '50%' }}>
        {ICONS[severity] ?? <Info size={15} />}
      </div>

      <div className="alert-body">
        <div className="alert-title">{title}</div>
        <div className="alert-detail">{description}</div>
        <div style={{ display: 'flex', alignItems: 'center', gap: 10, marginTop: 6, flexWrap: 'wrap' }}>
          <span style={{ fontFamily: 'var(--font-mono)', fontSize: '0.7rem', color: 'var(--text-dim)' }}>
            {ip}
          </span>
          <span style={{
            fontSize: '0.67rem', fontFamily: 'var(--font-mono)',
            background: 'var(--purple-glow)', border: '1px solid rgba(168,85,247,0.3)',
            color: 'var(--purple)', padding: '1px 7px', borderRadius: 8,
          }}>
            {mitre}
          </span>
          <span style={{
            fontSize: '0.67rem',
            color: status === 'open' ? 'var(--red)' : status === 'investigating' ? 'var(--orange)' : 'var(--green)',
            fontFamily: 'var(--font-mono)', fontWeight: 600,
          }}>
            ● {status.toUpperCase()}
          </span>
        </div>
        <div className="alert-time">
          {source} · {timeAgo(timestamp)}
        </div>
      </div>

      <div style={{ flexShrink: 0 }}>
        <span className={`severity-badge ${severity}`}>{severity}</span>
      </div>
    </div>
  )
}
