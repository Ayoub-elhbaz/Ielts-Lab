/**
 * IELTS Lab — Shared Components
 *
 * Exposes: IELTSLab  (object)   — loadNav, loadHeader, logout, authGuard
 *          loadHeader (function) — bare global alias for <script>loadHeader();</script>
 *
 * Usage on every inner page:
 *   1. Add <div id="header-container"></div> where the nav should appear.
 *   2. Before </body>:
 *        <script src="/js/components.js"></script>
 *        <script>loadHeader();</script>
 *
 * The nav injected is the exact navbar from IELTS-Lab.html — same CSS, same
 * structure, same auth-aware behaviour (Writing Clinic / Mock Tests links
 * appear when a session exists; CTA becomes "My Dashboard").
 */

const IELTSLab = (() => {

  // ─── CSS — copied verbatim from IELTS-Lab.html, adapted for sticky use ────
  const CSS = `
    /* Sticky wrapper */
    .ielts-site-header {
      background: rgba(9,9,11,0.82);
      backdrop-filter: blur(20px);
      -webkit-backdrop-filter: blur(20px);
      border-bottom: 1px solid rgba(255,255,255,0.04);
      position: sticky;
      top: 0;
      z-index: 50;
    }

    /* Nav row — matches .ui nav layout from IELTS-Lab.html */
    .ielts-site-nav {
      display: flex;
      align-items: center;
      justify-content: space-between;
      padding: 20px 48px;
      max-width: 1200px;
      margin: 0 auto;
    }

    /* Logo — exact copy */
    .ielts-site-header .nav-logo {
      display: flex;
      align-items: baseline;
      gap: 0;
      text-decoration: none;
    }
    .ielts-site-header .nl-ielts {
      font-family: 'Cormorant Garamond', serif;
      font-size: 22px;
      font-weight: 600;
      letter-spacing: 1px;
      color: #EEF4FF;
    }
    .ielts-site-header .nl-lab {
      font-family: 'Space Mono', monospace;
      font-size: 13px;
      font-weight: 700;
      letter-spacing: 3px;
      color: #C9952E;
      margin-left: 5px;
      padding-bottom: 1px;
      filter: drop-shadow(0 0 8px rgba(201,149,46,0.5));
    }
    .ielts-site-header .nl-flask {
      font-size: 16px;
      margin-left: 4px;
    }

    /* Nav links — exact copy */
    .ielts-site-header .nav-links {
      display: flex;
      gap: 32px;
      list-style: none;
      margin: 0;
      padding: 0;
    }
    .ielts-site-header .nav-links a {
      font-family: 'DM Sans', sans-serif;
      font-size: 11px;
      font-weight: 300;
      letter-spacing: 2.5px;
      text-transform: uppercase;
      color: rgba(200,216,255,0.45);
      text-decoration: none;
      transition: color 0.3s;
    }
    .ielts-site-header .nav-links a:hover { color: #C9952E; }

    /* CTA button — exact copy */
    .ielts-site-header .nav-cta {
      font-family: 'DM Sans', sans-serif;
      font-size: 10px;
      font-weight: 400;
      letter-spacing: 2px;
      text-transform: uppercase;
      padding: 9px 22px;
      border-radius: 2px;
      border: 1px solid rgba(201,149,46,0.4);
      color: #C9952E;
      background: rgba(201,149,46,0.07);
      cursor: pointer;
      text-decoration: none;
      transition: all 0.3s;
      display: inline-flex;
      align-items: center;
      white-space: nowrap;
    }
    .ielts-site-header .nav-cta:hover {
      background: rgba(201,149,46,0.15);
      border-color: #C9952E;
    }

    /* Mobile: hide nav links, tighten padding */
    @media (max-width: 768px) {
      .ielts-site-nav { padding: 16px 20px; }
      .ielts-site-header .nav-links { display: none; }
    }
  `;

  function _injectCSS() {
    if (document.getElementById('ielts-components-css')) return;
    const s = document.createElement('style');
    s.id = 'ielts-components-css';
    s.textContent = CSS;
    document.head.appendChild(s);
  }

  // ─── Auth helpers ───────────────────────────────────────────────────────────

  function logout(redirectTo) {
    localStorage.removeItem('ielts_session');
    window.location.replace(redirectTo || '/IELTS-Lab.html');
  }

  /**
   * Redirect to login if no session found; return the parsed session if valid.
   * Call at the top of any protected page's <script> block.
   */
  function authGuard(loginPath) {
    const raw = localStorage.getItem('ielts_session');
    if (!raw) { window.location.replace(loginPath); return null; }
    try {
      return JSON.parse(raw);
    } catch {
      localStorage.removeItem('ielts_session');
      window.location.replace(loginPath);
      return null;
    }
  }

  // ─── loadNav ────────────────────────────────────────────────────────────────

  /**
   * Inject the site nav into #header-container.
   *
   * @param {string} [basePath='../'] — path prefix to reach site root
   *   ''    for files at root  (e.g. /corrector.html)
   *   '../' for one level deep (e.g. /mock-tests/index.html)
   */
  function loadNav(basePath) {
    if (basePath === undefined) basePath = '../';

    _injectCSS();

    const home   = basePath + 'IELTS-Lab.html';
    const login  = basePath + 'login.html';
    const clinic = basePath + 'writing-clinic/index.html';
    const mock   = basePath + 'mock-tests/index.html';

    const html = `
      <header class="ielts-site-header">
        <nav class="ielts-site-nav">

          <a href="${home}" class="nav-logo">
            <span class="nl-ielts">IELTS</span>
            <span class="nl-lab">LAB</span>
            <span class="nl-flask">⚗️</span>
          </a>

          <ul class="nav-links">
            <li><a href="${home}#skills">Courses</a></li>
            <li><a href="${home}#teachers">Teachers</a></li>
            <li><a href="${home}#mock">AI Examiner</a></li>
            <li><a href="${home}#pricing">Pricing</a></li>
            <li id="clinicNavItem" style="display:none">
              <a href="${clinic}" style="color:#C9952E;opacity:1;font-weight:400;">✍️ Writing Clinic</a>
            </li>
            <li id="mockNavItem" style="display:none">
              <a href="${mock}" style="color:#C9952E;opacity:1;font-weight:400;">🧪 Mock Tests</a>
            </li>
          </ul>

          <a href="${login}" class="nav-cta" id="mainNavCta">Start Free Trial</a>

        </nav>
      </header>`;

    const container = document.getElementById('header-container');
    if (!container) {
      console.warn('[IELTSLab] #header-container not found.');
      return;
    }
    container.innerHTML = html;

    // Auth-aware behaviour — mirrors IELTS-Lab.html exactly
    const session = localStorage.getItem('ielts_session');
    if (session) {
      const clinicItem = document.getElementById('clinicNavItem');
      const mockItem   = document.getElementById('mockNavItem');
      const cta        = document.getElementById('mainNavCta');
      if (clinicItem) clinicItem.style.display = 'list-item';
      if (mockItem)   mockItem.style.display   = 'list-item';
      if (cta) {
        cta.textContent = 'My Dashboard';
        cta.href        = clinic;
      }
    }
  }

  // ─── loadHeader — zero-config wrapper ──────────────────────────────────────

  /**
   * Auto-detects basePath from the current URL and calls loadNav().
   * This is the function injected into every page by the migration script.
   *
   * It also runs authGuard() automatically on protected sections
   * (mock-tests/, writing-clinic/).
   */
  function loadHeader() {
    const parts     = window.location.pathname.replace(/^\//, '').split('/').filter(Boolean);
    const depth     = parts.length;
    const folder    = depth > 1 ? parts[0] : null;
    const basePath  = depth <= 1 ? '' : '../'.repeat(depth - 1);

    const AUTH_SECTIONS = ['mock-tests', 'writing-clinic'];
    if (folder && AUTH_SECTIONS.includes(folder)) {
      // Guard without redirect loop — only redirect if truly missing
      const raw = localStorage.getItem('ielts_session');
      if (!raw) {
        window.location.replace(basePath + 'login.html');
        return;
      }
    }

    loadNav(basePath);
  }

  return { loadNav, loadHeader, logout, authGuard };

})();

// Bare global so pages can call loadHeader() without the IELTSLab. prefix
var loadHeader = IELTSLab.loadHeader;
