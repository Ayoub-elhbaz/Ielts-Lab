#!/usr/bin/env python3
"""
Generate cam18-t{1..4}-writing.html
Content from Cambridge IELTS 20 Volume 3 PDF (used for Cambridge 18 slot)
"""
import os

BASE = '/Users/ayoubelhebaze/Downloads/claude md/mock-tests'

# ─── SVG: Chocolate making process (Test 4, 8 stages, linear snake) ──────────
SVG_T4 = '''<svg viewBox="-10 0 900 280" xmlns="http://www.w3.org/2000/svg"
     style="width:100%;max-width:860px;display:block;margin:0 auto;font-family:'Plus Jakarta Sans',sans-serif;">
  <defs>
    <marker id="arrC" markerWidth="9" markerHeight="7" refX="8" refY="3.5" orient="auto">
      <polygon points="0 0,9 3.5,0 7" fill="#7B3F00"/>
    </marker>
  </defs>

  <!-- ROW 1: stages 1→4 -->
  <!-- Box 1 -->
  <rect x="20"  y="20" width="155" height="82" rx="7" fill="#FFF3E0" stroke="#E65100" stroke-width="1.8"/>
  <text x="97"  y="42" text-anchor="middle" font-size="10" font-weight="700" fill="#BF360C">1. Harvesting</text>
  <text x="97"  y="57" text-anchor="middle" font-size="8.5" fill="#5D4037">cocoa pods cut</text>
  <text x="97"  y="69" text-anchor="middle" font-size="8.5" fill="#5D4037">from trees by hand</text>
  <line x1="175" y1="61" x2="200" y2="61" stroke="#7B3F00" stroke-width="1.6" marker-end="url(#arrC)"/>

  <!-- Box 2 -->
  <rect x="203" y="20" width="155" height="82" rx="7" fill="#FFF3E0" stroke="#E65100" stroke-width="1.8"/>
  <text x="280" y="42" text-anchor="middle" font-size="10" font-weight="700" fill="#BF360C">2. Fermenting</text>
  <text x="280" y="57" text-anchor="middle" font-size="8.5" fill="#5D4037">beans covered with</text>
  <text x="280" y="69" text-anchor="middle" font-size="8.5" fill="#5D4037">leaves for 5–7 days</text>
  <line x1="358" y1="61" x2="383" y2="61" stroke="#7B3F00" stroke-width="1.6" marker-end="url(#arrC)"/>

  <!-- Box 3 -->
  <rect x="386" y="20" width="155" height="82" rx="7" fill="#F3E5F5" stroke="#6A1B9A" stroke-width="1.8"/>
  <text x="463" y="42" text-anchor="middle" font-size="10" font-weight="700" fill="#4A148C">3. Drying</text>
  <text x="463" y="57" text-anchor="middle" font-size="8.5" fill="#5D4037">beans laid in sun</text>
  <text x="463" y="69" text-anchor="middle" font-size="8.5" fill="#5D4037">for about 1 week</text>
  <line x1="541" y1="61" x2="566" y2="61" stroke="#7B3F00" stroke-width="1.6" marker-end="url(#arrC)"/>

  <!-- Box 4 -->
  <rect x="569" y="20" width="155" height="82" rx="7" fill="#F3E5F5" stroke="#6A1B9A" stroke-width="1.8"/>
  <text x="646" y="42" text-anchor="middle" font-size="10" font-weight="700" fill="#4A148C">4. Roasting</text>
  <text x="646" y="57" text-anchor="middle" font-size="8.5" fill="#5D4037">beans heated at</text>
  <text x="646" y="69" text-anchor="middle" font-size="8.5" fill="#5D4037">120–150 °C in ovens</text>

  <!-- Turn: Box 4 → Box 5 (right side down) -->
  <polyline points="724,61 755,61 755,195 724,195"
            fill="none" stroke="#7B3F00" stroke-width="1.6" marker-end="url(#arrC)"/>

  <!-- ROW 2: stages 5→8 (right to left) -->
  <!-- Box 5 -->
  <rect x="569" y="154" width="155" height="82" rx="7" fill="#E8F5E9" stroke="#2E7D32" stroke-width="1.8"/>
  <text x="646" y="176" text-anchor="middle" font-size="10" font-weight="700" fill="#1B5E20">5. Grinding</text>
  <text x="646" y="191" text-anchor="middle" font-size="8.5" fill="#5D4037">shells removed,</text>
  <text x="646" y="203" text-anchor="middle" font-size="8.5" fill="#5D4037">beans ground to paste</text>
  <line x1="569" y1="195" x2="544" y2="195" stroke="#7B3F00" stroke-width="1.6" marker-end="url(#arrC)"/>

  <!-- Box 6 -->
  <rect x="386" y="154" width="155" height="82" rx="7" fill="#E8F5E9" stroke="#2E7D32" stroke-width="1.8"/>
  <text x="463" y="176" text-anchor="middle" font-size="10" font-weight="700" fill="#1B5E20">6. Mixing</text>
  <text x="463" y="191" text-anchor="middle" font-size="8.5" fill="#5D4037">sugar, milk powder</text>
  <text x="463" y="203" text-anchor="middle" font-size="8.5" fill="#5D4037">and cocoa butter added</text>
  <line x1="386" y1="195" x2="361" y2="195" stroke="#7B3F00" stroke-width="1.6" marker-end="url(#arrC)"/>

  <!-- Box 7 -->
  <rect x="203" y="154" width="155" height="82" rx="7" fill="#E3F2FD" stroke="#1565C0" stroke-width="1.8"/>
  <text x="280" y="172" text-anchor="middle" font-size="10" font-weight="700" fill="#0D47A1">7. Conching &amp;</text>
  <text x="280" y="184" text-anchor="middle" font-size="10" font-weight="700" fill="#0D47A1">Tempering</text>
  <text x="280" y="199" text-anchor="middle" font-size="8.5" fill="#5D4037">mixture stirred and</text>
  <text x="280" y="211" text-anchor="middle" font-size="8.5" fill="#5D4037">carefully cooled</text>
  <line x1="203" y1="195" x2="178" y2="195" stroke="#7B3F00" stroke-width="1.6" marker-end="url(#arrC)"/>

  <!-- Box 8 -->
  <rect x="20"  y="154" width="155" height="82" rx="7" fill="#E3F2FD" stroke="#1565C0" stroke-width="1.8"/>
  <text x="97"  y="172" text-anchor="middle" font-size="10" font-weight="700" fill="#0D47A1">8. Moulding &amp;</text>
  <text x="97"  y="184" text-anchor="middle" font-size="10" font-weight="700" fill="#0D47A1">Packaging</text>
  <text x="97"  y="199" text-anchor="middle" font-size="8.5" fill="#5D4037">liquid chocolate poured</text>
  <text x="97"  y="211" text-anchor="middle" font-size="8.5" fill="#5D4037">into bar moulds</text>

  <!-- Title -->
  <text x="372" y="265" text-anchor="middle" font-size="11" font-weight="700" fill="#3E2723">
    The Process of Making Chocolate (from Cocoa Bean to Bar)
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
  <title>Cambridge 18 · Test {n} — Writing | IELTS Lab</title>
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
        <span class="text-xs text-zinc-500 hidden sm:block">Cambridge 18 · Test {n} · Writing</span>
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
        <h1 class="font-display font-black text-2xl text-zinc-100">Cambridge IELTS 18 — Test {n}</h1>
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
          id: rid, date: Date.now(), book: 18, testNum: {n},
          skill: 'writing', trainingType: 'academic',
          testType: 'Writing — Cambridge 18 · Test {n}',
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
# TEST 1 — Dual-axis line graph: rainfall vs wildfires, Country A, 1990–2020
# ════════════════════════════════════════════════════════════════════════════
T1_CHART_HTML = '''
<div class="chart-area-title">Average Annual Rainfall and Number of Wildfires in Country A, 1990–2020</div>
<div style="position:relative;height:240px;">
  <canvas id="chartT1" style="width:100%;height:100%;"></canvas>
