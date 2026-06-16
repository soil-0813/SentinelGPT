import { PieChart, Pie, Cell, Tooltip, ResponsiveContainer } from 'recharts'

const COLORS = {
  critical: '#ff3b5c',
  high:     '#ff8c42',
  medium:   '#fbbf24',
  low:      '#00ff88',
  info:     '#00c8ff',
}

const CustomTooltip = ({ active, payload }) => {
  if (!active || !payload?.length) return null
  const { name, value } = payload[0]
  return (
    <div style={{
      background: 'var(--bg-elevated)',
      border: '1px solid var(--border-bright)',
      borderRadius: 'var(--radius-md)',
      padding: '10px 14px',
      fontSize: '0.8rem',
    }}>
      <div style={{ color: COLORS[name] ?? 'var(--cyan)', fontWeight: 700, textTransform: 'uppercase', marginBottom: 2 }}>{name}</div>
      <div style={{ color: 'var(--text-primary)', fontFamily: 'var(--font-mono)', fontSize: '1rem', fontWeight: 600 }}>{value}</div>
      <div style={{ color: 'var(--text-muted)', fontSize: '0.72rem' }}>alerts today</div>
    </div>
  )
}

export default function SeverityChart({ data }) {
  const chartData = data ?? [
    { name: 'critical', value: 7  },
    { name: 'high',     value: 15 },
    { name: 'medium',   value: 22 },
    { name: 'low',      value: 31 },
    { name: 'info',     value: 67 },
  ]

  const total = chartData.reduce((s, d) => s + d.value, 0)

  return (
    <div style={{ width: '100%', display: 'flex', flexDirection: 'column', gap: 16 }}>
      {/* Donut chart — always centred, never clips */}
      <div style={{ position: 'relative', width: '100%', height: 170 }}>
        <ResponsiveContainer width="100%" height="100%">
          <PieChart>
            <Pie
              data={chartData}
              cx="50%"
              cy="50%"
              innerRadius={52}
              outerRadius={74}
              paddingAngle={3}
              dataKey="value"
              strokeWidth={0}
            >
              {chartData.map((entry) => (
                <Cell
                  key={entry.name}
                  fill={COLORS[entry.name] ?? '#666'}
                  style={{
                    filter: `drop-shadow(0 0 5px ${COLORS[entry.name] ?? '#666'}66)`,
                    cursor: 'pointer',
                  }}
                />
              ))}
            </Pie>
            <Tooltip content={<CustomTooltip />} />
          </PieChart>
        </ResponsiveContainer>

        {/* Centre label — always on top of the donut hole */}
        <div style={{
          position: 'absolute',
          top: '50%', left: '50%',
          transform: 'translate(-50%, -50%)',
          textAlign: 'center',
          pointerEvents: 'none',
        }}>
          <div style={{
            fontFamily: 'var(--font-mono)',
            fontSize: '1.45rem',
            fontWeight: 700,
            color: 'var(--text-primary)',
            lineHeight: 1,
          }}>
            {total}
          </div>
          <div style={{
            fontSize: '0.6rem',
            color: 'var(--text-muted)',
            textTransform: 'uppercase',
            letterSpacing: '0.08em',
            marginTop: 4,
          }}>
            Total
          </div>
        </div>
      </div>

      {/* Legend — rendered outside the SVG, wraps naturally */}
      <div style={{
        display: 'flex',
        flexWrap: 'wrap',
        gap: '8px 18px',
        justifyContent: 'center',
      }}>
        {chartData.map(({ name, value }) => (
          <div key={name} style={{ display: 'flex', alignItems: 'center', gap: 6 }}>
            <div style={{
              width: 8, height: 8,
              borderRadius: '50%',
              background: COLORS[name] ?? '#666',
              boxShadow: `0 0 6px ${COLORS[name] ?? '#666'}`,
              flexShrink: 0,
            }} />
            <span style={{
              fontSize: '0.75rem',
              color: 'var(--text-secondary)',
              textTransform: 'capitalize',
              fontFamily: 'var(--font-mono)',
            }}>
              {name}
            </span>
            <span style={{
              fontSize: '0.72rem',
              color: COLORS[name] ?? 'var(--text-muted)',
              fontFamily: 'var(--font-mono)',
              fontWeight: 600,
            }}>
              {value}
            </span>
          </div>
        ))}
      </div>
    </div>
  )
}
