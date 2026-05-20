#!/usr/bin/env python3
"""
Generate cam19-t{1..4}-writing.html
Content from Cambridge IELTS 20 Volume 2 PDF (used for Cambridge 19 slot)
Charts: Chart.js (line / bar / pie) + SVG maps for Test 4
All chart init runs in window.onload.
"""
import os

BASE = '/Users/ayoubelhebaze/Downloads/claude md/mock-tests'

# ─── SVG: Greenfield University Campus maps (Test 4) ─────────────────────────
SVG_T4 = '''<svg viewBox="0 0 900 370" xmlns="http://www.w3.org/2000/svg"
     style="width:100%;max-width:860px;display:block;margin:0 auto;font-family:'Plus Jakarta Sans',sans-serif;">

  <!-- ── 2005 MAP (left) ──────────────────────────────── -->
  <text x="210" y="18" text-anchor="middle" font-size="11" font-weight="700" fill="#0D2B4E">Greenfield University Campus, 2005</text>

  <!-- outer border -->
  <rect x="20" y="26" width="380" height="310" rx="4" fill="#F9F6F0" stroke="#999" stroke-width="1.2"/>

  <!-- North arrow -->
  <text x="385" y="42" text-anchor="middle" font-size="9" fill="#555">&#8593;</text>
  <text x="385" y="52" text-anchor="middle" font-size="8" fill="#555">N</text>

  <!-- TOP ROW buildings -->
  <rect x="35"  y="40" width="95" height="70" rx="4" fill="#DBEAFE" stroke="#1565C0" stroke-width="1.3"/>
  <text x="82"  y="72" text-anchor="middle" font-size="9" font-weight="700" fill="#1565C0">Main</text>
  <text x="82"  y="84" text-anchor="middle" font-size="9" font-weight="700" fill="#1565C0">Building</text>

  <rect x="145" y="40" width="95" height="70" rx="4" fill="#DBEAFE" stroke="#1565C0" stroke-width="1.3"/>
  <text x="192" y="79" text-anchor="middle" font-size="9" font-weight="700" fill="#1565C0">Library</text>

  <rect x="255" y="40" width="95" height="70" rx="4" fill="#DBEAFE" stroke="#1565C0" stroke-width="1.3"/>
  <text x="302" y="79" text-anchor="middle" font-size="9" font-weight="700" fill="#1565C0">Cafeteria</text>

  <!-- Main Road -->
  <rect x="20" y="122" width="380" height="22" fill="#E5E7EB" stroke="none"/>
  <text x="50" y="137" font-size="8" fill="#6B7280">Main Road &#8594;</text>

  <!-- BOTTOM ROW -->
  <!-- Car Park (hatched) -->
  <rect x="35" y="156" width="120" height="130" rx="4" fill="url(#hatch2005)" stroke="#6B7280" stroke-width="1.3"/>
  <text x="95" y="218" text-anchor="middle" font-size="9" font-weight="700" fill="#374151">Car Park</text>

  <!-- Open Field -->
  <rect x="172" y="156" width="178" height="130" rx="4" fill="#D1FAE5" stroke="#059669" stroke-width="1.3"/>
  <text x="261" y="218" text-anchor="middle" font-size="9" font-weight="700" fill="#065F46">Open Field</text>

  <!-- Entrance -->
  <rect x="188" y="296" width="44" height="14" rx="2" fill="#9CA3AF"/>
  <text x="210" y="336" text-anchor="middle" font-size="8" fill="#374141">Entrance</text>

  <!-- hatch pattern for car parks -->
  <defs>
    <pattern id="hatch2005" patternUnits="userSpaceOnUse" width="8" height="8" patternTransform="rotate(45)">
      <line x1="0" y1="0" x2="0" y2="8" stroke="#9CA3AF" stroke-width="2"/>
    </pattern>
    <pattern id="hatch2025" patternUnits="userSpaceOnUse" width="8" height="8" patternTransform="rotate(45)">
      <line x1="0" y1="0" x2="0" y2="8" stroke="#9CA3AF" stroke-width="2"/>
    </pattern>
  </defs>

  <!-- ── 2025 MAP (right) ──────────────────────────────── -->
  <text x="700" y="18" text-anchor="middle" font-size="11" font-weight="700" fill="#0D2B4E">Greenfield University Campus, 2025</text>

  <!-- outer border -->
  <rect x="510" y="26" width="380" height="310" rx="4" fill="#F9F6F0" stroke="#999" stroke-width="1.2"/>

  <!-- North arrow -->
  <text x="875" y="42" text-anchor="middle" font-size="9" fill="#555">&#8593;</text>
  <text x="875" y="52" text-anchor="middle" font-size="8" fill="#555">N</text>

  <!-- TOP ROW -->
  <rect x="525" y="40" width="95" height="70" rx="4" fill="#DBEAFE" stroke="#1565C0" stroke-width="1.3"/>
  <text x="572" y="72" text-anchor="middle" font-size="9" font-weight="700" fill="#1565C0">Main</text>
  <text x="572" y="84" text-anchor="middle" font-size="9" font-weight="700" fill="#1565C0">Building</text>

  <rect x="635" y="40" width="95" height="70" rx="4" fill="#DBEAFE" stroke="#1565C0" stroke-width="1.3"/>
  <text x="682" y="79" text-anchor="middle" font-size="9" font-weight="700" fill="#1565C0">Library</text>

  <!-- Student Centre (expanded, was Cafeteria) -->
  <rect x="745" y="40" width="110" height="70" rx="4" fill="#FEF3C7" stroke="#D97706" stroke-width="1.8"/>
  <text x="800" y="65" text-anchor="middle" font-size="8.5" font-weight="700" fill="#92400E">Student</text>
  <text x="800" y="77" text-anchor="middle" font-size="8.5" font-weight="700" fill="#92400E">Centre</text>
  <text x="800" y="89" text-anchor="middle" font-size="7.5" fill="#B45309">(expanded)</text>

  <!-- Main Road -->
  <rect x="510" y="122" width="380" height="22" fill="#E5E7EB"/>
  <text x="540" y="137" font-size="8" fill="#6B7280">Main Road &#8594;</text>

  <!-- BOTTOM ROW -->
  <!-- Car Park reduced -->
  <rect x="525" y="156" width="72" height="130" rx="4" fill="url(#hatch2025)" stroke="#6B7280" stroke-width="1.3"/>
  <text x="561" y="210" text-anchor="middle" font-size="7.5" font-weight="700" fill="#374151">Car Park</text>
  <text x="561" y="222" text-anchor="middle" font-size="7" fill="#6B7280">(reduced)</text>

  <!-- Science Block NEW -->
  <rect x="610" y="156" width="88" height="60" rx="4" fill="#FCE7F3" stroke="#BE185D" stroke-width="1.8"/>
  <text x="654" y="181" text-anchor="middle" font-size="8" font-weight="700" fill="#9D174D">Science</text>
  <text x="654" y="193" text-anchor="middle" font-size="8" font-weight="700" fill="#9D174D">Block</text>
  <text x="654" y="205" text-anchor="middle" font-size="7" fill="#BE185D">(NEW)</text>

  <!-- Sports Hall NEW -->
  <rect x="610" y="226" width="88" height="60" rx="4" fill="#FCE7F3" stroke="#BE185D" stroke-width="1.8"/>
  <text x="654" y="251" text-anchor="middle" font-size="8" font-weight="700" fill="#9D174D">Sports Hall</text>
  <text x="654" y="263" text-anchor="middle" font-size="7" fill="#BE185D">(NEW)</text>

  <!-- Garden -->
  <rect x="712" y="156" width="143" height="130" rx="4" fill="#D1FAE5" stroke="#059669" stroke-width="1.3"/>
  <text x="783" y="218" text-anchor="middle" font-size="9" font-weight="700" fill="#065F46">Garden</text>

  <!-- Bike racks NEW -->
  <circle cx="615" cy="296" r="4" fill="#7C3AED"/>
  <circle cx="628" cy="296" r="4" fill="#7C3AED"/>
  <circle cx="641" cy="296" r="4" fill="#7C3AED"/>
  <text x="628" y="320" text-anchor="middle" font-size="7.5" fill="#5B21B6">Bike racks (NEW)</text>

  <!-- Entrance 2025 -->
  <rect x="678" y="296" width="44" height="14" rx="2" fill="#9CA3AF"/>
  <text x="700" y="336" text-anchor="middle" font-size="8" fill="#374141">Entrance</text>

  <!-- Title -->
  <text x="450" y="360" text-anchor="middle" font-size="10.5" font-weight="700" fill="#1a1a2e">
    Changes to Greenfield University Campus between 2005 and 2025
  </text>
</svg>'''


