#!/usr/bin/env python3
"""
Generate cam17-t{1..4}-writing.html
Content from Cambridge IELTS 20 Volume 4 PDF (used for Cambridge 17 slot)
"""
import os

BASE = '/Users/ayoubelhebaze/Downloads/claude md/mock-tests'

# ─── SVG: Riverside Town Centre map comparison (Test 4) ──────────────────────
SVG_T4 = '''<svg viewBox="0 0 900 310" xmlns="http://www.w3.org/2000/svg"
     style="width:100%;max-width:880px;display:block;margin:0 auto;font-family:'Plus Jakarta Sans',sans-serif;">

  <!-- ══ LEFT MAP: 1995 ══ -->
  <rect x="5" y="5" width="425" height="295" rx="4" fill="#F9F6EE" stroke="#999" stroke-width="1.2"/>
  <text x="217" y="22" text-anchor="middle" font-size="11" font-weight="700" fill="#1a1a2e">Riverside Town Centre, 1995</text>
  <!-- North arrow -->
  <text x="415" y="22" text-anchor="middle" font-size="9" fill="#333">↑</text>
  <text x="415" y="31" text-anchor="middle" font-size="7" fill="#333">N</text>

  <!-- North row: Town Hall, Church, School -->
  <rect x="18" y="32" width="100" height="54" rx="3" fill="#C8D8E8" stroke="#4A6FA5" stroke-width="1.2"/>
  <text x="68" y="57" text-anchor="middle" font-size="9" font-weight="700" fill="#1a1a2e">Town</text>
  <text x="68" y="69" text-anchor="middle" font-size="9" font-weight="700" fill="#1a1a2e">Hall</text>

  <rect x="148" y="32" width="100" height="54" rx="3" fill="#C8D8E8" stroke="#4A6FA5" stroke-width="1.2"/>
  <text x="198" y="63" text-anchor="middle" font-size="9" font-weight="700" fill="#1a1a2e">Church</text>

  <rect x="278" y="32" width="115" height="54" rx="3" fill="#C8D8E8" stroke="#4A6FA5" stroke-width="1.2"/>
  <text x="335" y="63" text-anchor="middle" font-size="9" font-weight="700" fill="#1a1a2e">School</text>

  <!-- Main Street label -->
  <line x1="18" y1="94" x2="393" y2="94" stroke="#aaa" stroke-width="0.8" stroke-dasharray="4,3"/>
  <text x="22" y="108" font-size="7.5" fill="#666" font-style="italic">Main Street →</text>

  <!-- South row 1995: Factory | Open-Air Market | Houses | Empty plot -->
  <rect x="18" y="114" width="88" height="80" rx="3" fill="#C0504D" stroke="#922B21" stroke-width="1.2"/>
  <text x="62" y="152" text-anchor="middle" font-size="9" font-weight="700" fill="#fff">Factory</text>

  <rect x="118" y="114" width="110" height="80" rx="3" fill="#F5CBA7" stroke="#CA6F1E" stroke-width="1.2"/>
  <text x="173" y="148" text-anchor="middle" font-size="9" font-weight="700" fill="#7D3C01">Open-Air</text>
  <text x="173" y="161" text-anchor="middle" font-size="9" font-weight="700" fill="#7D3C01">Market</text>

  <!-- Houses (two small boxes) -->
  <rect x="248" y="114" width="48" height="36" rx="2" fill="#D5D8DC" stroke="#7F8C8D" stroke-width="1.2"/>
  <rect x="248" y="158" width="48" height="36" rx="2" fill="#D5D8DC" stroke="#7F8C8D" stroke-width="1.2"/>
  <text x="272" y="130" text-anchor="middle" font-size="7.5" fill="#1a1a2e">Houses</text>

  <!-- Empty plot (dashed) -->
  <rect x="312" y="114" width="81" height="80" rx="3" fill="none" stroke="#aaa" stroke-width="1.2" stroke-dasharray="5,3"/>
  <text x="352" y="150" text-anchor="middle" font-size="8" fill="#888">Empty</text>
  <text x="352" y="162" text-anchor="middle" font-size="8" fill="#888">plot</text>

  <!-- River -->
  <rect x="18" y="204" width="375" height="30" rx="2" fill="#AED6F1" stroke="#2980B9" stroke-width="1"/>
  <text x="40" y="223" font-size="9" font-weight="700" fill="#1B4F72">River</text>

  <!-- Bridge -->
  <rect x="185" y="200" width="40" height="38" rx="1" fill="#95A5A6" stroke="#717D7E" stroke-width="1"/>
  <text x="205" y="244" text-anchor="middle" font-size="7.5" fill="#555">Bridge</text>

  <!-- ══ RIGHT MAP: 2025 ══ -->
  <rect x="470" y="5" width="425" height="295" rx="4" fill="#F9F6EE" stroke="#999" stroke-width="1.2"/>
  <text x="682" y="22" text-anchor="middle" font-size="11" font-weight="700" fill="#1a1a2e">Riverside Town Centre, 2025</text>
  <!-- North arrow -->
  <text x="880" y="22" text-anchor="middle" font-size="9" fill="#333">↑</text>
  <text x="880" y="31" text-anchor="middle" font-size="7" fill="#333">N</text>

  <!-- North row: unchanged -->
  <rect x="483" y="32" width="100" height="54" rx="3" fill="#C8D8E8" stroke="#4A6FA5" stroke-width="1.2"/>
  <text x="533" y="57" text-anchor="middle" font-size="9" font-weight="700" fill="#1a1a2e">Town</text>
  <text x="533" y="69" text-anchor="middle" font-size="9" font-weight="700" fill="#1a1a2e">Hall</text>

  <rect x="613" y="32" width="100" height="54" rx="3" fill="#C8D8E8" stroke="#4A6FA5" stroke-width="1.2"/>
  <text x="663" y="63" text-anchor="middle" font-size="9" font-weight="700" fill="#1a1a2e">Church</text>

  <rect x="743" y="32" width="115" height="54" rx="3" fill="#C8D8E8" stroke="#4A6FA5" stroke-width="1.2"/>
  <text x="800" y="63" text-anchor="middle" font-size="9" font-weight="700" fill="#1a1a2e">School</text>

  <!-- Main Street label -->
  <line x1="483" y1="94" x2="858" y2="94" stroke="#aaa" stroke-width="0.8" stroke-dasharray="4,3"/>
  <text x="487" y="108" font-size="7.5" fill="#666" font-style="italic">Main Street →</text>

  <!-- South row 2025: Park | Shopping Mall | Apartments | Car Park -->
  <!-- Park (NEW) — green -->
  <rect x="483" y="114" width="88" height="80" rx="3" fill="#A9DFBF" stroke="#1E8449" stroke-width="1.5"/>
  <text x="527" y="148" text-anchor="middle" font-size="8.5" font-weight="700" fill="#145A32">Park</text>
  <text x="527" y="161" text-anchor="middle" font-size="7.5" font-weight="700" fill="#1E8449">(NEW)</text>
  <circle cx="507" cy="172" r="5" fill="#27AE60"/>
  <circle cx="527" cy="174" r="5" fill="#27AE60"/>

  <!-- Shopping Mall (NEW) — orange/amber -->
  <rect x="583" y="114" width="110" height="80" rx="3" fill="#FAD7A0" stroke="#CA6F1E" stroke-width="1.5"/>
  <text x="638" y="146" text-anchor="middle" font-size="8.5" font-weight="700" fill="#784212">Shopping</text>
  <text x="638" y="158" text-anchor="middle" font-size="8.5" font-weight="700" fill="#784212">Mall</text>
  <text x="638" y="170" text-anchor="middle" font-size="7.5" font-weight="700" fill="#CA6F1E">(NEW)</text>

  <!-- Apartments (NEW) — blue-grey -->
  <rect x="705" y="114" width="75" height="80" rx="3" fill="#D6EAF8" stroke="#2471A3" stroke-width="1.5"/>
  <text x="742" y="148" text-anchor="middle" font-size="8.5" font-weight="700" fill="#1A5276">Apartments</text>
  <text x="742" y="160" text-anchor="middle" font-size="7.5" font-weight="700" fill="#2471A3">(NEW)</text>
  <!-- apartment windows -->
  <rect x="712" y="172" width="14" height="9" rx="1" fill="#85C1E9"/>
  <rect x="730" y="172" width="14" height="9" rx="1" fill="#85C1E9"/>
  <rect x="748" y="172" width="14" height="9" rx="1" fill="#85C1E9"/>

  <!-- Car Park (NEW) — hatched grey -->
  <rect x="792" y="114" width="66" height="80" rx="3" fill="#E8DAEF" stroke="#6C3483" stroke-width="1.5"/>
  <text x="825" y="148" text-anchor="middle" font-size="8" font-weight="700" fill="#4A235A">Car</text>
  <text x="825" y="160" text-anchor="middle" font-size="8" font-weight="700" fill="#4A235A">Park</text>
  <text x="825" y="172" text-anchor="middle" font-size="7.5" font-weight="700" fill="#6C3483">(NEW)</text>
  <!-- hatch lines -->
  <line x1="795" y1="118" x2="810" y2="133" stroke="#C39BD3" stroke-width="0.8"/>
  <line x1="805" y1="118" x2="820" y2="133" stroke="#C39BD3" stroke-width="0.8"/>
  <line x1="815" y1="118" x2="830" y2="133" stroke="#C39BD3" stroke-width="0.8"/>
  <line x1="825" y1="118" x2="840" y2="133" stroke="#C39BD3" stroke-width="0.8"/>
  <line x1="835" y1="118" x2="850" y2="133" stroke="#C39BD3" stroke-width="0.8"/>
  <line x1="845" y1="118" x2="855" y2="130" stroke="#C39BD3" stroke-width="0.8"/>

  <!-- River -->
  <rect x="483" y="204" width="375" height="30" rx="2" fill="#AED6F1" stroke="#2980B9" stroke-width="1"/>
  <text x="505" y="223" font-size="9" font-weight="700" fill="#1B4F72">River</text>

  <!-- Bridge (unchanged) -->
  <rect x="650" y="200" width="40" height="38" rx="1" fill="#95A5A6" stroke="#717D7E" stroke-width="1"/>
  <text x="670" y="244" text-anchor="middle" font-size="7.5" fill="#555">Bridge</text>

  <!-- Overall title -->
  <text x="450" y="300" text-anchor="middle" font-size="10" font-weight="700" fill="#444">
    Changes to Riverside Town Centre between 1995 and 2025
  </text>
</svg>'''