</div>'''

T1_CHART_JS = """
  var ctx1 = document.getElementById('chartT1');
  if (ctx1) {
    new Chart(ctx1.getContext('2d'), {
      type: 'line',
      data: {
        labels: ['1990','1995','2000','2005','2010','2015','2020'],
        datasets: [
          {
            label: 'Rainfall (mm)',
            data: [820,795,755,700,655,610,540],
            borderColor: '#1565C0', backgroundColor: 'rgba(21,101,192,0.07)',
            borderWidth: 2.5, pointRadius: 5, pointBackgroundColor: '#fff',
            pointBorderColor: '#1565C0', pointBorderWidth: 2.5, tension: 0.15,
            yAxisID: 'yRain'
          },
          {
            label: 'Wildfires (count)',
            data: [120,150,200,270,400,470,680],
            borderColor: '#C62828', backgroundColor: 'rgba(198,40,40,0.07)',
            borderWidth: 2.5, pointRadius: 5, pointBackgroundColor: '#fff',
            pointBorderColor: '#C62828', pointBorderWidth: 2.5, tension: 0.15,
            pointStyle: 'rect', yAxisID: 'yFire'
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
          yRain: {
            type: 'linear', position: 'left',
            min: 400, max: 900,
            title:{ display:true, text:'Rainfall (mm)', font:{ weight:'bold', size:10 }, color:'#1565C0' },
            ticks:{ color:'#1565C0', stepSize:100 },
            grid:{ color:'rgba(0,0,0,0.05)' }
          },
          yFire: {
            type: 'linear', position: 'right',
            min: 0, max: 800,
            title:{ display:true, text:'Wildfires per year', font:{ weight:'bold', size:10 }, color:'#C62828' },
            ticks:{ color:'#C62828', stepSize:200 },
            grid:{ drawOnChartArea: false }
          }
        }
      }
    });
  }"""

T1_QDATA = {
    'prompt': 'The graph below shows the average annual rainfall (in millimetres) and the number of wildfires recorded each year in Country A between 1990 and 2020. Summarise the information by selecting and reporting the main features, and make comparisons where relevant. Write at least 150 words.',
    'chartType': 'Dual-axis line graph',
}
T1_T2_QDATA = {
    'prompt': 'Climate change is one of the most pressing problems the world faces today. Some people argue that governments alone are responsible for tackling it, while others believe that individuals must also change their behaviour. Discuss both views and give your own opinion.',
    'essayType': 'Discussion (Both Views + Opinion)',
}

# ════════════════════════════════════════════════════════════════════════════
# TEST 2 — Bar chart: social media time, 3 countries × 5 platforms, 2024
# ════════════════════════════════════════════════════════════════════════════
T2_CHART_HTML = '''
<div class="chart-area-title">Average Daily Time Spent on Five Social Media Platforms<br>by Users in Three Countries, 2024 (minutes per day)</div>
<div style="position:relative;height:240px;">
  <canvas id="chartT2" style="width:100%;height:100%;"></canvas>
