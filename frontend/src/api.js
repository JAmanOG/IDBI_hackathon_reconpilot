async function req(path, options = {}) {
  const res = await fetch(path, {
    headers: { 'Content-Type': 'application/json' },
    ...options,
  })
  if (!res.ok) {
    const body = await res.json().catch(() => ({}))
    throw new Error(body.detail || `${res.status} ${res.statusText}`)
  }
  return res.json()
}

export const api = {
  generateData: (clean = 50000) => req('/api/generate-data', { method: 'POST', body: JSON.stringify({ clean }) }),
  runRecon: () => req('/api/recon/run', { method: 'POST' }),
  summary: () => req('/api/summary'),
  breaks: (params = {}) => {
    const q = new URLSearchParams(Object.entries(params).filter(([, v]) => v)).toString()
    return req(`/api/breaks${q ? `?${q}` : ''}`)
  },
  breakDetail: (id) => req(`/api/breaks/${id}`),
  investigate: (id) => req(`/api/breaks/${id}/investigate`, { method: 'POST' }),
  decide: (id, decision, reason = '') =>
    req(`/api/breaks/${id}/decision`, { method: 'POST', body: JSON.stringify({ decision, reason }) }),
  rules: () => req('/api/rules'),
  rulesNL: (instruction) => req('/api/rules/nl', { method: 'POST', body: JSON.stringify({ instruction }) }),
  promoteRules: (rules) => req('/api/rules/promote', { method: 'POST', body: JSON.stringify({ rules }) }),
}

export const inr = (n) =>
  new Intl.NumberFormat('en-IN', { style: 'currency', currency: 'INR', maximumFractionDigits: 0 }).format(n)

export const paise = (p) =>
  new Intl.NumberFormat('en-IN', { style: 'currency', currency: 'INR', minimumFractionDigits: 2 }).format(p / 100)

export const CLASS_LABELS = {
  TIMEOUT_DEBIT_NO_CREDIT: 'Timeout — debit w/o credit',
  MISSING_IN_CBS: 'Missing in CBS',
  MISSING_AT_NPCI: 'Orphan CBS posting',
  AMOUNT_MISMATCH: 'Amount mismatch',
  DUPLICATE_CBS_POSTING: 'Duplicate CBS posting',
  CROSS_CYCLE: 'Cross-cycle drift',
}
