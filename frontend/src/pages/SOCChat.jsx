import { useState, useRef, useEffect } from 'react'
import { Send, Bot, User, Shield, Zap, Globe, FileText, RotateCcw } from 'lucide-react'
import { sendChatMessage } from '../services/api.js'

const QUICK_PROMPTS = [
  { icon: <Shield size={13} />, text: 'Explain the current critical alerts' },
  { icon: <Zap size={13} />,    text: 'What MITRE techniques were detected today?' },
  { icon: <Globe size={13} />,  text: 'Analyze the active IOCs and their risk' },
  { icon: <FileText size={13} />, text: 'Recommend remediation steps for the top incident' },
]

const WELCOME_MSG = {
  id: 'welcome',
  role: 'assistant',
  content: `Hello! I'm **SentinelGPT**, your AI-powered SOC assistant. I have full context of your current security posture, active incidents, and threat intelligence feeds.

I can help you:
- **Analyze threats** and explain attack patterns
- **Correlate IOCs** against threat databases
- **Map behaviors** to MITRE ATT&CK techniques
- **Generate reports** and incident summaries
- **Recommend remediation** steps for active incidents

Ask me anything about your current security environment.`,
  time: new Date(),
}

function renderContent(text) {
  // Simple inline markdown: **bold**, `code`
  return text
    .split('\n')
    .map((line, i) => {
      const parts = line
        .replace(/\*\*(.*?)\*\*/g, '<strong>$1</strong>')
        .replace(/`(.*?)`/g, '<code>$1</code>')
      return <p key={i} style={{ margin: '3px 0' }} dangerouslySetInnerHTML={{ __html: parts || '&nbsp;' }} />
    })
}

function formatTime(date) {
  return new Date(date).toLocaleTimeString('en-GB', { hour: '2-digit', minute: '2-digit' })
}

export default function SOCChat() {
  const [messages, setMessages] = useState([WELCOME_MSG])
  const [input, setInput]       = useState('')
  const [loading, setLoading]   = useState(false)
  const bottomRef               = useRef(null)
  const textareaRef             = useRef(null)

  useEffect(() => {
    bottomRef.current?.scrollIntoView({ behavior: 'smooth' })
  }, [messages, loading])

  function autoGrow(e) {
    e.target.style.height = 'auto'
    e.target.style.height = Math.min(e.target.scrollHeight, 140) + 'px'
  }

  async function send() {
    const msg = input.trim()
    if (!msg || loading) return

    const userMsg = { id: Date.now(), role: 'user', content: msg, time: new Date() }
    setMessages(prev => [...prev, userMsg])
    setInput('')
    if (textareaRef.current) {
      textareaRef.current.style.height = 'auto'
    }
    setLoading(true)

    const history = messages
      .filter(m => m.id !== 'welcome')
      .map(m => ({ role: m.role, content: m.content }))

    try {
      const res = await sendChatMessage(msg, history)
      setMessages(prev => [
        ...prev,
        { id: Date.now() + 1, role: 'assistant', content: res.reply ?? res.message ?? 'No response.', time: new Date() }
      ])
    } catch {
      setMessages(prev => [
        ...prev,
        { id: Date.now() + 1, role: 'assistant', content: 'Error contacting backend. Please try again.', time: new Date() }
      ])
    } finally {
      setLoading(false)
    }
  }

  function handleKey(e) {
    if (e.key === 'Enter' && !e.shiftKey) {
      e.preventDefault()
      send()
    }
  }

  function clearChat() {
    setMessages([WELCOME_MSG])
  }

  return (
    <div style={{ display: 'flex', flexDirection: 'column', height: '100%', overflow: 'hidden' }}>
      {/* Topbar */}
      <div className="topbar">
        <div style={{ display: 'flex', alignItems: 'center', gap: 12 }}>
          <div style={{
            width: 36, height: 36, borderRadius: '50%',
            background: 'linear-gradient(135deg, #0d1b30, #1a2f50)',
            border: '1px solid var(--border-bright)',
            display: 'flex', alignItems: 'center', justifyContent: 'center',
          }}>
            <Bot size={17} color="var(--cyan)" />
          </div>
          <div>
            <div className="topbar-title">SentinelGPT Assistant</div>
            <div style={{ fontSize: '0.72rem', color: 'var(--green)', fontFamily: 'var(--font-mono)', display: 'flex', alignItems: 'center', gap: 5 }}>
              <span style={{ width: 6, height: 6, borderRadius: '50%', background: 'var(--green)', display: 'inline-block', animation: 'pulse-green 2s infinite' }} />
              Online · RAG + Threat Intel Active
            </div>
          </div>
        </div>
        <div style={{ display: 'flex', gap: 8 }}>
          <button className="btn btn-ghost btn-sm" onClick={clearChat}>
            <RotateCcw size={13} /> Clear
          </button>
        </div>
      </div>

      {/* Quick prompts */}
      <div style={{
        padding: '12px 24px',
        background: 'var(--bg-deep)',
        borderBottom: '1px solid var(--border)',
        display: 'flex', gap: 8, flexWrap: 'wrap',
      }}>
        {QUICK_PROMPTS.map((p, i) => (
          <button
            key={i}
            className="btn btn-ghost btn-sm"
            style={{ fontSize: '0.76rem', gap: 6 }}
            onClick={() => { setInput(p.text); textareaRef.current?.focus() }}
          >
            {p.icon} {p.text}
          </button>
        ))}
      </div>

      {/* Messages */}
      <div className="chat-messages">
        {messages.map((msg) => (
          <div key={msg.id} className={`chat-message ${msg.role}`}>
            <div className={`msg-avatar ${msg.role === 'user' ? 'user-avatar' : 'ai-avatar'}`}>
              {msg.role === 'user' ? <User size={15} /> : <Bot size={15} />}
            </div>
            <div>
              <div className={`msg-bubble ${msg.role}`}>
                {renderContent(msg.content)}
              </div>
              <div className={`msg-time ${msg.role === 'user' ? '' : ''}`} style={{ textAlign: msg.role === 'user' ? 'right' : 'left' }}>
                {formatTime(msg.time)}
              </div>
            </div>
          </div>
        ))}

        {/* Typing indicator */}
        {loading && (
          <div className="chat-message assistant">
            <div className="msg-avatar ai-avatar">
              <Bot size={15} />
            </div>
            <div className="msg-bubble assistant">
              <div className="typing-indicator">
                <div className="typing-dot" />
                <div className="typing-dot" />
                <div className="typing-dot" />
              </div>
            </div>
          </div>
        )}

        <div ref={bottomRef} />
      </div>

      {/* Input */}
      <div className="chat-input-area">
        <div className="chat-input-wrapper">
          <textarea
            ref={textareaRef}
            value={input}
            onChange={e => { setInput(e.target.value); autoGrow(e) }}
            onKeyDown={handleKey}
            placeholder="Ask about threats, IOCs, incidents, MITRE techniques… (Enter to send)"
            rows={1}
            disabled={loading}
          />
          <button
            className="chat-send-btn"
            onClick={send}
            disabled={!input.trim() || loading}
            title="Send (Enter)"
          >
            <Send size={15} />
          </button>
        </div>
        <div style={{ textAlign: 'center', fontSize: '0.68rem', color: 'var(--text-dim)', marginTop: 8 }}>
          SentinelGPT may make mistakes. Always verify conclusions with your team.
        </div>
      </div>
    </div>
  )
}
