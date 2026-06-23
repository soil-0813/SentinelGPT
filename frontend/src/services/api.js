const BASE_URL = "/api";

async function request(path, options = {}) {
  try {
    const res = await fetch(`${BASE_URL}${path}`, {
      headers: { "Content-Type": "application/json", ...options.headers },
      ...options,
    });
    if (!res.ok) throw new Error(`HTTP ${res.status}`);
    return await res.json();
  } catch (err) {
    console.warn(`[API] ${path} failed — using mock data. (${err.message})`);
    return null;
  }
}

// ── Alerts ─────────────────────────────────────────────
export async function fetchAlerts() {
  const data = await request("/alerts");
  return data ?? MOCK_ALERTS;
}

export async function fetchAlertById(id) {
  const data = await request(`/alerts/${id}`);
  return data ?? MOCK_ALERTS.find((a) => a.id === id) ?? null;
}

// ── Incidents ───────────────────────────────────────────
export async function fetchIncidents() {
  const data = await request("/incidents");
  return data ?? MOCK_INCIDENTS;
}

// ── Stats ───────────────────────────────────────────────
export async function fetchDashboardStats() {
  try {
    return await request("/dashboard/stats");
  } catch (err) {
    console.error("Dashboard API failed", err);
    return MOCK_STATS;
  }
}

// ── Timeline ───────────────────────────────────────────────
export async function fetchTimeline() {
  const data = await request("/timeline");
  return data ?? MOCK_TIMELINE;
}

// ── Threat Intelligence ───────────────────────────────────────────────
export async function fetchThreatIntel() {
  return await request("/threat-intel");
}

// ── Chat ────────────────────────────────────────────────
export async function sendChatMessage(message, history = []) {
  const data = await request("/chat", {
    method: "POST",
    body: JSON.stringify({ message, history }),
  });
  if (data) return data;
  // Mock intelligent reply
  await new Promise((r) => setTimeout(r, 800 + Math.random() * 600));
  return { reply: getMockReply(message) };
}

// ── Reports ─────────────────────────────────────────────
export async function fetchReports() {
  const data = await request("/reports");
  return data ?? MOCK_REPORTS;
}

export async function generateReport(type, params = {}) {
  const data = await request("/reports/generate", {
    method: "POST",
    body: JSON.stringify({ type, ...params }),
  });
  return data ?? MOCK_REPORTS[0];
}

// ─────────────────────────────────────────────────────────
// Mock Data
// ─────────────────────────────────────────────────────────
export const MOCK_STATS = {
  total_incidents: 142,
  active_threats: 23,
  resolved_today: 58,
  critical_alerts: 7,
  threat_level: "HIGH",
  system_status: "OPERATIONAL",
};

export const MOCK_ALERTS = [
  {
    id: "ALT-001",
    title: "Brute Force Login Detected",
    description: "Multiple failed SSH login attempts from IP 185.220.101.47",
    severity: "critical",
    source: "auth.log",
    ip: "185.220.101.47",
    mitre: "T1110",
    timestamp: new Date(Date.now() - 4 * 60000).toISOString(),
    status: "open",
  },
  {
    id: "ALT-002",
    title: "Suspicious PowerShell Execution",
    description: "Encoded PowerShell command executed via winrm.exe",
    severity: "high",
    source: "endpoint-edr",
    ip: "192.168.10.45",
    mitre: "T1059.001",
    timestamp: new Date(Date.now() - 12 * 60000).toISOString(),
    status: "investigating",
  },
  {
    id: "ALT-003",
    title: "Data Exfiltration Attempt",
    description: "Large outbound transfer to unknown external host",
    severity: "critical",
    source: "network-monitor",
    ip: "203.0.113.89",
    mitre: "T1048",
    timestamp: new Date(Date.now() - 22 * 60000).toISOString(),
    status: "open",
  },
  {
    id: "ALT-004",
    title: "Port Scan Detected",
    description: "SYN scan from external IP across 5000+ ports",
    severity: "medium",
    source: "firewall",
    ip: "45.33.32.156",
    mitre: "T1046",
    timestamp: new Date(Date.now() - 38 * 60000).toISOString(),
    status: "open",
  },
  {
    id: "ALT-005",
    title: "Malware Hash Match",
    description: "File hash matches known Emotet variant in threat database",
    severity: "high",
    source: "av-scanner",
    ip: "10.0.0.22",
    mitre: "T1204",
    timestamp: new Date(Date.now() - 55 * 60000).toISOString(),
    status: "contained",
  },
  {
    id: "ALT-006",
    title: "Privilege Escalation",
    description: "User account granted unexpected admin privileges",
    severity: "high",
    source: "siem",
    ip: "10.0.1.5",
    mitre: "T1548",
    timestamp: new Date(Date.now() - 80 * 60000).toISOString(),
    status: "investigating",
  },
  {
    id: "ALT-007",
    title: "DNS Tunneling Activity",
    description: "Unusual DNS query patterns suggest DNS tunneling",
    severity: "medium",
    source: "dns-monitor",
    ip: "10.0.2.14",
    mitre: "T1071.004",
    timestamp: new Date(Date.now() - 110 * 60000).toISOString(),
    status: "open",
  },
  {
    id: "ALT-008",
    title: "Credential Dumping",
    description: "LSASS memory read by non-system process",
    severity: "critical",
    source: "endpoint-edr",
    ip: "192.168.1.88",
    mitre: "T1003.001",
    timestamp: new Date(Date.now() - 150 * 60000).toISOString(),
    status: "open",
  },
];

