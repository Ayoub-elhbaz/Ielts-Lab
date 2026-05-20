#!/usr/bin/env python3
"""
Regenerate cam20-t{1..4}-writing.html
Content taken from Cambridge_IELTS_20_Writing_Practice_Tests.pdf
Charts: Chart.js (line / bar / pie) + SVG process diagram
All chart init runs in window.onload so canvas layout is computed first.
"""
import os

BASE = '/Users/ayoubelhebaze/Downloads/claude md/mock-tests'

# ─── Process diagram SVG (Test 4 — plastic bottle recycling, 8 stages) ───────
SVG_T4 = '''<svg viewBox="-50 0 920 340" xmlns="http://www.w3.org/2000/svg"
     style="width:100%;max-width:820px;display:block;margin:0 auto;font-family:'Plus Jakarta Sans',sans-serif;">
  <defs>
    <marker id="arr" markerWidth="9" markerHeight="7" refX="8" refY="3.5" orient="auto">
      <polygon points="0 0,9 3.5,0 7" fill="#444"/>
    </marker>
    <marker id="arr-d" markerWidth="9" markerHeight="7" refX="8" refY="3.5" orient="auto">
      <polygon points="0 0,9 3.5,0 7" fill="#999"/>
    </marker>
  </defs>
  <!-- ROW 1 -->
  <rect x="20" y="18" width="165" height="82" rx="7" fill="#EEF3FB" stroke="#1565C0" stroke-width="1.8"/>
  <text x="102" y="39"  text-anchor="middle" font-size="10.5" font-weight="700" fill="#1565C0">1. Collection</text>
  <text x="102" y="56"  text-anchor="middle" font-size="9" fill="#333">used bottles gathered</text>
  <text x="102" y="69"  text-anchor="middle" font-size="9" fill="#333">from homes &amp; bins</text>
  <line x1="185" y1="59" x2="212" y2="59" stroke="#444" stroke-width="1.6" marker-end="url(#arr)"/>
  <rect x="215" y="18" width="165" height="82" rx="7" fill="#EEF3FB" stroke="#1565C0" stroke-width="1.8"/>
  <text x="297" y="39"  text-anchor="middle" font-size="10.5" font-weight="700" fill="#1565C0">2. Sorting</text>
  <text x="297" y="56"  text-anchor="middle" font-size="9" fill="#333">bottles separated by</text>
  <text x="297" y="69"  text-anchor="middle" font-size="9" fill="#333">plastic type &amp; colour</text>
  <line x1="380" y1="59" x2="407" y2="59" stroke="#444" stroke-width="1.6" marker-end="url(#arr)"/>
  <rect x="410" y="18" width="165" height="82" rx="7" fill="#E8F5E9" stroke="#2E7D32" stroke-width="1.8"/>
  <text x="492" y="39"  text-anchor="middle" font-size="10.5" font-weight="700" fill="#2E7D32">3. Washing</text>
  <text x="492" y="56"  text-anchor="middle" font-size="9" fill="#333">labels &amp; residue</text>
  <text x="492" y="69"  text-anchor="middle" font-size="9" fill="#333">removed with hot water</text>
  <line x1="575" y1="59" x2="602" y2="59" stroke="#444" stroke-width="1.6" marker-end="url(#arr)"/>
  <rect x="605" y="18" width="165" height="82" rx="7" fill="#E8F5E9" stroke="#2E7D32" stroke-width="1.8"/>
  <text x="687" y="39"  text-anchor="middle" font-size="10.5" font-weight="700" fill="#2E7D32">4. Shredding</text>
  <text x="687" y="56"  text-anchor="middle" font-size="9" fill="#333">bottles cut into</text>
  <text x="687" y="69"  text-anchor="middle" font-size="9" fill="#333">small plastic flakes</text>
  <polyline points="770,59 820,59 820,261 770,261"
            fill="none" stroke="#444" stroke-width="1.6" marker-end="url(#arr)"/>
  <!-- ROW 2 -->
  <rect x="605" y="218" width="165" height="82" rx="7" fill="#FFF3E0" stroke="#E65100" stroke-width="1.8"/>
  <text x="687" y="239" text-anchor="middle" font-size="10.5" font-weight="700" fill="#E65100">5. Melting</text>
  <text x="687" y="256" text-anchor="middle" font-size="9" fill="#333">flakes heated into</text>
  <text x="687" y="269" text-anchor="middle" font-size="9" fill="#333">liquid plastic</text>
  <line x1="605" y1="261" x2="578" y2="261" stroke="#444" stroke-width="1.6" marker-end="url(#arr)"/>
  <rect x="410" y="218" width="165" height="82" rx="7" fill="#FFF3E0" stroke="#E65100" stroke-width="1.8"/>
  <text x="492" y="239" text-anchor="middle" font-size="10.5" font-weight="700" fill="#E65100">6. Pellet Forming</text>
  <text x="492" y="256" text-anchor="middle" font-size="9" fill="#333">liquid cooled into</text>
  <text x="492" y="269" text-anchor="middle" font-size="9" fill="#333">small pellets</text>
  <line x1="410" y1="261" x2="383" y2="261" stroke="#444" stroke-width="1.6" marker-end="url(#arr)"/>
  <rect x="215" y="218" width="165" height="82" rx="7" fill="#F3E5F5" stroke="#6A1B9A" stroke-width="1.8"/>
  <text x="297" y="239" text-anchor="middle" font-size="10.5" font-weight="700" fill="#6A1B9A">7. Manufacturing</text>
  <text x="297" y="256" text-anchor="middle" font-size="9" fill="#333">pellets used to make</text>
  <text x="297" y="269" text-anchor="middle" font-size="9" fill="#333">new bottles &amp; products</text>
  <line x1="215" y1="261" x2="188" y2="261" stroke="#444" stroke-width="1.6" marker-end="url(#arr)"/>
  <rect x="20" y="218" width="165" height="82" rx="7" fill="#F3E5F5" stroke="#6A1B9A" stroke-width="1.8"/>
  <text x="102" y="239" text-anchor="middle" font-size="10.5" font-weight="700" fill="#6A1B9A">8. Distribution</text>
  <text x="102" y="256" text-anchor="middle" font-size="9" fill="#333">new products sent</text>
  <text x="102" y="269" text-anchor="middle" font-size="9" fill="#333">back to consumers</text>
  <polyline points="20,261 -35,261 -35,59 20,59"
            fill="none" stroke="#999" stroke-width="1.5"
            stroke-dasharray="6,4" marker-end="url(#arr-d)"/>
  <text transform="rotate(-90,-35,160)" x="-35" y="160"
        text-anchor="middle" font-size="8.5" fill="#aaa">cyclical</text>
  <text x="385" y="328" text-anchor="middle" font-size="11.5" font-weight="700" fill="#1a1a2e">
    The Process of Recycling Plastic Bottles
  </text>
</svg>'''