def build(n, t1_intro, t1_chart_type, t1_chart_html, t1_chart_js, t1_qdata,
          t2_task_type, t2_prompt_html, t2_qdata):
    qd_js = (
        "const QD = {"
        f"task1:{{prompt:'{t1_qdata['prompt'].replace(chr(39), chr(92)+chr(39))}',chartType:'{t1_qdata['chartType']}'}},"
        f"task2:{{prompt:'{t2_qdata['prompt'].replace(chr(39), chr(92)+chr(39))}',essayType:'{t2_qdata['essayType']}'}}"
        "};"
    )
    return f'''<!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="UTF-8"/>
  <meta name="viewport" content="width=device-width,initial-scale=1.0"/>
  <title>Cambridge 17 · Test {n} — Writing | IELTS Lab</title>
  <script src="https://cdn.tailwindcss.com"></script>
  <script src="https://cdnjs.cloudflare.com/ajax/libs/Chart.js/4.4.0/chart.umd.min.js"></script>
  <link rel="preconnect" href="https://fonts.googleapis.com"/>
  <link rel="preconnect" href="https://fonts.gstatic.com" crossorigin/>
  <link href="https://fonts.googleapis.com/css2?family=Plus+Jakarta+Sans:ital,wght@0,300;0,400;0,500;0,600;1,400&display=swap" rel="stylesheet"/>
  <link href="https://api.fontshare.com/v2/css?f[]=satoshi@400,500,700,900&display=swap" rel="stylesheet"/>
  <link href="https://fonts.googleapis.com/css2?family=Cormorant+Garamond:ital,wght@0,300;0,600;1,300&family=Space+Mono:wght@400;700&display=swap" rel="stylesheet"/>
  <script>tailwind.config={{theme:{{extend:{{fontFamily:{{display:['Satoshi','Plus Jakarta Sans','system-ui','sans-serif'],sans:['Plus Jakarta Sans','system-ui','sans-serif']}}}}}}}}</script>
  <style>
    :root{{--gold:#C9952E;--gold-light:#DDB05A;--gold-dim:rgba(201,149,46,0.10);--gold-border:rgba(201,149,46,0.22);--white:#EEF4FF;}}
    *,*::before,*::after{{box-sizing:border-box;margin:0;padding:0;}}
    html{{background:#09090b;color:#fafafa;}}
    body{{font-family:'Plus Jakarta Sans',system-ui,sans-serif;-webkit-font-smoothing:antialiased;overflow-x:hidden;}}
    h1,h2,h3,.font-display{{font-family:'Satoshi','Plus Jakarta Sans',system-ui,sans-serif;}}
    ::-webkit-scrollbar{{width:5px;}} ::-webkit-scrollbar-track{{background:#09090b;}} ::-webkit-scrollbar-thumb{{background:#3f3f46;border-radius:3px;}}
    .nav-glass{{background:rgba(9,9,11,0.92);backdrop-filter:blur(20px);border-bottom:1px solid rgba(255,255,255,0.04);}}
    .nl-ielts{{font-family:'Cormorant Garamond',serif;font-size:20px;font-weight:600;letter-spacing:1px;color:var(--white);}}
    .nl-lab{{font-family:'Space Mono',monospace;font-size:12px;font-weight:700;letter-spacing:3px;color:var(--gold);margin-left:5px;filter:drop-shadow(0 0 6px rgba(201,149,46,0.5));}}
    .progress-bar{{height:3px;background:#18181b;position:fixed;top:64px;left:0;right:0;z-index:40;}}
    .progress-fill{{height:100%;background:linear-gradient(to right,var(--gold),#DDB05A);transition:width 1s linear;width:0%;}}
    .timer-box{{background:rgba(17,17,19,0.95);border:1px solid #1c1c1e;border-radius:0.75rem;padding:10px 18px;font-family:'Space Mono',monospace;font-size:1.25rem;font-weight:700;color:#fafafa;letter-spacing:2px;box-shadow:0 4px 20px rgba(0,0,0,0.4);}}
    .timer-box.warning{{color:#fbbf24;border-color:rgba(251,191,36,0.3);}}
    .timer-box.critical{{color:#f87171;border-color:rgba(248,113,113,0.3);animation:pulse 1s ease-in-out infinite;}}
    @keyframes pulse{{0%,100%{{opacity:1}}50%{{opacity:0.7}}}}
    .section-card{{background:rgba(17,17,19,0.7);border:1px solid #1c1c1e;border-radius:1.25rem;padding:1.75rem;}}
    .answer-area{{width:100%;background:#0c0c0e;border:1px solid #27272a;border-radius:0.75rem;padding:1rem;color:#e4e4e7;font-size:0.9375rem;line-height:1.75;resize:vertical;font-family:'Plus Jakarta Sans',system-ui,sans-serif;transition:border-color 0.2s;min-height:200px;}}
    .answer-area:focus{{outline:none;border-color:var(--gold-border);}}
    .word-counter{{font-size:0.75rem;font-family:'Space Mono',monospace;}}
    .word-counter.under{{color:#71717a;}} .word-counter.ok{{color:#4ade80;}} .word-counter.good{{color:var(--gold);}}
    .btn-gold{{background:linear-gradient(135deg,var(--gold) 0%,#a8741f 100%);color:#05081A;border:none;border-radius:0.5rem;padding:12px 32px;font-size:0.875rem;font-weight:700;letter-spacing:0.04em;cursor:pointer;transition:all 0.25s ease;box-shadow:0 0 20px rgba(201,149,46,0.25);}}
    .btn-gold:hover{{transform:translateY(-2px);box-shadow:0 0 32px rgba(201,149,46,0.45);}}
    .submit-overlay{{position:fixed;inset:0;z-index:300;display:flex;flex-direction:column;align-items:center;justify-content:center;background:rgba(9,9,11,0.97);}}
    .submit-overlay.hidden{{display:none;}}
    @keyframes spin{{to{{transform:rotate(360deg)}}}}
    .spinner{{width:40px;height:40px;border:3px solid #27272a;border-top-color:var(--gold);border-radius:50%;animation:spin 0.8s linear infinite;}}
    .task-prompt{{margin-bottom:1.25rem;padding:1rem 1.25rem;border-radius:0.875rem;border-left:3px solid var(--gold);background:rgba(201,149,46,0.06);}}
    .task-prompt .intro{{font-size:1rem;color:#e4e4e7;line-height:1.7;margin-bottom:0.5rem;font-weight:600;}}
    .task-prompt .rubric{{font-size:0.875rem;color:#a1a1aa;font-style:italic;line-height:1.6;margin-bottom:0.4rem;}}
    .task-prompt .word-req{{font-size:0.8rem;font-weight:700;color:var(--gold);}}
    .chart-area{{background:#fff;border-radius:0.875rem;padding:1.25rem 1rem 1rem;margin-bottom:1.25rem;border:1px solid rgba(201,149,46,0.2);}}
    .chart-area-title{{font-family:'Satoshi','Plus Jakarta Sans',sans-serif;font-size:0.8rem;font-weight:700;color:#0D2B4E;text-align:center;margin-bottom:0.75rem;}}
    .data-table{{width:100%;border-collapse:collapse;font-size:0.78rem;margin-top:1rem;}}
    .data-table th{{background:#EEF3FB;color:#0D2B4E;font-weight:700;padding:6px 10px;text-align:left;border-bottom:2px solid #0D2B4E;font-size:0.72rem;letter-spacing:0.04em;}}
    .data-table td{{padding:5px 10px;border-bottom:1px solid #E4E0D6;color:#1a1a2e;}}
    .data-table tr:last-child td{{border-bottom:none;}}
    .data-table tr:nth-child(even) td{{background:#F9F6F0;}}
    .t2-body{{font-size:1rem;color:#e4e4e7;line-height:1.7;margin-bottom:0.75rem;}}
    .t2-question{{font-size:1rem;font-weight:700;color:var(--gold-light);line-height:1.6;margin-bottom:0.5rem;}}
    .t2-rubric{{font-size:0.875rem;color:#a1a1aa;font-style:italic;}}
    #themeToggle{{background:transparent;border:1px solid rgba(201,149,46,0.25);color:#71717a;border-radius:8px;width:34px;height:34px;display:flex;align-items:center;justify-content:center;cursor:pointer;transition:all 0.2s;font-size:15px;flex-shrink:0;padding:0;}}
    #themeToggle:hover{{border-color:var(--gold-border);color:var(--gold);}}
    html[data-theme="light"]{{background:#F4F1EB !important;color:#1C1C2E !important;}}
    html[data-theme="light"] body{{background:#F4F1EB !important;}}
    html[data-theme="light"] .nav-glass{{background:rgba(244,241,235,0.94) !important;border-bottom-color:rgba(0,0,0,0.08) !important;}}
    html[data-theme="light"] .nl-ielts{{color:#1C1C2E !important;}}
    html[data-theme="light"] .section-card{{background:rgba(255,255,255,0.95) !important;border-color:#E4E0D6 !important;}}
    html[data-theme="light"] .timer-box{{background:#FFF !important;border-color:#D4D0C8 !important;color:#1C1C2E !important;}}
    html[data-theme="light"] .answer-area{{background:#F9F6F0 !important;border-color:#D4D0C8 !important;color:#1C1C2E !important;}}
    html[data-theme="light"] .task-prompt{{background:rgba(201,149,46,0.04) !important;}}
    html[data-theme="light"] .task-prompt .intro{{color:#1C1C2E !important;}}
    html[data-theme="light"] .task-prompt .rubric{{color:#585862 !important;}}
    html[data-theme="light"] .t2-body{{color:#1C1C2E !important;}}
    html[data-theme="light"] .t2-rubric{{color:#585862 !important;}}
    html[data-theme="light"] .submit-overlay{{background:rgba(244,241,235,0.97) !important;}}
    html[data-theme="light"] .spinner{{border-color:#D4D0C8 !important;border-top-color:var(--gold) !important;}}
    html[data-theme="light"] .progress-bar{{background:#E4E0D6 !important;}}
    html[data-theme="light"] ::-webkit-scrollbar-track{{background:#F4F1EB !important;}}
    html[data-theme="light"] ::-webkit-scrollbar-thumb{{background:#C4B07A !important;}}
  </style>
  <script>(function(){{var t=localStorage.getItem('ieltslab_theme')||'dark';document.documentElement.setAttribute('data-theme',t);}})();</script>
</head>
<body class="bg-zinc-950 text-zinc-50 min-h-screen flex flex-col">
  <div class="progress-bar"><div class="progress-fill" id="progressFill"></div></div>
  <nav class="nav-glass sticky top-0 z-50 h-16 flex items-center px-6">
    <div class="flex items-center justify-between w-full max-w-5xl mx-auto">
      <a href="../IELTS-Lab.html" class="flex items-baseline gap-0 no-underline">
        <span class="nl-ielts">IELTS</span><span class="nl-lab">LAB</span>
      </a>
      <div class="flex items-center gap-4">
        <span class="text-xs text-zinc-500 hidden sm:block">Cambridge 17 · Test {n} · Writing</span>
        <div class="timer-box" id="timerDisplay">60:00</div>
        <button id="themeToggle" onclick="toggleTheme()" title="Toggle theme">☀</button>
      </div>
    </div>
  </nav>
  <div class="submit-overlay hidden" id="submittingOverlay">
    <div class="spinner mb-6"></div>
    <div class="font-display font-bold text-zinc-200 text-xl mb-2">Grading Your Responses</div>
    <p class="text-sm text-zinc-500 max-w-xs text-center">Our AI examiner is analysing your writing using official IELTS band descriptors…</p>
  </div>
  <main class="flex-1 max-w-4xl mx-auto px-4 sm:px-6 py-8 w-full">
    <div class="flex flex-wrap items-start justify-between gap-4 mb-8">
      <div>
        <div class="text-xs font-medium tracking-widest uppercase mb-1" style="color:var(--gold);">✏️ Writing · Academic</div>
        <h1 class="font-display font-black text-2xl text-zinc-100">Cambridge IELTS 17 — Test {n}</h1>
        <p class="text-xs text-zinc-500 mt-1">Task 2 type: {t2_task_type}</p>
      </div>
      <div class="flex items-center gap-6 text-xs text-zinc-600 mt-1">
        <div>Task 1 <span class="text-zinc-500">~20 min · 150+ words</span></div>
        <div>Task 2 <span class="text-zinc-500">~40 min · 250+ words</span></div>
      </div>
    </div>
    <!-- TASK 1 -->
    <div class="section-card mb-6">
      <div class="flex items-center gap-3 mb-5">
        <span class="inline-flex items-center justify-center w-8 h-8 rounded-full text-sm font-bold"
              style="background:var(--gold-dim);border:1px solid var(--gold-border);color:var(--gold);">1</span>
        <div>
          <div class="font-display font-bold text-zinc-100">Task 1 — {t1_chart_type}</div>
          <div class="text-xs text-zinc-500">Minimum 150 words · ~20 minutes</div>
        </div>
      </div>
      <div class="task-prompt">
        <p class="intro">{t1_intro}</p>
        <p class="rubric">Summarise the information by selecting and reporting the main features, and make comparisons where relevant.</p>
        <p class="word-req">Write at least 150 words.</p>
      </div>
      <div class="chart-area">{t1_chart_html}</div>
      <textarea id="task1Answer" class="answer-area" placeholder="Write your Task 1 response here…" oninput="updateWordCount('task1')"></textarea>
      <div class="flex justify-between items-center mt-2">
        <div class="word-counter under" id="task1Counter">0 words</div>
        <div class="text-xs text-zinc-700">Minimum: 150 words</div>
      </div>
    </div>
    <!-- TASK 2 -->
    <div class="section-card mb-8">
      <div class="flex items-center gap-3 mb-5">
        <span class="inline-flex items-center justify-center w-8 h-8 rounded-full text-sm font-bold"
              style="background:var(--gold-dim);border:1px solid var(--gold-border);color:var(--gold);">2</span>
        <div>
          <div class="font-display font-bold text-zinc-100">Task 2 — Essay</div>
          <div class="text-xs text-zinc-500">Minimum 250 words · ~40 minutes · {t2_task_type}</div>
        </div>
      </div>
      <div class="task-prompt" style="border-left-color:#3A7BF7;">
        {t2_prompt_html}
        <p class="word-req" style="margin-top:0.6rem;">Write at least 250 words.</p>
      </div>
      <textarea id="task2Answer" class="answer-area" style="min-height:280px;" placeholder="Write your Task 2 essay here…" oninput="updateWordCount('task2')"></textarea>
      <div class="flex justify-between items-center mt-2">
        <div class="word-counter under" id="task2Counter">0 words</div>
        <div class="text-xs text-zinc-700">Minimum: 250 words</div>
      </div>
    </div>
    <div class="flex justify-center mb-16">
      <button onclick="confirmSubmit()" class="btn-gold px-12">Submit Writing Test</button>
    </div>
  </main>
  <div id="timesUpModal" style="display:none;position:fixed;inset:0;background:rgba(0,0,0,0.85);z-index:250;align-items:center;justify-content:center;">
    <div style="background:#111113;border:1px solid #27272a;border-radius:1.25rem;padding:2rem;max-width:400px;width:90%;text-align:center;">
      <div style="font-size:2.5rem;margin-bottom:1rem;">⏰</div>
      <div class="font-display font-bold text-xl" style="color:#fafafa;margin-bottom:0.5rem;">Time's Up!</div>
      <p style="font-size:0.875rem;color:#71717a;margin-bottom:1.5rem;">Your 60 minutes are up.</p>
      <button onclick="submitTest()" class="btn-gold w-full">Submit &amp; See Results</button>
    </div>
  </div>
  <script>
    var raw = localStorage.getItem('ielts_session');
    if (!raw) window.location.replace('../login.html');
    try {{ JSON.parse(raw); }} catch(e) {{ localStorage.removeItem('ielts_session'); window.location.replace('../login.html'); }}
    {qd_js}
    function toggleTheme() {{
      var c = document.documentElement.getAttribute('data-theme') || 'dark';
      var n = c === 'dark' ? 'light' : 'dark';
      document.documentElement.setAttribute('data-theme', n);
      localStorage.setItem('ieltslab_theme', n);
      var b = document.getElementById('themeToggle');
      if (b) b.textContent = n === 'dark' ? '☀' : '🌙';
    }}
    document.addEventListener('DOMContentLoaded', function() {{
      var b = document.getElementById('themeToggle');
      if (b) b.textContent = (document.documentElement.getAttribute('data-theme') || 'dark') === 'dark' ? '☀' : '🌙';
    }});
    window.addEventListener('load', function() {{
      {t1_chart_js}
    }});
    var TOTAL = 3600, left = TOTAL;
    var tmr = setInterval(function() {{
      left--;
      var m = Math.floor(left / 60), s = left % 60;
      document.getElementById('timerDisplay').textContent = String(m).padStart(2,'0') + ':' + String(s).padStart(2,'0');
      document.getElementById('progressFill').style.width = ((TOTAL - left) / TOTAL * 100) + '%';
      var el = document.getElementById('timerDisplay');
      if (left <= 300) el.className = 'timer-box critical';
      else if (left <= 600) el.className = 'timer-box warning';
      if (left <= 0) {{ clearInterval(tmr); document.getElementById('timesUpModal').style.display = 'flex'; }}
    }}, 1000);
    function countWords(t) {{ return t.trim() === '' ? 0 : t.trim().split(/\s+/).length; }}
    function updateWordCount(task) {{
      var ta = document.getElementById(task + 'Answer');
      var ct = document.getElementById(task + 'Counter');
      var min = task === 'task1' ? 150 : 250;
      var n = countWords(ta.value);
      ct.textContent = n + ' words';
      ct.className = 'word-counter ' + (n >= min ? (n >= min * 1.3 ? 'good' : 'ok') : 'under');
    }}
    function confirmSubmit() {{
      if (!confirm("Submit your writing test now?\\nYou cannot go back after this.")) return;
      submitTest();
    }}
    async function submitTest() {{
      document.getElementById('timesUpModal').style.display = 'none';
      clearInterval(tmr);
      var a1 = document.getElementById('task1Answer').value;
      var a2 = document.getElementById('task2Answer').value;
      if (!a1.trim() && !a2.trim()) {{ alert('Please write at least something before submitting.'); return; }}
      document.getElementById('submittingOverlay').classList.remove('hidden');
      try {{
        var res = await fetch('/api/mock/grade', {{
          method: 'POST',
          headers: {{'Content-Type': 'application/json'}},
          body: JSON.stringify({{ skill: 'writing', trainingType: 'academic', question: QD, answers: {{ task1: a1, task2: a2 }} }})
        }});
        if (!res.ok) throw new Error('HTTP ' + res.status);
        var result = await res.json();
        var rid = Date.now().toString();
        var saved = {{
          id: rid, date: Date.now(), book: 17, testNum: {n},
          skill: 'writing', trainingType: 'academic',
          testType: 'Writing — Cambridge 17 · Test {n}',
          scores: {{ writing: result.overall_band, overall: result.overall_band }},
          feedback: result, question: QD, answers: {{ task1: a1, task2: a2 }}
        }};
        var ex = JSON.parse(localStorage.getItem('ielts_mock_results') || '[]');
        ex.push(saved);
        localStorage.setItem('ielts_mock_results', JSON.stringify(ex));
        window.location.href = 'results.html?id=' + rid;
      }} catch (err) {{
        document.getElementById('submittingOverlay').classList.add('hidden');
        alert('Grading failed: ' + err.message + '\\n\\nPlease try again.');
      }}
    }}
  </script>
</body>
</html>'''


