/**
 * IELTS Lab — Global Navigation Component
 * Injected into every page via <div id="header-container"> + loadHeader()
 */
(function () {
  'use strict';

  const NAV_CSS = `
    <style id="ielts-nav-styles">
      .ielts-nav {
        position: sticky; top: 0; z-index: 1000;
        background: #0f1e3c;
        border-bottom: 1px solid rgba(255,255,255,0.07);
        font-family: 'DM Sans', system-ui, sans-serif;
        -webkit-font-smoothing: antialiased;
      }
      .ielts-nav-inner {
        max-width: 1200px; margin: 0 auto;
        padding: 0 24px; height: 62px;
        display: flex; align-items: center; justify-content: space-between; gap: 16px;
      }

      /* Logo */
      .ielts-nav-logo {
        display: flex; align-items: baseline; gap: 0;
        text-decoration: none; flex-shrink: 0; line-height: 1;
        transition: opacity 0.2s;
      }
      .ielts-nav-logo:hover { opacity: 0.85; }
      .nl-ielts {
        font-family: 'Playfair Display', 'Cormorant Garamond', 'Times New Roman', serif;
        font-size: 19px; font-weight: 600; letter-spacing: 1px; color: #ffffff;
      }
      .nl-lab {
        font-family: 'DM Sans', sans-serif;
        font-size: 11px; font-weight: 700; letter-spacing: 3px;
        color: #c9a84c; margin-left: 5px; text-transform: uppercase;
      }

      /* Desktop links */
      .ielts-nav-links {
        display: flex; align-items: center; gap: 2px; flex: 1; justify-content: center;
      }
      .ielts-nav-link {
        text-decoration: none; color: rgba(255,255,255,0.65);
        font-size: 13.5px; font-weight: 500;
        padding: 7px 14px; border-radius: 8px;
        transition: color 0.18s, background 0.18s;
        white-space: nowrap; letter-spacing: 0.01em;
      }
      .ielts-nav-link:hover { color: #ffffff; background: rgba(255,255,255,0.07); }
      .ielts-nav-link.ielts-active { color: #c9a84c; background: rgba(201,168,76,0.1); }

      /* CTA button */
      .ielts-nav-right { display: flex; align-items: center; gap: 10px; flex-shrink: 0; }
      .ielts-nav-cta {
        text-decoration: none;
        background: #c9a84c; color: #0f1e3c;
        font-size: 11.5px; font-weight: 700;
        letter-spacing: 0.07em; text-transform: uppercase;
        padding: 8px 18px; border-radius: 8px;
        transition: background 0.18s, transform 0.18s, box-shadow 0.18s;
        white-space: nowrap;
        box-shadow: 0 2px 8px rgba(201,168,76,0.25);
      }
      .ielts-nav-cta:hover {
        background: #e0b84e; transform: translateY(-1px);
        box-shadow: 0 4px 14px rgba(201,168,76,0.35);
      }

      /* Hamburger button */
      .ielts-hamburger {
        display: none; align-items: center; justify-content: center;
        background: none; border: none; cursor: pointer;
        padding: 8px; border-radius: 8px; flex-shrink: 0;
        transition: background 0.18s; -webkit-tap-highlight-color: transparent;
      }
      .ielts-hamburger:hover { background: rgba(255,255,255,0.08); }

      /* Mobile drawer */
      .ielts-drawer {
        display: none; flex-direction: column; gap: 3px;
        position: fixed; top: 62px; left: 0; right: 0;
        background: #0d1b36;
        border-bottom: 1px solid rgba(255,255,255,0.07);
        padding: 14px 16px 20px;
        box-shadow: 0 12px 40px rgba(0,0,0,0.3);
        z-index: 999;
        animation: ieltsSlideDown 0.22s cubic-bezier(0.16,1,0.3,1) both;
      }
      .ielts-drawer.open { display: flex; }
      @keyframes ieltsSlideDown {
        from { opacity: 0; transform: translateY(-8px); }
        to   { opacity: 1; transform: translateY(0); }
      }
      .ielts-drawer .ielts-nav-link {
        padding: 13px 16px; font-size: 14.5px; border-radius: 10px;
        color: rgba(255,255,255,0.78);
      }
      .ielts-drawer .ielts-nav-cta {
        display: block; text-align: center;
        padding: 13px 16px; font-size: 13px;
        margin-top: 10px; border-radius: 10px;
      }
      .ielts-drawer-divider {
        height: 1px; background: rgba(255,255,255,0.07); margin: 8px 0;
      }

      /* Responsive breakpoint */
      @media (max-width: 680px) {
        .ielts-nav-links { display: none; }
        .ielts-nav-right .ielts-nav-cta { display: none; }
        .ielts-hamburger { display: flex; }
      }
    </style>`;

  function getActiveClass(href) {
    const p = window.location.pathname;
    if (href === '/IELTS-Lab.html' && (p === '/' || p.endsWith('IELTS-Lab.html'))) return 'ielts-active';
    if (href.includes('writing-clinic') && p.includes('writing-clinic')) return 'ielts-active';
    if (href.includes('mock-tests') && p.includes('mock-tests')) return 'ielts-active';
    if (href.includes('guide') && p.includes('guide')) return 'ielts-active';
    if (href.includes('pricing') && p.includes('pricing')) return 'ielts-active';
    return '';
  }

  function buildNav() {
    const home   = getActiveClass('/IELTS-Lab.html');
    const clinic = getActiveClass('/writing-clinic/');
    const mocks  = getActiveClass('/mock-tests/');
    const guide  = getActiveClass('/guide/');
    const price  = getActiveClass('/pricing.html');

    return `
      ${NAV_CSS}
      <nav class="ielts-nav" role="navigation" aria-label="IELTS Lab navigation">
        <div class="ielts-nav-inner">

          <a href="/IELTS-Lab.html" class="ielts-nav-logo" aria-label="IELTS Lab — Home">
            <span class="nl-ielts">IELTS</span><span class="nl-lab">Lab</span>
          </a>

          <div class="ielts-nav-links">
            <a href="/IELTS-Lab.html"                   class="ielts-nav-link ${home}">Home</a>
            <a href="/guide/index.html"                 class="ielts-nav-link ${guide}">IELTS Guide</a>
            <a href="/pricing.html"                     class="ielts-nav-link ${price}">Pricing</a>
            <a href="/writing-clinic/corrector.html"    class="ielts-nav-link ${clinic}">Writing Clinic</a>
            <a href="/mock-tests/index.html"            class="ielts-nav-link ${mocks}">Mock Tests</a>
          </div>

          <div class="ielts-nav-right">
            <a href="/writing-clinic/corrector.html" class="ielts-nav-cta">
              My Dashboard
            </a>
            <button class="ielts-hamburger" id="ieltsHamburger"
              aria-label="Open menu" aria-expanded="false" aria-controls="ieltsDrawer">
              <svg id="ieltsHamIcon" width="22" height="22" viewBox="0 0 24 24"
                fill="none" stroke="rgba(255,255,255,0.85)" stroke-width="2"
                stroke-linecap="round">
                <line x1="3" y1="6"  x2="21" y2="6"/>
                <line x1="3" y1="12" x2="21" y2="12"/>
                <line x1="3" y1="18" x2="21" y2="18"/>
              </svg>
              <svg id="ieltsCloseIcon" width="22" height="22" viewBox="0 0 24 24"
                fill="none" stroke="rgba(255,255,255,0.85)" stroke-width="2"
                stroke-linecap="round" style="display:none;">
                <line x1="4" y1="4" x2="20" y2="20"/>
                <line x1="20" y1="4" x2="4" y2="20"/>
              </svg>
            </button>
          </div>

        </div>

        <div class="ielts-drawer" id="ieltsDrawer" role="menu">
          <a href="/IELTS-Lab.html"                class="ielts-nav-link ${home}"   role="menuitem">🏠 Home</a>
          <a href="/guide/index.html"              class="ielts-nav-link ${guide}"  role="menuitem">📖 IELTS Guide</a>
          <a href="/pricing.html"                  class="ielts-nav-link ${price}"  role="menuitem">💳 Pricing</a>
          <a href="/writing-clinic/corrector.html" class="ielts-nav-link ${clinic}" role="menuitem">✍️ Writing Clinic</a>
          <a href="/mock-tests/index.html"         class="ielts-nav-link ${mocks}"  role="menuitem">📝 Mock Tests</a>
          <div class="ielts-drawer-divider"></div>
          <a href="/writing-clinic/corrector.html" class="ielts-nav-cta" role="menuitem">My Dashboard →</a>
        </div>
      </nav>`;
  }

  function wireHamburger() {
    const btn    = document.getElementById('ieltsHamburger');
    const drawer = document.getElementById('ieltsDrawer');
    const hamIco = document.getElementById('ieltsHamIcon');
    const closeIco = document.getElementById('ieltsCloseIcon');
    if (!btn || !drawer) return;

    function toggle(force) {
      const open = typeof force === 'boolean' ? force : !drawer.classList.contains('open');
      drawer.classList.toggle('open', open);
      btn.setAttribute('aria-expanded', open);
      hamIco.style.display   = open ? 'none'  : '';
      closeIco.style.display = open ? ''      : 'none';
    }

    btn.addEventListener('click', (e) => { e.stopPropagation(); toggle(); });
    drawer.querySelectorAll('a').forEach(a => a.addEventListener('click', () => toggle(false)));
    document.addEventListener('click', (e) => {
      if (!btn.contains(e.target) && !drawer.contains(e.target)) toggle(false);
    });
    document.addEventListener('keydown', (e) => {
      if (e.key === 'Escape') toggle(false);
    });
  }

  function inject() {
    if (document.getElementById('ielts-nav-styles')) return; // already injected
    const container = document.getElementById('header-container');
    if (container) {
      container.innerHTML = buildNav();
    } else {
      const div = document.createElement('div');
      div.innerHTML = buildNav();
      document.body.insertBefore(div.firstElementChild, document.body.firstChild);
    }
    wireHamburger();
  }

  if (document.readyState === 'loading') {
    document.addEventListener('DOMContentLoaded', inject);
  } else {
    inject();
  }

  // Public API — backwards-compatible with all existing loadHeader() calls
  window.loadHeader = inject;
  window.IELTSLab  = window.IELTSLab || {};
  window.IELTSLab.loadNav = inject;
})();