# ─── HTML template (same structure as Cambridge 20) ──────────────────────────
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
  <title>Cambridge 19 · Test {n} — Writing | IELTS Lab</title>
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
        <span class="text-xs text-zinc-500 hidden sm:block">Cambridge 19 · Test {n} · Writing</span>
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
        <h1 class="font-display font-black text-2xl text-zinc-100">Cambridge IELTS 19 — Test {n}</h1>
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
      <div class="chart-area">
        {t1_chart_html}
      </div>
      <textarea id="task1Answer" class="answer-area"
                placeholder="Write your Task 1 response here…"
                oninput="updateWordCount('task1')"></textarea>
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
      <textarea id="task2Answer" class="answer-area" style="min-height:280px;"
                placeholder="Write your Task 2 essay here…"
                oninput="updateWordCount('task2')"></textarea>
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
          id: rid, date: Date.now(), book: 19, testNum: {n},
          skill: 'writing', trainingType: 'academic',
          testType: 'Writing — Cambridge 19 · Test {n}',
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
# TEST 1 — Line graph: international tourist arrivals, 4 cities 2010–2022
# ════════════════════════════════════════════════════════════════════════════
T1_CHART_HTML = '''
<div class="chart-area-title">International Tourist Arrivals in Four Cities, 2010–2022 (millions)</div>
<div style="position:relative;height:240px;">
  <canvas id="chartT1" style="width:100%;height:100%;"></canvas>
</div>'''

