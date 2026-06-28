// API client (CP19): base URL from env, JWT handling, refresh placeholder, error handling.
const API_BASE_URL = import.meta.env.VITE_API_BASE_URL || "http://localhost:8000/api/v1";

const TOKEN_KEY = "rpm_access_token";
const REFRESH_KEY = "rpm_refresh_token";

export const tokenStore = {
  get: () => localStorage.getItem(TOKEN_KEY),
  getRefresh: () => localStorage.getItem(REFRESH_KEY),
  set: (access, refresh) => {
    if (access) localStorage.setItem(TOKEN_KEY, access);
    if (refresh) localStorage.setItem(REFRESH_KEY, refresh);
  },
  clear: () => {
    localStorage.removeItem(TOKEN_KEY);
    localStorage.removeItem(REFRESH_KEY);
  },
};

async function _fetch(path, options = {}, withAuth = true) {
  const headers = { "Content-Type": "application/json", ...(options.headers || {}) };
  if (withAuth) {
    const t = tokenStore.get();
    if (t) headers.Authorization = `Bearer ${t}`;
  }
  const res = await fetch(`${API_BASE_URL}${path}`, { ...options, headers });
  return res;
}

async function _parse(res) {
  if (res.status === 204) return null;
  let body = null;
  try { body = await res.json(); } catch { /* non-json */ }
  if (!res.ok) {
    const err = new Error(body?.message || body?.detail || `Request failed (${res.status})`);
    err.status = res.status;
    err.body = body;
    throw err;
  }
  return body;
}

// Try a refresh once on 401 (refresh wiring placeholder; tokens exist from CP4).
async function _withRefresh(doRequest) {
  let res = await doRequest();
  if (res.status === 401 && tokenStore.getRefresh()) {
    try {
      const r = await _fetch("/auth/refresh", {
        method: "POST",
        body: JSON.stringify({ refresh_token: tokenStore.getRefresh() }),
      }, false);
      if (r.ok) {
        const data = await r.json();
        tokenStore.set(data.access_token, data.refresh_token);
        res = await doRequest();
      }
    } catch { /* fall through to original 401 */ }
  }
  return res;
}

export const api = {
  baseUrl: API_BASE_URL,
  get: (path) => _withRefresh(() => _fetch(path, { method: "GET" })).then(_parse),
  post: (path, body, withAuth = true) =>
    _withRefresh(() => _fetch(path, { method: "POST", body: JSON.stringify(body || {}) }, withAuth)).then(_parse),
  patch: (path, body) =>
    _withRefresh(() => _fetch(path, { method: "PATCH", body: JSON.stringify(body || {}) })).then(_parse),
  del: (path) => _withRefresh(() => _fetch(path, { method: "DELETE" })).then(_parse),
  health: () => _fetch("/health", { method: "GET" }, false).then(_parse),
};
