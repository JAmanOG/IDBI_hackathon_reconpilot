import React, { useCallback, useEffect, useState } from 'react'
import { api, inr, paise, CLASS_LABELS } from './api.js'

const Chip = ({ kind, children }) => (
  <span className={`chip ${kind}`}><span className="dot" aria-hidden="true" />{children}</span>
)

function useToast() {
  const [msg, setMsg] = useState(null)
  const toast = useCallback((m) => {
    setMsg(m)
    setTimeout(() => setMsg(null), 3500)
  }, [])
  return [msg, toast]
}

/* ---------------------------------------------------------------- dashboard */

function Dashboard({ summary, onNavigate }) {
  if (!summary?.run) {
    return (
      <div className="empty">
        No reconciliation run yet.<br />
        Use <b>Generate files</b> then <b>Run recon</b> above — three settlement files, one click.
      </div>
    )
  }
  const k = summary.kpis
  const classes = Object.entries(summary.by_class || {}).sort((a, b) => b[1] - a[1])
  const maxN = Math.max(1, ...classes.map(([, n]) => n))
  return (
    <>
      <div className="tiles">
        <div className="tile">
          <span className="label">Auto-match rate</span>
          <span className="value">{k.auto_match_rate}%</span>
          <span className="sub">{k.total_rrns?.toLocaleString('en-IN')} RRNs in {k.elapsed_ms} ms</span>
        </div>
        <div className="tile">
          <span className="label">Open breaks</span>
          <span className="value">{k.open_breaks}</span>
          <span className="sub">{paise(k.amount_at_risk_inr * 100)} at risk</span>
        </div>
        <div className="tile">
          <span className="label">RBI TAT penalty exposure</span>
          <span className="value">{inr(k.penalty_exposure_inr)}</span>
          <span className="sub accrual">accruing {inr(k.penalty_accruing_per_day_inr)}/day while open</span>
        </div>
        <div className="tile">
          <span className="label">Desk time saved</span>
          <span className="value">{k.minutes_saved} min</span>
          <span className="sub">{k.fte_saved} FTE-days · 25 → 4 min per break</span>
        </div>
      </div>
      <div className="grid-2">
        <section className="panel">
          <h2>Breaks by class</h2>
          <div className="bars">
            {classes.map(([cls, n]) => (
              <div className="bar-row" key={cls}>
                <span className="name" title={cls}>{CLASS_LABELS[cls] || cls}</span>
                <span className="bar-track"><span className="bar-fill" style={{ width: `${(n / maxN) * 100}%` }} /></span>
                <span className="n">{n}</span>
              </div>
            ))}
          </div>
        </section>
        <section className="panel">
          <h2>Queue status</h2>
          <div className="filters" style={{ marginBottom: 0 }}>
            {Object.entries(summary.by_status || {}).map(([st, n]) => (
              <Chip key={st} kind={`st-${st}`}>{st} · {n}</Chip>
            ))}
          </div>
          <p className="hint" style={{ marginTop: 14 }}>
            Matching rules v{summary.run.rules?.version} — amount tolerance {summary.run.rules?.amount_tolerance_paise} paise,
            cycle drift {summary.run.rules?.cycle_drift_tolerance}. Rules are authored in plain English in the Rules tab.
          </p>
          <button className="btn" style={{ marginTop: 8 }} onClick={() => onNavigate('queue')}>
            Open exceptions queue →
          </button>
        </section>
      </div>
    </>
  )
}

/* ---------------------------------------------------------------- queue */