T1_CHART_JS = """
  var ctx1 = document.getElementById('chartT1');
  if (ctx1) {
    new Chart(ctx1.getContext('2d'), {
      type: 'line',
      data: {
        labels: ['2010','2013','2016','2019','2022'],
        datasets: [
          { label:'Bangkok',   data:[11.5,16.5,21.0,23.0,12.5], borderColor:'#C62828', backgroundColor:'rgba(198,40,40,0.07)',   borderWidth:2.5, pointRadius:5, pointHoverRadius:7, pointBackgroundColor:'#fff', pointBorderColor:'#C62828', pointBorderWidth:2.5, tension:0.15 },
          { label:'Istanbul',  data:[7.5,10.0,12.5,14.5,16.0],  borderColor:'#1565C0', backgroundColor:'rgba(21,101,192,0.07)',  borderWidth:2.5, pointRadius:5, pointHoverRadius:7, pointBackgroundColor:'#fff', pointBorderColor:'#1565C0', pointBorderWidth:2.5, tension:0.15, pointStyle:'rect' },
          { label:'Dubai',     data:[8.5,11.0,14.5,16.0,14.0],  borderColor:'#F57F17', backgroundColor:'rgba(245,127,23,0.07)',  borderWidth:2.5, pointRadius:5, pointHoverRadius:7, pointBackgroundColor:'#fff', pointBorderColor:'#F57F17', pointBorderWidth:2.5, tension:0.15, pointStyle:'triangle' },
          { label:'Barcelona', data:[7.0,8.5,10.5,12.0,9.5],    borderColor:'#2E7D32', backgroundColor:'rgba(46,125,50,0.07)',   borderWidth:2.5, pointRadius:5, pointHoverRadius:7, pointBackgroundColor:'#fff', pointBorderColor:'#2E7D32', pointBorderWidth:2.5, tension:0.15, pointStyle:'star' }
        ]
      },
      options: {
        responsive: true, maintainAspectRatio: false,
        plugins: {
          legend: { position:'top', labels:{ boxWidth:13, font:{ size:11 } } },
          tooltip: { callbacks: { label: function(c){ return ' '+c.dataset.label+': '+c.parsed.y+'M'; } } }
        },
        scales: {
          x: { title:{ display:true, text:'Year', font:{ weight:'bold', size:11 } }, grid:{ color:'rgba(0,0,0,0.05)' } },
          y: { min:0, max:26, title:{ display:true, text:'Tourists (millions)', font:{ weight:'bold', size:11 } }, grid:{ color:'rgba(0,0,0,0.05)' }, ticks:{ stepSize:4 } }
        }
      }
    });
  }"""

