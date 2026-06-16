export default function IncidentSummary({ incidents }) {
  const rows = incidents ?? []

  function fmtDate(iso) {
    return new Date(iso).toLocaleString('en-GB', {
      day: '2-digit', month: 'short', hour: '2-digit', minute: '2-digit'
    })
  }

  const statusColor = {
    active:        'var(--red)',
    investigating: 'var(--orange)',
    resolved:      'var(--green)',
    contained:     'var(--cyan)',
  }

  return (
    <div style={{ overflowX: 'auto' }}>
      <table className="data-table">
        <thead>
          <tr>
            <th>ID</th>
            <th>Title</th>
            <th>Severity</th>
            <th>Status</th>
            <th>Affected</th>
            <th>Analyst</th>
            <th>Opened</th>
          </tr>
        </thead>
        <tbody>
          {rows.map((inc) => (
            <tr key={inc.id}>
              <td style={{ fontFamily: 'var(--font-mono)', fontSize: '0.76rem', color: 'var(--cyan)' }}>
                {inc.id}
              </td>
              <td style={{ color: 'var(--text-primary)', fontWeight: 500, maxWidth: 260, whiteSpace: 'nowrap', overflow: 'hidden', textOverflow: 'ellipsis' }}>
                {inc.title}
              </td>
              <td>
                <span className={`severity-badge ${inc.severity}`}>{inc.severity}</span>
              </td>
              <td>
                <span style={{
                  fontSize: '0.72rem', fontFamily: 'var(--font-mono)', fontWeight: 600,
                  color: statusColor[inc.status] ?? 'var(--text-muted)',
                  display: 'flex', alignItems: 'center', gap: 5,
                }}>
                  <span style={{ width: 6, height: 6, borderRadius: '50%', background: statusColor[inc.status], display: 'inline-block' }} />
                  {inc.status.toUpperCase()}
                </span>
              </td>
              <td style={{ fontFamily: 'var(--font-mono)', color: 'var(--orange)', fontWeight: 600 }}>
                {inc.affected}
              </td>
              <td style={{ color: 'var(--text-secondary)' }}>
                {inc.analyst}
              </td>
              <td style={{ fontFamily: 'var(--font-mono)', fontSize: '0.74rem', color: 'var(--text-muted)', whiteSpace: 'nowrap' }}>
                {fmtDate(inc.opened)}
              </td>
            </tr>
          ))}
          {rows.length === 0 && (
            <tr>
              <td colSpan={7} style={{ textAlign: 'center', padding: '30px', color: 'var(--text-muted)' }}>
                No incidents found
              </td>
            </tr>
          )}
        </tbody>
      </table>
    </div>
  )
}
