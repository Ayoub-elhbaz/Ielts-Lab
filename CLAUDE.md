# IELTS Lab — Claude Instructions

## What This Project Is
IELTS Lab is a premium IELTS preparation platform. It has:
- A public landing page (`IELTS-Lab.html`)
- Writing Clinic (essay corrector + AI chat coach) → `writing-clinic/`
- Mock Tests (Listening, Reading, Writing, Speaking, full exams) → `mock-tests/`
- Node.js/Express backend (`server.js`) with Claude API integration
- Auth via `localStorage` (`ielts_session` key, JSON with `name` field)

## Actual Tech Stack
- **CSS**: Tailwind CSS via CDN + custom CSS in `<style>` blocks (no separate `.css` files)
- **JS**: Vanilla JavaScript only — no jQuery, no frameworks
- **Shared components**: `js/components.js` exposes `IELTSLab` global (nav, auth, theme)
- **Backend**: Node.js + Express (`server.js`) — ESM modules (`import`, not `require`)
- **AI**: Claude API (`claude-sonnet-4-6`) via `POST https://api.anthropic.com/v1/messages`
- **Fonts**: Satoshi (headings/display), Plus Jakarta Sans (body), Cormorant Garamond (logo serif), Space Mono (mono accents), Caveat (handwritten)

## CSS Variables — Always Use These, Never Hard-Code Colors
```css
:root {
  --gold: #C9952E;          /* primary accent */
  --gold-light: #DDB05A;
  --gold-dim: rgba(201,149,46,0.10);
  --gold-border: rgba(201,149,46,0.22);
  --navy: #0d2b4e;          /* headings on light pages */
  --navy-mid: #1a3c6e;      /* active states */
  --blue: #3A7BF7;
  --teal: #2AFFD6;
  --white: #EEF4FF;         /* off-white for dark-bg text */
}
```

## API Endpoints (server.js)
| Method | Route | Purpose |
|--------|-------|---------|
| GET | `/api/health` | Server + API key status |
| POST | `/api/correct-essay` | V1 single-pass essay corrector |
| POST | `/api/correct-essay-v2` | V2 three-pass multi-agent pipeline |
| POST | `/api/ielts-expert` | IELTS chat agent (writing-clinic) |
| POST | `/api/mock/generate-question` | Generate mock test question |
| POST | `/api/mock/grade` | Grade mock test answer |

Request format for essay endpoints: `{ taskLabel, essay, question, image?, imageType? }`
Request format for mock: `{ skill, trainingType, mode?, question?, answers? }`

## File Structure (Actual)
```
/IELTS-Lab.html          ← public homepage (light theme)
/corrector.html          ← legacy corrector
/server.js               ← Express + Claude API
/mock-tests/
  index.html             ← mock test dashboard (light theme default)
  listening.html
  reading.html
  writing.html
  speaking.html
  results.html
  academic-reading-test.html
/writing-clinic/
  index.html
  corrector.html         ← main essay corrector (calls /api/correct-essay-v2)
  chat.html              ← IELTS expert chat (calls /api/ielts-expert)
/about/, /privacy/, /terms/
```

## Common Patterns — Reuse These Exactly

### Nav — Use the Shared Component (new pages)
For any new page, use `js/components.js` instead of duplicating nav HTML.

```html
<head>
  <!-- fonts, tailwind, etc. -->
  <!-- Theme IIFE must stay in <head> to prevent flash-of-wrong-theme -->
  <script>(function(){var t=localStorage.getItem('ieltslab_theme')||'dark';document.documentElement.setAttribute('data-theme',t);})();</script>
</head>
<body>
  <div id="header-container"></div>
  <!-- page content -->

  <script src="../js/components.js"></script>
  <script>
    // 1. Auth guard (omit on public pages)
    const session = IELTSLab.authGuard('../login.html');

    // 2. Load nav
    IELTSLab.loadNav({
      basePath:      '../',        // '' for root pages, '../' for subdirectories
      breadcrumb:    'Mock Tests', // null = no breadcrumb
      authenticated: true,         // false = hide sign-out + greeting
      themeDefault:  'dark',       // default when user has no saved preference
    });
  </script>
</body>
```

**`IELTSLab` API:**
| Method | Purpose |
|--------|---------|
| `loadNav(options)` | Inject nav into `#header-container` |
| `toggleTheme()` | Flip light/dark, update icon, persist to localStorage |
| `logout(redirectTo)` | Clear `ielts_session`, redirect |
| `authGuard(loginPath)` | Redirect if no session; return parsed session object |

**Nav variants:**
- `authenticated: true` → shows user greeting + ← Main Site + Sign Out + theme toggle
- `authenticated: false` → shows theme toggle only
- `breadcrumb: 'Page Name'` → shows `Home / Page Name` in the center (hidden on mobile)

**Existing pages** still use their own inline nav — only new pages should use the component.

