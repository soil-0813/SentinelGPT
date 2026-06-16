const MITRE_DATA = [
  { id: 'T1110',     name: 'Brute Force',           tactic: 'Credential Access' },
  { id: 'T1059.001', name: 'PowerShell',             tactic: 'Execution' },
  { id: 'T1003.001', name: 'LSASS Memory',           tactic: 'Credential Access' },
  { id: 'T1048',     name: 'Exfil Alt Protocol',     tactic: 'Exfiltration' },
  { id: 'T1046',     name: 'Network Scan',           tactic: 'Discovery' },
  { id: 'T1071.004', name: 'DNS Tunneling',          tactic: 'C2' },
  { id: 'T1566',     name: 'Phishing',               tactic: 'Initial Access' },
  { id: 'T1021',     name: 'Remote Services',        tactic: 'Lateral Movement' },
  { id: 'T1548',     name: 'Privilege Escalation',   tactic: 'Privilege Escalation' },
  { id: 'T1560',     name: 'Archive Data',           tactic: 'Collection' },
  { id: 'T1204',     name: 'User Execution',         tactic: 'Execution' },
  { id: 'T1486',     name: 'Data Encrypted',         tactic: 'Impact' },
]

export default function MitreMapping({ highlighted = [] }) {
  const active = new Set(highlighted)

  return (
    <div style={{ display: 'flex', flexDirection: 'column', gap: 10 }}>
      <div style={{ fontSize: '0.75rem', color: 'var(--text-muted)', marginBottom: 4 }}>
        Detected techniques from today's incidents
      </div>
      <div className="mitre-grid">
        {MITRE_DATA.map((t) => {
          const isActive = active.has(t.id) || active.size === 0
          return (
            <div
              key={t.id}
              className="mitre-tag"
              style={{
                opacity: active.size > 0 && !active.has(t.id) ? 0.35 : 1,
                borderColor: active.has(t.id) ? 'var(--purple)' : undefined,
                background: active.has(t.id) ? 'var(--purple-glow)' : undefined,
              }}
            >
              <div className="mitre-id">{t.id}</div>
              <div className="mitre-name">{t.name}</div>
              <div style={{ fontSize: '0.66rem', color: 'var(--text-dim)', marginTop: 3 }}>{t.tactic}</div>
            </div>
          )
        })}
      </div>
    </div>
  )
}