# ─── HTML template builder ────────────────────────────────────────────────────
# t1_chart_html = DOM-only (canvas/SVG/table, no <script>)
# t1_chart_js   = JS init code to run inside window.onload (no surrounding function)

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
  <title>Cambridge 20 · Test {n} — Writing | IELTS Lab</title>
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
        <span class="text-xs text-zinc-500 hidden sm:block">Cambridge 20 · Test {n} · Writing</span>
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
        <h1 class="font-display font-black text-2xl text-zinc-100">Cambridge IELTS 20 — Test {n}</h1>
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
    // AUTH
    var raw = localStorage.getItem('ielts_session');
    if (!raw) window.location.replace('../login.html');
    try {{ JSON.parse(raw); }} catch(e) {{ localStorage.removeItem('ielts_session'); window.location.replace('../login.html'); }}

    // QUESTION DATA
    {qd_js}

    // THEME
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

    // CHARTS — run after full page load so canvas has computed dimensions
    window.addEventListener('load', function() {{
      {t1_chart_js}
    }});

    // TIMER
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

    // WORD COUNT
    function countWords(t) {{ return t.trim() === '' ? 0 : t.trim().split(/\s+/).length; }}
    function updateWordCount(task) {{
      var ta = document.getElementById(task + 'Answer');
      var ct = document.getElementById(task + 'Counter');
      var min = task === 'task1' ? 150 : 250;
      var n = countWords(ta.value);
      ct.textContent = n + ' words';
      ct.className = 'word-counter ' + (n >= min ? (n >= min * 1.3 ? 'good' : 'ok') : 'under');
    }}

    // SUBMIT
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
          id: rid, date: Date.now(), book: 20, testNum: {n},
          skill: 'writing', trainingType: 'academic',
          testType: 'Writing — Cambridge 20 · Test {n}',
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
# TEST 1 — Line graph: daily screen time teenagers 4 countries 2000–2020
# ════════════════════════════════════════════════════════════════════════════
T1_CHART_HTML = '''
<div class="chart-area-title">Average Daily Screen Time Among Teenagers (Ages 13–18)<br>in Four Countries, 2000–2020 (hours per day)</div>
<canvas id="chartT1" height="260"></canvas>'''

