import React, { useState, useEffect, useCallback, useRef, useMemo } from "react";
import {
  LayoutDashboard, UploadCloud, ListChecks, History as HistoryIcon, Sun, Moon,
  Settings2, Wifi, WifiOff, ScanLine, Building2, ClipboardCheck, Copy, ScrollText,
  ShieldAlert, Sparkles, FileText, ChevronRight, RefreshCw, Loader2, ArrowRight,
  X, Check, Ban, Hash, CalendarDays, Coins, Cpu, Timer, Gauge, FileWarning,
  Search, SlidersHorizontal, ArrowUpRight, CircleAlert, CircleCheck, Info,
  FilePlus2, FileImage, FileType2, Trash2, PlugZap, ChevronDown, Zap, Landmark,
  BadgeCheck, TrendingUp, Database, ExternalLink, PlayCircle,
  Bot, Send, Menu, User, Trash, WandSparkles, AlertTriangle,
} from "lucide-react";

/* ============================================================================
   INVOICEPILOT AI — Agentic invoice-processing console
   Design language: "circuit ledger" — a dark operations console where the
   nine-skill agent pipeline is the signature element: a literal circuit
   board trace that lights up node by node as the backend executes. Every
   screen keeps that same trace motif in miniature so the product always
   reads as "an agent is doing legible work," not just a generic dashboard.
   ============================================================================ */

/* ---------------------------------- Design tokens (CSS) ------------------- */

const STYLE = `
@import url('https://fonts.googleapis.com/css2?family=Space+Grotesk:wght@500;600;700&family=Inter:wght@400;500;600;700&family=JetBrains+Mono:wght@400;500;600&display=swap');

.ip-root {
  --bg:            #111214;
  --bg-elev-1:     #191a1d;
  --bg-elev-2:     #212226;
  --bg-elev-3:     #2a2b30;
  --line:          #34363b;
  --line-soft:     #222327;
  --text:          #eef0f2;
  --text-dim:      #9a9ca4;
  --text-faint:    #6b6d76;
  --violet:        #5b6ee8;
  --violet-dim:    #4a56c4;
  --blue:          #20c2ae;
  --cyan:          #3fd6d0;
  --amber:         #f5b942;
  --orange:        #f4874b;
  --rose:          #f0526e;
  --green:         #35d08f;
  --grad-brand:    linear-gradient(120deg,#5b6ee8 0%,#20c2ae 100%);
  --grad-brand-soft: linear-gradient(120deg,rgba(91,110,232,.16),rgba(32,194,174,.10));
  --shadow-card: 0 1px 0 rgba(255,255,255,.02) inset, 0 12px 32px -18px rgba(0,0,0,.7);
  --radius: 16px;
  font-family: 'Inter', system-ui, sans-serif;
  background: var(--bg);
  color: var(--text);
  min-height: 100%;
  position: relative;
}
.ip-root[data-theme="light"] {
  --bg:            #f3f4fb;
  --bg-elev-1:     #ffffff;
  --bg-elev-2:     #ffffff;
  --bg-elev-3:     #eef0fa;
  --line:          #e3e5f2;
  --line-soft:     #ebedf7;
  --text:          #14162b;
  --text-dim:      #5c6086;
  --text-faint:    #9296b8;
  --shadow-card: 0 1px 0 rgba(255,255,255,.6) inset, 0 12px 28px -20px rgba(30,32,70,.22);
}
.ip-root * { box-sizing: border-box; }
.ip-mono { font-family: 'JetBrains Mono', monospace; }
.ip-display { font-family: 'Space Grotesk', sans-serif; letter-spacing: -0.01em; }

.ip-scrollbar::-webkit-scrollbar { width: 8px; height: 8px; }
.ip-scrollbar::-webkit-scrollbar-thumb { background: var(--line); border-radius: 8px; }
.ip-scrollbar::-webkit-scrollbar-track { background: transparent; }

.ip-bg-grid {
  position: absolute; inset: 0; pointer-events: none; opacity: .5;
  background-image:
    linear-gradient(var(--line-soft) 1px, transparent 1px),
    linear-gradient(90deg, var(--line-soft) 1px, transparent 1px);
  background-size: 42px 42px;
  mask-image: radial-gradient(ellipse 70% 55% at 20% 0%, black 10%, transparent 75%);
}

.ip-card {
  background: var(--bg-elev-1);
  border: 1px solid var(--line);
  border-radius: var(--radius);
  box-shadow: var(--shadow-card);
}
.ip-card-2 { background: var(--bg-elev-2); border: 1px solid var(--line); border-radius: var(--radius); }

.ip-btn {
  display: inline-flex; align-items: center; justify-content: center; gap: 8px;
  font-weight: 600; font-size: 13.5px; border-radius: 11px; padding: 10px 16px;
  cursor: pointer; border: 1px solid transparent; transition: all .15s ease; white-space: nowrap;
}
.ip-btn:active { transform: translateY(1px); }
.ip-btn:disabled { opacity: .5; cursor: not-allowed; }
.ip-btn-primary { background: var(--grad-brand); color: #fff; box-shadow: 0 8px 20px -8px rgba(91,110,232,.55); }
.ip-btn-primary:hover:not(:disabled) { filter: brightness(1.08); }
.ip-btn-ghost { background: var(--bg-elev-2); color: var(--text); border-color: var(--line); }
.ip-btn-ghost:hover:not(:disabled) { background: var(--bg-elev-3); }
.ip-btn-outline { background: transparent; color: var(--text-dim); border-color: var(--line); }
.ip-btn-outline:hover:not(:disabled) { color: var(--text); border-color: var(--text-faint); }
.ip-btn-danger { background: rgba(240,82,110,.12); color: #f0526e; border-color: rgba(240,82,110,.35); }
.ip-btn-danger:hover:not(:disabled) { background: rgba(240,82,110,.2); }
.ip-btn-sm { padding: 7px 12px; font-size: 12.5px; border-radius: 9px; }

.ip-input {
  background: var(--bg-elev-2); border: 1px solid var(--line); color: var(--text);
  border-radius: 10px; padding: 9px 12px; font-size: 13.5px; width: 100%; outline: none;
  transition: border-color .15s ease;
}
.ip-input:focus { border-color: var(--violet); }
.ip-input::placeholder { color: var(--text-faint); }

.ip-badge {
  display: inline-flex; align-items: center; gap: 6px; font-size: 11.5px; font-weight: 700;
  padding: 4px 9px; border-radius: 999px; letter-spacing: .02em; text-transform: uppercase;
  border: 1px solid transparent; white-space: nowrap;
}
.ip-dot { width: 6px; height: 6px; border-radius: 999px; flex: none; }

.ip-nav-item {
  display: flex; align-items: center; gap: 11px; padding: 10px 12px; border-radius: 11px;
  color: var(--text-dim); font-size: 13.5px; font-weight: 600; cursor: pointer;
  transition: all .15s ease; border: 1px solid transparent; position: relative;
}
.ip-nav-item:hover { background: var(--bg-elev-2); color: var(--text); }
.ip-nav-item.active { background: var(--grad-brand-soft); color: var(--text); border-color: rgba(91,110,232,.35); }
.ip-nav-item.active svg { color: var(--violet); }

.ip-fade-in { animation: ipFadeIn .38s cubic-bezier(.2,.8,.2,1) both; }
@keyframes ipFadeIn { from { opacity:0; transform: translateY(6px);} to {opacity:1; transform:none;} }
.ip-pop { animation: ipPop .3s cubic-bezier(.34,1.4,.64,1) both; }
@keyframes ipPop { from { opacity:0; transform: scale(.92);} to {opacity:1; transform:scale(1);} }

@keyframes ipPulse { 0%,100% { opacity:1; } 50% { opacity:.45; } }
.ip-pulse { animation: ipPulse 1.4s ease-in-out infinite; }

@keyframes ipSpin { to { transform: rotate(360deg); } }
.ip-spin { animation: ipSpin 1s linear infinite; }

@keyframes ipDash { to { stroke-dashoffset: 0; } }
.ip-trace-line { stroke-dasharray: 6 6; stroke-dashoffset: 240; animation: ipDash 1.6s linear infinite; }

@keyframes ipGlow { 0%,100% { box-shadow: 0 0 0 0 rgba(91,110,232,.5);} 50% { box-shadow: 0 0 0 8px rgba(91,110,232,0);} }
.ip-glow-ring { animation: ipGlow 1.6s ease-out infinite; }

.ip-node-line { stroke: var(--line); stroke-width: 2; transition: stroke .5s ease; }
.ip-node-line.done { stroke: url(#ipGradLine); }

.ip-scan {
  position: relative; overflow: hidden;
}
.ip-scan::after {
  content: ""; position: absolute; left: 0; top: -40%; width: 100%; height: 40%;
  background: linear-gradient(180deg, transparent, rgba(91,110,232,.14), transparent);
  animation: ipScan 2.2s ease-in-out infinite;
}
@keyframes ipScan { 0% { top: -40%; } 100% { top: 100%; } }

.ip-drop {
  border: 1.5px dashed var(--line); border-radius: 18px; transition: all .18s ease;
}
.ip-drop.active { border-color: var(--violet); background: var(--grad-brand-soft); }

.ip-table-row { transition: background .15s ease; }
.ip-table-row:hover { background: var(--bg-elev-2); }

.ip-tooltip-wrap { position: relative; }
.ip-progress-track { background: var(--bg-elev-3); border-radius: 999px; overflow: hidden; }
.ip-progress-fill { background: var(--grad-brand); border-radius: 999px; transition: width .4s ease; }

.ip-kbd {
  font-family: 'JetBrains Mono', monospace; font-size: 10.5px; padding: 2px 6px;
  border-radius: 5px; background: var(--bg-elev-3); border: 1px solid var(--line); color: var(--text-faint);
}

::selection { background: rgba(91,110,232,.35); }
`;

/* ---------------------------------- Constants matching backend ------------ */

const PIPELINE = [
  { skill: "extract_invoice", label: "Extract Invoice", desc: "Parses raw document into structured fields", Icon: ScanLine },
  { skill: "vendor_lookup", label: "Vendor Lookup", desc: "Matches vendor against the vendor ledger", Icon: Building2 },
  { skill: "validate_invoice", label: "Validation", desc: "Checks required fields and formatting", Icon: ClipboardCheck },
  { skill: "duplicate_detection", label: "Duplicate Detection", desc: "Scans prior executions for repeats", Icon: Copy },
  { skill: "policy_engine", label: "Policy Engine", desc: "Applies spend and approval policy rules", Icon: ScrollText },
  { skill: "risk_assessment", label: "Risk Assessment", desc: "Scores composite risk across signals", Icon: ShieldAlert },
  { skill: "recommendation", label: "Recommendation", desc: "Decides the routing outcome", Icon: Sparkles },
  { skill: "approval_queue", label: "Approval Queue", desc: "Queues for human sign-off if required", Icon: ListChecks },
  { skill: "audit_logger", label: "Audit Logger", desc: "Writes an immutable audit record", Icon: FileText },
];

const SUPPORTED_TYPES = [".pdf", ".png", ".jpg", ".jpeg", ".txt"];
const MAX_UPLOAD_MB = 25;

// localStorage keys — keeps processed invoices and copilot threads
// available across page reloads, since they'd otherwise vanish the
// moment this component remounts.
const HISTORY_STORAGE_KEY = "invoicepilot.history.v1";
const CHAT_THREADS_STORAGE_KEY = "invoicepilot.chatThreads.v1";

const SUGGESTED_QUESTIONS = [
  "Summarize this invoice",
  "Why wasn't this invoice approved?",
  "Explain the risk score",
  "Explain the policy decision",
  "What warnings were found?",
  "Tell me about this vendor",
  "Generate an approval summary",
];

const RISK_STYLE = {
  LOW:      { color: "#35d08f", bg: "rgba(53,208,143,.12)",  border: "rgba(53,208,143,.35)" },
  MEDIUM:   { color: "#f5b942", bg: "rgba(245,185,66,.12)",  border: "rgba(245,185,66,.35)" },
  HIGH:     { color: "#f4874b", bg: "rgba(244,135,75,.12)",  border: "rgba(244,135,75,.35)" },
  CRITICAL: { color: "#f0526e", bg: "rgba(240,82,110,.12)",  border: "rgba(240,82,110,.35)" },
};

const REC_STYLE = {
  AUTO_APPROVE:   { color: "#35d08f", bg: "rgba(53,208,143,.12)", border: "rgba(53,208,143,.35)", label: "Auto-approve" },
  FINANCE_REVIEW: { color: "#3b82f6", bg: "rgba(59,130,246,.12)", border: "rgba(59,130,246,.35)", label: "Finance review" },
  MANAGER_REVIEW: { color: "#f5b942", bg: "rgba(245,185,66,.12)", border: "rgba(245,185,66,.35)", label: "Manager review" },
  REJECT:         { color: "#f0526e", bg: "rgba(240,82,110,.12)", border: "rgba(240,82,110,.35)", label: "Reject" },
};

const APPROVAL_STYLE = {
  PENDING:  { color: "#f5b942", bg: "rgba(245,185,66,.12)", border: "rgba(245,185,66,.35)" },
  APPROVED: { color: "#35d08f", bg: "rgba(53,208,143,.12)", border: "rgba(53,208,143,.35)" },
  REJECTED: { color: "#f0526e", bg: "rgba(240,82,110,.12)", border: "rgba(240,82,110,.35)" },
};

/* ---------------------------------- Small helpers -------------------------- */

function cls(...xs) { return xs.filter(Boolean).join(" "); }

function fmtMoney(amount, currency) {
  if (amount === null || amount === undefined) return "—";
  try {
    return new Intl.NumberFormat(undefined, { style: "currency", currency: currency || "USD", maximumFractionDigits: 2 }).format(amount);
  } catch {
    return `${currency || ""} ${Number(amount).toLocaleString()}`.trim();
  }
}
/* ---------------------------------- Currency conversion (→ INR) ------------ */
/* Fallback rates used instantly (and whenever a live lookup fails or hasn't  */
/* resolved yet) so the UI never blocks on network. If a live rate loads,     */
/* it quietly takes over — the original international amount is always kept  */
/* front and center, this is purely an added "≈ ₹" reference figure.         */

const FX_FALLBACK_TO_INR = {
  USD: 87.5, EUR: 94.8, GBP: 110.4, AED: 23.8, SGD: 64.7, AUD: 56.9,
  CAD: 62.3, JPY: 0.58, CNY: 12.05, CHF: 98.6, HKD: 11.2, NZD: 51.6,
  SAR: 23.3, ZAR: 4.7, INR: 1,
};

let _fxRatesCache = null;
let _fxRatesPromise = null;