</div>
<table class="data-table" style="margin-top:1rem;">
  <thead><tr><th>Platform</th><th>Brazil (min)</th><th>Japan (min)</th><th>India (min)</th></tr></thead>
  <tbody>
    <tr><td>Platform A (short video)</td><td>115</td><td>42</td><td>95</td></tr>
    <tr><td>Platform B (messaging)</td><td>68</td><td>88</td><td>102</td></tr>
    <tr><td>Platform C (photos)</td><td>52</td><td>31</td><td>46</td></tr>
    <tr><td>Platform D (news / text)</td><td>24</td><td>38</td><td>18</td></tr>
    <tr><td>Platform E (professional)</td><td>12</td><td>22</td><td>8</td></tr>
  </tbody>
</table>'''

T2_CHART_JS = """
  var ctx2 = document.getElementById('chartT2');
  if (ctx2) {
    new Chart(ctx2.getContext('2d'), {
      type: 'bar',
      data: {
        labels: ['Platform A\\n(short video)','Platform B\\n(messaging)','Platform C\\n(photos)','Platform D\\n(news/text)','Platform E\\n(professional)'],
        datasets: [
          { label:'Brazil', data:[115,68,52,24,12], backgroundColor:'rgba(46,125,50,0.85)',  borderColor:'#2E7D32', borderWidth:1 },
          { label:'Japan',  data:[42,88,31,38,22],  backgroundColor:'rgba(198,40,40,0.85)',  borderColor:'#C62828', borderWidth:1 },
          { label:'India',  data:[95,102,46,18,8],  backgroundColor:'rgba(245,124,0,0.85)',  borderColor:'#E65100', borderWidth:1 }
        ]
      },
      options: {
        responsive: true, maintainAspectRatio: false,
        plugins: { legend:{ position:'top', labels:{ boxWidth:13, font:{ size:11 } } } },
        scales: {
          x: { title:{ display:true, text:'Social media platform', font:{ weight:'bold', size:11 } }, grid:{ display:false }, ticks:{ font:{ size:9 } } },
          y: { min:0, max:140, title:{ display:true, text:'Minutes per day', font:{ weight:'bold', size:11 } }, grid:{ color:'rgba(0,0,0,0.05)' }, ticks:{ stepSize:20 } }
        }
      }
    });
  }"""

T2_QDATA = {
    'prompt': 'The bar chart below shows the average daily time, in minutes, that users in Brazil, Japan and India spent on five different social media platforms in 2024. Summarise the information by selecting and reporting the main features, and make comparisons where relevant. Write at least 150 words.',
    'chartType': 'Grouped bar chart',
}
T2_T2_QDATA = {
    'prompt': 'In many countries, people of all ages are spending more and more time on social media. Some people see this as a positive development that helps people stay connected, while others see it as harmful to mental health and face-to-face relationships. Do the advantages of social media outweigh the disadvantages?',
    'essayType': 'Advantages / Disadvantages',
}

# ════════════════════════════════════════════════════════════════════════════
# TEST 3 — Three pie charts: leisure time by age group, Country B, 2024
# ════════════════════════════════════════════════════════════════════════════
T3_CHART_HTML = '''
<div class="chart-area-title">How Three Age Groups Spend Their Leisure Time, Country B (2024)</div>
<div style="display:flex;gap:1rem;flex-wrap:wrap;justify-content:center;align-items:flex-start;">
  <div style="flex:1;min-width:170px;max-width:230px;">
    <div style="text-align:center;font-weight:700;font-size:0.85rem;color:#0D2B4E;margin-bottom:0.4rem;">Age 15–24</div>
    <div style="position:relative;height:200px;">
      <canvas id="chartT3a" style="width:100%;height:100%;"></canvas>
    </div>
  </div>
  <div style="flex:1;min-width:170px;max-width:230px;">
    <div style="text-align:center;font-weight:700;font-size:0.85rem;color:#0D2B4E;margin-bottom:0.4rem;">Age 35–54</div>
    <div style="position:relative;height:200px;">
      <canvas id="chartT3b" style="width:100%;height:100%;"></canvas>
    </div>
  </div>
  <div style="flex:1;min-width:170px;max-width:230px;">
    <div style="text-align:center;font-weight:700;font-size:0.85rem;color:#0D2B4E;margin-bottom:0.4rem;">Age 65+</div>
    <div style="position:relative;height:200px;">
      <canvas id="chartT3c" style="width:100%;height:100%;"></canvas>
    </div>
  </div>