T1_CHART_JS = """
  var ctx1 = document.getElementById('chartT1');
  if (ctx1) {
    new Chart(ctx1.getContext('2d'), {
      type: 'line',
      data: {
        labels: ['2000','2005','2010','2015','2020'],
        datasets: [
          { label:'United Kingdom', data:[1.8,2.6,3.7,5.2,6.5], borderColor:'#1565C0', backgroundColor:'rgba(21,101,192,0.08)', borderWidth:2.5, pointRadius:6, pointHoverRadius:8, pointBackgroundColor:'#fff', pointBorderColor:'#1565C0', pointBorderWidth:2.5, tension:0.15 },
          { label:'Japan',          data:[2.2,3.1,4.1,5.7,6.8], borderColor:'#C62828', backgroundColor:'rgba(198,40,40,0.08)',   borderWidth:2.5, pointRadius:6, pointHoverRadius:8, pointBackgroundColor:'#fff', pointBorderColor:'#C62828', pointBorderWidth:2.5, tension:0.15, pointStyle:'rect' },
          { label:'Canada',         data:[1.7,2.3,3.4,5.0,6.2], borderColor:'#2E7D32', backgroundColor:'rgba(46,125,50,0.08)',   borderWidth:2.5, pointRadius:6, pointHoverRadius:8, pointBackgroundColor:'#fff', pointBorderColor:'#2E7D32', pointBorderWidth:2.5, tension:0.15, pointStyle:'triangle' },
          { label:'Germany',        data:[1.3,1.9,2.9,4.2,5.7], borderColor:'#7B1FA2', backgroundColor:'rgba(123,31,162,0.08)', borderWidth:2.5, pointRadius:6, pointHoverRadius:8, pointBackgroundColor:'#fff', pointBorderColor:'#7B1FA2', pointBorderWidth:2.5, tension:0.15, pointStyle:'star' }
        ]
      },
      options: {
        responsive: true,
        maintainAspectRatio: false,
        plugins: {
          legend: { position:'top', labels:{ boxWidth:14, font:{ size:11 } } },
          tooltip: { callbacks: { label: function(c){ return ' '+c.dataset.label+': '+c.parsed.y+' hrs/day'; } } }
        },
        scales: {
          x: { title:{ display:true, text:'Year', font:{ weight:'bold', size:12 } }, grid:{ color:'rgba(0,0,0,0.06)' } },
          y: { min:0, max:7, title:{ display:true, text:'Hours per day', font:{ weight:'bold', size:12 } }, grid:{ color:'rgba(0,0,0,0.06)' }, ticks:{ stepSize:1 } }
        }
      }
    });
  }"""

T1_QDATA = {
    'prompt': 'The graph below shows the average daily screen time among teenagers aged 13-18 in four countries between 2000 and 2020. Summarise the information by selecting and reporting the main features, and make comparisons where relevant. Write at least 150 words.',
    'chartType': 'Line graph',
}
T1_T2_QDATA = {
    'prompt': 'In many countries today, young people spend an increasing amount of time on electronic devices such as smartphones and tablets. Some people believe this is harmful to their development, while others argue it prepares them for the modern world. Discuss both these views and give your own opinion.',
    'essayType': 'Discussion (both views + opinion)',
}

# ════════════════════════════════════════════════════════════════════════════
# TEST 2 — Bar chart + data table: leisure activities by age group
# ════════════════════════════════════════════════════════════════════════════
T2_CHART_HTML = '''
<div class="chart-area-title">Percentage of Adults Participating in Five Leisure Activities<br>by Age Group, Country X (2022)</div>
<canvas id="chartT2" height="260"></canvas>
<table class="data-table" style="margin-top:1.1rem;">
  <thead><tr><th>Activity</th><th>18–29 (%)</th><th>30–49 (%)</th><th>50–64 (%)</th><th>65+ (%)</th></tr></thead>
  <tbody>
    <tr><td>Reading books</td><td>42</td><td>55</td><td>68</td><td>74</td></tr>
    <tr><td>Watching streaming</td><td>88</td><td>79</td><td>62</td><td>51</td></tr>
    <tr><td>Outdoor exercise</td><td>64</td><td>58</td><td>49</td><td>33</td></tr>
    <tr><td>Playing video games</td><td>71</td><td>46</td><td>19</td><td>8</td></tr>
    <tr><td>Visiting museums</td><td>28</td><td>36</td><td>44</td><td>39</td></tr>
  </tbody>
</table>'''