export const MOCK_INCIDENTS = [
  {
    id: "INC-2024-001",
    title: "APT29 Lateral Movement Campaign",
    severity: "critical",
    status: "active",
    affected: 12,
    analyst: "Aritra B.",
    opened: "2024-12-10T08:22:00Z",
    mitre: ["T1021", "T1078", "T1560"],
  },
  {
    id: "INC-2024-002",
    title: "Emotet Malware Outbreak",
    severity: "high",
    status: "active",
    affected: 5,
    analyst: "SOC Team",
    opened: "2024-12-10T11:44:00Z",
    mitre: ["T1204", "T1059", "T1566"],
  },
  {
    id: "INC-2024-003",
    title: "Insider Threat — Finance Dept",
    severity: "high",
    status: "investigating",
    affected: 2,
    analyst: "Aritra B.",
    opened: "2024-12-09T14:10:00Z",
    mitre: ["T1078", "T1048"],
  },
  {
    id: "INC-2024-004",
    title: "DDoS Attack — Web Infrastructure",
    severity: "medium",
    status: "resolved",
    affected: 0,
    analyst: "SOC Team",
    opened: "2024-12-08T09:30:00Z",
    mitre: ["T1498"],
  },
  {
    id: "INC-2024-005",
    title: "Phishing Campaign — HR Department",
    severity: "medium",
    status: "resolved",
    affected: 3,
    analyst: "Aritra B.",
    opened: "2024-12-07T13:00:00Z",
    mitre: ["T1566", "T1598"],
  },
  {
    id: "INC-2024-006",
    title: "Ransomware Precursor Activity",
    severity: "critical",
    status: "contained",
    affected: 7,
    analyst: "SOC Team",
    opened: "2024-12-06T07:15:00Z",
    mitre: ["T1486", "T1490"],
  },
];

export const MOCK_TIMELINE = [
  {
    id: 1,
    title: "Credential Dumping — LSASS",
    severity: "critical",
    time: "09:41 UTC",
    desc: "Non-system process accessed LSASS memory on WKSTN-088",
    ip: "192.168.1.88",
    mitre: "T1003.001",
  },
  {
    id: 2,
    title: "Brute Force Campaign Started",
    severity: "critical",
    time: "08:57 UTC",
    desc: "847 failed logins from TOR exit node in 3 minutes",
    ip: "185.220.101.47",
    mitre: "T1110",
  },
  {
    id: 3,
    title: "Lateral Movement Detected",
    severity: "high",
    time: "08:30 UTC",
    desc: "SMB connections to 8 internal hosts from compromised account",
    ip: "10.0.1.5",
    mitre: "T1021.002",
  },
  {
    id: 4,
    title: "Data Staging Observed",
    severity: "high",
    time: "07:55 UTC",
    desc: "Large archive created in temp directory before exfiltration",
    ip: "10.0.2.14",
    mitre: "T1560",
  },
  {
    id: 5,
    title: "Port Scan from External IP",
    severity: "medium",
    time: "06:22 UTC",
    desc: "SYN scan detected across full port range",
    ip: "45.33.32.156",
    mitre: "T1046",
  },
  {
    id: 6,
    title: "Suspicious DNS Queries",
    severity: "medium",
    time: "05:14 UTC",
    desc: "High-volume TXT record queries to newly registered domain",
    ip: "10.0.2.14",
    mitre: "T1071.004",
  },
  {
    id: 7,
    title: "C2 Beacon Established",
    severity: "critical",
    time: "04:03 UTC",
    desc: "Cobalt Strike beacon traffic to 203.0.113.89:443",
    ip: "192.168.10.45",
    mitre: "T1071.001",
  },
];

