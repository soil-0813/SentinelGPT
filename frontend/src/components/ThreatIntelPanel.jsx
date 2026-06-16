import { Globe, AlertOctagon, Shield, Zap } from 'lucide-react'

const INTEL_ITEMS = [
  {
    icon: <Globe size={16} color="var(--red)" />,
    bg: 'rgba(255,59,92,0.1)',
    title: '185.220.101.47',
    sub: 'TOR Exit Node · Brute Force Source · Blacklisted',
    severity: 'critical',
  },
  {
    icon: <AlertOctagon size={16} color="var(--orange)" />,
    bg: 'rgba(255,140,66,0.1)',
    title: '203.0.113.89',
    sub: 'Known C2 Server · Cobalt Strike Infrastructure',
    severity: 'high',
  },
  {
    icon: <Zap size={16} color="var(--yellow)" />,
    bg: 'rgba(251,191,36,0.1)',
    title: 'Emotet v5 Variant',
    sub: 'SHA256: b71c3a… · CVE-2024-21887 exploited',
    severity: 'high',
  },
  {
    icon: <Shield size={16} color="var(--cyan)" />,
    bg: 'var(--cyan-glow)',
    title: 'APT29 Campaign',
    sub: 'Nation-state · Persistence · Russia-linked',
    severity: 'critical',
  },
  {
    icon: <Globe size={16} color="var(--purple)" />,
    bg: 'var(--purple-glow)',
    title: 'c2.malicious-domain[.]com',
    sub: 'DNS Tunneling · Newly registered · Blocked',
    severity: 'medium',
  },
]

export default function ThreatIntelPanel({ items }) {
  const data = items ?? INTEL_ITEMS

  return (
    <div style={{ display: 'flex', flexDirection: 'column' }}>
      {data.map((item, i) => (
        <div key={i} className="intel-item">
          <div className="intel-icon" style={{ background: item.bg }}>
            {item.icon}
          </div>
          <div className="intel-text">
            <div className="intel-title" style={{ fontFamily: 'var(--font-mono)', fontSize: '0.78rem' }}>
              {item.title}
            </div>
            <div className="intel-sub">{item.sub}</div>
          </div>
          <span className={`severity-badge ${item.severity}`} style={{ flexShrink: 0, fontSize: '0.65rem' }}>
            {item.severity}
          </span>
        </div>
      ))}
    </div>
  )
}
