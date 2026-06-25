#!/usr/bin/env node
/**
 * Claude Account Switcher — standalone mini app
 * Zero dependencies. Reproduces NeoBoard's account switcher UI.
 * Reads/writes ~/.neoboard/accounts.json + ~/.claude/.credentials.json
 */

const http = require('http')
const os = require('os')
const path = require('path')
const fs = require('fs')
const crypto = require('crypto')
const { execFile } = require('child_process')

const PORT = parseInt(process.env.PORT || '3847', 10)
const DATA_DIR = path.join(os.homedir(), '.neoboard')
const ACCOUNTS_FILE = path.join(DATA_DIR, 'accounts.json')
const CREDENTIALS_FILE = path.join(os.homedir(), '.claude', '.credentials.json')
const OAUTH_TOKEN_URL = 'https://platform.claude.com/v1/oauth/token'
const OAUTH_CLIENT_ID = '9d1c250a-e61b-44d9-88ed-5944d1962f5e'
const CACHE_TTL = 45

// ── Accounts service ──────────────────────────────────────────────

function loadAccounts() {
    try {
        if (fs.existsSync(ACCOUNTS_FILE)) {
            const data = JSON.parse(fs.readFileSync(ACCOUNTS_FILE, 'utf-8'))
            return { accounts: Array.isArray(data.accounts) ? data.accounts : [], activeId: data.activeId || null }
        }
    } catch {}
    return { accounts: [], activeId: null }
}

function saveAccounts(data) {
    if (!fs.existsSync(DATA_DIR)) fs.mkdirSync(DATA_DIR, { recursive: true })
    fs.writeFileSync(ACCOUNTS_FILE, JSON.stringify(data, null, 2), 'utf-8')
}

function readFullCredentials() {
    try { return fs.existsSync(CREDENTIALS_FILE) ? JSON.parse(fs.readFileSync(CREDENTIALS_FILE, 'utf-8')) : null } catch { return null }
}

function writeCredentials(creds) {
    const dir = path.dirname(CREDENTIALS_FILE)
    if (!fs.existsSync(dir)) fs.mkdirSync(dir, { recursive: true })
    fs.writeFileSync(CREDENTIALS_FILE, JSON.stringify(creds, null, 2), 'utf-8')
}

function getToken(acc) {
    return acc?.credentials?.claudeAiOauth?.accessToken || acc?.token || null
}

function detectActive() {
    const { accounts } = loadAccounts()
    const creds = readFullCredentials()
    const token = creds?.claudeAiOauth?.accessToken
    if (!token || !accounts.length) return null
    const m = accounts.find(a => getToken(a) === token)
    return m ? m.id : null
}

function getAccountsList() {
    const data = loadAccounts()
    const realId = detectActive()
    if (realId && realId !== data.activeId) { data.activeId = realId; saveAccounts(data) }
    return {
        accounts: data.accounts.map(a => ({ id: a.id, name: a.name, source: a.source || 'local', sourceUsername: a.sourceUsername || null })),
        activeId: data.activeId,
    }
}

function refreshActiveCredentials() {
    const data = loadAccounts()
    if (!data.activeId) return
    const active = data.accounts.find(a => a.id === data.activeId)
    if (!active) return
    const fresh = readFullCredentials()
    if (fresh?.claudeAiOauth) { active.credentials = fresh; saveAccounts(data) }
}

function isExpired(acc) {
    const oauth = acc?.credentials?.claudeAiOauth
    if (!oauth?.expiresAt) return false
    return Date.now() > oauth.expiresAt
}

function refreshOAuth(acc) {
    const oauth = acc?.credentials?.claudeAiOauth
    if (!oauth?.refreshToken) return Promise.resolve({ ok: false, error: 'No refreshToken' })
    const payload = JSON.stringify({ grant_type: 'refresh_token', refresh_token: oauth.refreshToken, client_id: OAUTH_CLIENT_ID, scope: (oauth.scopes || []).join(' ') })
    const args = ['-s', '-X', 'POST', OAUTH_TOKEN_URL, '-H', 'Content-Type: application/json', '-d', payload]
    return new Promise(resolve => {
        const opts = { timeout: 15000, encoding: 'utf-8' }
        if (process.platform === 'win32') opts.windowsHide = true
        execFile('curl', args, opts, (err, stdout) => {
            if (err) return resolve({ ok: false, error: String(err) })
            try {
                const d = JSON.parse(stdout)
                if (!d.access_token) return resolve({ ok: false, error: d.error || 'No access_token' })
                resolve({ ok: true, credentials: { ...acc.credentials, claudeAiOauth: { ...oauth, accessToken: d.access_token, refreshToken: d.refresh_token || oauth.refreshToken, expiresAt: Date.now() + (d.expires_in || 3600) * 1000 } } })
            } catch (e) { resolve({ ok: false, error: String(e) }) }
        })
    })
}