function getFxRatesToINR() {
  if (_fxRatesCache) return Promise.resolve(_fxRatesCache);
  if (_fxRatesPromise) return _fxRatesPromise;
  _fxRatesPromise = fetch("https://api.exchangerate-api.com/v4/latest/INR")
    .then(r => (r.ok ? r.json() : Promise.reject(new Error("fx fetch failed"))))
    .then(data => {
      const rates = data?.rates;
      if (!rates || !rates.USD) throw new Error("bad fx payload");
      // API gives INR -> X, invert to get X -> INR.
      const toInr = {};
      Object.entries(rates).forEach(([code, rateFromInr]) => {
        if (rateFromInr) toInr[code] = 1 / rateFromInr;
      });
      toInr.INR = 1;
      _fxRatesCache = toInr;
      return toInr;
    })
    .catch(() => {
      _fxRatesCache = FX_FALLBACK_TO_INR;
      return FX_FALLBACK_TO_INR;
    });
  return _fxRatesPromise;
}

function useFxRates() {
  const [rates, setRates] = useState(_fxRatesCache || FX_FALLBACK_TO_INR);
  useEffect(() => {
    let alive = true;
    getFxRatesToINR().then(r => { if (alive) setRates(r); });
    return () => { alive = false; };
  }, []);
  return rates;
}

function convertToINR(amount, currency, rates) {
  if (amount === null || amount === undefined || !currency) return null;
  const code = String(currency).toUpperCase();
  if (code === "INR") return null;
  const rate = (rates || FX_FALLBACK_TO_INR)[code];
  if (!rate) return null;
  return Math.round(amount * rate * 100) / 100;
}

function fmtINR(amount) {
  if (amount === null || amount === undefined) return "—";
  try {
    return new Intl.NumberFormat("en-IN", { style: "currency", currency: "INR", maximumFractionDigits: 0 }).format(amount);
  } catch {
    return `₹${Number(amount).toLocaleString("en-IN")}`;
  }
}

/** Shows the original (international) amount unchanged, plus a small
 *  "≈ ₹..." INR reference line/inline when the currency isn't already INR.
 *  The original currency figure is never removed or replaced. */
function MoneyWithINR({ amount, currency, size = 13, inline = false }) {
  const rates = useFxRates();
  const original = fmtMoney(amount, currency);
  const inr = convertToINR(amount, currency, rates);
  if (inr === null) return <span style={{ fontSize: size }}>{original}</span>;
  return inline ? (
    <span style={{ fontSize: size }}>
      {original} <span className="ip-mono" style={{ color: "var(--text-faint)", fontSize: size - 1.5 }}>(≈ {fmtINR(inr)})</span>
    </span>
  ) : (
    <span style={{ display: "inline-flex", flexDirection: "column", alignItems: "flex-end", lineHeight: 1.35 }}>
      <span style={{ fontSize: size }}>{original}</span>
      <span className="ip-mono" style={{ color: "var(--text-faint)", fontSize: size - 2 }}>≈ {fmtINR(inr)}</span>
    </span>
  );
}

function fmtDate(d) {
  if (!d) return "—";
  try {
    const dt = new Date(d);
    if (isNaN(dt.getTime())) return String(d);
    return dt.toLocaleString(undefined, { year: "numeric", month: "short", day: "numeric", hour: "2-digit", minute: "2-digit" });
  } catch { return String(d); }
}
function fmtDateOnly(d) {
  if (!d) return "—";
  try {
    const dt = new Date(d);
    if (isNaN(dt.getTime())) return String(d);
    return dt.toLocaleDateString(undefined, { year: "numeric", month: "short", day: "numeric" });
  } catch { return String(d); }
}
function fmtBytes(n) {
  if (n < 1024) return `${n} B`;
  if (n < 1024 * 1024) return `${(n / 1024).toFixed(1)} KB`;
  return `${(n / (1024 * 1024)).toFixed(2)} MB`;
}
function timeAgo(d) {
  const diff = (Date.now() - new Date(d).getTime()) / 1000;
  if (diff < 60) return "just now";
  if (diff < 3600) return `${Math.floor(diff / 60)}m ago`;
  if (diff < 86400) return `${Math.floor(diff / 3600)}h ago`;
  return `${Math.floor(diff / 86400)}d ago`;
}
function uid() { return Math.random().toString(36).slice(2, 10); }

/* ---------------------------------- Tiny markdown renderer ---------------- */
/* Supports **bold**, *italic*, `code`, and "- " bullet lists — enough for   */
/* the copilot's chat answers, with no HTML injection risk.                 */

function renderInline(text, keyBase) {
  const parts = String(text).split(/(\*\*[^*]+\*\*|`[^`]+`|\*[^*]+\*)/g);
  return parts.filter(Boolean).map((chunk, i) => {
    const key = `${keyBase}-${i}`;
    if (chunk.startsWith("**") && chunk.endsWith("**")) return <strong key={key}>{chunk.slice(2, -2)}</strong>;
    if (chunk.startsWith("`") && chunk.endsWith("`")) return <code key={key} className="ip-mono" style={{ background: "var(--bg-elev-3)", padding: "1px 5px", borderRadius: 5, fontSize: "0.92em" }}>{chunk.slice(1, -1)}</code>;
    if (chunk.startsWith("*") && chunk.endsWith("*") && chunk.length > 2) return <em key={key}>{chunk.slice(1, -1)}</em>;
    return chunk;
  });
}

function Markdown({ text }) {
  const lines = String(text || "").split("\n");
  const blocks = [];
  let list = [];
  const flushList = (key) => {
    if (list.length) { blocks.push(<ul key={`ul-${key}`} style={{ margin: "4px 0 8px", paddingLeft: 18 }}>{list}</ul>); list = []; }
  };
  lines.forEach((line, i) => {
    const trimmed = line.trim();
    if (/^[-*]\s+/.test(trimmed)) {
      list.push(<li key={`li-${i}`} style={{ fontSize: "inherit", lineHeight: 1.6 }}>{renderInline(trimmed.replace(/^[-*]\s+/, ""), i)}</li>);
    } else {
      flushList(i);
      if (trimmed === "") { blocks.push(<div key={`sp-${i}`} style={{ height: 6 }} />); }
      else blocks.push(<p key={`p-${i}`} style={{ margin: "0 0 6px", lineHeight: 1.6 }}>{renderInline(line, i)}</p>);
    }
  });
  flushList("end");
  return <div>{blocks}</div>;
}

/* ---------------------------------- Mock data (offline demo mode) --------- */

function buildMockEvents() {
  const now = Date.now();
  const msgs = {
    extract_invoice: "Extracted 11 fields with high model confidence",
    vendor_lookup: "Matched existing vendor in ledger",
    validate_invoice: "All required fields present and well-formed",
    duplicate_detection: "No matching prior execution found",
    policy_engine: "Within standard spend policy thresholds",
    risk_assessment: "Composite risk score computed from 5 signals",
    recommendation: "Routed for finance review — amount above auto-approve limit",
    approval_queue: "Queued for human sign-off",
    audit_logger: "Immutable audit record written",
  };
  return PIPELINE.map((p, i) => ({
    skill: p.skill, state: p.label.toUpperCase(), status: "SUCCESS",
    message: msgs[p.skill], timestamp: new Date(now + i * 240).toISOString(),
  }));
}

function buildMockSkillTimings() {
  // Rough, plausible per-stage split of total processing time for demo mode
  // (the real backend reports these from actual wall-clock measurements).
  const t = {};
  PIPELINE.forEach(p => {
    t[p.skill] = p.skill === "extract_invoice"
      ? Math.round((Math.random() * 0.5 + 0.35) * 100) / 100 // LLM call dominates
      : Math.round((Math.random() * 0.08 + 0.01) * 100) / 100;
  });
  return t;
}

function buildMockResult(file) {
  const amount = Math.round((Math.random() * 180000 + 900) * 100) / 100;
  const isHigh = amount > 100000;
  const risk = isHigh ? "HIGH" : amount > 40000 ? "MEDIUM" : "LOW";
  // Demo mode mirrors the real backend policy: automation only
  // flags risk, it never gives the final sign-off — every invoice,
  // however low-risk, still lands in front of a human.
  const rec = isHigh ? "MANAGER_REVIEW" : "FINANCE_REVIEW";
  const vendors = ["Meridian Office Supplies", "Northwind Logistics", "Vertex Cloud Services", "Halcyon Facilities Group"];
  const vendor = vendors[Math.floor(Math.random() * vendors.length)];
  return {
    success: true, status: "COMPLETED",
    invoice: {
      vendor_name: vendor, invoice_number: `INV-${Math.floor(Math.random() * 90000 + 10000)}`,
      invoice_date: new Date(Date.now() - Math.random() * 30 * 86400000).toISOString().slice(0, 10),
      total_amount: amount, currency: "USD",
    },
    vendor: {
      name: vendor, gst_number: "29AAFCM1234K1ZP", status: "ACTIVE", total_invoices: Math.floor(Math.random() * 40) + 1,
      total_spend: Math.round(amount * (Math.random() * 6 + 2)), currencies: ["USD"], is_new_vendor: Math.random() < 0.2,
      first_seen: new Date(Date.now() - 200 * 86400000).toISOString(), last_seen: new Date().toISOString(),
    },
    duplicate: { is_duplicate: false, match_type: "NONE", matched_execution_ids: [], reason: "No overlapping vendor/amount/date signature found." },
    recommendation: rec, risk_level: risk, risk_score: isHigh ? 68 : amount > 40000 ? 38 : 14,
    requires_human_review: rec !== "AUTO_APPROVE", queued_for_approval: rec !== "AUTO_APPROVE",
    errors: [], warnings: amount > 40000 ? ["Amount exceeds standard auto-approve threshold."] : [],
    events: buildMockEvents(),
    metadata: (() => {
      const skill_timings = buildMockSkillTimings();
      const processing_time = Math.round(Object.values(skill_timings).reduce((a, b) => a + b, 0) * 100) / 100;
      return { execution_id: `exec_${uid()}`, provider_used: "groq", processing_time, retry_count: 0, skill_timings };
    })(),
    _filename: file?.name || "sample-invoice.pdf",
  };
}

function buildMockApprovals(n = 4) {
  const vendors = ["Meridian Office Supplies", "Northwind Logistics", "Vertex Cloud Services", "Halcyon Facilities Group", "Solace Print Co."];
  return Array.from({ length: n }).map((_, i) => {
    const amount = Math.round((Math.random() * 160000 + 20000) * 100) / 100;
    const risk = amount > 100000 ? "HIGH" : "MEDIUM";
    return {
      execution_id: `exec_${uid()}`, invoice_number: `INV-${Math.floor(Math.random() * 90000 + 10000)}`,
      vendor_name: vendors[i % vendors.length], total_amount: amount, currency: "USD",
      recommendation: amount > 100000 ? "MANAGER_REVIEW" : "FINANCE_REVIEW", risk_level: risk,
      risk_score: risk === "HIGH" ? 66 : 36, reason: "Amount exceeds standard auto-approve threshold.",
      status: "PENDING", created_at: new Date(Date.now() - i * 3600000).toISOString(),
      decided_at: null, decided_by: null, decision_notes: null,
    };
  });
}

function buildMockChatAnswer(question, result) {
  const inv = result?.invoice || {};
  const q = (question || "").toLowerCase();
  const vendor = inv.vendor_name || "this vendor";
  const amount = fmtMoney(inv.total_amount, inv.currency);
  if (q.includes("summar")) {
    return `**${vendor}** billed **${amount}** on invoice \`${inv.invoice_number || "—"}\`. The agent scored it **${result?.risk_level || "LOW"}** risk (${result?.risk_score ?? 0}/100) and routed it to **${(result?.recommendation || "AUTO_APPROVE").replace(/_/g, " ").toLowerCase()}**.\n\nKey points:\n- Duplicate check: ${result?.duplicate?.is_duplicate ? "possible match found" : "no matching prior invoice"}\n- Warnings: ${result?.warnings?.length ? result.warnings.length : "none"}`;
  }
  if (q.includes("risk")) {
    return `The risk score of **${result?.risk_score ?? 0}/100** blends signals like invoice amount vs. policy thresholds, vendor history, and duplicate/validation flags. A score in the **${result?.risk_level || "LOW"}** band typically reflects ${result?.risk_level === "LOW" ? "routine spend with a well-known vendor" : "amount or vendor signals worth a second look"}.`;
  }
  if (q.includes("polic")) {
    return `Policy engine outcome: **${(result?.recommendation || "AUTO_APPROVE").replace(/_/g, " ")}**.\n\nThis is decided by comparing the invoice total (**${amount}**) against configured auto-approve and review thresholds, alongside vendor status and any warnings raised earlier in the pipeline.`;
  }
  if (q.includes("warn")) {
    return result?.warnings?.length ? `The pipeline raised **${result.warnings.length}** warning(s):\n${result.warnings.map(w => `- ${w}`).join("\n")}` : "No warnings were raised for this invoice — every check passed cleanly.";
  }
  if (q.includes("vendor")) {
    const v = result?.vendor || {};
    return `**${v.name || vendor}** is ${v.is_new_vendor ? "a **new** vendor in the ledger" : "an existing, known vendor"} with status **${v.status || "ACTIVE"}**.\n- Total invoices on file: ${v.total_invoices ?? "—"}\n- Total spend: ${fmtMoney(v.total_spend, inv.currency)}`;
  }
  if (q.includes("approv")) {
    return `Approval summary for \`${inv.invoice_number || "—"}\`: **${vendor}**, **${amount}**, risk **${result?.risk_level || "LOW"}**, recommendation **${(result?.recommendation || "AUTO_APPROVE").replace(/_/g, " ")}**. ${result?.requires_human_review ? "This invoice is queued for human sign-off." : "This invoice was auto-approved and needs no further action."}`;
  }
  return `Based on this execution, **${vendor}**'s invoice for **${amount}** was routed as **${(result?.recommendation || "AUTO_APPROVE").replace(/_/g, " ").toLowerCase()}** with **${result?.risk_level || "LOW"}** risk. Ask me about the risk score, policy decision, vendor, or warnings for more detail.`;
}

/* ---------------------------------- API client ------------------------------ */

function useApi(apiBase) {
  const call = useCallback(async (path, options = {}) => {
    const res = await fetch(`${apiBase.replace(/\/$/, "")}${path}`, options);
    let body = null;
    const text = await res.text();
    try { body = text ? JSON.parse(text) : null; } catch { body = text; }
    if (!res.ok) {
      const detail = body && typeof body === "object" && body.detail ? body.detail : `Request failed (${res.status})`;
      const err = new Error(detail);
      err.status = res.status;
      throw err;
    }
    return body;
  }, [apiBase]);
  return call;
}

