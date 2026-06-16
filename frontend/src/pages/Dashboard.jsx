import { useEffect, useState } from 'react'
import {
  AreaChart, Area, XAxis, YAxis, CartesianGrid,
  Tooltip, ResponsiveContainer
} from 'recharts'
import {
  AlertTriangle, ShieldOff, CheckCircle2, Flame,
  RefreshCw, Activity, TrendingUp, TrendingDown
} from 'lucide-react'

import SeverityChart   from '../components/SeverityChart.jsx'
import ThreatTimeline  from '../components/ThreatTimeline.jsx'
import IncidentSummary from '../components/IncidentSummary.jsx'
import MitreMapping    from '../components/MitreMapping.jsx'
import ThreatIntelPanel from '../components/ThreatIntelPanel.jsx'
import AlertCard        from '../components/AlertCard.jsx'

import {
  fetchDashboardStats, fetchAlerts, fetchIncidents,
  MOCK_TIMELINE
} from '../services/api.js'

const ACTIVITY_DATA = [
  { h: '00', events: 14 }, { h: '01', events: 9  }, { h: '02', events: 6  },
  { h: '03', events: 18 }, { h: '04', events: 32 }, { h: '05', events: 27 },
  { h: '06', events: 41 }, { h: '07', events: 55 }, { h: '08', events: 63 },
  { h: '09', events: 47 }, { h: '10', events: 38 }, { h: '11', events: 52 },
  { h: '12', events: 29 }, { h: '13', events: 18 },
]

const CustomAreaTooltip = ({ active, payload, label }) => {
  if (!active || !payload?.length) return null
  return (
    <div style={{
      background: 'var(--bg-elevated)', border: '1px solid var(--border-bright)',
      borderRadius: 'var(--radius-md)', padding: '8px 14px', fontSize: '0.78rem',
    }}>
      <div style={{ color: 'var(--text-muted)', marginBottom: 3 }}>{label}:00 UTC</div>
      <div style={{ color: 'var(--cyan)', fontFamily: 'var(--font-mono)', fontWeight: 700 }}>
        {payload[0].value} events
      </div>
    </div>
  )
}