T1_QDATA = {
    'prompt': 'The graph below shows the number of international tourists (in millions) visiting four major cities between 2010 and 2022. Summarise the information by selecting and reporting the main features, and make comparisons where relevant. Write at least 150 words.',
    'chartType': 'Line graph',
}
T1_T2_QDATA = {
    'prompt': 'International tourism has grown enormously in recent decades and now brings significant economic benefits to many countries. However, some people argue that the negative impacts on local communities and the environment outweigh these benefits. To what extent do you agree or disagree?',
    'essayType': 'Agree / Disagree',
}

# ════════════════════════════════════════════════════════════════════════════
# TEST 2 — Bar chart: monthly household spending by category, Country Z 2023
# ════════════════════════════════════════════════════════════════════════════
T2_CHART_HTML = '''
<div class="chart-area-title">Average Monthly Household Spending by Category<br>Low-income vs High-income Households, Country Z (2023)</div>
<div style="position:relative;height:240px;">
  <canvas id="chartT2" style="width:100%;height:100%;"></canvas>
</div>
<table class="data-table" style="margin-top:1rem;">
  <thead><tr><th>Category</th><th>Low-income (USD/mo)</th><th>High-income (USD/mo)</th></tr></thead>
  <tbody>
    <tr><td>Housing &amp; utilities</td><td>$620</td><td>$1,450</td></tr>
    <tr><td>Food &amp; groceries</td><td>$410</td><td>$720</td></tr>
    <tr><td>Transport</td><td>$180</td><td>$540</td></tr>
    <tr><td>Education</td><td>$90</td><td>$480</td></tr>
    <tr><td>Healthcare</td><td>$110</td><td>$290</td></tr>
    <tr><td>Leisure &amp; entertainment</td><td>$70</td><td>$610</td></tr>
  </tbody>
</table>'''

T2_CHART_JS = """
  var ctx2 = document.getElementById('chartT2');
  if (ctx2) {
    new Chart(ctx2.getContext('2d'), {
      type: 'bar',
      data: {
        labels: ['Housing & utilities','Food & groceries','Transport','Education','Healthcare','Leisure & entertainment'],
        datasets: [
          { label:'Low-income',  data:[620,410,180,90,110,70],   backgroundColor:'rgba(21,101,192,0.85)',  borderColor:'#1565C0', borderWidth:1 },
          { label:'High-income', data:[1450,720,540,480,290,610], backgroundColor:'rgba(245,124,0,0.85)',  borderColor:'#E65100', borderWidth:1 }
        ]
      },
      options: {
        responsive: true, maintainAspectRatio: false,
        plugins: { legend: { position:'top', labels:{ boxWidth:13, font:{ size:11 } } } },
        scales: {
          x: { title:{ display:true, text:'Spending category', font:{ weight:'bold', size:11 } }, grid:{ display:false }, ticks:{ maxRotation:20, font:{ size:9 } } },
          y: { min:0, max:1600, title:{ display:true, text:'USD per month', font:{ weight:'bold', size:11 } }, grid:{ color:'rgba(0,0,0,0.05)' }, ticks:{ stepSize:400, callback: function(v){ return '$'+v; } } }
        }
      }
    });
  }"""