T2_CHART_JS = """
  var ctx2 = document.getElementById('chartT2');
  if (ctx2) {
    new Chart(ctx2.getContext('2d'), {
      type: 'bar',
      data: {
        labels: ['Reading books','Watching streaming','Outdoor exercise','Playing video games','Visiting museums'],
        datasets: [
          { label:'18-29', data:[42,88,64,71,28], backgroundColor:'rgba(21,101,192,0.85)',  borderColor:'#1565C0', borderWidth:1 },
          { label:'30-49', data:[55,79,58,46,36], backgroundColor:'rgba(46,125,50,0.85)',  borderColor:'#2E7D32', borderWidth:1 },
          { label:'50-64', data:[68,62,49,19,44], backgroundColor:'rgba(245,124,0,0.85)',  borderColor:'#E65100', borderWidth:1 },
          { label:'65+',   data:[74,51,33,8,39],  backgroundColor:'rgba(123,31,162,0.85)', borderColor:'#7B1FA2', borderWidth:1 }
        ]
      },
      options: {
        responsive: true,
        maintainAspectRatio: false,
        plugins: {
          legend: { position:'top', labels:{ boxWidth:14, font:{ size:11 } } }
        },
        scales: {
          x: { title:{ display:true, text:'Leisure activity', font:{ weight:'bold', size:12 } }, grid:{ display:false } },
          y: { min:0, max:100, title:{ display:true, text:'Percentage of adults (%)', font:{ weight:'bold', size:12 } }, grid:{ color:'rgba(0,0,0,0.06)' }, ticks:{ stepSize:20, callback: function(v){ return v+'%'; } } }
        }
      }
    });
  }"""

T2_QDATA = {
    'prompt': 'The chart below shows the percentage of adults in Country X who participated in five different leisure activities in 2022, broken down by age group. Summarise the information by selecting and reporting the main features, and make comparisons where relevant. Write at least 150 words.',
    'chartType': 'Grouped bar chart',
}
T2_T2_QDATA = {
    'prompt': 'Some people think that governments should invest more public money in promoting healthy lifestyles in order to reduce the cost of healthcare. Others believe that this money would be better spent on improving medical treatment and hospital facilities. Discuss both views and give your own opinion.',
    'essayType': 'Discussion (both views + opinion)',
}

# ════════════════════════════════════════════════════════════════════════════
# TEST 3 — Two pie charts: household energy City Y 1990 vs 2020
# ════════════════════════════════════════════════════════════════════════════
T3_CHART_HTML = '''
<div class="chart-area-title">Sources of Household Energy Consumption in City Y, 1990 and 2020</div>
<div style="display:flex;gap:1.5rem;flex-wrap:wrap;justify-content:center;align-items:flex-start;">
  <div style="flex:1;min-width:240px;max-width:320px;">
    <div style="text-align:center;font-weight:700;font-size:0.9rem;color:#0D2B4E;margin-bottom:0.5rem;">1990</div>
    <canvas id="chartT3a" height="220"></canvas>
  </div>
  <div style="flex:1;min-width:240px;max-width:320px;">
    <div style="text-align:center;font-weight:700;font-size:0.9rem;color:#0D2B4E;margin-bottom:0.5rem;">2020</div>
    <canvas id="chartT3b" height="220"></canvas>
  </div>
</div>'''

T3_CHART_JS = """
  var pieLabels = ['Coal','Natural gas','Electricity (grid)','Wood / biomass','Solar'];
  var pieColors = ['#37474F','#4A90D9','#FFC107','#795548','#F44336'];
  function makePie(id, data) {
    var el = document.getElementById(id);
    if (!el) return;
    new Chart(el.getContext('2d'), {
      type: 'pie',
      data: {
        labels: pieLabels,
        datasets: [{ data: data, backgroundColor: pieColors, borderColor: '#fff', borderWidth: 2.5 }]
      },
      options: {
        responsive: true,
        maintainAspectRatio: false,
        plugins: {
          legend: { position:'bottom', labels:{ boxWidth:13, font:{ size:10 } } },
          tooltip: { callbacks: { label: function(c){ return ' '+c.label+': '+c.parsed+'%'; } } }
        }
      }
    });
  }
  makePie('chartT3a', [41,28,18,12,1]);
  makePie('chartT3b', [8,32,39,4,17]);"""

T3_QDATA = {
    'prompt': 'The pie charts below show the sources of household energy consumption in City Y in 1990 and 2020. Summarise the information by selecting and reporting the main features, and make comparisons where relevant. Write at least 150 words.',
    'chartType': 'Two pie charts (comparison)',
}
T3_T2_QDATA = {
    'prompt': 'In many cities around the world, traffic congestion and air pollution have become increasingly serious problems. What are the main causes of these problems, and what measures can governments and individuals take to address them?',
    'essayType': 'Problem / Solution',
}