/* ---------------------------------- Atoms ----------------------------------- */

function Badge({ color, bg, border, children, icon: Icon }) {
  return (
    <span className="ip-badge" style={{ color, background: bg, borderColor: border }}>
      {Icon ? <Icon size={11.5} strokeWidth={2.75} /> : <span className="ip-dot" style={{ background: color }} />}
      {children}
    </span>
  );
}

function RiskBadge({ level }) {
  const s = RISK_STYLE[level] || RISK_STYLE.LOW;
  return <Badge color={s.color} bg={s.bg} border={s.border}>{level || "—"}</Badge>;
}
function RecBadge({ rec }) {
  const s = REC_STYLE[rec] || { color: "#9498b8", bg: "rgba(148,152,184,.12)", border: "rgba(148,152,184,.3)", label: rec || "—" };
  return <Badge color={s.color} bg={s.bg} border={s.border}>{s.label}</Badge>;
}
function ApprovalStatusBadge({ status }) {
  const s = APPROVAL_STYLE[status] || APPROVAL_STYLE.PENDING;
  return <Badge color={s.color} bg={s.bg} border={s.border}>{status}</Badge>;
}

function IconTile({ Icon, tone = "violet", size = 18 }) {
  const tones = {
    violet: { bg: "rgba(91,110,232,.14)", color: "#5b6ee8" },
    blue: { bg: "rgba(32,194,174,.14)", color: "#20c2ae" },
    green: { bg: "rgba(53,208,143,.14)", color: "#35d08f" },
    amber: { bg: "rgba(245,185,66,.14)", color: "#f5b942" },
    rose: { bg: "rgba(240,82,110,.14)", color: "#f0526e" },
  };
  const t = tones[tone] || tones.violet;
  return (
    <div style={{ background: t.bg, color: t.color, width: 38, height: 38, borderRadius: 11, display: "flex", alignItems: "center", justifyContent: "center", flex: "none" }}>
      <Icon size={size} strokeWidth={2.2} />
    </div>
  );
}

function StatCard({ label, value, sub, tone, Icon, trend }) {
  return (
    <div className="ip-card ip-fade-in" style={{ padding: "18px 20px" }}>
      <div style={{ display: "flex", alignItems: "flex-start", justifyContent: "space-between" }}>
        <div style={{ fontSize: 12.5, color: "var(--text-dim)", fontWeight: 600 }}>{label}</div>
        <IconTile Icon={Icon} tone={tone} size={16} />
      </div>
      <div className="ip-display" style={{ fontSize: 28, fontWeight: 700, marginTop: 14, lineHeight: 1 }}>{value}</div>
      {sub && (
        <div style={{ fontSize: 12, color: trend === "up" ? "#35d08f" : trend === "down" ? "#f0526e" : "var(--text-faint)", marginTop: 8, display: "flex", alignItems: "center", gap: 4, fontWeight: 600 }}>
          {trend === "up" && <TrendingUp size={12} />}
          {sub}
        </div>
      )}
    </div>
  );
}

function EmptyState({ Icon, title, body, action }) {
  return (
    <div className="ip-card ip-fade-in" style={{ padding: "56px 24px", textAlign: "center" }}>
      <div style={{ width: 52, height: 52, borderRadius: 14, background: "var(--grad-brand-soft)", display: "flex", alignItems: "center", justifyContent: "center", margin: "0 auto 16px" }}>
        <Icon size={24} color="#5b6ee8" strokeWidth={1.8} />
      </div>
      <div className="ip-display" style={{ fontSize: 16, fontWeight: 700 }}>{title}</div>
      <div style={{ fontSize: 13, color: "var(--text-dim)", marginTop: 6, maxWidth: 380, margin: "6px auto 0" }}>{body}</div>
      {action && <div style={{ marginTop: 18 }}>{action}</div>}
    </div>
  );
}

function Toast({ toasts, onDismiss }) {
  return (
    <div style={{ position: "fixed", top: 18, right: 18, zIndex: 200, display: "flex", flexDirection: "column", gap: 10, width: 340, maxWidth: "calc(100vw - 36px)" }}>
      {toasts.map(t => (
        <div key={t.id} className="ip-card ip-pop" style={{ padding: "13px 14px", display: "flex", gap: 10, alignItems: "flex-start" }}>
          <div style={{ marginTop: 1, flex: "none" }}>
            {t.type === "error" ? <CircleAlert size={17} color="#f0526e" /> : t.type === "success" ? <CircleCheck size={17} color="#35d08f" /> : <Info size={17} color="#20c2ae" />}
          </div>
          <div style={{ fontSize: 13, lineHeight: 1.4, flex: 1 }}>{t.message}</div>
          <button onClick={() => onDismiss(t.id)} className="ip-btn ip-btn-ghost ip-btn-sm" style={{ padding: 4 }}><X size={13} /></button>
        </div>
      ))}
    </div>
  );
}

/* ---------------------------------- Pipeline trace (signature element) ---- */

function PipelineTrace({ events, running, compact }) {
  const doneSkills = new Set((events || []).map(e => e.skill));
  const activeIndex = running ? Math.min(events?.length || 0, PIPELINE.length - 1) : -1;

  if (compact) {
    return (
      <div style={{ display: "flex", alignItems: "center", gap: 0, overflowX: "auto" }} className="ip-scrollbar">
        {PIPELINE.map((p, i) => {
          const done = doneSkills.has(p.skill);
          return (
            <React.Fragment key={p.skill}>
              <div title={p.label} style={{
                width: 26, height: 26, borderRadius: 8, flex: "none", display: "flex", alignItems: "center", justifyContent: "center",
                background: done ? "var(--grad-brand)" : "var(--bg-elev-3)", color: done ? "#fff" : "var(--text-faint)",
              }}>
                <p.Icon size={13} strokeWidth={2.4} />
              </div>
              {i < PIPELINE.length - 1 && <div style={{ width: 16, height: 2, background: done && doneSkills.has(PIPELINE[i + 1]?.skill) ? "var(--violet)" : "var(--line)", flex: "none" }} />}
            </React.Fragment>
          );
        })}
      </div>
    );
  }

  return (
    <div style={{ position: "relative" }}>
      <div style={{ display: "flex", flexDirection: "column" }}>
        {PIPELINE.map((p, i) => {
          const evt = (events || []).find(e => e.skill === p.skill);
          const done = !!evt;
          // Three distinct outcomes, not two: a WARNING (e.g. a
          // duplicate flag, a new/blocked vendor, a policy or risk
          // flag) means the skill ran fine and surfaced something for
          // a human to look at — it is NOT the same as the skill
          // actually failing. Only a real FAILED status renders red.
          const isWarn = evt?.status === "WARNING";
          const isFail = evt?.status === "FAILED";
          const isActive = running && !done && i === activeIndex;
          const isLast = i === PIPELINE.length - 1;
          const nodeColor = isFail ? "#f0526e" : isWarn ? "#f5b942" : null;
          return (
            <div key={p.skill} style={{ display: "flex", gap: 16 }}>
              <div style={{ display: "flex", flexDirection: "column", alignItems: "center", flex: "none" }}>
                <div className={cls(isActive && "ip-glow-ring")} style={{
                  width: 42, height: 42, borderRadius: 13, display: "flex", alignItems: "center", justifyContent: "center",
                  background: nodeColor ? `${nodeColor}29` : done ? "var(--grad-brand)" : isActive ? "var(--bg-elev-3)" : "var(--bg-elev-2)",
                  color: nodeColor || (done ? "#fff" : isActive ? "#5b6ee8" : "var(--text-faint)"),
                  border: done ? "none" : "1px solid var(--line)",
                  transition: "all .4s ease", flex: "none",
                }}>
                  {isActive ? <Loader2 size={18} className="ip-spin" /> : <p.Icon size={18} strokeWidth={2.2} />}
                </div>
                {!isLast && (
                  <div style={{ width: 2, flex: 1, minHeight: 26, marginTop: 2, marginBottom: 2, background: done && doneSkills.has(PIPELINE[i + 1]?.skill) ? "var(--violet)" : "var(--line)", transition: "background .5s ease" }} />
                )}
              </div>
              <div style={{ paddingBottom: isLast ? 0 : 22, paddingTop: 4, flex: 1, minWidth: 0 }}>
                <div style={{ display: "flex", alignItems: "center", gap: 8, flexWrap: "wrap" }}>
                  <div className="ip-display" style={{ fontSize: 14.5, fontWeight: 700, color: done || isActive ? "var(--text)" : "var(--text-faint)" }}>{p.label}</div>
                  {done && !isWarn && !isFail && <Badge color="#35d08f" bg="rgba(53,208,143,.12)" border="rgba(53,208,143,.3)" icon={Check}>done</Badge>}
                  {isWarn && <Badge color="#f5b942" bg="rgba(245,185,66,.12)" border="rgba(245,185,66,.35)" icon={AlertTriangle}>warning</Badge>}
                  {isFail && <Badge color="#f0526e" bg="rgba(240,82,110,.12)" border="rgba(240,82,110,.3)" icon={X}>failed</Badge>}
                  {isActive && <Badge color="#5b6ee8" bg="rgba(91,110,232,.14)" border="rgba(91,110,232,.35)">running</Badge>}
                  {evt?.timestamp && <span className="ip-mono" style={{ fontSize: 10.5, color: "var(--text-faint)" }}>{new Date(evt.timestamp).toLocaleTimeString()}</span>}
                </div>
                <div style={{ fontSize: 12.5, color: "var(--text-dim)", marginTop: 3 }}>
                  {evt?.message || (isActive ? "Working…" : p.desc)}
                </div>
              </div>
            </div>
          );
        })}
      </div>
    </div>
  );
}

/* ---------------------------------- Sidebar --------------------------------- */

function Sidebar({ page, setPage, theme, setTheme, health, pendingCount, apiBase, setShowSettings, mobileOpen, setMobileOpen }) {
  const items = [
    { id: "dashboard", label: "Dashboard", Icon: LayoutDashboard },
    { id: "upload", label: "Upload & Process", Icon: UploadCloud },
    { id: "copilot", label: "AI Copilot", Icon: Bot },
    { id: "approvals", label: "Approval Queue", Icon: ListChecks, badge: pendingCount },
    { id: "history", label: "History", Icon: HistoryIcon },
  ];
  return (
    <>
      {mobileOpen && <div onClick={() => setMobileOpen(false)} style={{ position: "fixed", inset: 0, background: "rgba(0,0,0,.5)", zIndex: 39, display: "none" }} className="ip-mobile-overlay" />}
      <aside className={cls("ip-sidebar", mobileOpen && "open")} style={{
        width: 246, flex: "none", borderRight: "1px solid var(--line)", background: "var(--bg-elev-1)",
        display: "flex", flexDirection: "column", padding: "20px 14px", position: "sticky", top: 0, height: "100vh", zIndex: 40,
      }}>
        <div
          role="button"
          title="Go to Dashboard"
          onClick={() => { setPage("dashboard"); setMobileOpen(false); }}
          style={{ display: "flex", alignItems: "center", gap: 10, padding: "4px 8px 22px", cursor: "pointer" }}
        >
          <div style={{ width: 34, height: 34, borderRadius: 10, background: "var(--grad-brand)", display: "flex", alignItems: "center", justifyContent: "center", flex: "none" }}>
            <Zap size={18} color="#fff" strokeWidth={2.4} />
          </div>
          <div>
            <div className="ip-display" style={{ fontSize: 15, fontWeight: 700, lineHeight: 1.1 }}>InvoicePilot</div>
            <div style={{ fontSize: 10.5, color: "var(--text-faint)", fontWeight: 600, letterSpacing: ".04em" }}>AGENTIC AI CONSOLE</div>
          </div>
        </div>

        <nav style={{ display: "flex", flexDirection: "column", gap: 3 }}>
          {items.map(it => (
            <div key={it.id} className={cls("ip-nav-item", page === it.id && "active")} onClick={() => { setPage(it.id); setMobileOpen(false); }}>
              <it.Icon size={16.5} strokeWidth={2.2} />
              <span style={{ flex: 1 }}>{it.label}</span>
              {!!it.badge && (
                <span className="ip-mono" style={{ fontSize: 10.5, fontWeight: 700, background: "var(--grad-brand)", color: "#fff", borderRadius: 999, padding: "1px 6px" }}>{it.badge}</span>
              )}
            </div>
          ))}
        </nav>

        <div style={{ marginTop: 22, padding: "12px 12px", borderRadius: 12, background: "var(--bg-elev-2)", border: "1px solid var(--line)" }}>
          <div style={{ fontSize: 10.5, color: "var(--text-faint)", fontWeight: 700, letterSpacing: ".04em", marginBottom: 8 }}>AGENT PIPELINE</div>
          <PipelineTrace compact events={[]} />
        </div>

        <div style={{ flex: 1 }} />

        <div style={{ display: "flex", alignItems: "center", gap: 8, padding: "8px 8px", borderRadius: 10, background: "var(--bg-elev-2)", border: "1px solid var(--line)", marginBottom: 8 }}>
          {health.connected ? <Wifi size={14} color="#35d08f" /> : <WifiOff size={14} color="#f0526e" />}
          <div style={{ flex: 1, minWidth: 0 }}>
            <div style={{ fontSize: 11.5, fontWeight: 700, color: health.connected ? "#35d08f" : "#f0526e" }}>
              {health.connected ? "Backend online" : "Backend offline"}
            </div>
            <div className="ip-mono" style={{ fontSize: 10, color: "var(--text-faint)", overflow: "hidden", textOverflow: "ellipsis", whiteSpace: "nowrap" }}>{apiBase}</div>
          </div>
          <button className="ip-btn ip-btn-ghost ip-btn-sm" style={{ padding: 6 }} onClick={() => setShowSettings(true)}><Settings2 size={13} /></button>
        </div>

        <button className="ip-btn ip-btn-ghost" style={{ width: "100%" }} onClick={() => setTheme(t => t === "dark" ? "light" : "dark")}>
          {theme === "dark" ? <Sun size={15} /> : <Moon size={15} />}
          {theme === "dark" ? "Light mode" : "Dark mode"}
        </button>
      </aside>
    </>
  );
}

function TopBar({ title, subtitle, right, mobileOpen, setMobileOpen }) {
  return (
    <div style={{ display: "flex", alignItems: "center", justifyContent: "space-between", gap: 16, marginBottom: 22, flexWrap: "wrap" }}>
      <div>
        <h1 className="ip-display" style={{ fontSize: 23, fontWeight: 700, margin: 0 }}>{title}</h1>
        {subtitle && <div style={{ fontSize: 13, color: "var(--text-dim)", marginTop: 4 }}>{subtitle}</div>}
      </div>
      <div style={{ display: "flex", gap: 10, alignItems: "center" }}>{right}</div>
    </div>
  );
}