function Queue({ onOpen }) {
  const [rows, setRows] = useState(null)
  const [cls, setCls] = useState('')
  const [status, setStatus] = useState('')

  useEffect(() => {
    api.breaks({ break_class: cls, status }).then(setRows).catch(() => setRows([]))
  }, [cls, status])

  if (!rows) return <div className="empty">Loading…</div>
  return (
    <section className="panel">
      <h2>Exceptions queue — sorted by severity × exposure</h2>
      <div className="filters">
        <select value={cls} onChange={(e) => setCls(e.target.value)} aria-label="Filter by break class">
          <option value="">All classes</option>
          {Object.keys(CLASS_LABELS).map((c) => <option key={c} value={c}>{CLASS_LABELS[c]}</option>)}
        </select>
        <select value={status} onChange={(e) => setStatus(e.target.value)} aria-label="Filter by status">
          <option value="">All statuses</option>
          {['OPEN', 'INVESTIGATING', 'PROPOSED', 'APPROVED', 'REJECTED'].map((s) => <option key={s}>{s}</option>)}
        </select>
      </div>
      {rows.length === 0 ? <div className="empty">No breaks match this filter.</div> : (
        <div style={{ overflowX: 'auto' }}>
          <table className="queue">
            <thead>
              <tr>
                <th>Severity</th><th>Class</th><th>RRN</th>
                <th className="right">Amount</th><th className="right">Age</th>
                <th className="right">TAT clock</th><th>Status</th>
              </tr>
            </thead>
            <tbody>
              {rows.map((b) => (
                <tr key={b.id} className="row" onClick={() => onOpen(b.id)}>
                  <td><Chip kind={`sev-${b.severity}`}>{b.severity}</Chip></td>
                  <td>{CLASS_LABELS[b.break_class] || b.break_class}</td>
                  <td className="rrn">{b.rrn}</td>
                  <td className="right">{paise(b.amount_paise)}</td>
                  <td className="right">{b.age_days}d</td>
                  <td className="right">
                    {b.tat?.breached
                      ? <span className="tat-clock">{inr(b.tat.compensation_accrued_inr)} ↗</span>
                      : <span className="hint">—</span>}
                  </td>
                  <td><Chip kind={`st-${b.status}`}>{b.status}</Chip></td>
                </tr>
              ))}
            </tbody>
          </table>
        </div>
      )}
    </section>
  )
}

/* ---------------------------------------------------------------- detail */

const EvCard = ({ title, rows, none }) => (
  <div className="ev-card">
    <h3>{title}</h3>
    {(!rows || rows.length === 0) ? <div className="none">{none}</div> : rows.map((r, i) => (
      <div className="kv" key={i} style={i > 0 ? { borderTop: '1px dashed var(--grid)' } : {}}>
        {Object.entries(r).map(([k, v]) => (
          <div key={k}><span className="k">{k}</span><span className="v">{String(v)}</span></div>
        ))}
      </div>
    ))}
  </div>
)

function pickFields(leg) {
  if (!leg) return leg
  const keep = ['txn_id', 'amount_paise', 'dr_cr', 'resp_code', 'status', 'cycle', 'txn_date',
    'payer_vpa', 'payee_vpa', 'account_no', 'narration', 'raw_ref']
  return Object.fromEntries(keep.filter((k) => leg[k] !== '' && leg[k] != null).map((k) => [k, leg[k]]))
}

