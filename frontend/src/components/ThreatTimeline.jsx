export default function ThreatTimeline({ events }) {
  const items = events ?? []

  return (
    <div className="timeline">
      {items.map((evt, i) => (
        <div key={evt.id ?? i} className="timeline-item" style={{ animationDelay: `${i * 0.06}s` }}>
          <div className={`timeline-dot ${evt.severity}`} />
          <div className="timeline-content">
            <div className="timeline-header">
              <span className="timeline-title">{evt.title}</span>
              <span className="timeline-time">{evt.time}</span>
            </div>
            <div className="timeline-desc" style={{ marginBottom: 6 }}>{evt.desc}</div>
            <div style={{ display: 'flex', gap: 8, flexWrap: 'wrap' }}>
              <span style={{
                fontFamily: 'var(--font-mono)', fontSize: '0.68rem',
                color: 'var(--text-dim)', background: 'var(--bg-surface)',
                padding: '2px 8px', borderRadius: 6,
              }}>
                {evt.ip}
              </span>
              <span style={{
                fontFamily: 'var(--font-mono)', fontSize: '0.68rem',
                color: 'var(--purple)',
                background: 'rgba(168,85,247,0.1)',
                border: '1px solid rgba(168,85,247,0.25)',
                padding: '2px 8px', borderRadius: 6,
              }}>
                {evt.mitre}
              </span>
              <span className={`severity-badge ${evt.severity}`} style={{ fontSize: '0.65rem', padding: '2px 8px' }}>
                {evt.severity}
              </span>
            </div>
          </div>
        </div>
      ))}

      {items.length === 0 && (
        <div style={{ color: 'var(--text-muted)', fontSize: '0.85rem', padding: '20px 0' }}>
          No timeline events
        </div>
      )}
    </div>
  )
}