/* ---------------------------------- Settings modal -------------------------- */

function SettingsModal({ open, onClose, apiBase, setApiBase, onTestConnection, testing, health }) {
  const [draft, setDraft] = useState(apiBase);
  useEffect(() => { if (open) setDraft(apiBase); }, [open, apiBase]);
  if (!open) return null;
  return (
    <div style={{ position: "fixed", inset: 0, background: "rgba(4,5,10,.6)", zIndex: 100, display: "flex", alignItems: "center", justifyContent: "center", padding: 16 }} onClick={onClose}>
      <div className="ip-card ip-pop" style={{ width: 460, maxWidth: "100%", padding: 22 }} onClick={e => e.stopPropagation()}>
        <div style={{ display: "flex", alignItems: "center", justifyContent: "space-between", marginBottom: 4 }}>
          <div className="ip-display" style={{ fontSize: 16, fontWeight: 700, display: "flex", alignItems: "center", gap: 8 }}><PlugZap size={17} color="#5b6ee8" />Backend connection</div>
          <button className="ip-btn ip-btn-ghost ip-btn-sm" style={{ padding: 6 }} onClick={onClose}><X size={14} /></button>
        </div>
        <p style={{ fontSize: 12.5, color: "var(--text-dim)", margin: "6px 0 16px" }}>
          Point this console at your FastAPI backend. It runs entirely in your browser, so a backend on <span className="ip-mono">localhost</span> works fine as long as CORS allows this origin.
        </p>
        <div style={{ fontSize: 12, fontWeight: 700, color: "var(--text-dim)", marginBottom: 6 }}>API base URL</div>
        <input className="ip-input ip-mono" value={draft} onChange={e => setDraft(e.target.value)} placeholder="http://localhost:8000" />
        <div style={{ display: "flex", gap: 8, marginTop: 8, marginBottom: 16 }}>
          {["http://localhost:8000", "http://127.0.0.1:8000"].map(u => (
            <button key={u} className="ip-btn ip-btn-outline ip-btn-sm" onClick={() => setDraft(u)}>{u}</button>
          ))}
        </div>

        {!health.connected && (
          <div className="ip-card-2" style={{ padding: 12, marginBottom: 16, fontSize: 12, color: "var(--text-dim)", lineHeight: 1.5 }}>
            <div style={{ fontWeight: 700, color: "var(--text)", marginBottom: 4, display: "flex", alignItems: "center", gap: 6 }}><Info size={13} color="#20c2ae" />Enable CORS on the backend</div>
            Add this to <span className="ip-mono">app/api/main.py</span> so the browser is allowed to call it:
            <pre className="ip-mono ip-scrollbar" style={{ background: "var(--bg-elev-3)", padding: "8px 10px", borderRadius: 8, marginTop: 8, overflowX: "auto", fontSize: 11 }}>
{`from fastapi.middleware.cors import CORSMiddleware
app.add_middleware(CORSMiddleware,
  allow_origins=["*"], allow_methods=["*"], allow_headers=["*"])`}
            </pre>
          </div>
        )}

        <div style={{ display: "flex", gap: 10 }}>
          <button className="ip-btn ip-btn-outline" style={{ flex: 1 }} onClick={() => onTestConnection(draft)} disabled={testing}>
            {testing ? <Loader2 size={14} className="ip-spin" /> : <Wifi size={14} />} Test connection
          </button>
          <button className="ip-btn ip-btn-primary" style={{ flex: 1 }} onClick={() => { setApiBase(draft); onClose(); }}>Save & close</button>
        </div>
        {health.lastTested && (
          <div style={{ marginTop: 12, fontSize: 12, display: "flex", alignItems: "center", gap: 6, color: health.connected ? "#35d08f" : "#f0526e" }}>
            {health.connected ? <CircleCheck size={13} /> : <CircleAlert size={13} />}
            {health.connected ? `Connected — ${health.app || "InvoicePilot AI"} v${health.version || "?"}` : (health.error || "Could not reach backend.")}
          </div>
        )}
      </div>
    </div>
  );
}

/* ---------------------------------- Dashboard -------------------------------- */

function Dashboard({ history, approvals, health, goto, setShowSettings }) {
  const totalProcessed = history.length;
  const autoApproved = history.filter(h => h.recommendation === "AUTO_APPROVE").length;
  const avgRisk = history.length ? Math.round(history.reduce((a, h) => a + (h.risk_score || 0), 0) / history.length) : 0;
  const pending = approvals.filter(a => a.status === "PENDING").length;

  return (
    <div className="ip-fade-in">
      <TopBar
        title="Dashboard"
        subtitle="A live view of the invoice agent's throughput, risk, and review queue."
        right={<button className="ip-btn ip-btn-primary" onClick={() => goto("upload")}><UploadCloud size={15} />Process an invoice</button>}
      />

      {!health.connected && (
        <div className="ip-card" style={{ padding: "14px 16px", marginBottom: 18, display: "flex", alignItems: "center", gap: 12, borderColor: "rgba(240,82,110,.3)" }}>
          <CircleAlert size={18} color="#f0526e" style={{ flex: "none" }} />
          <div style={{ flex: 1, fontSize: 13, color: "var(--text-dim)" }}>
            <b style={{ color: "var(--text)" }}>Backend not reachable.</b> Numbers below reflect this session only. Connect a live backend to pull real vendor and approval data.
          </div>
          <button className="ip-btn ip-btn-outline ip-btn-sm" onClick={() => setShowSettings(true)}>Connect</button>
        </div>
      )}

      <div style={{ display: "grid", gridTemplateColumns: "repeat(auto-fit, minmax(190px, 1fr))", gap: 14, marginBottom: 20 }}>
        <StatCard label="Processed this session" value={totalProcessed} sub={totalProcessed ? `${autoApproved} auto-approved` : "No invoices yet"} tone="violet" Icon={FileText} />
        <StatCard label="Pending approvals" value={pending} sub={pending ? "Awaiting human sign-off" : "Queue is clear"} tone="amber" Icon={ListChecks} />
        <StatCard label="Avg. risk score" value={totalProcessed ? avgRisk : "—"} sub={totalProcessed ? "out of 100" : "Nothing scored yet"} tone="blue" Icon={Gauge} />
        <StatCard label="Auto-approve rate" value={totalProcessed ? `${Math.round((autoApproved / totalProcessed) * 100)}%` : "—"} sub={totalProcessed ? "of processed invoices" : "Nothing processed"} tone="green" Icon={BadgeCheck} trend={totalProcessed && autoApproved / totalProcessed > 0.5 ? "up" : undefined} />
      </div>

      <div style={{ display: "grid", gridTemplateColumns: "1.55fr 1fr", gap: 16, alignItems: "start" }} className="ip-dashboard-grid">
        <div className="ip-card" style={{ padding: 20 }}>
          <div style={{ display: "flex", alignItems: "center", justifyContent: "space-between", marginBottom: 14 }}>
            <div className="ip-display" style={{ fontSize: 15, fontWeight: 700 }}>Recent invoices</div>
            {history.length > 0 && <button className="ip-btn ip-btn-ghost ip-btn-sm" onClick={() => goto("history")}>View all<ArrowRight size={13} /></button>}
          </div>
          {history.length === 0 ? (
            <EmptyState Icon={FilePlus2} title="No invoices processed yet" body="Upload a document and the agent will extract, validate, score, and route it in seconds." action={<button className="ip-btn ip-btn-primary" onClick={() => goto("upload")}><UploadCloud size={14} />Upload your first invoice</button>} />
          ) : (
            <div style={{ display: "flex", flexDirection: "column" }}>
              {history.slice(0, 6).map(h => (
                <div key={h._id} className="ip-table-row" style={{ display: "flex", alignItems: "center", gap: 12, padding: "11px 8px", borderBottom: "1px solid var(--line-soft)", cursor: "pointer", borderRadius: 10 }} onClick={() => goto("history")}>
                  <IconTile Icon={fileIconFor(h._filename)} tone="violet" size={15} />
                  <div style={{ flex: 1, minWidth: 0 }}>
                    <div style={{ fontSize: 13.5, fontWeight: 600, overflow: "hidden", textOverflow: "ellipsis", whiteSpace: "nowrap" }}>{h.invoice?.vendor_name || "Unknown vendor"}</div>
                    <div className="ip-mono" style={{ fontSize: 11, color: "var(--text-faint)" }}>{h.invoice?.invoice_number || "—"} · {timeAgo(h._processedAt)}</div>
                  </div>
                  <div style={{ fontSize: 13, fontWeight: 700, textAlign: "right" }} className="ip-mono"><MoneyWithINR amount={h.invoice?.total_amount} currency={h.invoice?.currency} size={13} /></div>
                  <RiskBadge level={h.risk_level} />
                  <RecBadge rec={h.recommendation} />
                </div>
              ))}
            </div>
          )}
        </div>

        <div className="ip-card" style={{ padding: 20 }}>
          <div className="ip-display" style={{ fontSize: 15, fontWeight: 700, marginBottom: 4 }}>Agent pipeline</div>
          <div style={{ fontSize: 12, color: "var(--text-dim)", marginBottom: 14 }}>Nine skills run in sequence for every invoice.</div>
          <PipelineTrace events={[]} />
        </div>
      </div>
    </div>
  );
}

function fileIconFor(name) {
  const ext = (name || "").split(".").pop()?.toLowerCase();
  if (["png", "jpg", "jpeg"].includes(ext)) return FileImage;
  if (ext === "txt") return FileType2;
  return FileText;
}

/* ---------------------------------- Upload & Process -------------------------- */

const MIN_PASTED_TEXT_LEN = 20;