T2_QDATA = {
    'prompt': 'The bar chart below shows the average monthly spending on six categories by low-income and high-income households in Country Z in 2023. Summarise the information by selecting and reporting the main features, and make comparisons where relevant. Write at least 150 words.',
    'chartType': 'Grouped bar chart',
}
T2_T2_QDATA = {
    'prompt': 'The gap between rich and poor is widening in many countries, with wealthy households able to afford far more in areas such as education, healthcare and leisure than low-income households. What are the main causes of this inequality, and what can be done to reduce it?',
    'essayType': 'Problem / Solution',
}

# ════════════════════════════════════════════════════════════════════════════
# TEST 3 — Two pie charts: reasons for choosing job, Men vs Women
# ════════════════════════════════════════════════════════════════════════════
T3_CHART_HTML = '''
<div class="chart-area-title">Main Reasons for Choosing Current Job, Country W (2023)</div>
<div style="display:flex;gap:1.5rem;flex-wrap:wrap;justify-content:center;align-items:flex-start;">
  <div style="flex:1;min-width:200px;max-width:280px;">
    <div style="text-align:center;font-weight:700;font-size:0.9rem;color:#0D2B4E;margin-bottom:0.5rem;">Men</div>
    <div style="position:relative;height:220px;">
      <canvas id="chartT3a" style="width:100%;height:100%;"></canvas>
    </div>
  </div>
  <div style="flex:1;min-width:200px;max-width:280px;">
    <div style="text-align:center;font-weight:700;font-size:0.9rem;color:#0D2B4E;margin-bottom:0.5rem;">Women</div>
    <div style="position:relative;height:220px;">
      <canvas id="chartT3b" style="width:100%;height:100%;"></canvas>
    </div>
  </div>
</div>'''

T3_CHART_JS = """
  var pieLabels = ['Good salary','Job security','Work-life balance','Interesting work','Career advancement','Close to home'];
  var pieColors = ['#1565C0','#2E7D32','#F57F17','#C62828','#6A1B9A','#00838F'];
  function makePie(id, data) {
    var el = document.getElementById(id);
    if (!el) return;
    new Chart(el.getContext('2d'), {
      type: 'pie',
      data: { labels: pieLabels, datasets: [{ data: data, backgroundColor: pieColors, borderColor: '#fff', borderWidth: 2 }] },
      options: {
        responsive: true, maintainAspectRatio: false,
        plugins: {
          legend: { position:'bottom', labels:{ boxWidth:11, font:{ size:9 } } },
          tooltip: { callbacks: { label: function(c){ return ' '+c.label+': '+c.parsed+'%'; } } }
        }
      }
    });
  }
  makePie('chartT3a', [34,22,12,14,13,5]);
  makePie('chartT3b', [21,18,28,16,8,9]);"""

T3_QDATA = {
    'prompt': 'The pie charts below show the main reasons men and women in Country W gave for choosing their current job, based on a survey carried out in 2023. Summarise the information by selecting and reporting the main features, and make comparisons where relevant. Write at least 150 words.',
    'chartType': 'Two pie charts (comparison)',
}
T3_T2_QDATA = {
    'prompt': 'Some people believe that the most important factor when choosing a job is the salary it offers. Others think that other factors, such as work-life balance or job satisfaction, matter more. Discuss both views and give your own opinion.',
    'essayType': 'Discussion (Both Views + Opinion)',
}

# ════════════════════════════════════════════════════════════════════════════
# TEST 4 — Map comparison: Greenfield University Campus 2005 vs 2025
# ════════════════════════════════════════════════════════════════════════════
T4_CHART_HTML = f'''
<div class="chart-area-title">Changes to Greenfield University Campus between 2005 and 2025</div>
{SVG_T4}'''