export default function Dashboard() {
  const [stats, setStats]         = useState(null)
  const [alerts, setAlerts]       = useState([])
  const [incidents, setIncidents] = useState([])
  const [loading, setLoading]     = useState(true)
  const [lastRefresh, setLastRefresh] = useState(new Date())

  async function load() {
    setLoading(true)
    const [s, a, inc] = await Promise.all([
      fetchDashboardStats(),
      fetchAlerts(),
      fetchIncidents(),
    ])
    setStats(s)
    setAlerts(a)
    setIncidents(inc)
    setLastRefresh(new Date())
    setLoading(false)
  }

  useEffect(() => { load() }, [])

  const STAT_CARDS = [
    {
      label: 'Total Incidents',
      value: stats?.total_incidents ?? 142,
      icon: <Activity size={20} />,
      iconBg: 'rgba(0,200,255,0.12)',
      iconColor: 'var(--cyan)',
      accentColor: 'var(--cyan)',
      accentGlow: 'rgba(0,200,255,0.15)',
      delta: { label: '+12 from yesterday', dir: 'up' },
    },
    {
      label: 'Active Threats',
      value: stats?.active_threats ?? 23,
      icon: <ShieldOff size={20} />,
      iconBg: 'rgba(255,59,92,0.12)',
      iconColor: 'var(--red)',
      accentColor: 'var(--red)',
      accentGlow: 'rgba(255,59,92,0.15)',
      delta: { label: '3 escalated', dir: 'up' },
    },
    {
      label: 'Resolved Today',
      value: stats?.resolved_today ?? 58,
      icon: <CheckCircle2 size={20} />,
      iconBg: 'rgba(0,255,136,0.1)',
      iconColor: 'var(--green)',
      accentColor: 'var(--green)',
      accentGlow: 'rgba(0,255,136,0.12)',
      delta: { label: '89% resolution rate', dir: 'down' },
    },
    {
      label: 'Critical Alerts',
      value: stats?.critical_alerts ?? 7,
      icon: <Flame size={20} />,
      iconBg: 'rgba(255,140,66,0.12)',
      iconColor: 'var(--orange)',
      accentColor: 'var(--orange)',
      accentGlow: 'rgba(255,140,66,0.15)',
      delta: { label: 'Needs attention', dir: 'up' },
    },
  ]

  return (
    <div className="page-body">
      {/* Page Header */}
      <div style={{ display: 'flex', alignItems: 'center', justifyContent: 'space-between', marginBottom: 24 }}>
        <div className="page-header" style={{ marginBottom: 0 }}>
          <h1>SOC Dashboard</h1>
          <p>Real-time security operations overview · {lastRefresh.toLocaleTimeString()}</p>
        </div>
        <button
          className="btn btn-ghost btn-sm"
          onClick={load}
          disabled={loading}
          style={{ display: 'flex', alignItems: 'center', gap: 6 }}
        >
          <RefreshCw size={14} className={loading ? 'spin' : ''} style={loading ? { animation: 'spin 0.7s linear infinite' } : {}} />
          Refresh
        </button>
      </div>

      {/* Stat Cards */}
      <div className="stat-grid">
        {STAT_CARDS.map((c) => (
          <div
            key={c.label}
            className="stat-card"
            style={{
              '--accent-color': c.accentColor,
              '--accent-glow':  c.accentGlow,
            }}
          >
            <div className="stat-icon" style={{ background: c.iconBg, color: c.iconColor }}>
              {c.icon}
            </div>
            <div className="stat-value" style={{ color: c.accentColor }}>{loading ? '—' : c.value}</div>
            <div className="stat-label">{c.label}</div>
            <div className={`stat-delta ${c.delta.dir}`}>
              {c.delta.dir === 'up' ? <TrendingUp size={11} /> : <TrendingDown size={11} />}
              {c.delta.label}
            </div>
          </div>
        ))}
      </div>

      {/* Activity Chart + Severity Chart */}
      <div className="dashboard-grid" style={{ gridTemplateColumns: '2fr 1fr', marginBottom: 20 }}>
        {/* Activity Area Chart */}
        <div className="card">
          <div className="card-header">
            <span className="card-title">Event Activity (24h)</span>
            <span className="card-badge cyan">LIVE</span>
          </div>
          <ResponsiveContainer width="100%" height={180}>
            <AreaChart data={ACTIVITY_DATA} margin={{ top: 5, right: 10, bottom: 0, left: -25 }}>
              <defs>
                <linearGradient id="areaGrad" x1="0" y1="0" x2="0" y2="1">
                  <stop offset="5%"  stopColor="#00c8ff" stopOpacity={0.25} />
                  <stop offset="95%" stopColor="#00c8ff" stopOpacity={0.02} />
                </linearGradient>
              </defs>
              <CartesianGrid strokeDasharray="3 3" />
              <XAxis dataKey="h" tick={{ fontSize: 11, fill: 'var(--text-muted)', fontFamily: 'var(--font-mono)' }} />
              <YAxis tick={{ fontSize: 11, fill: 'var(--text-muted)', fontFamily: 'var(--font-mono)' }} />
              <Tooltip content={<CustomAreaTooltip />} />
              <Area
                type="monotone" dataKey="events"
                stroke="#00c8ff" strokeWidth={2}
                fill="url(#areaGrad)"
                dot={false} activeDot={{ r: 5, fill: '#00c8ff', stroke: '#000', strokeWidth: 2 }}
              />
            </AreaChart>
          </ResponsiveContainer>
        </div>

        {/* Severity Donut */}
        <div className="card">
          <div className="card-header">
            <span className="card-title">Alert Severity</span>
            <span className="card-badge red">TODAY</span>
          </div>
          <SeverityChart />
        </div>
      </div>

      {/* Attack Timeline + Threat Intel */}
      <div className="dashboard-grid" style={{ gridTemplateColumns: '1fr 1fr', marginBottom: 20 }}>
        <div className="card" style={{ maxHeight: 440, overflow: 'hidden', display: 'flex', flexDirection: 'column' }}>
          <div className="card-header">
            <span className="card-title">Attack Timeline</span>
            <span className="card-badge cyan">{MOCK_TIMELINE.length} events</span>
          </div>
          <div style={{ flex: 1, overflowY: 'auto', paddingRight: 4 }}>
            <ThreatTimeline events={MOCK_TIMELINE} />
          </div>
        </div>

        <div className="card" style={{ maxHeight: 440, overflow: 'hidden', display: 'flex', flexDirection: 'column' }}>
          <div className="card-header">
            <span className="card-title">Threat Intelligence</span>
            <span className="card-badge green">FEEDS</span>
          </div>
          <div style={{ flex: 1, overflowY: 'auto' }}>
            <ThreatIntelPanel />
          </div>
        </div>
      </div>

      {/* MITRE Mapping */}
      <div className="card" style={{ marginBottom: 20 }}>
        <div className="card-header">
          <span className="card-title">MITRE ATT&CK Mapping</span>
          <span className="card-badge" style={{ color: 'var(--purple)', borderColor: 'rgba(168,85,247,0.35)', background: 'var(--purple-glow)' }}>
            {incidents.flatMap(i => i.mitre ?? []).filter(Boolean).length} techniques
          </span>
        </div>
        <MitreMapping highlighted={incidents.flatMap(i => i.mitre ?? []).filter(Boolean)} />
      </div>

      {/* Active Alerts */}
      <div className="card" style={{ marginBottom: 20 }}>
        <div className="card-header">
          <span className="card-title">Active Alerts</span>
          <div style={{ display: 'flex', gap: 8 }}>
            <span className="card-badge red">{alerts.filter(a => a.status === 'open').length} OPEN</span>
          </div>
        </div>
        <div style={{ display: 'flex', flexDirection: 'column', gap: 8 }}>
          {alerts.slice(0, 6).map(a => (
            <AlertCard key={a.id} alert={a} />
          ))}
        </div>
      </div>

      {/* Incident Table */}
      <div className="card">
        <div className="card-header">
          <span className="card-title">Incident Log</span>
          <span className="card-badge cyan">{incidents.length} total</span>
        </div>
        <IncidentSummary incidents={incidents} />
      </div>
    </div>
  )
}