# ════════════════════════════════════════════════════════════════════════════
# TEST 1 — Line graph: birth rate in 4 countries, 1960–2020
# ════════════════════════════════════════════════════════════════════════════
T1_CHART_HTML = '''
<div class="chart-area-title">Birth Rate (Live Births per 1,000 People) in Four Countries, 1960–2020</div>
<div style="position:relative;height:240px;">
  <canvas id="chartT1" style="width:100%;height:100%;"></canvas>
</div>'''

T1_CHART_JS = """
  var ctx1 = document.getElementById('chartT1');
  if (ctx1) {
    new Chart(ctx1.getContext('2d'), {
      type: 'line',
      data: {
        labels: ['1960','1980','2000','2020'],
        datasets: [
          {
            label: 'Italy',
            data: [19, 11, 9.5, 6.8],
            borderColor: '#1565C0', backgroundColor: 'rgba(21,101,192,0.07)',
            borderWidth: 2.5, pointRadius: 5, pointBackgroundColor: '#fff',
            pointBorderColor: '#1565C0', pointBorderWidth: 2.5, tension: 0.2
          },
          {
            label: 'South Korea',
            data: [42, 22, 15, 5.3],
            borderColor: '#C62828', backgroundColor: 'rgba(198,40,40,0.07)',
            borderWidth: 2.5, pointRadius: 5, pointBackgroundColor: '#fff',
            pointBorderColor: '#C62828', pointBorderWidth: 2.5, tension: 0.2,
            borderDash: [5,3]
          },
          {
            label: 'Egypt',
            data: [44, 38, 26, 22],
            borderColor: '#E65100', backgroundColor: 'rgba(230,81,0,0.07)',
            borderWidth: 2.5, pointRadius: 5, pointBackgroundColor: '#fff',
            pointBorderColor: '#E65100', pointBorderWidth: 2.5, tension: 0.2
          },
          {
            label: 'USA',
            data: [24, 16.5, 14.5, 11],
            borderColor: '#2E7D32', backgroundColor: 'rgba(46,125,50,0.07)',
            borderWidth: 2.5, pointRadius: 5, pointBackgroundColor: '#fff',
            pointBorderColor: '#2E7D32', pointBorderWidth: 2.5, tension: 0.2,
            borderDash: [5,3]
          }
        ]
      },
      options: {
        responsive: true, maintainAspectRatio: false,
        plugins: {
          legend: { position:'top', labels:{ boxWidth:13, font:{ size:11 } } }
        },
        scales: {
          x: { title:{ display:true, text:'Year', font:{ weight:'bold', size:11 } }, grid:{ color:'rgba(0,0,0,0.05)' } },
          y: {
            min: 0, max: 50,
            title:{ display:true, text:'Births per 1,000 people', font:{ weight:'bold', size:11 } },
            grid:{ color:'rgba(0,0,0,0.05)' },
            ticks:{ stepSize:10 }
          }
        }
      }
    });
  }"""

