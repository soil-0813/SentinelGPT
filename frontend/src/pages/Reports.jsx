import { useState, useEffect } from 'react'
import {
  FileText, Download, RefreshCw, Plus,
  AlertTriangle, CheckCircle2, Clock, Shield
} from 'lucide-react'
import { fetchReports, generateReport, MOCK_REPORTS } from '../services/api.js'

const REPORT_TYPE_ICONS = {
  incident: <AlertTriangle size={14} color="var(--red)" />,
  threat:   <Shield size={14} color="var(--orange)" />,
  summary:  <CheckCircle2 size={14} color="var(--green)" />,
}

const SEVERITY_COLOR = {
  critical: 'var(--red)',
  high:     'var(--orange)',
  medium:   'var(--yellow)',
  low:      'var(--green)',
}

function fmtDate(iso) {
  return new Date(iso).toLocaleDateString('en-GB', {
    day: '2-digit', month: 'short', year: 'numeric',
    hour: '2-digit', minute: '2-digit'
  })
}

function ReportListItem({ report, isActive, onClick }) {
  return (
    <div
      className={`report-item ${isActive ? 'active' : ''}`}
      onClick={onClick}
      role="button"
      tabIndex={0}
    >
      <div style={{ display: 'flex', alignItems: 'center', gap: 7, marginBottom: 6 }}>
        {REPORT_TYPE_ICONS[report.type] ?? <FileText size={14} />}
        <span className="report-item-title">{report.title}</span>
      </div>
      <div className="report-item-meta">
        <span style={{ color: SEVERITY_COLOR[report.severity] }}>⬤ {report.severity}</span>
        <span>{report.analyst}</span>
        <span>{fmtDate(report.created)}</span>
      </div>
    </div>
  )
}

function ReportViewer({ report }) {
  if (!report) {
    return (
      <div className="report-viewer" style={{ alignItems: 'center', justifyContent: 'center' }}>
        <div className="empty-state">
          <FileText size={48} color="var(--text-muted)" />
          <p>Select a report from the list to view it here.</p>
        </div>
      </div>
    )
  }

  function downloadMock() {
    const content = Object.entries(report.sections)
      .map(([k, v]) => `\n## ${k.replace(/_/g, ' ').toUpperCase()}\n${v}`)
      .join('\n')
    const blob = new Blob([`# ${report.title}\n\n${content}`], { type: 'text/plain' })
    const url  = URL.createObjectURL(blob)
    const a    = document.createElement('a')
    a.href = url; a.download = `${report.id}.txt`; a.click()
    URL.revokeObjectURL(url)
  }

  return (
    <div className="report-viewer">
      {/* Header */}
      <div className="report-viewer-header">
        <div>
          <div style={{ display: 'flex', alignItems: 'center', gap: 8, marginBottom: 4 }}>
            {REPORT_TYPE_ICONS[report.type]}
            <span style={{ fontSize: '1rem', fontWeight: 700, color: 'var(--text-primary)' }}>{report.title}</span>
          </div>
          <div style={{ display: 'flex', gap: 12, fontSize: '0.74rem', color: 'var(--text-muted)', fontFamily: 'var(--font-mono)', flexWrap: 'wrap' }}>
            <span>ID: {report.id}</span>
            <span>Analyst: {report.analyst}</span>
            <span>Created: {fmtDate(report.created)}</span>
            <span style={{ color: SEVERITY_COLOR[report.severity] }}>Severity: {report.severity.toUpperCase()}</span>
          </div>
        </div>
        <button className="btn btn-ghost btn-sm" onClick={downloadMock}>
          <Download size={13} /> Export
        </button>
      </div>

      {/* Body */}
      <div className="report-viewer-body">
        {/* Summary banner */}
        <div style={{
          background: 'var(--bg-elevated)', border: '1px solid var(--border)',
          borderLeft: `3px solid ${SEVERITY_COLOR[report.severity]}`,
          borderRadius: 'var(--radius-md)', padding: '14px 18px', marginBottom: 24,
        }}>
          <div style={{ fontSize: '0.72rem', color: 'var(--text-muted)', textTransform: 'uppercase', letterSpacing: '0.08em', marginBottom: 6 }}>TL;DR</div>
          <p style={{ fontSize: '0.87rem', color: 'var(--text-secondary)', lineHeight: 1.7, margin: 0 }}>{report.summary}</p>
        </div>

        {/* Sections */}
        {Object.entries(report.sections).map(([key, value]) => (
          <div key={key} className="report-section">
            <h3>{key.replace(/_/g, ' ')}</h3>
            <p>{value}</p>
          </div>
        ))}

        {/* Footer watermark */}
        <div className="glow-line" />
        <div style={{
          display: 'flex', alignItems: 'center', justifyContent: 'space-between',
          fontSize: '0.72rem', color: 'var(--text-dim)', fontFamily: 'var(--font-mono)',
        }}>
          <span>SentinelGPT · Automated Report · {report.id}</span>
          <span>Generated {fmtDate(report.created)}</span>
        </div>
      </div>
    </div>
  )
}