function Detail({ id, onBack, toast, refresh }) {
  const [brk, setBrk] = useState(null)
  const [busy, setBusy] = useState(false)

  const load = useCallback(() => api.breakDetail(id).then(setBrk), [id])
  useEffect(() => { load() }, [load])

  if (!brk) return <div className="empty">Loading…</div>
  const res = brk.proposal?.resolution
  const voucher = brk.proposal?.voucher
  const udir = brk.proposal?.udir_action

  const investigate = async () => {
    setBusy(true)
    try {
      await api.investigate(id)
      await load()
      toast('Agent proposed a resolution — review below')
    } catch (e) { toast(`Investigation failed: ${e.message}`) }
    setBusy(false)
  }
  const decide = async (d) => {
    setBusy(true)
    try {
      await api.decide(id, d)
      await load(); refresh()
      toast(d === 'approve' ? 'Approved — voucher and UDIR action released to maker-checker' : 'Rejected — returned to queue')
    } catch (e) { toast(e.message) }
    setBusy(false)
  }

  return (
    <>
      <div className="detail-head">
        <button className="btn sm" onClick={onBack}>← Queue</button>
        <span className="rrn">RRN {brk.rrn}</span>
        <Chip kind={`sev-${brk.severity}`}>{brk.severity}</Chip>
        <Chip kind={`st-${brk.status}`}>{brk.status}</Chip>
        <span className="hint">{CLASS_LABELS[brk.break_class]} · {paise(brk.amount_paise)} · {brk.txn_date} · {brk.age_days}d old</span>
      </div>

      <section className="panel">
        <h2>3-way evidence</h2>
        <div className="evidence">
          <EvCard title="NPCI settlement file" rows={(brk.legs?.NPCI || []).map(pickFields)} none="NO RECORD AT NPCI" />
          <EvCard title="UPI switch log" rows={(brk.legs?.SWITCH || []).map(pickFields)} none="NO SWITCH ENTRY" />
          <EvCard title="Finacle CBS" rows={(brk.legs?.CBS || []).map(pickFields)} none="NO CBS POSTING" />
        </div>
        <p className="hint" style={{ marginTop: 10 }}>{brk.note}</p>
        {brk.tat?.breached && (
          <p className="tat-clock" style={{ margin: '6px 0 0' }}>
            RBI T+1 breached by {brk.tat.days_past_tat} day(s) — {inr(brk.tat.compensation_accrued_inr)} compensation accrued, +₹100/day until resolved.
          </p>
        )}
      </section>

      {brk.status === 'OPEN' || brk.status === 'INVESTIGATING' ? (
        <section className="panel">
          <h2>Agent investigation</h2>
          <button className="btn primary" disabled={busy} onClick={investigate}>
            {busy ? <><span className="spin">◌</span> Investigating…</> : '▶ Investigate with agent'}
          </button>
          <p className="hint" style={{ marginTop: 8 }}>
            The agent pulls all three records, checks precedent, computes the TAT position, drafts the
            voucher + UDIR action, and submits a resolution — every step lands in the audit log. You approve; it never posts.
          </p>
        </section>
      ) : null}

      {res && (
        <section className="panel">
          <h2>Proposed resolution — awaiting supervisor {brk.proposal.mode === 'mock' ? '(offline agent)' : ''}</h2>
          <div className="proposal">
            <div className="row">
              <Chip kind="st-PROPOSED">impact: {res.customer_impact}</Chip>
              <Chip kind="st-PROPOSED">confidence: {res.confidence}</Chip>
              {udir && <Chip kind="st-PROPOSED">UDIR: {udir.action}</Chip>}
              {res.compensation_due_inr > 0 && <span className="chip comp">compensation {inr(res.compensation_due_inr)}</span>}
            </div>
            <p className="rc"><b>Root cause:</b> {res.root_cause}</p>
            <p className="rc"><b>Recommended:</b> {res.recommended_action}</p>
            {voucher && (
              <pre className="rules-json">{JSON.stringify(
                { voucher_type: voucher.voucher_type, dr: voucher.dr_account, cr: voucher.cr_account, amount_paise: voucher.amount_paise, narration: voucher.narration },
                null, 2)}</pre>
            )}
            {brk.status === 'PROPOSED' && (
              <div className="actions" style={{ marginTop: 12 }}>
                <button className="btn good" disabled={busy} onClick={() => decide('approve')}>✓ Approve</button>
                <button className="btn danger" disabled={busy} onClick={() => decide('reject')}>✗ Reject</button>
              </div>
            )}
          </div>
        </section>
      )}

      {brk.agent_trace && (
        <section className="panel">
          <h2>Reasoning trace ({brk.agent_trace.length} steps)</h2>
          <div className="trace">
            {brk.agent_trace.map((s, i) =>
              s.step === 'narrative' ? (
                <div className="step narrative" key={i}><span className="text">{s.text}</span></div>
              ) : (
                <details className="step" key={i}>
                  <summary><span className="tool-name">{s.tool}</span> <span className="hint">{JSON.stringify(s.input)}</span></summary>
                  <pre>{JSON.stringify(s.output, null, 2)}</pre>
                </details>
              ))}
          </div>
        </section>
      )}

      <section className="panel">
        <h2>Audit log</h2>
        <div className="audit">
          {brk.audit.map((a, i) => (
            <div key={i}>
              <span className="at">{a.at.replace('T', ' ').replace('+00:00', 'Z')}</span>
              <span className="actor">{a.actor}</span>
              <span>{a.action}</span>
            </div>
          ))}
        </div>
      </section>
    </>
  )
}

/* ---------------------------------------------------------------- rules lab */

const EXAMPLES = [
  'Tolerate 1-cycle date drift between NPCI and CBS',
  'Set amount tolerance of 100 paise',
  'Strict matching — no drift, zero tolerance',
]