T1_QDATA = {
    'prompt': 'The graph below shows the birth rate (live births per 1,000 people) in four countries between 1960 and 2020. Summarise the information by selecting and reporting the main features, and make comparisons where relevant. Write at least 150 words.',
    'chartType': 'Multi-line graph',
}
T1_T2_QDATA = {
    'prompt': 'In many developed countries, the birth rate has fallen sharply and the population is ageing rapidly. Some people believe that governments should introduce policies to encourage families to have more children, while others think this is not the role of the government. Discuss both views and give your own opinion.',
    'essayType': 'Discussion (Both Views + Opinion)',
}

# ════════════════════════════════════════════════════════════════════════════
# TEST 2 — Grouped bar chart: male/female enrolment by field, Country C, 2023
# ════════════════════════════════════════════════════════════════════════════
T2_CHART_HTML = '''
<div class="chart-area-title">Percentage of University Students by Field of Study and Gender, Country C, 2023</div>
<div style="position:relative;height:240px;">
  <canvas id="chartT2" style="width:100%;height:100%;"></canvas>
</div>
<table class="data-table" style="margin-top:1rem;">
  <thead><tr><th>Field of study</th><th>Male students (%)</th><th>Female students (%)</th></tr></thead>
  <tbody>
    <tr><td>Engineering</td><td>78</td><td>22</td></tr>
    <tr><td>Computer science</td><td>71</td><td>29</td></tr>
    <tr><td>Business</td><td>54</td><td>46</td></tr>
    <tr><td>Medicine &amp; health</td><td>38</td><td>62</td></tr>
    <tr><td>Education</td><td>22</td><td>78</td></tr>
    <tr><td>Arts &amp; humanities</td><td>35</td><td>65</td></tr>
  </tbody>
</table>'''