async function switchAccount(accountId) {
    const data = loadAccounts()
    const acc = data.accounts.find(a => a.id === accountId)
    if (!acc) return { ok: false, error: 'Compte non trouvé' }
    let refreshed = false
    if (isExpired(acc)) {
        const r = await refreshOAuth(acc)
        if (r.ok) { acc.credentials = r.credentials; saveAccounts(data); refreshed = true }
        else { if (acc.credentials) writeCredentials(acc.credentials); data.activeId = accountId; saveAccounts(data); return { ok: true, name: acc.name, refreshed: false } }
    }
    if (acc.credentials) writeCredentials(acc.credentials)
    else if (acc.token) writeCredentials({ claudeAiOauth: { accessToken: acc.token } })
    data.activeId = accountId; saveAccounts(data)
    return { ok: true, name: acc.name, refreshed }
}

function addAccountFromCreds(name, credentials) {
    if (!name) return { ok: false, error: 'Nom requis' }
    const token = credentials?.claudeAiOauth?.accessToken
    if (!token) return { ok: false, error: 'Credentials invalides' }
    const data = loadAccounts()
    if (data.accounts.some(a => getToken(a) === token)) return { ok: false, error: 'Ce compte existe déjà' }
    const acc = { id: crypto.randomUUID(), name: name.trim(), credentials }
    data.accounts.push(acc)
    if (!data.activeId) data.activeId = acc.id
    saveAccounts(data)
    return { ok: true, account: { id: acc.id, name: acc.name } }
}

function importCurrentAccount(name) {
    const creds = readFullCredentials()
    if (!creds?.claudeAiOauth) return { ok: false, error: 'Aucun token dans .credentials.json' }
    return addAccountFromCreds(name || 'Compte actuel', creds)
}

function importFromCredJson(name, jsonStr) {
    if (!name) return { ok: false, error: 'Nom requis' }
    let creds; try { creds = JSON.parse(jsonStr) } catch { return { ok: false, error: 'JSON invalide' } }
    if (!creds?.claudeAiOauth?.accessToken) return { ok: false, error: 'Pas de claudeAiOauth.accessToken' }
    return addAccountFromCreds(name, creds)
}

function removeAccount(accountId) {
    const data = loadAccounts()
    const idx = data.accounts.findIndex(a => a.id === accountId)
    if (idx === -1) return { ok: false, error: 'Compte non trouvé' }
    data.accounts.splice(idx, 1)
    if (data.activeId === accountId) {
        if (data.accounts.length > 0) { data.activeId = data.accounts[0].id; writeCredentials(data.accounts[0].credentials) }
        else data.activeId = null
    }
    saveAccounts(data)
    return { ok: true }
}

function renameAccount(accountId, newName) {
    const data = loadAccounts()
    const acc = data.accounts.find(a => a.id === accountId)
    if (!acc) return { ok: false, error: 'Compte non trouvé' }
    acc.name = newName.trim(); saveAccounts(data)
    return { ok: true }
}

// ── Quota service ─────────────────────────────────────────────────

function format5h(ts) { if (!ts) return ''; const d = new Date(ts * 1000); return String(d.getHours()).padStart(2, '0') + 'h' + String(d.getMinutes()).padStart(2, '0') }
function format7d(ts) { if (!ts) return ''; const d = new Date(ts * 1000); const days = ['dim','lun','mar','mer','jeu','ven','sam']; return days[d.getDay()] + ' ' + String(d.getDate()).padStart(2,'0') + '/' + String(d.getMonth()+1).padStart(2,'0') + ' ' + String(d.getHours()).padStart(2,'0') + 'h' }

function parseHeaders(headers) {
    const result = { quotas: [], fetchedAt: new Date().toISOString(), error: null }
    const m5 = headers.match(/unified-5h-utilization:\s*([\d.]+)/), m5r = headers.match(/unified-5h-reset:\s*(\d+)/)
    if (m5) result.quotas.push({ label: 'Session (5h)', percent: Math.round(parseFloat(m5[1]) * 100), resets: format5h(m5r ? parseInt(m5r[1]) : 0) })
    const m7 = headers.match(/unified-7d-utilization:\s*([\d.]+)/), m7r = headers.match(/unified-7d-reset:\s*(\d+)/)
    if (m7) result.quotas.push({ label: 'Semaine (7j)', percent: Math.round(parseFloat(m7[1]) * 100), resets: format7d(m7r ? parseInt(m7r[1]) : 0) })
    return result
}