# ════════════════════════════════════════════════════════════════════════════
# TEST 4 — Process diagram: recycling plastic bottles (8 stages)
# ════════════════════════════════════════════════════════════════════════════
T4_CHART_HTML = f'''
<div class="chart-area-title">The Process of Recycling Plastic Bottles (8 Stages)</div>
{SVG_T4}'''

T4_CHART_JS = ""  # SVG diagram needs no JS

T4_QDATA = {
    'prompt': 'The diagram below shows the process of recycling plastic bottles. Summarise the information by selecting and reporting the main features, and make comparisons where relevant. Write at least 150 words.',
    'chartType': 'Process diagram (8 stages, cyclical)',
}
T4_T2_QDATA = {
    'prompt': 'Working from home has become increasingly common in many parts of the world. While this offers a number of benefits, it also has significant drawbacks for both employees and employers. Do the advantages of working from home outweigh the disadvantages?',
    'essayType': 'Advantages / Disadvantages',
}

# ════════════════════════════════════════════════════════════════════════════
# GENERATE ALL 4 FILES
# ════════════════════════════════════════════════════════════════════════════
FILES = [
    (1,
     'The graph below shows the average daily screen time among teenagers aged 13–18 in four countries between 2000 and 2020.',
     'Line Graph', T1_CHART_HTML, T1_CHART_JS, T1_QDATA,
     'Discussion (Both Views + Opinion)',
     '''<p class="t2-body">In many countries today, young people spend an increasing amount of time on electronic devices such as smartphones and tablets. Some people believe this is harmful to their development, while others argue it prepares them for the modern world.</p>
     <p class="t2-question">Discuss both these views and give your own opinion.</p>
     <p class="t2-rubric">Give reasons for your answer and include any relevant examples from your own knowledge or experience.</p>''',
     T1_T2_QDATA),

    (2,
     'The chart below shows the percentage of adults in Country X who participated in five different leisure activities in 2022, broken down by age group.',
     'Grouped Bar Chart + Data Table', T2_CHART_HTML, T2_CHART_JS, T2_QDATA,
     'Discussion (Both Views + Opinion)',
     '''<p class="t2-body">Some people think that governments should invest more public money in promoting healthy lifestyles in order to reduce the cost of healthcare. Others believe that this money would be better spent on improving medical treatment and hospital facilities.</p>
     <p class="t2-question">Discuss both views and give your own opinion.</p>
     <p class="t2-rubric">Give reasons for your answer and include any relevant examples from your own knowledge or experience.</p>''',
     T2_T2_QDATA),

    (3,
     'The pie charts below show the sources of household energy consumption in City Y in 1990 and 2020.',
     'Two Pie Charts (Comparison)', T3_CHART_HTML, T3_CHART_JS, T3_QDATA,
     'Problem / Solution',
     '''<p class="t2-body">In many cities around the world, traffic congestion and air pollution have become increasingly serious problems.</p>
     <p class="t2-question">What are the main causes of these problems, and what measures can governments and individuals take to address them?</p>
     <p class="t2-rubric">Give reasons for your answer and include any relevant examples from your own knowledge or experience.</p>''',
     T3_T2_QDATA),

    (4,
     'The diagram below shows the process of recycling plastic bottles.',
     'Process Diagram (8 Stages)', T4_CHART_HTML, T4_CHART_JS, T4_QDATA,
     'Advantages / Disadvantages',
     '''<p class="t2-body">Working from home has become increasingly common in many parts of the world. While this offers a number of benefits, it also has significant drawbacks for both employees and employers.</p>
     <p class="t2-question">Do the advantages of working from home outweigh the disadvantages?</p>
     <p class="t2-rubric">Give reasons for your answer and include any relevant examples from your own knowledge or experience.</p>''',
     T4_T2_QDATA),
]

if __name__ == '__main__':
    for (n, t1_intro, t1_type, t1_chart_html, t1_chart_js, t1_qd, t2_type, t2_html, t2_qd) in FILES:
        html = build(n, t1_intro, t1_type, t1_chart_html, t1_chart_js, t1_qd, t2_type, t2_html, t2_qd)
        path = os.path.join(BASE, f'cam20-t{n}-writing.html')
        with open(path, 'w', encoding='utf-8') as f:
            f.write(html)
        print(f'Written: {path}  ({len(html):,} chars)')
    print('Done.')
