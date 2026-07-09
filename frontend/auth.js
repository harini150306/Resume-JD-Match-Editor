/* ===========================================================
   MatchScan — shared auth helpers
   Handles token storage, route guarding, and authenticated fetch.
   =========================================================== */

const AUTH_TOKEN_KEY = "matchscan_token";
const AUTH_NAME_KEY = "matchscan_name";
const AUTH_EMAIL_KEY = "matchscan_email";

function saveSession({ access_token, full_name, email }) {
  localStorage.setItem(AUTH_TOKEN_KEY, access_token);
  if (full_name) localStorage.setItem(AUTH_NAME_KEY, full_name);
  if (email) localStorage.setItem(AUTH_EMAIL_KEY, email);
}

function getToken() {
  return localStorage.getItem(AUTH_TOKEN_KEY);
}

function getDisplayName() {
  return localStorage.getItem(AUTH_NAME_KEY) || localStorage.getItem(AUTH_EMAIL_KEY) || "there";
}

function clearSession() {
  localStorage.removeItem(AUTH_TOKEN_KEY);
  localStorage.removeItem(AUTH_NAME_KEY);
  localStorage.removeItem(AUTH_EMAIL_KEY);
}

/** Call at the top of any protected page. Redirects to login if no token. */
function requireAuth() {
  if (!getToken()) {
    window.location.href = "index.html";
  }
}

/** fetch() wrapper that automatically attaches the Bearer token. */
async function authFetch(url, options = {}) {
  const token = getToken();
  const headers = { ...(options.headers || {}), Authorization: `Bearer ${token}` };
  const res = await fetch(url, { ...options, headers });

  if (res.status === 401) {
    clearSession();
    window.location.href = "index.html";
    throw new Error("Session expired. Please log in again.");
  }
  return res;
}

function wireLogoutButton(buttonId = "logoutBtn") {
  const btn = document.getElementById(buttonId);
  if (!btn) return;
  btn.addEventListener("click", () => {
    clearSession();
    window.location.href = "index.html";
  });
}

function fillUserDisplays() {
  document.querySelectorAll("[data-user-name]").forEach((el) => {
    el.textContent = getDisplayName();
  });
}