function fetchQuotaAsync(token) {
    const nullDev = process.platform === 'win32' ? 'NUL' : '/dev/null'
    const args = ['-s', '-D', '-', '-o', nullDev, 'https://api.anthropic.com/v1/messages', '-H', 'Authorization: Bearer ' + token, '-H', 'anthropic-version: 2023-06-01', '-H', 'anthropic-beta: oauth-2025-04-20', '-H', 'content-type: application/json', '-d', '{"model":"claude-haiku-4-5-20251001","max_tokens":1,"messages":[{"role":"user","content":"hi"}]}']
    return new Promise(resolve => {
        const opts = { timeout: 15000, encoding: 'utf-8' }
        if (process.platform === 'win32') opts.windowsHide = true
        execFile('curl', args, opts, (err, stdout) => {
            if (err) return resolve({ quotas: [], error: String(err) })
            resolve(parseHeaders(stdout))
        })
    })
}

async function fetchAllQuotas() {
    refreshActiveCredentials()
    const data = loadAccounts()
    const tasks = data.accounts.map(async acc => {
        const cacheFile = path.join(DATA_DIR, 'quota-cache-' + acc.id + '.json')
        try {
            if (fs.existsSync(cacheFile)) {
                const cached = JSON.parse(fs.readFileSync(cacheFile, 'utf-8'))
                const age = Date.now() / 1000 - fs.statSync(cacheFile).mtimeMs / 1000
                if (age < CACHE_TTL && cached.quotas?.length > 0) return { id: acc.id, name: acc.name, quotas: cached.quotas, error: null }
            }
        } catch {}
        if (isExpired(acc)) { const r = await refreshOAuth(acc); if (r.ok) { acc.credentials = r.credentials; const d2 = loadAccounts(); const s = d2.accounts.find(a => a.id === acc.id); if (s) { s.credentials = r.credentials; saveAccounts(d2) } } }
        const token = getToken(acc)
        if (!token) return { id: acc.id, name: acc.name, quotas: [], error: 'no token' }
        const result = await fetchQuotaAsync(token)
        if (result.quotas?.length > 0) { try { fs.writeFileSync(cacheFile, JSON.stringify(result), 'utf-8') } catch {} }
        return { id: acc.id, name: acc.name, quotas: result.quotas || [], error: result.error || null }
    })
    return Promise.all(tasks)
}

// ── HTTP Server ───────────────────────────────────────────────────

function readBody(req) {
    return new Promise(resolve => {
        let body = ''; req.on('data', c => body += c); req.on('end', () => { try { resolve(JSON.parse(body)) } catch { resolve({}) } })
    })
}

function json(res, data) {
    const str = JSON.stringify(data)
    res.writeHead(200, { 'Content-Type': 'application/json', 'Access-Control-Allow-Origin': '*' })
    res.end(str)
}

const server = http.createServer(async (req, res) => {
    const url = new URL(req.url, 'http://localhost')
    const p = url.pathname
    const m = req.method

    if (m === 'OPTIONS') { res.writeHead(204, { 'Access-Control-Allow-Origin': '*', 'Access-Control-Allow-Methods': 'GET,POST', 'Access-Control-Allow-Headers': 'Content-Type' }); res.end(); return }

    // API routes
    if (p === '/api/accounts' && m === 'GET') return json(res, getAccountsList())
    if (p === '/api/accounts/quotas' && m === 'GET') return json(res, { accounts: await fetchAllQuotas() })
    if (p === '/api/accounts/switch' && m === 'POST') { refreshActiveCredentials(); const b = await readBody(req); return json(res, await switchAccount(b.id)) }
    if (p === '/api/accounts/add' && m === 'POST') { const b = await readBody(req); return json(res, addAccountFromCreds(b.name, { claudeAiOauth: { accessToken: b.token } })) }
    if (p === '/api/accounts/remove' && m === 'POST') { const b = await readBody(req); return json(res, removeAccount(b.id)) }
    if (p === '/api/accounts/rename' && m === 'POST') { const b = await readBody(req); return json(res, renameAccount(b.id, b.name)) }
    if (p === '/api/accounts/import-current' && m === 'POST') { const b = await readBody(req); return json(res, importCurrentAccount(b.name)) }
    if (p === '/api/accounts/import-credentials' && m === 'POST') { const b = await readBody(req); return json(res, importFromCredJson(b.name, b.credentials)) }

    // Serve HTML
    if (p === '/' || p === '/index.html') {
        res.writeHead(200, { 'Content-Type': 'text/html; charset=utf-8' })
        res.end(HTML)
        return
    }

    res.writeHead(404); res.end('Not found')
})

function openBrowser() {
    const cmd = process.platform === 'win32' ? 'start' : process.platform === 'darwin' ? 'open' : 'xdg-open'
    require('child_process').exec(`${cmd} http://127.0.0.1:${PORT}`)
}