T2_CHART_JS = """
  var ctx2 = document.getElementById('chartT2');
  if (ctx2) {
    new Chart(ctx2.getContext('2d'), {
      type: 'bar',
      data: {
        labels: ['Engineering','Computer science','Business','Medicine & health','Education','Arts & humanities'],
        datasets: [
          { label:'Male',   data:[78,71,54,38,22,35], backgroundColor:'rgba(21,101,192,0.85)',  borderColor:'#1565C0', borderWidth:1 },
          { label:'Female', data:[22,29,46,62,78,65], backgroundColor:'rgba(198,40,40,0.85)',   borderColor:'#C62828', borderWidth:1 }
        ]
      },
      options: {
        responsive: true, maintainAspectRatio: false,
        plugins: { legend:{ position:'top', labels:{ boxWidth:13, font:{ size:11 } } } },
        scales: {
          x: { title:{ display:true, text:'Field of study', font:{ weight:'bold', size:11 } }, grid:{ display:false }, ticks:{ font:{ size:8.5 } } },
          y: { min:0, max:90, title:{ display:true, text:'Percentage of students (%)', font:{ weight:'bold', size:11 } }, grid:{ color:'rgba(0,0,0,0.05)' }, ticks:{ stepSize:10 } }
        }
      }
    });
  }"""