function RulesLab({ toast, refresh }) {
  const [rules, setRules] = useState(null)
  const [instruction, setInstruction] = useState('')
  const [proposal, setProposal] = useState(null)
  const [busy, setBusy] = useState(false)

  useEffect(() => { api.rules().then(setRules) }, [])

  const propose = async () => {
    if (!instruction.trim()) return
    setBusy(true)
    try { setProposal(await api.rulesNL(instruction)) }
    catch (e) { toast(e.message) }
    setBusy(false)
  }
  const promote = async () => {
    setBusy(true)
    try {
      const r = await api.promoteRules(proposal.proposed_rules)
      setRules(r.promoted); setProposal(null)
      await api.runRecon(); refresh()
      toast('Rules promoted and recon re-run with the new ruleset')
    } catch (e) { toast(e.message) }
    setBusy(false)
  }

  return (
    <div className="grid-2">
      <section className="panel">
        <h2>Active matching rules {rules ? `— v${rules.version}` : ''}</h2>
        {rules && <pre className="rules-json">{JSON.stringify(rules, null, 2)}</pre>}
        <p className="hint" style={{ marginTop: 10 }}>
          Changing recon rules normally means a vendor change-request. Here the ops manager types the
          policy in plain English; every proposal is dry-run against today's files before promotion.
        </p>
      </section>
      <section className="panel">
        <h2>Author a rule in plain English</h2>
        <div className="nl-input">
          <input
            value={instruction}
            placeholder='e.g. "Tolerate 1-cycle date drift between NPCI and CBS"'
            onChange={(e) => setInstruction(e.target.value)}
            onKeyDown={(e) => e.key === 'Enter' && propose()}
          />
          <button className="btn primary" disabled={busy} onClick={propose}>{busy ? '…' : 'Dry run'}</button>
        </div>
        <div className="suggestions">
          {EXAMPLES.map((s) => <button key={s} onClick={() => setInstruction(s)}>{s}</button>)}
        </div>
        {proposal && (
          <>
            <p style={{ marginBottom: 4 }}><b>Interpreted:</b> {proposal.explanation} <span className="hint">({proposal.mode} mode)</span></p>
            <pre className="rules-json">{JSON.stringify(proposal.proposed_rules, null, 2)}</pre>
            <div className="dry-run">
              <span>Dry run on today's files:</span>
              <span className="big">{proposal.dry_run.breaks_before}</span>
              <span className="arrow">→</span>
              <span className="big" style={{ color: proposal.dry_run.breaks_after < proposal.dry_run.breaks_before ? 'var(--good-text)' : 'var(--ink)' }}>
                {proposal.dry_run.breaks_after}
              </span>
              <span>breaks</span>
            </div>
            <button className="btn good" disabled={busy} onClick={promote}>Promote ruleset + re-run recon</button>
          </>
        )}
      </section>
    </div>
  )
}

/* ---------------------------------------------------------------- app shell */

function initialRoute() {
  const h = window.location.hash
  const m = h.match(/^#break\/(\d+)/)
  if (m) return { view: 'queue', detailId: Number(m[1]) }
  if (h === '#queue' || h === '#rules') return { view: h.slice(1), detailId: null }
  return { view: 'dashboard', detailId: null }
}

export default function App() {
  const [view, setView] = useState(initialRoute().view)
  const [detailId, setDetailId] = useState(initialRoute().detailId)
  const [summary, setSummary] = useState(null)
  const [busy, setBusy] = useState(false)
  const [toastMsg, toast] = useToast()

  const refresh = useCallback(() => { api.summary().then(setSummary).catch(() => {}) }, [])
  useEffect(() => { refresh() }, [refresh])

  const generate = async () => {
    setBusy(true)
    try {
      const r = await api.generateData(50000)
      toast(`Generated ${r.generated.npci.toLocaleString('en-IN')} NPCI rows across 3 files`)
    } catch (e) { toast(e.message) }
    setBusy(false)
  }
  const run = async () => {
    setBusy(true)
    try {
      const r = await api.runRecon()
      refresh()
      toast(`Matched ${r.auto_match_rate}% of ${r.stats.total_rrns.toLocaleString('en-IN')} RRNs in ${r.elapsed_ms} ms — ${r.breaks} breaks to the desk`)
    } catch (e) { toast(e.message) }
    setBusy(false)
  }

  return (
    <div className="shell">
      <header className="top">
        <div className="brand">
          <h1>ReconPilot</h1>
          <span>UPI 3-way reconciliation · agentic exceptions desk</span>
        </div>
        <button className="btn sm" disabled={busy} onClick={generate}>Generate files</button>
        <button className="btn sm primary" disabled={busy} onClick={run}>{busy ? 'Working…' : 'Run recon'}</button>
        <nav className="tabs" aria-label="Views">
          {[['dashboard', 'Dashboard'], ['queue', 'Exceptions'], ['rules', 'Rules']].map(([v, label]) => (
            <button key={v} className={view === v && !detailId ? 'active' : ''}
              onClick={() => { setView(v); setDetailId(null) }}>{label}</button>
          ))}
        </nav>
      </header>

      {detailId ? (
        <Detail id={detailId} onBack={() => setDetailId(null)} toast={toast} refresh={refresh} />
      ) : view === 'dashboard' ? (
        <Dashboard summary={summary} onNavigate={setView} />
      ) : view === 'queue' ? (
        <Queue onOpen={setDetailId} />
      ) : (
        <RulesLab toast={toast} refresh={refresh} />
      )}

      {toastMsg && <div className="toast" role="status">{toastMsg}</div>}
    </div>
  )
}