function UploadPage({ apiCall, onComplete, addToast, connected }) {
  const [mode, setMode] = useState("file"); // "file" | "text"
  const [dragActive, setDragActive] = useState(false);

  // Pre-run queue — as many invoices (files or pasted-text blocks) as
  // the user wants to add before hitting "Run the agent".
  const [items, setItems] = useState([]); // { id, kind: 'file'|'text', file?, name, text?, filename? }

  const [running, setRunning] = useState(false);
  const [batchDone, setBatchDone] = useState(false);
  // Per-item run state, keyed by item id: { status, revealCount, result, error }
  const [runState, setRunState] = useState({});

  const inputRef = useRef(null);
  const mountedRef = useRef(true);
  useEffect(() => {
    // Runs on every mount (including React StrictMode's dev-only
    // mount → cleanup → re-mount cycle) so mountedRef is correctly
    // `true` for the instance that's actually on screen — otherwise
    // the cleanup below can leave it permanently `false` and silently
    // stall runBatch() before it ever calls the backend.
    mountedRef.current = true;
    return () => { mountedRef.current = false; };
  }, []);

  const validateFile = (f) => {
    if (!f) return "No file selected.";
    const ext = "." + f.name.split(".").pop()?.toLowerCase();
    if (!SUPPORTED_TYPES.includes(ext)) return `Unsupported file type "${ext}". Use ${SUPPORTED_TYPES.join(", ")}.`;
    if (f.size > MAX_UPLOAD_MB * 1024 * 1024) return `File is larger than the ${MAX_UPLOAD_MB} MB limit.`;
    if (f.size === 0) return "File is empty.";
    return null;
  };

  const addFiles = (fileList) => {
    const incoming = Array.from(fileList || []);
    if (!incoming.length) return;
    const accepted = [];
    incoming.forEach(f => {
      const err = validateFile(f);
      if (err) { addToast(`${f.name}: ${err}`, "error"); return; }
      accepted.push({ id: uid(), kind: "file", file: f, name: f.name });
    });
    if (accepted.length) setItems(prev => [...prev, ...accepted]);
  };

  const addTextItem = () => {
    setItems(prev => [...prev, { id: uid(), kind: "text", text: "", filename: "" }]);
  };

  const updateTextItem = (id, patch) => {
    setItems(prev => prev.map(it => it.id === id ? { ...it, ...patch } : it));
  };

  const removeItem = (id) => {
    setItems(prev => prev.filter(it => it.id !== id));
    setRunState(prev => { const n = { ...prev }; delete n[id]; return n; });
  };

  const resetAll = () => {
    setItems([]);
    setRunState({});
    setRunning(false);
    setBatchDone(false);
  };

  const onDrop = (e) => {
    e.preventDefault(); setDragActive(false);
    addFiles(e.dataTransfer.files);
  };

  // Switching modes clears the queue — mixing file and pasted-text
  // invoices in one batch would be confusing to review.
  const switchMode = (m) => {
    if (m === mode) return;
    setMode(m);
    resetAll();
  };

  const itemLabel = (it) => it.kind === "file" ? it.name : (it.filename.trim() || "pasted-invoice.txt");

  const textItemsInvalid = items.some(it => it.kind === "text" && it.text.trim().length < MIN_PASTED_TEXT_LEN);
  const canRun = items.length > 0 && !running && !textItemsInvalid;

  const revealItemEvents = (id, events) => new Promise((resolve) => {
    if (!events || !events.length) { resolve(); return; }
    let i = 0;
    const tick = () => {
      if (!mountedRef.current) { resolve(); return; }
      i += 1;
      setRunState(prev => ({ ...prev, [id]: { ...prev[id], revealCount: i } }));
      if (i >= events.length) setTimeout(resolve, 420);
      else setTimeout(tick, 380);
    };
    tick();
  });

  const setItemState = (id, patch) => {
    if (!mountedRef.current) return;
    setRunState(prev => ({ ...prev, [id]: { ...prev[id], ...patch } }));
  };

  const runBatch = async (useMock) => {
    if (!items.length) return;
    setRunning(true);
    setBatchDone(false);

    const initial = {};
    items.forEach(it => { initial[it.id] = { status: "queued", revealCount: 0, result: null, error: null }; });
    setRunState(initial);

    let lastEnriched = null;
    let succeeded = 0;
    let failed = 0;

    for (const it of items) {
      if (!mountedRef.current) return;
      setItemState(it.id, { status: "processing" });

      try {
        let res;
        if (useMock) {
          await new Promise(r => setTimeout(r, 260));
          res = buildMockResult({ name: itemLabel(it) });
        } else if (it.kind === "file") {
          const fd = new FormData();
          fd.append("file", it.file);
          res = await apiCall("/process-invoice", { method: "POST", body: fd });
        } else {
          res = await apiCall("/process-invoice-text", {
            method: "POST",
            headers: { "Content-Type": "application/json" },
            body: JSON.stringify({ text: it.text, filename: it.filename.trim() || undefined }),
          });
        }

        res._filename = itemLabel(it);
        setItemState(it.id, { events: res.events || [] });
        await revealItemEvents(it.id, res.events || []);

        const enriched = { ...res, _id: uid(), _processedAt: new Date().toISOString(), _filename: res._filename };
        setItemState(it.id, { status: "done", result: enriched });
        onComplete(enriched);
        lastEnriched = enriched;
        succeeded += 1;
      } catch (e) {
        setItemState(it.id, { status: "error", error: e.message || "Processing failed." });
        addToast(`${itemLabel(it)}: ${e.message || "Processing failed."}`, "error");
        failed += 1;
      }
    }

    if (!mountedRef.current) return;
    setRunning(false);
    setBatchDone(true);

    if (succeeded && !failed) addToast(`${succeeded} invoice${succeeded > 1 ? "s" : ""} processed.`, "success");
    else if (succeeded && failed) addToast(`${succeeded} processed, ${failed} failed — see details below.`, "info");
    else if (failed) addToast(`All ${failed} invoice${failed > 1 ? "s" : ""} failed to process.`, "error");
  };

  const showQueue = running || batchDone;
  const doneCount = Object.values(runState).filter(s => s?.status === "done").length;
  const errorCount = Object.values(runState).filter(s => s?.status === "error").length;

  return (
    <div className="ip-fade-in">
      <TopBar
        title="Upload & process"
        subtitle="Add one invoice or a whole batch — files, pasted text, or a mix in separate runs — and the agent extracts, validates, scores, and routes every one."
      />

      {!showQueue ? (
        <div style={{ display: "grid", gridTemplateColumns: "1.3fr 1fr", gap: 16 }} className="ip-dashboard-grid">
          <div className="ip-card" style={{ padding: 22 }}>
            <div style={{ display: "flex", gap: 6, padding: 4, marginBottom: 18, background: "var(--bg-elev-2)", border: "1px solid var(--line)", borderRadius: 12, width: "fit-content" }}>
              <button
                className={cls("ip-btn ip-btn-sm", mode === "file" ? "ip-btn-primary" : "ip-btn-ghost")}
                style={mode === "file" ? {} : { background: "transparent", border: "1px solid transparent" }}
                onClick={() => switchMode("file")}
              >
                <UploadCloud size={13} />Upload files
              </button>
              <button
                className={cls("ip-btn ip-btn-sm", mode === "text" ? "ip-btn-primary" : "ip-btn-ghost")}
                style={mode === "text" ? {} : { background: "transparent", border: "1px solid transparent" }}
                onClick={() => switchMode("text")}
              >
                <FileType2 size={13} />Paste / type text
              </button>
              {items.length > 0 && (
                <Badge color="#5b6ee8" bg="rgba(91,110,232,.14)" border="rgba(91,110,232,.35)">
                  {items.length} queued
                </Badge>
              )}
            </div>

            {mode === "file" ? (
              <>
                <div
                  className={cls("ip-drop", dragActive && "active")}
                  style={{ padding: "36px 20px", textAlign: "center", cursor: "pointer" }}
                  onDragOver={e => { e.preventDefault(); setDragActive(true); }}
                  onDragLeave={() => setDragActive(false)}
                  onDrop={onDrop}
                  onClick={() => inputRef.current?.click()}
                >
                  <input ref={inputRef} type="file" multiple accept={SUPPORTED_TYPES.join(",")} style={{ display: "none" }} onChange={e => { addFiles(e.target.files); e.target.value = ""; }} />
                  <div style={{ width: 54, height: 54, borderRadius: 16, background: "var(--grad-brand-soft)", display: "flex", alignItems: "center", justifyContent: "center", margin: "0 auto 14px" }}>
                    <UploadCloud size={24} color="#5b6ee8" />
                  </div>
                  <div className="ip-display" style={{ fontSize: 15.5, fontWeight: 700 }}>Drag and drop invoices here</div>
                  <div style={{ fontSize: 12.5, color: "var(--text-dim)", marginTop: 6 }}>or click to browse — select as many as you need · {SUPPORTED_TYPES.join(", ")} up to {MAX_UPLOAD_MB} MB each</div>
                </div>

                {items.length > 0 && (
                  <div style={{ display: "flex", flexDirection: "column", gap: 8, marginTop: 16 }}>
                    {items.map(it => (
                      <div key={it.id} className="ip-card-2 ip-pop" style={{ padding: "12px 14px", display: "flex", alignItems: "center", gap: 12 }}>
                        <IconTile Icon={fileIconFor(it.name)} tone="violet" size={16} />
                        <div style={{ flex: 1, minWidth: 0 }}>
                          <div style={{ fontSize: 13.5, fontWeight: 600, overflow: "hidden", textOverflow: "ellipsis", whiteSpace: "nowrap" }}>{it.name}</div>
                          <div className="ip-mono" style={{ fontSize: 11, color: "var(--text-faint)" }}>{fmtBytes(it.file.size)}</div>
                        </div>
                        <button className="ip-btn ip-btn-ghost ip-btn-sm" style={{ padding: 7 }} onClick={() => removeItem(it.id)}><Trash2 size={13} /></button>
                      </div>
                    ))}
                  </div>
                )}
              </>
            ) : (
              <>
                {items.map((it, idx) => (
                  <div key={it.id} className="ip-card-2 ip-pop" style={{ padding: 14, marginBottom: 12 }}>
                    <div style={{ display: "flex", alignItems: "center", justifyContent: "space-between", marginBottom: 8 }}>
                      <div style={{ fontSize: 12, fontWeight: 700, color: "var(--text-dim)" }}>Invoice {idx + 1}</div>
                      <button className="ip-btn ip-btn-ghost ip-btn-sm" style={{ padding: 6 }} onClick={() => removeItem(it.id)}><Trash2 size={12} /></button>
                    </div>
                    <input
                      className="ip-input"
                      placeholder="Display name (optional) — e.g. meridian-office-supplies.txt"
                      value={it.filename}
                      onChange={e => updateTextItem(it.id, { filename: e.target.value })}
                      style={{ marginBottom: 10 }}
                    />
                    <textarea
                      className="ip-input"
                      rows={7}
                      style={{ resize: "vertical", fontFamily: "'JetBrains Mono', monospace", fontSize: 12.5, lineHeight: 1.6 }}
                      placeholder={`Paste or type the invoice contents here — vendor, invoice number, date, line items, total, etc.`}
                      value={it.text}
                      onChange={e => updateTextItem(it.id, { text: e.target.value })}
                    />
                    <div style={{ display: "flex", justifyContent: "space-between", marginTop: 6 }}>
                      <span className="ip-mono" style={{ fontSize: 10.5, color: "var(--text-faint)" }}>{it.text.trim().length} chars</span>
                      {it.text.trim().length > 0 && it.text.trim().length < MIN_PASTED_TEXT_LEN && (
                        <span style={{ fontSize: 10.5, color: "#f0526e" }}>Add a bit more detail</span>
                      )}
                    </div>
                  </div>
                ))}
                <button className="ip-btn ip-btn-outline" style={{ width: "100%" }} onClick={addTextItem}>
                  <FilePlus2 size={14} />{items.length ? "Add another invoice" : "Add an invoice text block"}
                </button>
              </>
            )}

            <div style={{ display: "flex", gap: 10, marginTop: 18 }}>
              <button className="ip-btn ip-btn-primary" style={{ flex: 1 }} disabled={!canRun} onClick={() => runBatch(false)}>
                <Sparkles size={15} />Run the agent{items.length > 1 ? ` on ${items.length} invoices` : ""}
              </button>
              {!connected && (
                <button className="ip-btn ip-btn-outline" disabled={!canRun} onClick={() => runBatch(true)}>
                  <PlayCircle size={15} />Try with sample data
                </button>
              )}
            </div>
            {!connected && <div style={{ fontSize: 11.5, color: "var(--text-faint)", marginTop: 10 }}>Backend isn't connected — "Run the agent" will call it anyway and show a clear error per invoice, or use sample data to preview the full flow.</div>}
          </div>

          <div className="ip-card" style={{ padding: 20 }}>
            <div className="ip-display" style={{ fontSize: 14.5, fontWeight: 700, marginBottom: 4 }}>What happens next</div>
            <div style={{ fontSize: 12, color: "var(--text-dim)", marginBottom: 14 }}>
              Each invoice is sent — one at a time, in order — to
              {" "}{mode === "file" ? <span className="ip-mono">/process-invoice</span> : <span className="ip-mono">/process-invoice-text</span>}
              {" "}and run through all nine skills. One failing invoice never blocks the rest of the batch.
            </div>
            <PipelineTrace events={[]} />
          </div>
        </div>
      ) : (
        <div style={{ display: "grid", gridTemplateColumns: "1fr", gap: 16, maxWidth: 720 }}>
          {batchDone && (
            <div className="ip-card" style={{ padding: "14px 18px", display: "flex", alignItems: "center", gap: 12, flexWrap: "wrap" }}>
              <IconTile Icon={errorCount && !doneCount ? FileWarning : BadgeCheck} tone={errorCount && !doneCount ? "rose" : "green"} size={16} />
              <div style={{ flex: 1, minWidth: 200, fontSize: 13, color: "var(--text-dim)" }}>
                <b style={{ color: "var(--text)" }}>{doneCount} of {items.length} processed successfully.</b>
                {errorCount > 0 && ` ${errorCount} need attention — see below.`}
              </div>
              {doneCount > 0 && (
                <button className="ip-btn ip-btn-primary ip-btn-sm" onClick={() => onComplete(null, true)}>
                  View latest result<ArrowRight size={14} />
                </button>
              )}
              <button className="ip-btn ip-btn-outline ip-btn-sm" onClick={resetAll}>Process another batch</button>
            </div>
          )}

          {items.map(it => {
            const st = runState[it.id] || { status: "queued", revealCount: 0 };
            const label = itemLabel(it);
            return (
              <div key={it.id} className={cls("ip-card", st.status === "processing" && "ip-scan")} style={{ padding: 18 }}>
                <div style={{ display: "flex", alignItems: "center", gap: 12, marginBottom: st.status === "processing" ? 14 : 0 }}>
                  <IconTile Icon={fileIconFor(label)} tone={st.status === "error" ? "rose" : st.status === "done" ? "green" : "violet"} size={16} />
                  <div style={{ flex: 1, minWidth: 0 }}>
                    <div style={{ fontSize: 13.5, fontWeight: 700, overflow: "hidden", textOverflow: "ellipsis", whiteSpace: "nowrap" }}>{label}</div>
                    <div style={{ fontSize: 11.5, color: "var(--text-faint)" }}>
                      {st.status === "queued" && "Waiting in queue…"}
                      {st.status === "processing" && "Agent is running…"}
                      {st.status === "done" && "Completed"}
                      {st.status === "error" && (st.error || "Processing failed.")}
                    </div>
                  </div>
                  {st.status === "processing" && <Loader2 size={17} className="ip-spin" color="#5b6ee8" />}
                  {st.status === "done" && st.result && (
                    <div style={{ display: "flex", gap: 8, alignItems: "center" }}>
                      <RiskBadge level={st.result.risk_level} />
                      <RecBadge rec={st.result.recommendation} />
                    </div>
                  )}
                  {st.status === "error" && <CircleAlert size={17} color="#f0526e" />}
                </div>
                {st.status === "processing" && (
                  <PipelineTrace compact events={(st.events || []).slice(0, st.revealCount || 0)} running />
                )}
              </div>
            );
          })}
        </div>
      )}
    </div>
  );
}

/* ---------------------------------- Results ---------------------------------- */

function RiskGauge({ score = 0, level = "LOW" }) {
  const s = RISK_STYLE[level] || RISK_STYLE.LOW;
  const pct = Math.max(0, Math.min(100, score));
  const angle = (pct / 100) * 270 - 135;
  const r = 54, cx = 70, cy = 70;
  const toXY = (deg) => {
    const rad = (deg * Math.PI) / 180;
    return [cx + r * Math.cos(rad), cy + r * Math.sin(rad)];
  };
  const startDeg = -135, endDeg = -135 + (pct / 100) * 270;
  const [sx, sy] = toXY(startDeg);
  const [ex, ey] = toXY(endDeg);
  const largeArc = endDeg - startDeg > 180 ? 1 : 0;
  const [bgx, bgy] = toXY(135);
  return (
    <div style={{ display: "flex", flexDirection: "column", alignItems: "center" }}>
      <svg width="140" height="120" viewBox="0 0 140 110">
        <path d={`M ${toXY(-135)[0]} ${toXY(-135)[1]} A ${r} ${r} 0 1 1 ${bgx} ${bgy}`} fill="none" stroke="var(--bg-elev-3)" strokeWidth="11" strokeLinecap="round" />
        {pct > 0 && <path d={`M ${sx} ${sy} A ${r} ${r} 0 ${largeArc} 1 ${ex} ${ey}`} fill="none" stroke={s.color} strokeWidth="11" strokeLinecap="round" />}
        <text x="70" y="66" textAnchor="middle" fontSize="26" fontWeight="700" fill="var(--text)" fontFamily="Space Grotesk, sans-serif">{Math.round(pct)}</text>
        <text x="70" y="84" textAnchor="middle" fontSize="10" fill="var(--text-faint)" fontFamily="Inter, sans-serif" letterSpacing="0.05em">/ 100 RISK</text>
      </svg>
      <div style={{ marginTop: -4 }}><RiskBadge level={level} /></div>
    </div>
  );
}

function DetailRow({ label, value, mono }) {
  return (
    <div style={{ display: "flex", justifyContent: "space-between", alignItems: "center", padding: "9px 0", borderBottom: "1px solid var(--line-soft)" }}>
      <span style={{ fontSize: 12.5, color: "var(--text-dim)" }}>{label}</span>
      <span className={mono ? "ip-mono" : ""} style={{ fontSize: 13, fontWeight: 600, textAlign: "right" }}>{value ?? "—"}</span>
    </div>
  );
}

const TIMING_LABELS = {
  extract_invoice: "Groq LLM",
  vendor_lookup: "Vendor Lookup",
  validate_invoice: "Validation",
  duplicate_detection: "Duplicate Engine",
  policy_engine: "Policy Engine",
  risk_assessment: "Risk Assessment",
  recommendation: "Recommendation",
  approval_queue: "Approval Queue",
  audit_logger: "Audit Logger",
};

function ProcessingTimeCard({ meta, addToast }) {
  const timings = meta?.skill_timings || {};
  const rows = PIPELINE
    .map(p => ({ key: p.skill, label: TIMING_LABELS[p.skill] || p.label, seconds: timings[p.skill] }))
    .filter(r => typeof r.seconds === "number");

  const total = meta?.processing_time;
  if ((total === null || total === undefined) && rows.length === 0) return null;

  const copyBreakdown = () => {
    const lines = [
      `Execution Time: ${total !== undefined && total !== null ? `${Number(total).toFixed(2)} sec` : "—"}`,
      ...rows.map(r => `${r.label}: ${r.seconds.toFixed(2)} sec`),
    ];
    const text = lines.join("\n");
    if (navigator.clipboard?.writeText) {
      navigator.clipboard.writeText(text).then(() => addToast?.("Processing time copied", "success")).catch(() => {});
    }
  };

  return (
    <div className="ip-card" style={{ padding: 20 }}>
      <div style={{ display: "flex", alignItems: "center", justifyContent: "space-between", marginBottom: 10 }}>
        <div className="ip-display" style={{ fontSize: 14, fontWeight: 700, display: "flex", alignItems: "center", gap: 7 }}>
          <Timer size={14} color="#5b6ee8" />Processing Time
        </div>
        <button
          className="ip-btn ip-btn-ghost ip-btn-sm"
          title="Copy processing time"
          onClick={copyBreakdown}
          style={{ padding: 6 }}
        >
          <Copy size={13} />
        </button>
      </div>
      <div style={{ borderRadius: 12, background: "var(--bg-elev-2)", border: "1px solid var(--line)", padding: "14px 16px" }}>
        <DetailRow label="Execution Time" value={total !== undefined && total !== null ? `${Number(total).toFixed(2)} sec` : "—"} mono />
        {rows.map(r => (
          <DetailRow key={r.key} label={r.label} value={`${r.seconds.toFixed(2)} sec`} mono />
        ))}
      </div>
    </div>
  );
}

function ResultsPage({ result, goto, onDecision, apiCall, addToast, connected, onAskCopilot }) {
  if (!result) {
    return <EmptyState Icon={FileWarning} title="No result selected" body="Process an invoice first, or open one from History." action={<button className="ip-btn ip-btn-primary" onClick={() => goto("upload")}><UploadCloud size={14} />Upload an invoice</button>} />;
  }
  const inv = result.invoice || {};
  const vendor = result.vendor || {};
  const dup = result.duplicate || {};
  const meta = result.metadata || {};
  const hasIssues = (result.errors?.length || 0) + (result.warnings?.length || 0) > 0;

  return (
    <div className="ip-fade-in">
      <TopBar
        title={inv.vendor_name || "Invoice result"}
        subtitle={<span className="ip-mono">{inv.invoice_number || "—"} · exec {meta.execution_id?.slice(0, 12) || "—"}</span>}
        right={
          <>
            <RecBadge rec={result.recommendation} />
            {result.queued_for_approval && <button className="ip-btn ip-btn-outline ip-btn-sm" onClick={() => goto("approvals")}>In approval queue<ArrowUpRight size={12} /></button>}
            <button className="ip-btn ip-btn-outline ip-btn-sm" onClick={() => onAskCopilot?.(meta.execution_id)}><Bot size={13} />Ask AI Copilot</button>
            <button className="ip-btn ip-btn-primary ip-btn-sm" onClick={() => goto("upload")}><UploadCloud size={13} />New invoice</button>
          </>
        }
      />

      {result.requires_human_review && (
        <div className="ip-card" style={{ padding: "13px 16px", marginBottom: 16, display: "flex", alignItems: "center", gap: 12, borderColor: "rgba(245,185,66,.35)", background: "rgba(245,185,66,.05)" }}>
          <ShieldAlert size={17} color="#f5b942" style={{ flex: "none" }} />
          <div style={{ fontSize: 13, color: "var(--text-dim)" }}><b style={{ color: "var(--text)" }}>This invoice needs human review.</b> It has been queued for approval — decide it from the Approval Queue.</div>
        </div>
      )}

      <div style={{ display: "grid", gridTemplateColumns: "1fr 1.4fr", gap: 16, alignItems: "start" }} className="ip-dashboard-grid">
        <div style={{ display: "flex", flexDirection: "column", gap: 16 }}>
          <div className="ip-card" style={{ padding: 20, display: "flex", flexDirection: "column", alignItems: "center" }}>
            <RiskGauge score={result.risk_score} level={result.risk_level} />
            <div style={{ width: "100%", marginTop: 10 }}>
              <DetailRow label="Provider used" value={meta.provider_used || "—"} mono />
              <DetailRow label="Retries" value={meta.retry_count ?? 0} mono />
              <DetailRow label="Validation status" value={hasIssues ? "Issues flagged" : "Passed"} />
            </div>
          </div>

          <ProcessingTimeCard meta={meta} addToast={addToast} />

          <div className="ip-card" style={{ padding: 20 }}>
            <div className="ip-display" style={{ fontSize: 14, fontWeight: 700, marginBottom: 10, display: "flex", alignItems: "center", gap: 7 }}><Copy size={14} color="#5b6ee8" />Duplicate check</div>
            <DetailRow label="Is duplicate" value={dup.is_duplicate ? "Yes" : "No"} />
            <DetailRow label="Match type" value={dup.match_type || "NONE"} />
            {dup.reason && <div style={{ fontSize: 12, color: "var(--text-dim)", marginTop: 8 }}>{dup.reason}</div>}
          </div>
        </div>

        <div style={{ display: "flex", flexDirection: "column", gap: 16 }}>
          <div className="ip-card" style={{ padding: 20 }}>
            <div className="ip-display" style={{ fontSize: 14, fontWeight: 700, marginBottom: 10, display: "flex", alignItems: "center", gap: 7 }}><FileText size={14} color="#5b6ee8" />Invoice details</div>
            <div style={{ display: "grid", gridTemplateColumns: "1fr 1fr", gap: "0 24px" }}>
              <DetailRow label="Vendor" value={inv.vendor_name} />
              <DetailRow label="Invoice number" value={inv.invoice_number} mono />
              <DetailRow label="Invoice date" value={fmtDateOnly(inv.invoice_date)} />
              <DetailRow label="Currency" value={inv.currency} />
              <DetailRow label="Amount" value={<MoneyWithINR amount={inv.total_amount} currency={inv.currency} size={16} />} />
              <DetailRow label="Recommendation" value={<RecBadge rec={result.recommendation} />} />
            </div>
          </div>

          <div className="ip-card" style={{ padding: 20 }}>
            <div className="ip-display" style={{ fontSize: 14, fontWeight: 700, marginBottom: 10, display: "flex", alignItems: "center", gap: 7 }}><Landmark size={14} color="#5b6ee8" />Vendor ledger</div>
            <div style={{ display: "flex", alignItems: "center", gap: 10, marginBottom: 10 }}>
              <div style={{ fontSize: 14, fontWeight: 700 }}>{vendor.name || "—"}</div>
              {vendor.is_new_vendor && <Badge color="#20c2ae" bg="rgba(32,194,174,.12)" border="rgba(32,194,174,.3)">New vendor</Badge>}
              {vendor.status && <Badge color="#35d08f" bg="rgba(53,208,143,.12)" border="rgba(53,208,143,.3)">{vendor.status}</Badge>}
            </div>
            <div style={{ display: "grid", gridTemplateColumns: "1fr 1fr", gap: "0 24px" }}>
              <DetailRow label="GST number" value={vendor.gst_number} mono />
              <DetailRow label="Total invoices" value={vendor.total_invoices} />
              <DetailRow label="Total spend" value={<MoneyWithINR amount={vendor.total_spend} currency={inv.currency} />} />
              <DetailRow label="Currencies" value={(vendor.currencies || []).join(", ") || "—"} />
              <DetailRow label="First seen" value={fmtDateOnly(vendor.first_seen)} />
              <DetailRow label="Last seen" value={fmtDateOnly(vendor.last_seen)} />
            </div>
          </div>

          {hasIssues && (
            <div className="ip-card" style={{ padding: 20 }}>
              <div className="ip-display" style={{ fontSize: 14, fontWeight: 700, marginBottom: 10, display: "flex", alignItems: "center", gap: 7 }}><CircleAlert size={14} color="#f5b942" />Flags raised</div>
              {result.errors?.map((e, i) => (
                <div key={`e${i}`} style={{ display: "flex", gap: 8, fontSize: 12.5, color: "#f0526e", padding: "6px 0" }}><CircleAlert size={14} style={{ flex: "none", marginTop: 1 }} />{e}</div>
              ))}
              {result.warnings?.map((w, i) => (
                <div key={`w${i}`} style={{ display: "flex", gap: 8, fontSize: 12.5, color: "#f5b942", padding: "6px 0" }}><Info size={14} style={{ flex: "none", marginTop: 1 }} />{w}</div>
              ))}
            </div>
          )}

          <div className="ip-card" style={{ padding: 20 }}>
            <div className="ip-display" style={{ fontSize: 14, fontWeight: 700, marginBottom: 10 }}>Execution trace</div>
            <PipelineTrace events={result.events || []} />
          </div>
        </div>
      </div>
    </div>
  );
}

/* ---------------------------------- Approval Queue ---------------------------------- */

function DecisionModal({ open, action, item, onClose, onConfirm, submitting }) {
  const [decidedBy, setDecidedBy] = useState("");
  const [notes, setNotes] = useState("");
  useEffect(() => { if (open) { setDecidedBy(""); setNotes(""); } }, [open]);
  if (!open) return null;
  const isApprove = action === "approve";
  return (
    <div style={{ position: "fixed", inset: 0, background: "rgba(4,5,10,.6)", zIndex: 100, display: "flex", alignItems: "center", justifyContent: "center", padding: 16 }} onClick={onClose}>
      <div className="ip-card ip-pop" style={{ width: 420, maxWidth: "100%", padding: 22 }} onClick={e => e.stopPropagation()}>
        <div style={{ display: "flex", alignItems: "center", gap: 10, marginBottom: 4 }}>
          <IconTile Icon={isApprove ? Check : Ban} tone={isApprove ? "green" : "rose"} size={16} />
          <div role="heading" aria-level={2} className="ip-display" style={{ fontSize: 15.5, fontWeight: 700 }}>{isApprove ? "Approve invoice" : "Reject invoice"}</div>
        </div>
        <div style={{ fontSize: 12.5, color: "var(--text-dim)", margin: "8px 0 16px" }}>
          {item?.vendor_name} · <span className="ip-mono">{item?.invoice_number}</span> · {fmtMoney(item?.total_amount, item?.currency)}
        </div>
        <div style={{ fontSize: 12, fontWeight: 700, color: "var(--text-dim)", marginBottom: 6 }}>Your name (optional)</div>
        <input className="ip-input" value={decidedBy} onChange={e => setDecidedBy(e.target.value)} placeholder="e.g. Priya Shah" style={{ marginBottom: 12 }} />
        <div style={{ fontSize: 12, fontWeight: 700, color: "var(--text-dim)", marginBottom: 6 }}>Notes (optional)</div>
        <textarea className="ip-input" rows={3} value={notes} onChange={e => setNotes(e.target.value)} placeholder="Add context for the audit trail…" style={{ resize: "vertical", marginBottom: 18 }} />
        <div style={{ display: "flex", gap: 10 }}>
          <button className="ip-btn ip-btn-outline" style={{ flex: 1 }} onClick={onClose}>Cancel</button>
          <button className={cls("ip-btn", isApprove ? "ip-btn-primary" : "ip-btn-danger")} style={{ flex: 1 }} disabled={submitting} onClick={() => onConfirm({ decided_by: decidedBy || undefined, notes: notes || undefined })}>
            {submitting ? <Loader2 size={14} className="ip-spin" /> : (isApprove ? <Check size={14} /> : <Ban size={14} />)}
            {isApprove ? "Approve" : "Reject"}
          </button>
        </div>
      </div>
    </div>
  );
}

function ApprovalsPage({ approvals, loading, pendingOnly, setPendingOnly, onRefresh, onDecide, addToast, connected }) {
  const [modal, setModal] = useState(null); // { action, item }
  const [submitting, setSubmitting] = useState(false);

  const confirm = async (payload) => {
    setSubmitting(true);
    try {
      await onDecide(modal.item, modal.action, payload);
      addToast(`Invoice ${modal.action === "approve" ? "approved" : "rejected"}.`, "success");
      setModal(null);
    } catch (e) {
      addToast(e.message || "Could not record decision.", "error");
    } finally {
      setSubmitting(false);
    }
  };

  return (
    <div className="ip-fade-in">
      <TopBar
        title="Approval queue"
        subtitle="Invoices the policy engine routed to a human for sign-off."
        right={
          <>
            <div className="ip-card-2" style={{ display: "flex", padding: 3, borderRadius: 10 }}>
              {[{ v: true, l: "Pending" }, { v: false, l: "All" }].map(o => (
                <button key={o.l} onClick={() => setPendingOnly(o.v)} className="ip-btn ip-btn-sm" style={{
                  background: pendingOnly === o.v ? "var(--grad-brand)" : "transparent", color: pendingOnly === o.v ? "#fff" : "var(--text-dim)",
                }}>{o.l}</button>
              ))}
            </div>
            <button className="ip-btn ip-btn-outline ip-btn-sm" onClick={onRefresh} disabled={loading}>
              <RefreshCw size={13} className={loading ? "ip-spin" : ""} />Refresh
            </button>
          </>
        }
      />

      {!connected && (
        <div className="ip-card" style={{ padding: "13px 16px", marginBottom: 16, display: "flex", alignItems: "center", gap: 12, borderColor: "rgba(240,82,110,.3)" }}>
          <CircleAlert size={17} color="#f0526e" style={{ flex: "none" }} />
          <div style={{ fontSize: 13, color: "var(--text-dim)" }}>Backend not reachable — showing sample queue data so you can preview the review flow.</div>
        </div>
      )}

      {loading ? (
        <div className="ip-card" style={{ padding: 40, textAlign: "center", color: "var(--text-dim)", fontSize: 13 }}><Loader2 size={20} className="ip-spin" style={{ margin: "0 auto 10px" }} />Loading queue…</div>
      ) : approvals.length === 0 ? (
        <EmptyState Icon={ListChecks} title={pendingOnly ? "Queue is clear" : "No approval history yet"} body={pendingOnly ? "Every processed invoice is currently within auto-approve policy." : "Decisions you make will appear here."} />
      ) : (
        <div style={{ display: "flex", flexDirection: "column", gap: 12 }}>
          {approvals.map(item => (
            <div key={item.execution_id} className="ip-card ip-fade-in" style={{ padding: "16px 18px", display: "flex", alignItems: "center", gap: 16, flexWrap: "wrap" }}>
              <IconTile Icon={ShieldAlert} tone={item.risk_level === "CRITICAL" || item.risk_level === "HIGH" ? "rose" : "amber"} size={17} />
              <div style={{ flex: "1 1 220px", minWidth: 180 }}>
                <div style={{ fontSize: 14, fontWeight: 700 }}>{item.vendor_name || "Unknown vendor"}</div>
                <div className="ip-mono" style={{ fontSize: 11.5, color: "var(--text-faint)" }}>{item.invoice_number} · {timeAgo(item.created_at)}</div>
              </div>
              <div style={{ fontSize: 15, fontWeight: 700 }} className="ip-mono"><MoneyWithINR amount={item.total_amount} currency={item.currency} size={15} /></div>
              <RiskBadge level={item.risk_level} />
              <RecBadge rec={item.recommendation} />
              <div style={{ flex: "1 1 160px", minWidth: 140, fontSize: 12, color: "var(--text-dim)" }}>{item.reason}</div>
              {item.status === "PENDING" ? (
                <div style={{ display: "flex", gap: 8 }}>
                  <button className="ip-btn ip-btn-danger ip-btn-sm" onClick={() => setModal({ action: "reject", item })}><Ban size={13} />Reject</button>
                  <button className="ip-btn ip-btn-primary ip-btn-sm" onClick={() => setModal({ action: "approve", item })}><Check size={13} />Approve</button>
                </div>
              ) : (
                <div style={{ textAlign: "right" }}>
                  <ApprovalStatusBadge status={item.status} />
                  {item.decided_by && <div style={{ fontSize: 11, color: "var(--text-faint)", marginTop: 4 }}>by {item.decided_by}</div>}
                </div>
              )}
            </div>
          ))}
        </div>
      )}

      <DecisionModal open={!!modal} action={modal?.action} item={modal?.item} onClose={() => setModal(null)} onConfirm={confirm} submitting={submitting} />
    </div>
  );
}

/* ---------------------------------- History ---------------------------------- */

function HistoryPage({ history, goto, setActiveResult, onRemove }) {
  const [query, setQuery] = useState("");
  const [riskFilter, setRiskFilter] = useState("ALL");
  const [recFilter, setRecFilter] = useState("ALL");
  const [pendingRemoval, setPendingRemoval] = useState(null); // _id awaiting confirmation

  const filtered = useMemo(() => {
    return history.filter(h => {
      const q = query.trim().toLowerCase();
      const matchesQuery = !q || (h.invoice?.vendor_name || "").toLowerCase().includes(q) || (h.invoice?.invoice_number || "").toLowerCase().includes(q);
      const matchesRisk = riskFilter === "ALL" || h.risk_level === riskFilter;
      const matchesRec = recFilter === "ALL" || h.recommendation === recFilter;
      return matchesQuery && matchesRisk && matchesRec;
    });
  }, [history, query, riskFilter, recFilter]);

  const requestRemove = (e, item) => {
    e.stopPropagation();
    setPendingRemoval(item._id);
  };

  const confirmRemove = (e, item) => {
    e.stopPropagation();
    setPendingRemoval(null);
    onRemove?.(item);
  };

  const cancelRemove = (e) => {
    e.stopPropagation();
    setPendingRemoval(null);
  };

  return (
    <div className="ip-fade-in">
      <TopBar title="History" subtitle="Every invoice this console has processed in the current session." />

      <div style={{ display: "flex", gap: 10, marginBottom: 16, flexWrap: "wrap" }}>
        <div style={{ position: "relative", flex: "1 1 240px" }}>
          <Search size={14} style={{ position: "absolute", left: 12, top: "50%", transform: "translateY(-50%)", color: "var(--text-faint)" }} />
          <input className="ip-input" style={{ paddingLeft: 34 }} placeholder="Search vendor or invoice number…" value={query} onChange={e => setQuery(e.target.value)} />
        </div>
        <select className="ip-input" style={{ width: 170 }} value={riskFilter} onChange={e => setRiskFilter(e.target.value)}>
          <option value="ALL">All risk levels</option>
          {Object.keys(RISK_STYLE).map(r => <option key={r} value={r}>{r}</option>)}
        </select>
        <select className="ip-input" style={{ width: 190 }} value={recFilter} onChange={e => setRecFilter(e.target.value)}>
          <option value="ALL">All recommendations</option>
          {Object.keys(REC_STYLE).map(r => <option key={r} value={r}>{REC_STYLE[r].label}</option>)}
        </select>
      </div>

      {history.length === 0 ? (
        <EmptyState Icon={Database} title="No history yet" body="Processed invoices will show up here for the rest of this session, with search and filters." action={<button className="ip-btn ip-btn-primary" onClick={() => goto("upload")}><UploadCloud size={14} />Upload an invoice</button>} />
      ) : filtered.length === 0 ? (
        <EmptyState Icon={Search} title="No matches" body="Try a different search term or clear the filters." />
      ) : (
        <div className="ip-card" style={{ overflow: "hidden" }}>
          <div className="ip-scrollbar" style={{ overflowX: "auto" }}>
            <table style={{ width: "100%", borderCollapse: "collapse", minWidth: 760 }}>
              <thead>
                <tr style={{ borderBottom: "1px solid var(--line)" }}>
                  {["Vendor", "Invoice #", "Date", "Amount", "Risk", "Recommendation", "Status", ""].map(h => (
                    <th key={h} style={{ textAlign: "left", fontSize: 11, fontWeight: 700, color: "var(--text-faint)", textTransform: "uppercase", letterSpacing: ".04em", padding: "12px 14px" }}>{h}</th>
                  ))}
                </tr>
              </thead>
              <tbody>
                {filtered.map(h => (
                  <tr key={h._id} className="ip-table-row" style={{ borderBottom: "1px solid var(--line-soft)", cursor: "pointer" }} onClick={() => { setActiveResult(h); goto("results"); }}>
                    <td style={{ padding: "12px 14px", fontSize: 13, fontWeight: 600 }}>{h.invoice?.vendor_name || "—"}</td>
                    <td style={{ padding: "12px 14px", fontSize: 12.5 }} className="ip-mono">{h.invoice?.invoice_number || "—"}</td>
                    <td style={{ padding: "12px 14px", fontSize: 12.5, color: "var(--text-dim)" }}>{fmtDateOnly(h.invoice?.invoice_date)}</td>
                    <td style={{ padding: "12px 14px", fontSize: 13, fontWeight: 600 }} className="ip-mono"><MoneyWithINR amount={h.invoice?.total_amount} currency={h.invoice?.currency} size={13} inline /></td>
                    <td style={{ padding: "12px 14px" }}><RiskBadge level={h.risk_level} /></td>
                    <td style={{ padding: "12px 14px" }}><RecBadge rec={h.recommendation} /></td>
                    <td style={{ padding: "12px 14px", fontSize: 12, color: "var(--text-dim)" }}>{h.queued_for_approval ? "Queued" : "Resolved"}</td>
                    <td style={{ padding: "12px 14px", display: "flex", alignItems: "center", gap: 6 }}>
                      {pendingRemoval === h._id ? (
                        <>
                          <button className="ip-btn ip-btn-sm" style={{ padding: "6px 9px", background: "rgba(240,82,110,.14)", borderColor: "rgba(240,82,110,.4)", color: "#f0526e" }} title="Confirm removal" onClick={(e) => confirmRemove(e, h)}>
                            Remove
                          </button>
                          <button className="ip-btn ip-btn-ghost ip-btn-sm" style={{ padding: "6px 9px" }} title="Cancel" onClick={cancelRemove}>
                            Cancel
                          </button>
                        </>
                      ) : (
                        <button
                          className="ip-btn ip-btn-ghost ip-btn-sm"
                          style={{ padding: 6 }}
                          title="Remove from history"
                          onClick={(e) => requestRemove(e, h)}
                        >
                          <Trash2 size={13} />
                        </button>
                      )}
                      <ChevronRight size={15} color="var(--text-faint)" />
                    </td>
                  </tr>
                ))}
              </tbody>
            </table>
          </div>
        </div>
      )}
    </div>
  );
}

/* ---------------------------------- AI Copilot (chat) ---------------------- */

function TypingDots() {
  return (
    <div style={{ display: "flex", gap: 4, padding: "2px 2px" }}>
      {[0, 1, 2].map(i => (
        <span key={i} className="ip-pulse" style={{
          width: 6, height: 6, borderRadius: 999, background: "var(--text-faint)",
          animationDelay: `${i * 0.18}s`,
        }} />
      ))}
    </div>
  );
}

function ChatBubble({ role, content, meta, pending }) {
  const isUser = role === "user";
  return (
    <div style={{ display: "flex", gap: 10, flexDirection: isUser ? "row-reverse" : "row", alignItems: "flex-start" }} className="ip-fade-in">
      <div style={{
        width: 30, height: 30, borderRadius: 9, flex: "none", display: "flex", alignItems: "center", justifyContent: "center",
        background: isUser ? "var(--bg-elev-3)" : "var(--grad-brand)", color: isUser ? "var(--text-dim)" : "#fff",
      }}>
        {isUser ? <User size={14} /> : <Bot size={15} />}
      </div>
      <div style={{ maxWidth: "78%", display: "flex", flexDirection: "column", gap: 4, alignItems: isUser ? "flex-end" : "flex-start" }}>
        <div className={cls("ip-card-2", isUser && "ip-chat-user")} style={{
          padding: "10px 13px", borderRadius: 14, borderTopLeftRadius: isUser ? 14 : 4, borderTopRightRadius: isUser ? 4 : 14,
          background: isUser ? "var(--grad-brand-soft)" : "var(--bg-elev-2)", fontSize: 13.5, color: "var(--text)",
        }}>
          {pending ? <TypingDots /> : (isUser ? <span style={{ whiteSpace: "pre-wrap", lineHeight: 1.55 }}>{content}</span> : <Markdown text={content} />)}
        </div>
        {!pending && meta && (
          <div className="ip-mono" style={{ fontSize: 10.5, color: "var(--text-faint)", padding: "0 4px" }}>
            {meta.provider ? `${meta.provider} · ` : ""}{meta.confidence != null ? `${Math.round(meta.confidence * 100)}% confidence` : ""}
          </div>
        )}
      </div>
    </div>
  );
}

function ChatPage({ history, activeResult, preselectId, apiCall, addToast, connected, threads, setThreads }) {
  const options = history.length ? history : (activeResult ? [activeResult] : []);
  const [selectedId, setSelectedId] = useState(preselectId || activeResult?.metadata?.execution_id || options[0]?.metadata?.execution_id || null);
  const [draft, setDraft] = useState("");
  const [sending, setSending] = useState(false);
  const [restoring, setRestoring] = useState(false);
  const scrollRef = useRef(null);
  const hydratedIds = useRef(new Set());

  useEffect(() => {
    if (preselectId) setSelectedId(preselectId);
  }, [preselectId]);

  useEffect(() => {
    if (!selectedId && options[0]) setSelectedId(options[0].metadata?.execution_id);
  }, [options, selectedId]);

  const selected = options.find(h => h.metadata?.execution_id === selectedId) || null;
  const execId = selected?.metadata?.execution_id;
  const messages = (execId && threads[execId]) || [];

  // Restore a saved conversation from the backend the first time an
  // invoice with no local messages yet is opened — e.g. after a page
  // reload, or when picking up a chat started in an earlier session.
  useEffect(() => {
    if (!execId || !connected) return;
    if (hydratedIds.current.has(execId)) return;
    if ((threads[execId] || []).length > 0) { hydratedIds.current.add(execId); return; }

    hydratedIds.current.add(execId);
    setRestoring(true);
    apiCall(`/chat/${execId}/history`)
      .then(res => {
        const saved = (res?.messages || []).map(m => ({
          id: uid(),
          role: m.role,
          content: m.content,
          meta: null,
        }));
        if (saved.length) {
          setThreads(prev => (prev[execId] || []).length ? prev : { ...prev, [execId]: saved });
        }
      })
      .catch(() => { /* No saved history yet, or backend unreachable — fine, start fresh. */ })
      .finally(() => setRestoring(false));
  }, [execId, connected, apiCall, setThreads]); // eslint-disable-line react-hooks/exhaustive-deps

  useEffect(() => {
    if (scrollRef.current) scrollRef.current.scrollTop = scrollRef.current.scrollHeight;
  }, [messages, sending]);

  const pushMessage = (id, msg) => {
    setThreads(prev => ({ ...prev, [id]: [...(prev[id] || []), msg] }));
  };

  const send = async (questionOverride) => {
    const question = (questionOverride ?? draft).trim();
    if (!question || !execId || sending) return;
    setDraft("");
    pushMessage(execId, { id: uid(), role: "user", content: question });
    setSending(true);
    try {
      let answer, provider, confidence;
      if (connected) {
        const res = await apiCall("/chat", {
          method: "POST",
          headers: { "Content-Type": "application/json" },
          body: JSON.stringify({ execution_id: execId, question }),
        });
        answer = res.answer; provider = res.provider; confidence = res.confidence;
      } else {
        await new Promise(r => setTimeout(r, 650 + Math.random() * 500));
        answer = buildMockChatAnswer(question, selected);
        provider = "demo-mode"; confidence = 0.86;
      }
      // The backend already saved this turn (question + answer) to its
      // own persistent history as part of handling /chat — the local
      // thread here just mirrors it for instant rendering.
      pushMessage(execId, { id: uid(), role: "assistant", content: answer, meta: { provider, confidence } });
    } catch (e) {
      addToast(`Copilot couldn't answer: ${e.message}`, "error");
      pushMessage(execId, { id: uid(), role: "assistant", content: "Sorry — I couldn't reach the reasoning engine for that question. Please try again.", meta: null });
    } finally {
      setSending(false);
    }
  };

  const clearThread = async () => {
    if (!execId) return;
    setThreads(prev => ({ ...prev, [execId]: [] }));
    if (connected) {
      try {
        await apiCall(`/chat/${execId}/history`, { method: "DELETE" });
      } catch (e) {
        addToast(`Couldn't clear saved history: ${e.message}`, "error");
      }
    }
  };

  if (options.length === 0) {
    return (
      <div className="ip-fade-in">
        <TopBar title="AI Copilot" subtitle="Ask natural-language questions about a processed invoice." />
        <EmptyState Icon={Bot} title="Nothing to ask about yet" body="Process an invoice first — the copilot answers questions grounded in that execution's extraction, risk, and policy results." />
      </div>
    );
  }

  return (
    <div className="ip-fade-in" style={{ display: "flex", flexDirection: "column", height: "calc(100vh - 86px)" }}>
      <TopBar
        title="AI Copilot"
        subtitle="Ask questions about a processed invoice — grounded in its actual pipeline results."
        right={!connected && <Badge color="#f5b942" bg="rgba(245,185,66,.12)" border="rgba(245,185,66,.35)">Demo mode</Badge>}
      />

      <div style={{ display: "grid", gridTemplateColumns: "260px 1fr", gap: 16, flex: 1, minHeight: 0 }} className="ip-chat-grid">
        <div className="ip-card ip-scrollbar" style={{ padding: 10, overflowY: "auto", display: "flex", flexDirection: "column", gap: 4 }}>
          <div style={{ fontSize: 11, fontWeight: 700, color: "var(--text-faint)", letterSpacing: ".04em", textTransform: "uppercase", padding: "6px 8px" }}>Invoices this session</div>
          {options.map(h => {
            const id = h.metadata?.execution_id;
            const active = id === execId;
            const count = (threads[id] || []).length;
            return (
              <div key={id || h._id} onClick={() => setSelectedId(id)} className="ip-table-row" style={{
                padding: "9px 10px", borderRadius: 10, cursor: "pointer",
                background: active ? "var(--grad-brand-soft)" : "transparent",
                border: active ? "1px solid rgba(91,110,232,.35)" : "1px solid transparent",
              }}>
                <div style={{ display: "flex", alignItems: "center", justifyContent: "space-between", gap: 6 }}>
                  <div style={{ fontSize: 13, fontWeight: 600, overflow: "hidden", textOverflow: "ellipsis", whiteSpace: "nowrap" }}>{h.invoice?.vendor_name || "Unknown vendor"}</div>
                  {count > 0 && <span className="ip-mono" style={{ fontSize: 10, color: "var(--text-faint)" }}>{count}</span>}
                </div>
                <div className="ip-mono" style={{ fontSize: 10.5, color: "var(--text-faint)", marginTop: 2 }}>{h.invoice?.invoice_number || "—"}</div>
                <div style={{ marginTop: 6 }}><RiskBadge level={h.risk_level} /></div>
              </div>
            );
          })}
        </div>

        <div className="ip-card" style={{ display: "flex", flexDirection: "column", minHeight: 0, overflow: "hidden" }}>
          {selected && (
            <div style={{ padding: "14px 18px", borderBottom: "1px solid var(--line)", display: "flex", alignItems: "center", gap: 12, flexWrap: "wrap" }}>
              <IconTile Icon={Bot} tone="violet" size={16} />
              <div style={{ flex: 1, minWidth: 160 }}>
                <div style={{ fontSize: 14, fontWeight: 700 }}>{selected.invoice?.vendor_name || "Unknown vendor"}</div>
                <div className="ip-mono" style={{ fontSize: 11, color: "var(--text-faint)" }}>{selected.invoice?.invoice_number || "—"} · {fmtMoney(selected.invoice?.total_amount, selected.invoice?.currency)}</div>
              </div>
              <RiskBadge level={selected.risk_level} />
              <RecBadge rec={selected.recommendation} />
              {restoring && <span className="ip-mono" style={{ fontSize: 10.5, color: "var(--text-faint)", display: "flex", alignItems: "center", gap: 5 }}><Loader2 size={11} className="ip-spin" />Restoring…</span>}
              {messages.length > 0 && (
                <button className="ip-btn ip-btn-ghost ip-btn-sm" onClick={clearThread}><Trash size={12} />Clear</button>
              )}
            </div>
          )}

          <div ref={scrollRef} className="ip-scrollbar" style={{ flex: 1, overflowY: "auto", padding: 18, display: "flex", flexDirection: "column", gap: 16 }}>
            {messages.length === 0 && (
              <div style={{ margin: "auto", textAlign: "center", maxWidth: 420 }}>
                <div style={{ width: 46, height: 46, borderRadius: 14, background: "var(--grad-brand-soft)", display: "flex", alignItems: "center", justifyContent: "center", margin: "0 auto 12px" }}>
                  <WandSparkles size={20} color="#5b6ee8" />
                </div>
                <div className="ip-display" style={{ fontSize: 15, fontWeight: 700 }}>Ask the copilot anything</div>
                <div style={{ fontSize: 12.5, color: "var(--text-dim)", marginTop: 6, marginBottom: 16 }}>It can explain the risk score, the policy decision, vendor history, or summarize the whole execution.</div>
                <div style={{ display: "flex", flexWrap: "wrap", gap: 8, justifyContent: "center" }}>
                  {SUGGESTED_QUESTIONS.map(q => (
                    <button key={q} className="ip-btn ip-btn-outline ip-btn-sm" onClick={() => send(q)} disabled={sending}>{q}</button>
                  ))}
                </div>
              </div>
            )}
            {messages.map(m => <ChatBubble key={m.id} role={m.role} content={m.content} meta={m.meta} />)}
            {sending && <ChatBubble role="assistant" pending />}
          </div>

          {messages.length > 0 && (
            <div style={{ padding: "10px 14px", borderTop: "1px solid var(--line-soft)", display: "flex", flexWrap: "wrap", gap: 6 }}>
              {SUGGESTED_QUESTIONS.slice(0, 4).map(q => (
                <button key={q} className="ip-btn ip-btn-outline ip-btn-sm" onClick={() => send(q)} disabled={sending}>{q}</button>
              ))}
            </div>
          )}

          <div style={{ padding: 14, borderTop: "1px solid var(--line)", display: "flex", gap: 10, alignItems: "flex-end" }}>
            <textarea
              className="ip-input ip-scrollbar"
              rows={1}
              placeholder={selected ? "Ask about this invoice…" : "Select an invoice first…"}
              value={draft}
              disabled={!selected || sending}
              onChange={e => setDraft(e.target.value)}
              onKeyDown={e => { if (e.key === "Enter" && !e.shiftKey) { e.preventDefault(); send(); } }}
              style={{ resize: "none", maxHeight: 120, fontFamily: "inherit" }}
            />
            <button className="ip-btn ip-btn-primary" style={{ flex: "none" }} disabled={!selected || !draft.trim() || sending} onClick={() => send()}>
              {sending ? <Loader2 size={15} className="ip-spin" /> : <Send size={15} />}
            </button>
          </div>
        </div>
      </div>
    </div>
  );
}

/* ---------------------------------- App ---------------------------------- */

export default function InvoicePilotAI() {
  const [theme, setTheme] = useState("dark");
  const [page, setPage] = useState("dashboard");
  const [apiBase, setApiBase] = useState("https://hackathon-3-t5fo.onrender.com");
  const [showSettings, setShowSettings] = useState(false);
  const [mobileOpen, setMobileOpen] = useState(false);
  const [health, setHealth] = useState({ connected: false, lastTested: false });
  const [testing, setTesting] = useState(false);

  const [history, setHistory] = useState(() => {
    try {
      const raw = localStorage.getItem(HISTORY_STORAGE_KEY);
      return raw ? JSON.parse(raw) : [];
    } catch { return []; }
  });
  const [activeResult, setActiveResult] = useState(null);
  const [chatThreads, setChatThreads] = useState(() => {
    try {
      const raw = localStorage.getItem(CHAT_THREADS_STORAGE_KEY);
      return raw ? JSON.parse(raw) : {};
    } catch { return {}; }
  });
  const [chatPreselectId, setChatPreselectId] = useState(null);
  const [approvals, setApprovals] = useState([]);
  const [pendingOnly, setPendingOnly] = useState(true);
  const [approvalsLoading, setApprovalsLoading] = useState(false);

  const [toasts, setToasts] = useState([]);
  const addToast = useCallback((message, type = "info") => {
    const id = uid();
    setToasts(t => [...t, { id, message, type }]);
    setTimeout(() => setToasts(t => t.filter(x => x.id !== id)), 5000);
  }, []);
  const dismissToast = (id) => setToasts(t => t.filter(x => x.id !== id));

  const apiCall = useApi(apiBase);

  // Persist processed invoices and copilot threads so old invoices
  // — and the ability to ask the copilot about them — survive a
  // page reload, not just this component's lifetime.
  useEffect(() => {
    try { localStorage.setItem(HISTORY_STORAGE_KEY, JSON.stringify(history)); } catch { /* storage unavailable */ }
  }, [history]);
  useEffect(() => {
    try { localStorage.setItem(CHAT_THREADS_STORAGE_KEY, JSON.stringify(chatThreads)); } catch { /* storage unavailable */ }
  }, [chatThreads]);

  const testConnection = useCallback(async (base) => {
    setTesting(true);
    const url = (base || apiBase).replace(/\/$/, "");
    try {
      const res = await fetch(`${url}/health`);
      const body = await res.json();
      if (!res.ok) throw new Error("Unhealthy response");
      setHealth({ connected: true, lastTested: true, app: body.application, version: body.version });
    } catch (e) {
      setHealth({ connected: false, lastTested: true, error: "Could not reach backend — check it's running and CORS allows this origin." });
    } finally {
      setTesting(false);
    }
  }, [apiBase]);

  useEffect(() => { testConnection(apiBase); }, [apiBase]); // eslint-disable-line react-hooks/exhaustive-deps
  useEffect(() => {
    const t = setInterval(() => testConnection(apiBase), 20000);
    return () => clearInterval(t);
  }, [apiBase, testConnection]);

  const refreshApprovals = useCallback(async () => {
    setApprovalsLoading(true);
    try {
      if (health.connected) {
        const res = await apiCall(`/approvals?pending_only=${pendingOnly}`);
        setApprovals(res.items || []);
      } else {
        setApprovals(buildMockApprovals());
      }
    } catch (e) {
      addToast(`Couldn't load approvals: ${e.message}`, "error");
      setApprovals([]);
    } finally {
      setApprovalsLoading(false);
    }
  }, [apiCall, health.connected, pendingOnly, addToast]);

  useEffect(() => { refreshApprovals(); }, [pendingOnly, health.connected]); // eslint-disable-line react-hooks/exhaustive-deps

  const goto = (p) => { setPage(p); setMobileOpen(false); };

  const askCopilot = (executionId) => {
    setChatPreselectId(executionId || null);
    goto("copilot");
  };

  const onUploadComplete = (enriched, viewOnly) => {
    if (viewOnly) { goto("results"); return; }
    if (!enriched) return;
    setHistory(h => [enriched, ...h]);
    setActiveResult(enriched);
  };

  const removeHistoryItem = useCallback(async (item) => {
    if (!item) return;
    const execId = item.metadata?.execution_id;
    setHistory(h => h.filter(x => x._id !== item._id));
    setActiveResult(prev => (prev?._id === item._id ? null : prev));
    if (execId) {
      setChatThreads(prev => {
        if (!(execId in prev)) return prev;
        const next = { ...prev };
        delete next[execId];
        return next;
      });
      if (health.connected) {
        try {
          await apiCall(`/executions/${execId}`, { method: "DELETE" });
        } catch {
          // The invoice is already gone from the UI — a failed
          // server-side cleanup call isn't worth bothering the user
          // about.
        }
      }
    }
  }, [apiCall, health.connected]);

  const onDecide = async (item, action, payload) => {
    if (health.connected) {
      const res = await apiCall(`/approvals/${item.execution_id}/${action}`, {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify(payload || {}),
      });
      setApprovals(prev => pendingOnly ? prev.filter(a => a.execution_id !== item.execution_id) : prev.map(a => a.execution_id === item.execution_id ? res : a));
    } else {
      setApprovals(prev => pendingOnly
        ? prev.filter(a => a.execution_id !== item.execution_id)
        : prev.map(a => a.execution_id === item.execution_id ? { ...a, status: action === "approve" ? "APPROVED" : "REJECTED", decided_by: payload?.decided_by || "You", decided_at: new Date().toISOString(), decision_notes: payload?.notes || null } : a));
    }
  };

  const pendingCount = approvals.filter(a => a.status === "PENDING").length;

  return (
    <div className="ip-root" data-theme={theme} style={{ display: "flex", minHeight: "100vh" }}>
      <style>{STYLE}</style>
      <div className="ip-bg-grid" />
      <style>{`
        @media (max-width: 880px) {
          .ip-dashboard-grid { grid-template-columns: 1fr !important; }
          .ip-chat-grid { grid-template-columns: 1fr !important; }
          .ip-sidebar { position: fixed !important; left: 0; top: 0; transform: translateX(-100%); transition: transform .22s ease; box-shadow: 0 0 0 2000px rgba(4,5,10,.001); }
          .ip-sidebar.open { transform: translateX(0); z-index: 45; }
          .ip-mobile-overlay { display: block !important; }
          .ip-mobile-topbar { display: flex !important; }
          main { padding-top: 74px !important; }
        }
      `}</style>

      <div className="ip-mobile-topbar" style={{ display: "none", position: "fixed", top: 0, left: 0, right: 0, height: 58, zIndex: 41, alignItems: "center", gap: 10, padding: "0 14px", background: "var(--bg-elev-1)", borderBottom: "1px solid var(--line)" }}>
        <button className="ip-btn ip-btn-ghost ip-btn-sm" style={{ padding: 7 }} onClick={() => setMobileOpen(true)}><Menu size={16} /></button>
        <div style={{ width: 26, height: 26, borderRadius: 8, background: "var(--grad-brand)", display: "flex", alignItems: "center", justifyContent: "center" }}><Zap size={14} color="#fff" /></div>
        <div className="ip-display" style={{ fontSize: 14, fontWeight: 700 }}>InvoicePilot</div>
      </div>

      <Sidebar page={page} setPage={goto} theme={theme} setTheme={setTheme} health={health} pendingCount={pendingCount} apiBase={apiBase} setShowSettings={setShowSettings} mobileOpen={mobileOpen} setMobileOpen={setMobileOpen} />

      <main style={{ flex: 1, padding: "26px 30px 60px", position: "relative", minWidth: 0 }}>
        {page === "dashboard" && <Dashboard history={history} approvals={approvals} health={health} goto={goto} setShowSettings={setShowSettings} />}
        {page === "upload" && <UploadPage apiCall={apiCall} onComplete={onUploadComplete} addToast={addToast} connected={health.connected} />}
        {page === "results" && <ResultsPage result={activeResult} goto={goto} apiCall={apiCall} addToast={addToast} connected={health.connected} onAskCopilot={askCopilot} />}
        {page === "copilot" && <ChatPage history={history} activeResult={activeResult} preselectId={chatPreselectId} apiCall={apiCall} addToast={addToast} connected={health.connected} threads={chatThreads} setThreads={setChatThreads} />}
        {page === "approvals" && <ApprovalsPage approvals={approvals} loading={approvalsLoading} pendingOnly={pendingOnly} setPendingOnly={setPendingOnly} onRefresh={refreshApprovals} onDecide={onDecide} addToast={addToast} connected={health.connected} />}
        {page === "history" && <HistoryPage history={history} goto={goto} setActiveResult={setActiveResult} onRemove={removeHistoryItem} />}
      </main>

      <SettingsModal open={showSettings} onClose={() => setShowSettings(false)} apiBase={apiBase} setApiBase={setApiBase} onTestConnection={testConnection} testing={testing} health={health} />
      <Toast toasts={toasts} onDismiss={dismissToast} />
    </div>
  );
}