T2_QDATA = {
    'prompt': 'The bar chart below shows the percentage of male and female students enrolled in six different fields of study at universities in Country C in 2023. Summarise the information by selecting and reporting the main features, and make comparisons where relevant. Write at least 150 words.',
    'chartType': 'Grouped bar chart',
}
T2_T2_QDATA = {
    'prompt': 'In some countries, men and women still tend to choose very different subjects at university and end up in very different careers. What are the reasons for this pattern, and what can be done to encourage more balanced participation in different fields?',
    'essayType': 'Causes / Solutions',
}

# ════════════════════════════════════════════════════════════════════════════
# TEST 3 — Two pie charts: news sources, City D, 2005 vs 2025
# ════════════════════════════════════════════════════════════════════════════
T3_CHART_HTML = '''
<div class="chart-area-title">Main Sources of News for Adults in City D, 2005 vs 2025</div>
<div style="display:flex;gap:1.5rem;flex-wrap:wrap;justify-content:center;align-items:flex-start;">
  <div style="flex:1;min-width:200px;max-width:270px;">
    <div style="text-align:center;font-weight:700;font-size:0.85rem;color:#0D2B4E;margin-bottom:0.4rem;">2005</div>
    <div style="position:relative;height:210px;">
      <canvas id="chartT3a" style="width:100%;height:100%;"></canvas>
    </div>
  </div>
  <div style="flex:1;min-width:200px;max-width:270px;">
    <div style="text-align:center;font-weight:700;font-size:0.85rem;color:#0D2B4E;margin-bottom:0.4rem;">2025</div>
    <div style="position:relative;height:210px;">
      <canvas id="chartT3b" style="width:100%;height:100%;"></canvas>
    </div>
  </div>
</div>'''