server.on('error', (err) => {
    if (err.code === 'EADDRINUSE') {
        console.log(`\n  Port ${PORT} already in use — opening browser to existing instance.\n`)
        openBrowser()
        setTimeout(() => process.exit(0), 1000)
    } else {
        console.error(err)
        process.exit(1)
    }
})

server.listen(PORT, '127.0.0.1', () => {
    console.log(`\n  Claude Switcher running at http://127.0.0.1:${PORT}\n`)
    openBrowser()
})

// ── HTML UI ───────────────────────────────────────────────────────

const HTML = `<!DOCTYPE html>
<html lang="fr">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>Claude Switcher</title>
<style>
:root {
    --bg: #0d1117;
    --bg-surface: #161b22;
    --bg-elevated: #1c2128;
    --bg-hover: #1f2937;
    --bg-deep: #0a0e14;
    --border: #30363d;
    --border-subtle: #21262d;
    --border-strong: #484f58;
    --text: #e6edf3;
    --text-secondary: #8b949e;
    --text-muted: #484f58;
    --accent: #6c5ce7;
    --accent-dim: rgba(108,92,231,0.12);
    --green: #3fb950;
    --orange: #d29922;
    --red: #f85149;
    --radius: 10px;
    --radius-xs: 6px;
    --font-mono: 'SF Mono', 'Cascadia Code', 'Fira Code', monospace;
    --transition-fast: 150ms ease;
}
* { margin: 0; padding: 0; box-sizing: border-box; }
body {
    font-family: 'Inter', -apple-system, BlinkMacSystemFont, 'Segoe UI', system-ui, sans-serif;
    background: var(--bg);
    color: var(--text);
    min-height: 100vh;
    display: flex;
    align-items: center;
    justify-content: center;
    -webkit-font-smoothing: antialiased;
}
.container {
    width: 460px;
    background: var(--bg-surface);
    border: 1px solid var(--border);
    border-radius: var(--radius);
    box-shadow: 0 8px 32px rgba(0,0,0,0.45);
    overflow: hidden;
}
.header {
    display: flex;
    align-items: center;
    justify-content: space-between;
    padding: 14px 16px;
    border-bottom: 1px solid var(--border-subtle);
}
.header h1 {
    font-size: 13px;
    font-weight: 600;
    color: var(--text);
    display: flex;
    align-items: center;
    gap: 8px;
}
.header h1 svg { width: 16px; height: 16px; stroke: var(--accent); fill: none; stroke-width: 1.5; stroke-linecap: round; stroke-linejoin: round; }
.header .refresh-btn {
    background: none; border: none; color: var(--text-muted); cursor: pointer; padding: 4px; border-radius: 4px; display: flex; align-items: center;
    transition: all var(--transition-fast);
}
.header .refresh-btn:hover { color: var(--text); background: var(--bg-hover); }
.header .refresh-btn svg { width: 14px; height: 14px; stroke: currentColor; fill: none; stroke-width: 1.5; stroke-linecap: round; stroke-linejoin: round; }
.header .refresh-btn.spinning svg { animation: spin 0.8s linear infinite; }
@keyframes spin { to { transform: rotate(360deg); } }

/* Account list */
.account-list { max-height: 400px; overflow-y: auto; }
.account-item {
    display: flex; align-items: center; justify-content: space-between;
    padding: 10px 14px; cursor: pointer; transition: background var(--transition-fast);
    gap: 10px; position: relative;
}
.account-item + .account-item { border-top: 1px solid rgba(33,38,45,0.5); }
.account-item:hover { background: rgba(31,41,55,0.7); }
.account-item.active { background: rgba(108,92,231,0.1); cursor: default; }

.account-item-left { display: flex; align-items: center; gap: 10px; min-width: 0; }
.account-dot { width: 8px; height: 8px; border-radius: 50%; flex-shrink: 0; }
.account-cross { width: 10px; height: 10px; flex-shrink: 0; margin: 0 -1px; stroke: var(--text-muted); fill: none; stroke-width: 2; stroke-linecap: round; opacity: 0.5; }
.account-name { font-size: 13px; font-weight: 600; line-height: 1; color: var(--text); white-space: nowrap; overflow: hidden; text-overflow: ellipsis; letter-spacing: 0.2px; }
.account-name.disconnected { color: var(--text-muted); opacity: 0.5; }
.ext-tag { font-size: 9px; font-weight: 700; color: var(--accent); background: rgba(108,92,231,0.14); border: 1px solid rgba(108,92,231,0.3); padding: 1px 5px; border-radius: 8px; text-transform: uppercase; letter-spacing: 0.5px; margin-left: 6px; flex-shrink: 0; }

/* Hover button */
.hover-btn {
    display: none; position: absolute; inset: 0; margin: auto;
    width: fit-content; height: fit-content; z-index: 2;
    padding: 3px 14px; background: var(--accent); border: none; border-radius: var(--radius-xs);
    color: #fff; font-size: 10px; font-weight: 600; cursor: pointer; white-space: nowrap; letter-spacing: 0.2px;
    transition: opacity var(--transition-fast);
}
.hover-btn:hover { opacity: 0.85; }
.account-item:hover .hover-btn { display: block; }
.account-item.active .hover-btn { display: none; }

/* Quotas */
.account-right { width: 250px; flex-shrink: 0; position: relative; }
.account-info { display: flex; align-items: center; justify-content: flex-end; min-height: 32px; }
.account-item:hover .account-info { visibility: hidden; }

.quotas-grid { display: grid; grid-template-columns: 14px 60px 90px 28px; gap: 3px 5px; align-items: center; }
.q-label { font-size: 9px; color: rgba(72,79,88,0.8); text-align: right; font-family: var(--font-mono); text-transform: uppercase; letter-spacing: 0.3px; }
.q-bar { width: 60px; height: 6px; background: #1a202c; border-radius: 3px; overflow: hidden; }
.q-fill { height: 100%; border-radius: 3px; transition: width 0.3s ease; }
.q-reset { font-size: 8px; color: rgba(72,79,88,0.7); font-family: var(--font-mono); white-space: nowrap; text-align: right; display: flex; align-items: center; justify-content: flex-end; gap: 3px; }
.q-reset svg { width: 9px; height: 9px; stroke: currentColor; fill: none; stroke-width: 1.5; stroke-linecap: round; stroke-linejoin: round; flex-shrink: 0; opacity: 0.6; }
.q-pct { font-size: 10px; color: var(--text); text-align: right; font-family: var(--font-mono); font-weight: 600; }

.quotas-grid.disconnected .q-bar { opacity: 0.3; }
.quotas-grid.disconnected .q-label { opacity: 0.4; }
.disconnected-chip { position: absolute; right: 0; top: 50%; transform: translateY(-50%); font-size: 9px; color: var(--text-muted); border: 1px solid var(--border-strong); background: var(--bg-surface); padding: 1px 8px; border-radius: 8px; white-space: nowrap; font-weight: 500; letter-spacing: 0.2px; }

/* Actions on hover */
.account-actions { position: absolute; inset: 0; display: none; align-items: center; justify-content: flex-end; gap: 4px; }
.account-item:hover .account-actions { display: flex; }
.act-btn { width: 26px; height: 26px; display: flex; align-items: center; justify-content: center; background: rgba(22,27,34,0.8); border: 1px solid var(--border-subtle); border-radius: var(--radius-xs); color: var(--text-muted); cursor: pointer; transition: all var(--transition-fast); }
.act-btn svg { width: 12px; height: 12px; stroke: currentColor; fill: none; stroke-width: 1.5; stroke-linecap: round; stroke-linejoin: round; }
.act-btn:hover { background: var(--bg-hover); color: var(--text); border-color: var(--border); }
.act-btn.danger:hover { color: var(--red); border-color: rgba(248,81,73,0.3); }

/* Rename inline */
.rename-wrap { display: flex; align-items: center; gap: 4px; }
.rename-input { width: 100px; height: 20px; padding: 0 4px; background: var(--bg-deep); border: 1px solid var(--accent); border-radius: 3px; color: var(--text); font-size: 11px; outline: none; }
.rename-ok { height: 20px; padding: 0 6px; background: var(--accent); border: none; border-radius: 3px; color: #fff; font-size: 9px; cursor: pointer; }

/* Action bar */
.action-bar { display: flex; gap: 0; border-top: 1px solid var(--border-subtle); }
.bar-btn { flex: 1; display: flex; align-items: center; justify-content: center; gap: 4px; padding: 7px 4px; background: transparent; border: none; color: var(--text-secondary); font-size: 10px; cursor: pointer; transition: all var(--transition-fast); }
.bar-btn:hover { background: var(--bg-hover); color: var(--text); }
.bar-btn svg { width: 12px; height: 12px; stroke: currentColor; fill: none; stroke-width: 1.5; stroke-linecap: round; stroke-linejoin: round; flex-shrink: 0; }

/* Add form */
.add-form { padding: 8px 12px; border-top: 1px solid var(--border-subtle); display: none; flex-direction: column; gap: 6px; }
.add-form.visible { display: flex; }
.add-input { width: 100%; padding: 6px 8px; background: var(--bg-deep); border: 1px solid var(--border); border-radius: var(--radius-xs); color: var(--text); font-size: 11px; outline: none; }
.add-input:focus { border-color: var(--accent); }
.file-label { display: flex; align-items: center; gap: 5px; padding: 6px 8px; background: var(--bg-deep); border: 1px dashed var(--border-strong); border-radius: var(--radius-xs); color: var(--text-secondary); font-size: 11px; cursor: pointer; transition: all var(--transition-fast); }
.file-label:hover { border-color: var(--accent); color: var(--text); }
.file-label.loaded { border-style: solid; border-color: var(--green); color: var(--green); background: rgba(63,185,80,0.08); }
.file-label svg { width: 14px; height: 14px; stroke: currentColor; fill: none; stroke-width: 1.2; stroke-linecap: round; stroke-linejoin: round; flex-shrink: 0; }
.file-label.loaded svg { stroke: var(--green); fill: rgba(63,185,80,0.15); }
.file-hidden { display: none; }
.form-submit { width: 100%; padding: 4px 14px; background: var(--accent); border: none; border-radius: var(--radius-xs); color: #fff; font-size: 11px; cursor: pointer; transition: opacity var(--transition-fast); }
.form-submit:disabled { opacity: 0.4; cursor: default; }
.form-submit:not(:disabled):hover { opacity: 0.85; }
.form-error { font-size: 10px; color: var(--red); }

/* Loading overlay */
.loading-overlay { position: absolute; inset: 0; display: none; align-items: center; justify-content: center; background: rgba(0,0,0,0.5); color: var(--text); font-size: 12px; border-radius: var(--radius); z-index: 10; }
.loading-overlay.visible { display: flex; }

/* Empty state */
.empty-state { padding: 24px; text-align: center; }
.empty-state p { color: var(--text-secondary); font-size: 12px; margin-bottom: 12px; }
.setup-row { display: flex; align-items: center; justify-content: center; gap: 6px; }
.setup-input { width: 140px; height: 28px; padding: 0 8px; background: var(--bg-deep); border: 1px solid var(--accent); border-radius: 4px; color: var(--text); font-size: 11px; outline: none; }
.setup-ok { height: 28px; padding: 0 12px; background: var(--accent); border: none; border-radius: 4px; color: #fff; font-size: 11px; cursor: pointer; }
.setup-ok:disabled { opacity: 0.4; cursor: default; }
</style>
</head>
<body>

<div class="container" style="position:relative;">
    <div class="header">
        <h1>
            <svg viewBox="0 0 16 16"><circle cx="8" cy="5" r="3"/><path d="M2 14c0-3.3 2.7-6 6-6s6 2.7 6 6"/></svg>
            Claude Switcher
        </h1>
        <button class="refresh-btn" id="refreshBtn" title="Rafraîchir les quotas">
            <svg viewBox="0 0 16 16"><path d="M13.5 2.5v4h-4"/><path d="M2.5 13.5v-4h4"/><path d="M3.5 6a6 6 0 0 1 9.9-1.5l.1.1"/><path d="M12.5 10a6 6 0 0 1-9.9 1.5l-.1-.1"/></svg>
        </button>
    </div>
    <div id="accountList" class="account-list"></div>
    <div id="emptyState" class="empty-state" style="display:none;">
        <p>Aucun compte configuré</p>
        <div class="setup-row">
            <input id="setupName" class="setup-input" placeholder="Nom de la licence" />
            <button id="setupOk" class="setup-ok" disabled>Importer le compte actuel</button>
        </div>
        <div id="setupError" class="form-error" style="margin-top:6px;"></div>
    </div>
    <div id="actionBar" class="action-bar">
        <button class="bar-btn" id="addBtn">
            <svg viewBox="0 0 16 16"><line x1="8" y1="3" x2="8" y2="13"/><line x1="3" y1="8" x2="13" y2="8"/></svg>
            Ajouter une licence Claude
        </button>
    </div>
    <div class="add-form" id="addForm">
        <input id="addName" class="add-input" placeholder="Nom du compte" />
        <label class="file-label" id="fileLabel">
            <svg viewBox="0 0 16 16"><path d="M14 2H6a2 2 0 0 0-2 2v8a2 2 0 0 0 2 2h8a2 2 0 0 0 2-2V4a2 2 0 0 0-2-2z"/><polyline points="10 2 10 6 14 6"/></svg>
            <span id="fileLabelText">Importer .credentials.json</span>
            <input type="file" accept=".json" class="file-hidden" id="credFile" />
        </label>
        <div id="addError" class="form-error"></div>
        <button id="addSubmit" class="form-submit" disabled>Ajouter la licence Claude</button>
    </div>
    <div class="loading-overlay" id="loadingOverlay">Changement de compte...</div>
</div>

<script>
let accounts = [], activeId = null, quotas = {}, renameId = null, credJson = '';

function qColor(pct) { if (pct === null || pct === undefined) return 'var(--text-muted)'; if (pct > 80) return 'var(--red)'; if (pct > 50) return 'var(--orange)'; return 'var(--green)' }
function isDisconnected(id) { const q = quotas[id]; return q?.error || (q && q.session === null && q.week === null) }

async function api(path, method, body) {
    const opts = { method: method || 'GET', headers: { 'Content-Type': 'application/json' } };
    if (body) opts.body = JSON.stringify(body);
    const r = await fetch('/api/' + path, opts);
    return r.json();
}

async function loadAccounts() {
    const d = await api('accounts');
    accounts = d.accounts || []; activeId = d.activeId;
    render();
}

async function loadQuotas() {
    document.getElementById('refreshBtn').classList.add('spinning');
    const d = await api('accounts/quotas');
    quotas = {};
    for (const a of (d.accounts || [])) {
        const s = (a.quotas || []).find(q => q.label.includes('5h'));
        const w = (a.quotas || []).find(q => q.label.includes('7j'));
        quotas[a.id] = { session: s ? s.percent : null, sessionReset: s ? s.resets : '', week: w ? w.percent : null, weekReset: w ? w.resets : '', error: a.error };
    }
    document.getElementById('refreshBtn').classList.remove('spinning');
    render();
}

async function doSwitch(id) {
    if (id === activeId) return;
    document.getElementById('loadingOverlay').classList.add('visible');
    await api('accounts/switch', 'POST', { id });
    activeId = id;
    document.getElementById('loadingOverlay').classList.remove('visible');
    await loadQuotas();
}

async function doRemove(id) {
    const acc = accounts.find(a => a.id === id);
    if (!acc || !confirm('Supprimer le compte "' + acc.name + '" ?')) return;
    await api('accounts/remove', 'POST', { id });
    await loadAccounts(); await loadQuotas();
}

function startRename(id) { renameId = id; render(); setTimeout(() => { const el = document.getElementById('renameInput'); if (el) el.focus(); }, 0); }

async function doRename() {
    const val = document.getElementById('renameInput')?.value?.trim();
    if (!renameId || !val) return;
    await api('accounts/rename', 'POST', { id: renameId, name: val });
    renameId = null;
    await loadAccounts();
}

function renderQuotas(id) {
    const q = quotas[id];
    if (!q) return '<span style="font-size:10px;color:var(--text-muted)">...</span>';
    if (q.error || (q.session === null && q.week === null)) {
        return '<div class="quotas-grid disconnected">' +
            '<span class="q-label">5h</span><div class="q-bar"><div class="q-fill"></div></div><span class="q-reset"></span><span class="q-pct"></span>' +
            '<span class="q-label">7j</span><div class="q-bar"><div class="q-fill"></div></div><span class="q-reset"></span><span class="q-pct"></span>' +
            '<span class="disconnected-chip">Déconnecté</span></div>';
    }
    function row(label, pct, reset, resetIcon) {
        const color = qColor(pct);
        const resetHtml = reset ? resetIcon + ' ' + reset : '';
        return '<span class="q-label">' + label + '</span>' +
            '<div class="q-bar"><div class="q-fill" style="width:' + (pct||0) + '%;background:' + color + '"></div></div>' +
            '<span class="q-reset">' + resetHtml + '</span>' +
            '<span class="q-pct">' + (pct ?? '—') + '%</span>';
    }
    const clockIcon = '<svg viewBox="0 0 16 16"><circle cx="8" cy="8" r="6"/><polyline points="8,4.5 8,8 10.5,9.5"/></svg>';
    const calIcon = '<svg viewBox="0 0 16 16"><rect x="3" y="4" width="10" height="9" rx="1"/><line x1="3" y1="7" x2="13" y2="7"/><line x1="6" y1="2" x2="6" y2="5"/><line x1="10" y1="2" x2="10" y2="5"/></svg>';
    return '<div class="quotas-grid">' + row('5h', q.session, q.sessionReset, clockIcon) + row('7j', q.week, q.weekReset, calIcon) + '</div>';
}

function render() {
    const list = document.getElementById('accountList');
    const bar = document.getElementById('actionBar');
    const empty = document.getElementById('emptyState');

    if (accounts.length === 0) {
        list.innerHTML = ''; bar.style.display = 'none'; empty.style.display = 'block';
        document.getElementById('addForm').classList.remove('visible');
        return;
    }
    empty.style.display = 'none'; bar.style.display = 'flex';

    list.innerHTML = accounts.map(acc => {
        const isActive = acc.id === activeId;
        const disc = !isActive && isDisconnected(acc.id);
        const dotColor = isActive ? qColor(quotas[acc.id]?.session) : 'var(--text-muted)';

        const leftDot = disc
            ? '<svg class="account-cross" viewBox="0 0 16 16"><line x1="4" y1="4" x2="12" y2="12"/><line x1="12" y1="4" x2="4" y2="12"/></svg>'
            : '<span class="account-dot" style="background:' + dotColor + '"></span>';

        const nameHtml = renameId === acc.id
            ? '<div class="rename-wrap"><input id="renameInput" class="rename-input" value="' + acc.name.replace(/"/g,'&quot;') + '" /><button class="rename-ok" data-action="rename">OK</button></div>'
            : '<span class="account-name' + (disc ? ' disconnected' : '') + '">' + acc.name + '</span>';

        const extTag = acc.source === 'users-file' ? '<span class="ext-tag">ext</span>' : '';

        const hoverBtn = !isActive
            ? '<button class="hover-btn" data-action="switch" data-id="' + acc.id + '">' + (disc ? 'RECONNECTER LA LICENCE' : 'SÉLECTIONNER') + '</button>'
            : '';

        const quotaHtml = renderQuotas(acc.id);

        const actions = '<div class="account-actions">' +
            '<button class="act-btn" title="Renommer" data-action="start-rename" data-id="' + acc.id + '"><svg viewBox="0 0 16 16"><path d="M11.5 1.5l3 3L5 14H2v-3L11.5 1.5z"/></svg></button>' +
            '<button class="act-btn danger" title="Supprimer" data-action="remove" data-id="' + acc.id + '"><svg viewBox="0 0 16 16"><line x1="4" y1="4" x2="12" y2="12"/><line x1="12" y1="4" x2="4" y2="12"/></svg></button>' +
            '</div>';

        return '<div class="account-item' + (isActive ? ' active' : '') + '" data-action="switch" data-id="' + acc.id + '">' +
            '<div class="account-item-left">' + leftDot + nameHtml + extTag + '</div>' +
            hoverBtn +
            '<div class="account-right"><div class="account-info">' + quotaHtml + '</div>' + actions + '</div>' +
            '</div>';
    }).join('');
}

// Event delegation on account list
document.getElementById('accountList').addEventListener('click', (e) => {
    const btn = e.target.closest('[data-action]');
    if (!btn) return;
    e.stopPropagation();
    const action = btn.dataset.action;
    const id = btn.dataset.id;
    if (action === 'switch' && id) doSwitch(id);
    else if (action === 'start-rename' && id) startRename(id);
    else if (action === 'remove' && id) doRemove(id);
    else if (action === 'rename') doRename();
});

// Add form logic
const addBtn = document.getElementById('addBtn');
const addForm = document.getElementById('addForm');
const addName = document.getElementById('addName');
const addSubmit = document.getElementById('addSubmit');
const addError = document.getElementById('addError');
const credFile = document.getElementById('credFile');
const fileLabel = document.getElementById('fileLabel');
const fileLabelText = document.getElementById('fileLabelText');

addBtn.onclick = () => { addForm.classList.toggle('visible'); addError.textContent = ''; };
function checkAddReady() { addSubmit.disabled = !(addName.value.trim() && credJson); }
addName.oninput = checkAddReady;

credFile.onchange = (e) => {
    const file = e.target.files[0]; if (!file) return;
    const reader = new FileReader();
    reader.onload = () => { credJson = reader.result; fileLabel.classList.add('loaded'); fileLabelText.textContent = '.credentials.json'; checkAddReady(); };
    reader.readAsText(file);
};

addSubmit.onclick = async () => {
    addError.textContent = '';
    if (!addName.value.trim() || !credJson) { addError.textContent = 'Nom et fichier requis'; return; }
    const r = await api('accounts/import-credentials', 'POST', { name: addName.value.trim(), credentials: credJson });
    if (r.ok) { addName.value = ''; credJson = ''; credFile.value = ''; fileLabel.classList.remove('loaded'); fileLabelText.textContent = 'Importer .credentials.json'; addForm.classList.remove('visible'); checkAddReady(); await loadAccounts(); await loadQuotas(); }
    else { addError.textContent = r.error || 'Erreur'; }
};

// Setup (no accounts)
const setupName = document.getElementById('setupName');
const setupOk = document.getElementById('setupOk');
const setupError = document.getElementById('setupError');
setupName.oninput = () => { setupOk.disabled = !setupName.value.trim(); };
setupOk.onclick = async () => {
    if (!setupName.value.trim()) return;
    const r = await api('accounts/import-current', 'POST', { name: setupName.value.trim() });
    if (r.ok) { setupName.value = ''; setupError.textContent = ''; await loadAccounts(); await loadQuotas(); }
    else { setupError.textContent = r.error || 'Erreur'; }
};

// Rename on Enter/Escape
document.addEventListener('keyup', e => {
    if (renameId && e.key === 'Enter') doRename();
    if (renameId && e.key === 'Escape') { renameId = null; render(); }
});

// Refresh button
document.getElementById('refreshBtn').onclick = loadQuotas;

// Init
(async () => { await loadAccounts(); await loadQuotas(); })();
// Auto-refresh every 60s
setInterval(loadQuotas, 60000);
</script>
</body>
</html>`;