export const MOCK_REPORTS = [
  {
    id: "RPT-001",
    title: "Incident Report — APT29 Campaign",
    type: "incident",
    severity: "critical",
    created: "2024-12-10T08:00:00Z",
    analyst: "Aritra B.",
    summary:
      "Nation-state actor APT29 exploited a VPN vulnerability to gain initial access, then conducted lateral movement across 12 internal hosts over a 6-hour window.",
    sections: {
      executive_summary:
        "A sophisticated cyber intrusion attributed to APT29 was detected on December 10, 2024. The threat actor gained initial access through a known vulnerability in the Pulse Secure VPN appliance (CVE-2024-21887) and proceeded to perform extensive lateral movement and data reconnaissance.",
      timeline:
        "Initial compromise detected at 02:14 UTC. Lateral movement began at 04:03 UTC. Data staging observed at 07:55 UTC. Alert triggered at 08:22 UTC. Containment achieved at 11:30 UTC.",
      iocs: "185.220.101.47, 203.0.113.89, c2.malicious-domain[.]com, SHA256: 4a5f2c3b...",
      mitre_techniques:
        "T1078 (Valid Accounts), T1021 (Remote Services), T1560 (Archive Collected Data), T1071 (Application Layer Protocol)",
      remediation:
        "1. Reset all privileged credentials. 2. Patch CVE-2024-21887 on all VPN appliances. 3. Implement network segmentation. 4. Deploy EDR on remaining unprotected endpoints.",
    },
  },
  {
    id: "RPT-002",
    title: "Threat Report — Emotet Resurgence",
    type: "threat",
    severity: "high",
    created: "2024-12-10T11:00:00Z",
    analyst: "SOC Team",
    summary:
      "Emotet malware detected on 5 endpoints via spearphishing attachments in a targeted campaign against the Finance department.",
    sections: {
      executive_summary:
        "Emotet banking trojan, a modular malware known for loading secondary payloads, was identified on 5 endpoints within the Finance department on December 10, 2024.",
      timeline:
        "Phishing emails received at 10:15 UTC. First execution at 10:47 UTC. Sandbox detonation confirmed 11:12 UTC. Containment at 11:44 UTC.",
      iocs: "10.0.0.22, doc_invoice.xlsm (SHA256: b71c3a...), hxxp://185.x.x.x/update.exe",
      mitre_techniques:
        "T1566.001 (Spearphishing Attachment), T1204.002 (User Execution), T1059.005 (Visual Basic)",
      remediation:
        "1. Isolate and reimage affected endpoints. 2. Block identified C2 infrastructure. 3. Conduct awareness training for Finance team.",
    },
  },
  {
    id: "RPT-003",
    title: "Daily SOC Summary — Dec 10",
    type: "summary",
    severity: "medium",
    created: "2024-12-10T23:59:00Z",
    analyst: "Automated",
    summary:
      "142 events processed. 23 alerts generated. 2 critical incidents opened. 58 events resolved. Overall threat posture: HIGH.",
    sections: {
      executive_summary:
        "December 10, 2024 was a high-activity day for the SOC. Two critical incidents were opened related to an APT campaign and malware outbreak. The team responded effectively, achieving containment within expected SLA windows.",
      timeline:
        "High-traffic window: 06:00–12:00 UTC. Peak alert volume at 09:00 UTC with 47 events/hour.",
      iocs: "See individual incident reports for specific IOC details.",
      mitre_techniques:
        "Most common: T1110 (Brute Force), T1566 (Phishing), T1059 (Command & Scripting Interpreter)",
      remediation:
        "No immediate remediation required. Follow up on open incidents INC-2024-001 and INC-2024-002.",
    },
  },
];

const MOCK_REPLIES = {
  default: [
    "Based on the current threat landscape, I recommend investigating the lateral movement patterns across your internal network. The MITRE ATT&CK technique T1021 (Remote Services) appears most relevant here.",
    "The indicators of compromise suggest a staged attack. I've cross-referenced the source IPs against our threat intelligence feeds — 185.220.101.47 is a known TOR exit node associated with APT campaigns.",
    "Analyzing the timeline of events, the initial access vector appears to be a spearphishing attachment (T1566.001), followed by credential harvesting using T1003.001. I recommend immediate password resets for affected accounts.",
    "This pattern is consistent with Emotet malware behavior. The beaconing interval (~45s) and encoded payload structure match TTPs in our threat database. I'd recommend isolating affected hosts immediately.",
    "I've reviewed the DNS query patterns. High-volume TXT record lookups to a newly registered domain strongly suggest DNS tunneling (T1071.004) for C2 communication. Blocking the domain at the resolver level should disrupt the channel.",
  ],
};

function getMockReply(msg) {
  const m = msg.toLowerCase();
  if (m.includes("mitre") || m.includes("ttp"))
    return "The MITRE ATT&CK framework maps these behaviors: T1110 (Brute Force), T1059.001 (PowerShell), T1003.001 (LSASS Dumping), T1048 (Exfiltration Over Alternative Protocol). I recommend prioritizing containment of the credential dumping activity as it indicates post-exploitation activity.";
  if (m.includes("ip") || m.includes("indicator"))
    return "Current active IOCs: 185.220.101.47 (TOR exit, brute force source), 203.0.113.89 (C2 server), 45.33.32.156 (scanner). All three IPs have been submitted to threat intel platforms. Recommend adding to firewall blocklist immediately.";
  if (m.includes("report") || m.includes("pdf"))
    return "I can generate an Incident Report, Threat Intelligence Brief, or Daily SOC Summary. Navigate to the Reports page to access the report builder and PDF viewer.";
  if (m.includes("remediat") || m.includes("fix") || m.includes("respond"))
    return "Recommended remediation steps: 1) Isolate affected endpoints immediately. 2) Reset all privileged credentials. 3) Patch CVE-2024-21887 on VPN appliances. 4) Block identified C2 infrastructure at perimeter. 5) Enable enhanced logging on AD domain controllers.";
  const replies = MOCK_REPLIES.default;
  return replies[Math.floor(Math.random() * replies.length)];
}