T3_CHART_JS = """
  var pieColors3 = ['#1565C0','#424242','#E65100','#2E7D32','#9C27B0','#F57F17'];
  var pieLabels3 = ['Television','Newspapers (print)','Radio','News websites','Social media','Podcasts'];
  function makePieNews(id, data) {
    var el = document.getElementById(id);
    if (!el) return;
    new Chart(el.getContext('2d'), {
      type: 'pie',
      data: { labels: pieLabels3, datasets: [{ data: data, backgroundColor: pieColors3, borderColor: '#fff', borderWidth: 2 }] },
      options: {
        responsive: true, maintainAspectRatio: false,
        plugins: {
          legend: { position:'bottom', labels:{ boxWidth:10, font:{ size:8 } } },
          tooltip: { callbacks: { label: function(c){ return ' '+c.label+': '+c.parsed+'%'; } } }
        }
      }
    });
  }
  makePieNews('chartT3a', [48, 28, 14, 6, 3, 1]);
  makePieNews('chartT3b', [22,  5,  8, 24, 33, 8]);"""

T3_QDATA = {
    'prompt': 'The pie charts below show the main sources of news for adults in City D in 2005 and 2025. Summarise the information by selecting and reporting the main features, and make comparisons where relevant. Write at least 150 words.',
    'chartType': 'Two pie charts',
}
T3_T2_QDATA = {
    'prompt': 'Today, more and more people get their news from social media rather than from traditional sources such as newspapers and television. Is this a positive or negative development?',
    'essayType': 'Positive / Negative Development',
}