T4_CHART_JS = ""

T4_QDATA = {
    'prompt': 'The maps below show the layout of Greenfield University campus in 2005 and how it had changed by 2025. Summarise the information by selecting and reporting the main features, and make comparisons where relevant. Write at least 150 words.',
    'chartType': 'Map comparison (2005 vs 2025)',
}
T4_T2_QDATA = {
    'prompt': 'In many countries, universities are placing increasing emphasis on subjects such as science, technology, engineering and mathematics, and reducing support for the arts and humanities. Is this a positive or negative development?',
    'essayType': 'Positive / Negative Development',
}

# ════════════════════════════════════════════════════════════════════════════
FILES = [
    (1,
     'The graph below shows the number of international tourists (in millions) visiting four major cities between 2010 and 2022.',
     'Line Graph', T1_CHART_HTML, T1_CHART_JS, T1_QDATA,
     'Agree / Disagree',
     '''<p class="t2-body">International tourism has grown enormously in recent decades and now brings significant economic benefits to many countries. However, some people argue that the negative impacts on local communities and the environment outweigh these benefits.</p>
     <p class="t2-question">To what extent do you agree or disagree?</p>
     <p class="t2-rubric">Give reasons for your answer and include any relevant examples from your own knowledge or experience.</p>''',
     T1_T2_QDATA),

    (2,
     'The bar chart below shows the average monthly spending on six categories by low-income and high-income households in Country Z in 2023.',
     'Grouped Bar Chart + Data Table', T2_CHART_HTML, T2_CHART_JS, T2_QDATA,
     'Problem / Solution',
     '''<p class="t2-body">The gap between rich and poor is widening in many countries, with wealthy households able to afford far more in areas such as education, healthcare and leisure than low-income households.</p>
     <p class="t2-question">What are the main causes of this inequality, and what can be done to reduce it?</p>
     <p class="t2-rubric">Give reasons for your answer and include any relevant examples from your own knowledge or experience.</p>''',
     T2_T2_QDATA),

    (3,
     'The pie charts below show the main reasons men and women in Country W gave for choosing their current job, based on a survey carried out in 2023.',
     'Two Pie Charts (Comparison)', T3_CHART_HTML, T3_CHART_JS, T3_QDATA,
     'Discussion (Both Views + Opinion)',
     '''<p class="t2-body">Some people believe that the most important factor when choosing a job is the salary it offers. Others think that other factors, such as work–life balance or job satisfaction, matter more.</p>
     <p class="t2-question">Discuss both views and give your own opinion.</p>
     <p class="t2-rubric">Give reasons for your answer and include any relevant examples from your own knowledge or experience.</p>''',
     T3_T2_QDATA),

    (4,
     'The maps below show the layout of Greenfield University campus in 2005 and how it had changed by 2025.',
     'Map Comparison (2005 vs 2025)', T4_CHART_HTML, T4_CHART_JS, T4_QDATA,
     'Positive / Negative Development',
     '''<p class="t2-body">In many countries, universities are placing increasing emphasis on subjects such as science, technology, engineering and mathematics, and reducing support for the arts and humanities.</p>
     <p class="t2-question">Is this a positive or negative development?</p>
     <p class="t2-rubric">Give reasons for your answer and include any relevant examples from your own knowledge or experience.</p>''',
     T4_T2_QDATA),
]

if __name__ == '__main__':
    for (n, t1_intro, t1_type, t1_chart_html, t1_chart_js, t1_qd, t2_type, t2_html, t2_qd) in FILES:
        html = build(n, t1_intro, t1_type, t1_chart_html, t1_chart_js, t1_qd, t2_type, t2_html, t2_qd)
        path = os.path.join(BASE, f'cam19-t{n}-writing.html')
        with open(path, 'w', encoding='utf-8') as f:
            f.write(html)
        print(f'Written: {path}  ({len(html):,} chars)')
    print('Done.')