</div>'''

T3_CHART_JS = """
  var pieLabels3 = ['Watching screens','Socialising','Sport & exercise','Hobbies / crafts','Reading','Other'];
  var pieColors3 = ['#1565C0','#F57F17','#2E7D32','#9C27B0','#C62828','#78909C'];
  function makePie3(id, data) {
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
  makePie3('chartT3a', [48,24,14,6,5,3]);
  makePie3('chartT3b', [34,22,16,12,10,6]);
  makePie3('chartT3c', [22,18,12,20,22,6]);"""

T3_QDATA = {
    'prompt': 'The pie charts below show how three different age groups in Country B spent their leisure time in 2024. Summarise the information by selecting and reporting the main features, and make comparisons where relevant. Write at least 150 words.',
    'chartType': 'Three pie charts (age groups)',
}
T3_T2_QDATA = {
    'prompt': 'Many older people today report feeling isolated and disconnected from younger generations. What are the main causes of this problem, and what can be done to bring different generations closer together?',
    'essayType': 'Problem / Solution',
}

# ════════════════════════════════════════════════════════════════════════════
# TEST 4 — Process SVG: chocolate making, 8 stages, linear
# ════════════════════════════════════════════════════════════════════════════
T4_CHART_HTML = f'''
<div class="chart-area-title">The Process of Making Chocolate (from Cocoa Bean to Bar) — 8 Stages</div>
{SVG_T4}'''

T4_CHART_JS = ""

T4_QDATA = {
    'prompt': 'The diagram below shows the process by which chocolate is made, from the harvesting of cocoa pods to the finished chocolate bar. Summarise the information by selecting and reporting the main features, and make comparisons where relevant. Write at least 150 words.',
    'chartType': 'Process diagram (8 stages, linear)',
}
T4_T2_QDATA = {
    'prompt': 'In recent years, large food and drink companies have been criticised for the impact of their products on people\'s health and on the environment. Some people argue that these companies should be more strictly regulated by governments, while others believe consumers should be free to make their own choices. To what extent do you agree or disagree?',
    'essayType': 'Agree / Disagree',
}

# ════════════════════════════════════════════════════════════════════════════
FILES = [
    (1,
     'The graph below shows the average annual rainfall (in millimetres) and the number of wildfires recorded each year in Country A between 1990 and 2020.',
     'Dual-Axis Line Graph', T1_CHART_HTML, T1_CHART_JS, T1_QDATA,
     'Discussion (Both Views + Opinion)',
     '''<p class="t2-body">Climate change is one of the most pressing problems the world faces today. Some people argue that governments alone are responsible for tackling it, while others believe that individuals must also change their behaviour.</p>
     <p class="t2-question">Discuss both views and give your own opinion.</p>
     <p class="t2-rubric">Give reasons for your answer and include any relevant examples from your own knowledge or experience.</p>''',
     T1_T2_QDATA),

    (2,
     'The bar chart below shows the average daily time, in minutes, that users in Brazil, Japan and India spent on five different social media platforms in 2024.',
     'Grouped Bar Chart + Data Table', T2_CHART_HTML, T2_CHART_JS, T2_QDATA,
     'Advantages / Disadvantages',
     '''<p class="t2-body">In many countries, people of all ages are spending more and more time on social media. Some people see this as a positive development that helps people stay connected, while others see it as harmful to mental health and face-to-face relationships.</p>
     <p class="t2-question">Do the advantages of social media outweigh the disadvantages?</p>
     <p class="t2-rubric">Give reasons for your answer and include any relevant examples from your own knowledge or experience.</p>''',
     T2_T2_QDATA),

    (3,
     'The pie charts below show how three different age groups in Country B spent their leisure time in 2024.',
     'Three Pie Charts (Age Groups)', T3_CHART_HTML, T3_CHART_JS, T3_QDATA,
     'Problem / Solution',
     '''<p class="t2-body">Many older people today report feeling isolated and disconnected from younger generations.</p>
     <p class="t2-question">What are the main causes of this problem, and what can be done to bring different generations closer together?</p>
     <p class="t2-rubric">Give reasons for your answer and include any relevant examples from your own knowledge or experience.</p>''',
     T3_T2_QDATA),

    (4,
     'The diagram below shows the process by which chocolate is made, from the harvesting of cocoa pods to the finished chocolate bar.',
     'Process Diagram (8 Stages, Linear)', T4_CHART_HTML, T4_CHART_JS, T4_QDATA,
     'Agree / Disagree',
     '''<p class="t2-body">In recent years, large food and drink companies have been criticised for the impact of their products on people\'s health and on the environment. Some people argue that these companies should be more strictly regulated by governments, while others believe consumers should be free to make their own choices.</p>
     <p class="t2-question">To what extent do you agree or disagree?</p>
     <p class="t2-rubric">Give reasons for your answer and include any relevant examples from your own knowledge or experience.</p>''',
     T4_T2_QDATA),
]

if __name__ == '__main__':
    for (n, t1_intro, t1_type, t1_chart_html, t1_chart_js, t1_qd, t2_type, t2_html, t2_qd) in FILES:
        html = build(n, t1_intro, t1_type, t1_chart_html, t1_chart_js, t1_qd, t2_type, t2_html, t2_qd)
        path = os.path.join(BASE, f'cam18-t{n}-writing.html')
        with open(path, 'w', encoding='utf-8') as f:
            f.write(html)
        print(f'Written: {path}  ({len(html):,} chars)')
    print('Done.')