# ════════════════════════════════════════════════════════════════════════════
# TEST 4 — Map comparison: Riverside Town Centre 1995 vs 2025
# ════════════════════════════════════════════════════════════════════════════
T4_CHART_HTML = f'''
<div class="chart-area-title">Changes to Riverside Town Centre between 1995 and 2025</div>
{SVG_T4}'''

T4_CHART_JS = ""

T4_QDATA = {
    'prompt': 'The maps below show the centre of Riverside town in 1995 and how it had changed by 2025. Summarise the information by selecting and reporting the main features, and make comparisons where relevant. Write at least 150 words.',
    'chartType': 'Map comparison (two periods)',
}
T4_T2_QDATA = {
    'prompt': 'In many towns and cities, traditional buildings, small shops and open markets are being replaced by modern apartment blocks, shopping malls and car parks. Some people see this as progress, while others see it as a loss of culture and community. Do the advantages of this kind of urban development outweigh the disadvantages?',
    'essayType': 'Advantages / Disadvantages',
}

# ════════════════════════════════════════════════════════════════════════════
FILES = [
    (1,
     'The graph below shows the birth rate (live births per 1,000 people) in four countries between 1960 and 2020.',
     'Multi-Line Graph', T1_CHART_HTML, T1_CHART_JS, T1_QDATA,
     'Discussion (Both Views + Opinion)',
     '''<p class="t2-body">In many developed countries, the birth rate has fallen sharply and the population is ageing rapidly. Some people believe that governments should introduce policies to encourage families to have more children, while others think this is not the role of the government.</p>
     <p class="t2-question">Discuss both views and give your own opinion.</p>
     <p class="t2-rubric">Give reasons for your answer and include any relevant examples from your own knowledge or experience.</p>''',
     T1_T2_QDATA),

    (2,
     'The bar chart below shows the percentage of male and female students enrolled in six different fields of study at universities in Country C in 2023.',
     'Grouped Bar Chart + Data Table', T2_CHART_HTML, T2_CHART_JS, T2_QDATA,
     'Causes / Solutions',
     '''<p class="t2-body">In some countries, men and women still tend to choose very different subjects at university and end up in very different careers.</p>
     <p class="t2-question">What are the reasons for this pattern, and what can be done to encourage more balanced participation in different fields?</p>
     <p class="t2-rubric">Give reasons for your answer and include any relevant examples from your own knowledge or experience.</p>''',
     T2_T2_QDATA),

    (3,
     'The pie charts below show the main sources of news for adults in City D in 2005 and 2025.',
     'Two Pie Charts', T3_CHART_HTML, T3_CHART_JS, T3_QDATA,
     'Positive / Negative Development',
     '''<p class="t2-body">Today, more and more people get their news from social media rather than from traditional sources such as newspapers and television.</p>
     <p class="t2-question">Is this a positive or negative development?</p>
     <p class="t2-rubric">Give reasons for your answer and include any relevant examples from your own knowledge or experience.</p>''',
     T3_T2_QDATA),

    (4,
     'The maps below show the centre of Riverside town in 1995 and how it had changed by 2025.',
     'Map Comparison', T4_CHART_HTML, T4_CHART_JS, T4_QDATA,
     'Advantages / Disadvantages',
     '''<p class="t2-body">In many towns and cities, traditional buildings, small shops and open markets are being replaced by modern apartment blocks, shopping malls and car parks. Some people see this as progress, while others see it as a loss of culture and community.</p>
     <p class="t2-question">Do the advantages of this kind of urban development outweigh the disadvantages?</p>
     <p class="t2-rubric">Give reasons for your answer and include any relevant examples from your own knowledge or experience.</p>''',
     T4_T2_QDATA),
]

if __name__ == '__main__':
    for (n, t1_intro, t1_type, t1_chart_html, t1_chart_js, t1_qd, t2_type, t2_html, t2_qd) in FILES:
        html = build(n, t1_intro, t1_type, t1_chart_html, t1_chart_js, t1_qd, t2_type, t2_html, t2_qd)
        path = os.path.join(BASE, f'cam17-t{n}-writing.html')
        with open(path, 'w', encoding='utf-8') as f:
            f.write(html)
        print(f'Written: {path}  ({len(html):,} chars)')
    print('Done.')