export default function Reports() {
  const [reports, setReports]     = useState([])
  const [selected, setSelected]   = useState(null)
  const [loading, setLoading]     = useState(true)
  const [generating, setGenerating] = useState(false)

  async function load() {
    setLoading(true)
    const data = await fetchReports()
    setReports(data ?? MOCK_REPORTS)
    if (data?.length) setSelected(data[0])
    setLoading(false)
  }

  useEffect(() => { load() }, [])

  async function handleGenerate(type) {
    setGenerating(true)
    const newReport = await generateReport(type)
    if (newReport) {
      setReports(prev => [newReport, ...prev])
      setSelected(newReport)
    }
    setGenerating(false)
  }

  return (
    <div className="page-body" style={{ display: 'flex', flexDirection: 'column', height: '100%' }}>
      {/* Page header */}
      <div style={{ display: 'flex', alignItems: 'center', justifyContent: 'space-between', marginBottom: 20 }}>
        <div className="page-header" style={{ marginBottom: 0 }}>
          <h1>Reports</h1>
          <p>Incident reports, threat briefs, and daily SOC summaries</p>
        </div>
        <div style={{ display: 'flex', gap: 8 }}>
          <button className="btn btn-ghost btn-sm" onClick={load} disabled={loading}>
            <RefreshCw size={13} style={loading ? { animation: 'spin 0.7s linear infinite' } : {}} />
            Refresh
          </button>
          <button
            className="btn btn-primary btn-sm"
            onClick={() => handleGenerate('incident')}
            disabled={generating}
          >
            <Plus size={14} />
            {generating ? 'Generating…' : 'New Report'}
          </button>
        </div>
      </div>

      {/* Report type quick filters */}
      <div style={{ display: 'flex', gap: 8, marginBottom: 20, flexWrap: 'wrap' }}>
        {['all', 'incident', 'threat', 'summary'].map(type => (
          <button key={type} className="btn btn-ghost btn-sm" style={{ textTransform: 'capitalize', fontSize: '0.76rem' }}>
            {type === 'all' ? 'All Reports' : type}
          </button>
        ))}
      </div>

      {/* Main layout */}
      <div className="reports-layout" style={{ flex: 1, minHeight: 0 }}>
        {/* List */}
        <div>
          <div style={{ fontSize: '0.72rem', color: 'var(--text-muted)', textTransform: 'uppercase', letterSpacing: '0.08em', marginBottom: 12, fontWeight: 600 }}>
            {reports.length} Reports
          </div>
          <div className="report-list">
            {loading
              ? Array(3).fill(0).map((_, i) => (
                  <div key={i} style={{ height: 75, background: 'var(--bg-elevated)', borderRadius: 'var(--radius-md)', border: '1px solid var(--border)' }} />
                ))
              : reports.map(r => (
                  <ReportListItem
                    key={r.id}
                    report={r}
                    isActive={selected?.id === r.id}
                    onClick={() => setSelected(r)}
                  />
                ))
            }
          </div>
        </div>

        {/* Viewer */}
        <ReportViewer report={selected} />
      </div>
    </div>
  )
}