### Scroll Reveal (IntersectionObserver)
```css
.reveal { opacity:0; transform:translateY(28px); transition: opacity 0.7s, transform 0.7s; }
.reveal.visible { opacity:1; transform:translateY(0); }
.d100 { transition-delay:0.1s; } /* .d200, .d300, .d400 */
```
```js
const observer = new IntersectionObserver(entries => {
  entries.forEach(e => { if (e.isIntersecting) { e.target.classList.add('visible'); observer.unobserve(e.target); } });
}, { threshold: 0.08 });
document.querySelectorAll('.reveal').forEach(el => observer.observe(el));
```

### Auth Guard (top of every protected page `<script>`)
```js
const rawSession = localStorage.getItem('ielts_session');
if (!rawSession) window.location.replace('../login.html');
let session;
try { session = JSON.parse(rawSession); }
catch { localStorage.removeItem('ielts_session'); window.location.replace('../login.html'); }
const firstName = (session.name || 'Student').split(' ')[0];
```

### Dark/Light Theme Toggle
- localStorage key: `ieltslab_theme` → `'light'` or `'dark'`
- Set via `data-theme` attribute on `<html>`
- Dark pages default: `||'dark'`; light pages default: `||'light'`
- IIFE in `<head>` (before `</style>`) to avoid flash-of-wrong-theme
```js
(function(){ var t=localStorage.getItem('ieltslab_theme')||'dark'; document.documentElement.setAttribute('data-theme',t); })();
```
- Button: `<button id="themeToggle" onclick="toggleTheme()">☀</button>`
- Overrides use `html[data-theme="light"] .classname { ... !important }`

### Band Score Chips
```css
.band-chip { display:inline-flex; align-items:center; justify-content:center; min-width:36px; padding:2px 8px; border-radius:4px; font-size:0.75rem; font-weight:700; font-family:'Space Mono',monospace; }
.band-high { background:rgba(42,255,214,0.12); color:#2affd6; border:1px solid rgba(42,255,214,0.2); } /* 7.0+ */
.band-mid  { background:var(--gold-dim); color:var(--gold-light); border:1px solid var(--gold-border); } /* 5.5–6.5 */
.band-low  { background:rgba(239,68,68,0.1); color:#f87171; border:1px solid rgba(239,68,68,0.2); }  /* <5.5 */
```

### localStorage Keys Reference
| Key | Value | Used for |
|-----|-------|---------|
| `ielts_session` | `{ name, email, ... }` | Auth across all pages |
| `ieltslab_theme` | `'light'` \| `'dark'` | Theme preference |
| `ielts_mock_results` | Array of result objects | Past mock test scores |
| `mockTestSetup` | sessionStorage: `{ mode, skill, type, startedAt, completedSkills }` | Active test session |

## Code Quality Rules
- **2-space indentation** throughout
- **Semantic HTML5** — use `<header>`, `<nav>`, `<main>`, `<section>`, `<footer>`
- **Inline styles are acceptable** when overriding Tailwind or applying one-off values — but prefer CSS classes for anything repeated
- **No Bootstrap** — Tailwind CDN + custom CSS only
- **No jQuery** — vanilla JS only
- **Always close HTML tags** properly
- **No placeholder text** — never leave Lorem ipsum or TODO in production code
- **Mobile-first** — every page must work on phone, tablet, desktop

## Design Rules
- Check existing `:root` variables before adding any new color
- Fonts: Satoshi for headings (`font-display`), Plus Jakarta Sans for body (`font-sans`), Space Mono for band scores/labels, Cormorant Garamond for logo
- Consistent page max-width: `max-w-6xl mx-auto px-6`
- Cards use `border-radius: 1.25rem` (dark pages) or `16px` (light pages)
- Gold hover accents: `border-color: var(--gold-border)` + `box-shadow` with gold tint
- All transitions: `0.2s–0.25s ease` or `cubic-bezier(0.16,1,0.3,1)` for lift effects

## IELTS Content Rules
- All IELTS information must be accurate (May 2023 BC descriptors are the authoritative source)
- Band scores: 1–9 in 0.5 steps; overall = average of 4 criteria rounded to nearest 0.5
- Use exact IELTS terminology: Task Achievement, Coherence & Cohesion, Lexical Resource, Grammatical Range & Accuracy
- Target audience: students aiming for band 6.0–8.0
- API keys: stored in `.env` (`ANTHROPIC_API_KEY`) — never expose in frontend code

## Before Every Task
1. Identify the exact file being edited and its theme (dark/light default)
2. Check `:root` variables before adding any new color value
3. Match existing card/nav/button styles already on that page
4. For server-side changes: keep ESM (`import`/`export`) — no CommonJS (`require`)
5. For new API routes: follow the pattern in `server.js` — `callAnthropic()` + `extractJSON()` + error handling with retry
