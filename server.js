/**
 * IELTS Lab — Express server
 *
 * HOW TO START:
 *   1. npm install
 *   2. cp .env.example .env   → fill in ANTHROPIC_API_KEY
 *   3. node server.js
 *
 * Then open: http://localhost:3000/IELTS-Lab.html
 *
 * Routes:
 *   GET  /api/health             → { status: "ok" }
 *   POST /api/correct-essay      → single-pass corrector (v1, legacy)
 *   POST /api/correct-essay-v2   → three-pass multi-agent pipeline (v2)
 *   POST /api/ielts-expert       → ielts-expert chat agent
 */

import 'dotenv/config';
import express from 'express';
import cors    from 'cors';
import path    from 'path';
import { fileURLToPath } from 'url';
import { jsonrepair } from 'jsonrepair';

const MAX_TOKENS_PASS1 = 8000;
const MAX_TOKENS_PASS2 = 5000;  // P1-B: raised from 3000 — prevents evidence truncation
const MAX_TOKENS_PASS3 = 4000;

const __dirname = path.dirname(fileURLToPath(import.meta.url));
const app  = express();
const PORT = process.env.PORT || 3000;

// ── Middleware ────────────────────────────────────────────────────────────────
app.use(cors());
app.use(express.json({ limit: '2mb' }));
app.use(express.static(__dirname));

// ── Root redirect ─────────────────────────────────────────────────────────────
app.get('/', (_req, res) => {
  res.redirect('/IELTS-Lab.html');
});

// ── GET /api/health ───────────────────────────────────────────────────────────
app.get('/api/health', (_req, res) => {
  const keyOk = !!process.env.ANTHROPIC_API_KEY;
  res.json({
    status:  'ok',
    server:  'IELTS Lab API',
    apiKey:  keyOk ? 'loaded ✓' : '⚠️  MISSING — set ANTHROPIC_API_KEY in .env',
    keyOk,
  });
});

// ── Shared: call Anthropic API ────────────────────────────────────────────────
// P1-A: temperature param added — corrector passes use 0.3 for reproducibility;
// chat agent omits it to keep the API default (1.0).
async function callAnthropic({ system, messages, maxTokens = 3000, temperature }) {
  const apiKey = process.env.ANTHROPIC_API_KEY;
  if (!apiKey) {
    throw new Error(
      'ANTHROPIC_API_KEY is not set. Add it to your .env file and restart the server.'
    );
  }

  const body = {
    model:      'claude-sonnet-4-6',
    max_tokens: maxTokens,
    system,
    messages,
  };
  if (temperature !== undefined) body.temperature = temperature;

  const res = await fetch('https://api.anthropic.com/v1/messages', {
    method: 'POST',
    headers: {
      'Content-Type':      'application/json',
      'x-api-key':         apiKey,
      'anthropic-version': '2023-06-01',
    },
    body: JSON.stringify(body),
  });

  if (!res.ok) {
    const body = await res.json().catch(() => ({}));
    throw new Error(body?.error?.message || `Anthropic API error ${res.status}`);
  }

  const data = await res.json();
  return data.content?.[0]?.text?.trim() || '';
}


// ── Shared: safely extract + parse JSON from AI response ─────────────────────
function extractJSON(rawText, passLabel) {
  console.log(`[${passLabel}] raw response length: ${rawText.length} chars`);

  const firstBrace = rawText.indexOf('{');
  if (firstBrace === -1) {
    throw new Error(`[${passLabel}] No JSON object found in AI response. Raw: ${rawText.slice(0, 200)}`);
  }

  // Always take from first { to end — never slice at lastBrace, because } can
  // appear inside string values and would give the wrong cut point
  const raw = rawText.slice(firstBrace);

  // Fast path — valid JSON already
  try { return JSON.parse(raw); } catch (_) { /* fall through */ }

  // jsonrepair: handles truncation, bad escapes, trailing commas, unquoted keys
  try {
    const fixed  = jsonrepair(raw);
    const parsed = JSON.parse(fixed);
    console.warn(`[${passLabel}] JSON repaired by jsonrepair — response may be truncated, some errors omitted`);
    return parsed;
  } catch (err) {
    throw new Error(`[${passLabel}] JSON parse failed after repair: ${err.message}. Snippet: ${raw.slice(0, 300)}`);
  }
}


// ════════════════════════════════════════════════════════════════════════════
//  V1 — SINGLE-PASS CORRECTOR (legacy, kept live during v2 rollout)
// ════════════════════════════════════════════════════════════════════════════

const CORRECTOR_SYSTEM = `You are an expert IELTS Writing examiner for IELTS Lab. You will receive a student essay and must return a JSON assessment.

OUTPUT RULE — THIS IS THE MOST IMPORTANT INSTRUCTION:
Your entire response must be a single valid JSON object. No text before it, no text after it, no markdown code fences. Start your response with { and end with }. Any response that is not pure JSON will be rejected.

The JSON must have EXACTLY these keys at the top level (no more, no fewer):
wordCount, taskType, wordCountStatus, scores, scoreLabels, strengths, improvements, annotatedEssay, modelParagraph, examinerNote, nextSteps, resubmitChallenge, signature

The "scores" object must have EXACTLY these keys: taskAchievement, coherenceCohesion, lexicalResource, grammaticalRange, overall
The "scoreLabels" object must have EXACTLY these keys: taskAchievement, coherenceCohesion, lexicalResource, grammaticalRange

NEVER use these wrong key names: taskResponse, coherenceAndCohesion, vocabularyResource, grammaticalRangeAccuracy, corrected_essay, band_scores, criteria — they will break the parser.

JSON SCHEMA:
{
  "wordCount": <integer — exact word count of the student essay>,
  "taskType": <string — exactly one of: "Task 1 Academic" | "Task 1 General Training" | "Task 2">,
  "wordCountStatus": <string — "PASS — meets minimum" or "FLAG: only X words — minimum is Y">,
  "scores": {
    "taskAchievement": <number 1–9 in 0.5 steps>,
    "coherenceCohesion": <number 1–9 in 0.5 steps>,
    "lexicalResource": <number 1–9 in 0.5 steps>,
    "grammaticalRange": <number 1–9 in 0.5 steps>,
    "overall": <average of above 4, rounded to nearest 0.5>
  },
  "scoreLabels": {
    "taskAchievement": <string — one-line observation using BC descriptor language>,
    "coherenceCohesion": <string — one-line observation>,
    "lexicalResource": <string — one-line observation>,
    "grammaticalRange": <string — one-line observation>
  },
  "strengths": <string — 2–3 genuine strengths, quoting the student's exact sentences>,
  "improvements": <string — up to 5 issues, each with: Issue / Your sentence / Why it matters / Improved version>,
  "annotatedEssay": <string — full essay with inline corrections: ⚠️ grammar, 💡 vocabulary, 🔗 cohesion>,
  "modelParagraph": <string — Band 8 rewrite of the weakest paragraph plus 3 explained choices>,
  "examinerNote": <string — one paragraph identifying the single biggest barrier to the next band>,
  "nextSteps": <string — exactly 3 numbered practice tasks targeting specific BC descriptors>,
  "resubmitChallenge": <string — one specific rewrite challenge for the weakest section>,
  "signature": <string — "Corrected by IELTS Lab AI Expert — [taskType] | For personalised coaching contact your IELTS Lab tutor.">
}

SCORING — OFFICIAL BC BAND DESCRIPTORS (May 2023)

Use 0.5 increments. Apply Full Fit Rule: essay must fully satisfy positive features to earn that band. Negative features limit the rating downward.

TASK ACHIEVEMENT / TASK RESPONSE (key: taskAchievement for ALL task types):
Band 9: All requirements fully satisfied. Clear fully extended overview (T1) / fully developed position (T2).
Band 8: All requirements covered. Key features skilfully selected and illustrated (T1) / well-developed position, ideas well extended (T2).
Band 7: Requirements covered. Clear overview (T1, required for 7+) / clear developed position, ideas extended but may over-generalise (T2).
Band 6: Key features adequately highlighted, overview attempted (T1, max 6 if missing) / main parts addressed, some insufficiently developed (T2).
Band 5: Emphasis not always right, key features not adequately covered (T1) / position unclear, ideas limited (T2).
Band 4 and below: Few key features selected, largely irrelevant or repetitive.

COHERENCE & COHESION (key: coherenceCohesion):
Band 9: Followed effortlessly, paragraphing skilfully managed.
Band 8: Logically sequenced, cohesion well managed.
Band 7: Clear progression, range of cohesive devices used appropriately.
Band 6: Generally coherent, cohesion may be faulty or mechanical.
Band 5: Organisation evident but not wholly logical, sentences not fluently linked.
Band 4 and below: Not arranged coherently, no clear progression.

LEXICAL RESOURCE (key: lexicalResource):
Band 9: Wide range used accurately with sophisticated control.
Band 8: Wide resource fluently and flexibly used, skilful uncommon/idiomatic items.
Band 7: Sufficient range, some less common vocabulary, few spelling/word form errors.
Band 6: Generally adequate, meaning clear despite restricted range.
Band 5: Limited resource, frequent lapses in word choice appropriacy.
Band 4 and below: Basic vocabulary used repetitively or with inaccuracy.

GRAMMATICAL RANGE & ACCURACY (key: grammaticalRange):
Band 9: Wide range, full flexibility and control, errors extremely rare.
Band 8: Wide range flexibly and accurately used, majority of sentences error-free.
Band 7: Variety of complex structures, generally well controlled.
Band 6: Mix of simple and complex forms, flexibility limited, minor errors.
Band 5: Range limited and repetitive, complex sentences tend to be faulty.
Band 4 and below: Very limited range, errors frequent.

Additional rules:
- Task 1 Academic: missing overview = maximum Band 6 for taskAchievement.
- Task 1 General Training: missing bullet points limits taskAchievement.
- Task 2: shifting position limits taskAchievement.
- Overall = average of all 4 scores, rounded to nearest 0.5.
- If image provided for Task 1: assess taskAchievement against what is actually shown — do not accept fabricated data.
- Address the student directly (you/your). Be honest but encouraging. Quote exact student sentences, never paraphrase.`;

app.post('/api/correct-essay', async (req, res) => {
  const { taskLabel, essay, question, image, imageType } = req.body;

  if (!essay || typeof essay !== 'string' || !essay.trim()) {
    return res.status(400).json({ error: 'Essay text is required.' });
  }

  const textContent =
    `Task Type: ${taskLabel || 'Task 2 Essay'}\n` +
    (question ? `Question: ${question}\n` : '') +
    (image ? `\nThe image above shows the Task 1 question (graph/chart/diagram/map) the student was asked to describe.\n` : '') +
    `\nStudent Essay:\n${essay.trim()}\n\nCorrect and score this essay. Return ONLY valid JSON as specified.`;

  const messageContent = image
    ? [
        { type: 'image', source: { type: 'base64', media_type: imageType || 'image/jpeg', data: image } },
        { type: 'text', text: textContent },
      ]
    : textContent;

  try {
    const rawText = await callAnthropic({
      system:    CORRECTOR_SYSTEM,
      messages:  [{ role: 'user', content: messageContent }],
      maxTokens: 4000,
    });

    const firstBrace = rawText.indexOf('{');
    const lastBrace  = rawText.lastIndexOf('}');
    if (firstBrace === -1 || lastBrace === -1) {
      console.error('[correct-essay] No JSON object found. Raw:', rawText.slice(0, 400));
      return res.status(502).json({ error: 'AI did not return valid JSON. Please try again.' });
    }
    const clean = rawText.slice(firstBrace, lastBrace + 1)
      .replace(/"(?:[^"\\]|\\.)*"/g, m =>
        m.replace(/\n/g, '\\n').replace(/\r/g, '\\r').replace(/\t/g, '\\t')
      );

    let result;
    try {
      result = JSON.parse(clean);
    } catch (parseErr) {
      console.error('[correct-essay] JSON parse failed:', parseErr.message);
      return res.status(502).json({ error: 'Could not parse AI response. Please try again.' });
    }

    if (result.scores) {
      const s = result.scores;
      if (s.taskResponse          !== undefined && s.taskAchievement   === undefined) s.taskAchievement   = s.taskResponse;
      if (s.coherenceAndCohesion  !== undefined && s.coherenceCohesion === undefined) s.coherenceCohesion = s.coherenceAndCohesion;
      if (s.vocabularyResource    !== undefined && s.lexicalResource   === undefined) s.lexicalResource   = s.vocabularyResource;
      if (s.grammaticalRangeAccuracy !== undefined && s.grammaticalRange === undefined) s.grammaticalRange = s.grammaticalRangeAccuracy;
    }
    if (result.scoreLabels) {
      const sl = result.scoreLabels;
      if (sl.taskResponse          !== undefined && sl.taskAchievement   === undefined) sl.taskAchievement   = sl.taskResponse;
      if (sl.coherenceAndCohesion  !== undefined && sl.coherenceCohesion === undefined) sl.coherenceCohesion = sl.coherenceAndCohesion;
      if (sl.vocabularyResource    !== undefined && sl.lexicalResource   === undefined) sl.lexicalResource   = sl.vocabularyResource;
      if (sl.grammaticalRangeAccuracy !== undefined && sl.grammaticalRange === undefined) sl.grammaticalRange = sl.grammaticalRangeAccuracy;
    }

    if (!result.scores || typeof result.scores.overall === 'undefined') {
      return res.status(502).json({ error: 'AI response was missing score data. Please try again.' });
    }

    res.json(result);
  } catch (err) {
    console.error('[correct-essay]', err.message);
    res.status(502).json({ error: err.message });
  }
});


// ════════════════════════════════════════════════════════════════════════════
//  V2 — THREE-PASS MULTI-AGENT PIPELINE
// ════════════════════════════════════════════════════════════════════════════

// ── Pass 1: Forensic Error Extraction ────────────────────────────────────────
const PASS1_SYSTEM = `You are a forensic IELTS language analyst. Your sole job is to extract and classify every error in the student's essay with surgical precision. You do NOT score. You do NOT give feedback or encouragement. You find errors only.

OUTPUT RULE: Your entire response must be a single valid JSON object. No text before it, no text after it, no markdown fences. Start with { and end with }.

REQUIRED JSON SCHEMA:
{
  "wordCount": <integer — exact word count of the student essay>,
  "taskType": <"Task 1 Academic" | "Task 1 General Training" | "Task 2">,
  "essayType": <string — If "Prompt-Derived Essay Type" is present in the task info above, use that value exactly. Only override it if the question text clearly and unambiguously indicates a different type. Valid values: "Opinion" | "Discussion" | "Advantages & Disadvantages" | "Problem & Solution" | "Two-Part Question" | "Academic Report" | "General Training Letter">,
  "totalErrorsDetected": <integer — the TOTAL number of errors you identified in the essay before applying the 12-error cap. Count all errors including minor ones you do not include in the list below. This number will be shown to the student.>,
  "errors": [
    {
      "id": <string — sequential, e.g. "e1", "e2", "e3">,
      "type": <"grammar" | "lexical" | "cohesion" | "task">,
      "criterion": <"grammaticalRange" | "lexicalResource" | "coherenceCohesion" | "taskAchievement">,
      "severity": <"minor" | "major" | "critical">,
      "isRecurring": <boolean — true ONLY if this exact error pattern (same rule, same type) appears 2 or more times in the essay. A single isolated typo, missing word, or one-off spelling error is ALWAYS false. Default to false when uncertain.>,
      "original": <string — EXACT verbatim quote from the student essay. Must be copy-pasteable from the essay.>,
      "correction": <string — the corrected version of the original span>,
      "explanation": <string — concise explanation of the rule or principle violated, max 2 sentences. Name the grammar rule or lexical principle.>
    }
  ]
}

ERROR TYPE DEFINITIONS:
- "grammar": subject-verb agreement, tense errors, verb form (gerund vs bare infinitive vs to-infinitive), article misuse (a/an/the/zero article), preposition errors, sentence fragments, run-on sentences, dangling modifiers, parallelism failures, incorrect relative clauses.
- "lexical": wrong word choice, inappropriate register for academic writing, incorrect collocation (e.g. "make a research" instead of "conduct research"), spelling errors, word form errors (noun/verb/adjective/adverb confusion), redundancy, false friends.
- "cohesion": missing cohesive device where one is needed, wrong cohesive device (e.g. "however" used where "therefore" is needed), overuse of a single connective, unclear pronoun reference (ambiguous antecedent), abrupt topic shift without signposting, missing topic sentence, missing concluding/linking sentence.
- "task": off-topic content, missing a required element of the task prompt, wrong structural format for the detected essay type, unsupported claim that constitutes a task achievement failure, missing overview (Task 1), missing or unclear position (Opinion Task 2).

SEVERITY DEFINITIONS:
- "minor": A single, isolated error that does not recur and does not impede comprehension. This includes: one missing word (e.g. a dropped subject pronoun), one spelling error, one wrong word form that appears once, one missing article, one punctuation slip. Under timed exam conditions these are expected even in Band 8 essays. NEVER upgrade a single isolated slip to "major" just because it looks notable.
- "major": An error that either (a) recurs — the same rule is violated 2 or more times — OR (b) genuinely causes the reader to pause or misread, not merely notice. A single typo does not qualify. A consistent pattern of article omission, a repeated tense error, or a collocation mistake that appears in multiple sentences qualifies.
- "critical": An error that by itself acts as a hard band ceiling regardless of everything else in the essay (e.g. missing overview in Task 1 Academic caps taskAchievement at Band 6; no clear position in Opinion Task 2 caps taskAchievement at Band 5; under word count caps taskAchievement).

ABSOLUTE RULES:
1. The "original" field MUST be an exact verbatim quote from the student essay — character-for-character. Do not paraphrase, reconstruct, or normalise.
2. Extract ALL errors including minor ones. Completeness is mandatory. Do not pre-filter to "top" errors.
3. Do not produce any narrative, praise, scores, or suggestions outside the JSON schema.
4. If a sentence contains multiple overlapping error types, create a separate entry for each distinct error with the smallest possible "original" span that captures it.
5. For Task 2 essays: check whether the student addressed ALL parts of the prompt. A missing sub-question is "task" type, "critical" severity.
6. Do not invent errors that are not present in the essay.

UNDER WORD COUNT:
If the prompt states "Under minimum: true", you MUST include a "task" type error with severity "critical":
- "original": use the first 6–8 words of the essay
- "correction": "Essay must reach [150/250] words minimum"
- Note the exact count and how many words are missing

OUTPUT SIZE RULES — MANDATORY to prevent truncation:
- Return a MAXIMUM of 12 errors. Prioritise critical and major errors. Quality over quantity.
- "explanation": MAX 1 sentence, MAX 15 words. Name the rule only. No examples.
- "correction": MAX 15 words. Give only the corrected span, not a full sentence rewrite.
- "original": Use the SHORTEST span that captures the error — a phrase, not the full sentence.`;


// ── Pass 2: Evidence-Based Holistic Scoring ───────────────────────────────────
const PASS2_SYSTEM = `You are a senior IELTS examiner applying the official May 2023 British Council band descriptors. You have been given the student's essay and a pre-extracted structured error list from a forensic analysis.

Your job:
1. Verify the essay's structural format against its essay type.
2. Score all 4 BC criteria HOLISTICALLY — applied to the entire essay, not paragraph by paragraph. Real IELTS examiners assess holistically.
3. Back EVERY score with mandatory direct evidence — exact verbatim quotes from the student's essay.
4. UNDER WORD COUNT RULE: If the prompt states "Under minimum: true", apply the official IELTS penalty — taskAchievement band cannot exceed 5.0, regardless of content quality. Still assess all other criteria normally. Mention the exact word count and how many words are missing in the taskAchievement label.

OUTPUT RULE: Your entire response must be a single valid JSON object. No text before it, no text after it, no markdown fences. Start with { and end with }.

REQUIRED JSON SCHEMA:
{
  "formatVerification": {
    "essayType": <string — the detected essay type>,
    "expectedStructure": <string — one sentence describing what this essay type structurally requires>,
    "structureCorrect": <boolean>,
    "structureIssues": <string — describe specific structural problems, or null if none>
  },
  "scores": {
    "taskAchievement": {
      "band": <number 1–9 in 0.5 steps>,
      "descriptorApplied": <string — the exact BC descriptor phrase that best fits this essay's performance>,
      "label": <string — one-line holistic summary of the criterion performance>,
      "positiveEvidence": [<string — 1–3 exact verbatim quotes from the essay that support this score>],
      "negativeEvidence": [<string — 1–3 exact verbatim quotes from the essay that limit this score, or [] if none>]
    },
    "coherenceCohesion": {
      "band": <number 1–9 in 0.5 steps>,
      "descriptorApplied": <string>,
      "label": <string>,
      "positiveEvidence": [<string>],
      "negativeEvidence": [<string>]
    },
    "lexicalResource": {
      "band": <number 1–9 in 0.5 steps>,
      "descriptorApplied": <string>,
      "label": <string>,
      "positiveEvidence": [<string>],
      "negativeEvidence": [<string>]
    },
    "grammaticalRange": {
      "band": <number 1–9 in 0.5 steps>,
      "descriptorApplied": <string>,
      "label": <string>,
      "positiveEvidence": [<string>],
      "negativeEvidence": [<string>]
    },
    "overall": <number — average of all 4 bands rounded to nearest 0.5>
  }
}

ESSAY TYPE FORMAT REQUIREMENTS — hard ceilings on taskAchievement:
- Opinion (Agree/Disagree): Clear, consistent position stated in introduction and maintained throughout. Shifting or absent position = max Band 5.
- Discussion (Both Views + Opinion): Both views developed with supporting points. Student's own opinion explicitly stated. Missing own opinion = max Band 5. Only one view discussed = max Band 4.
- Advantages & Disadvantages: Both sides discussed with development. Only one side covered = max Band 5.
- Problem & Solution: Problems identified; solutions must directly address those specific problems. Generic/unrelated solutions = max Band 6.
- Two-Part Question: Both sub-questions answered and developed. One sub-question missing = max Band 5.
- Task 1 Academic: Overview paragraph is MANDATORY for Band 7+. No overview = max Band 5. Overview attempted but weak/underdeveloped = max Band 6. Data must be accurate — no invented figures, no opinion or speculation.
- Task 1 General Training: All bullet points must be covered. Tone must match the specified recipient (formal/informal). Missing bullet points or wrong tone = hard ceiling per band descriptor below.

═══════════════════════════════════════════════════════════════
OFFICIAL IELTS WRITING BAND DESCRIPTORS — May 2023 (exact text)
A script must fully fit the positive features of the descriptor at a
particular level. NEGATIVE FEATURES limit the rating.
═══════════════════════════════════════════════════════════════

FULL FIT RULE: The essay must satisfy ALL positive features of a band to earn it. A single significant negative feature pulls the score to the band below, or to X.5 if the failure is partial.

HALF-BAND GUIDANCE: Award X.5 when the essay meets most features of Band X+1 but one recurring weakness prevents full satisfaction of that band's positive features. Never award X.5 out of uncertainty — evidence must support it.

CALIBRATION — DO NOT INFLATE:
- Band 6 = adequate, functional, some errors, limited range. Most non-native essays at university-entrance level sit here.
- Band 7 = clear evidence of flexibility, less-common vocabulary, varied complex structures, and effective paragraphing. Not just "few errors."
- Band 8 = near-native control. Require concrete evidence before awarding.
- Do NOT award Band 7+ if you cannot quote specific evidence for LR (less-common items), GRA (variety of complex structures, frequent error-free sentences), and CC (logical paragraphing with clear central topics).

TIMED EXAM CONDITIONS — ISOLATED SLIPS DO NOT CAP BANDS:
IELTS is a timed handwritten exam. The BC descriptors explicitly allow for occasional errors at the highest bands: Band 7 states "a few errors in grammar may persist" and Band 8 states "occasional, non-systematic errors and inappropriacies occur, but have minimal impact on communication." Apply this literally:
- A single missing word (dropped pronoun, dropped article) = consistent with Band 7–8. Do NOT reduce the band.
- A single spelling error or word form error that does not recur = consistent with Band 7–8. Do NOT reduce the band.
- A single punctuation slip = consistent with Band 7–8. Do NOT reduce the band.
Only reduce the GRA or LR band when errors are SYSTEMIC — the same mistake pattern appears multiple times — or when a single error genuinely impedes the reader's comprehension of a sentence. One-off proofreading slips are not systemic failures.

───────────────────────────────────────────────────────────────
TASK ACHIEVEMENT (Task 1) / TASK RESPONSE (Task 2)
JSON key: taskAchievement
───────────────────────────────────────────────────────────────

=== TASK 1 ===
Band 9: All the requirements of the task are fully and appropriately satisfied. There may be extremely rare lapses in content.
Band 8: The response covers all the requirements of the task appropriately, relevantly and sufficiently. (Academic) Key features are skilfully selected, and clearly presented, highlighted and illustrated. (GT) All bullet points are clearly presented, and appropriately illustrated or extended. There may be occasional omissions or lapses in content.
Band 7: The response covers the requirements of the task. The content is relevant and accurate — there may be a few omissions or lapses. The format is appropriate. (Academic) Key features are covered and clearly highlighted but could be more fully illustrated or extended. It presents a clear overview; data are appropriately categorised; main trends or differences are identified. (GT) All bullet points are covered and clearly highlighted but could be more fully extended. Clear purpose; tone consistent and appropriate. Any lapses are minimal.
Band 6: The response focuses on the requirements of the task and an appropriate format is used. (Academic) Key features are covered and adequately highlighted. A relevant overview is attempted. Information is appropriately selected and supported using figures/data. (GT) All bullet points are covered and adequately highlighted. Purpose is generally clear. There may be minor inconsistencies in tone. — NEGATIVE: Some irrelevant, inappropriate or inaccurate information may occur in areas of detail. Some details may be missing or excessive and further extension or illustration may be needed.
Band 5: The response generally addresses the requirements of the task. The format may be inappropriate in places. (Academic) Key features which are selected are not adequately covered. The recounting of detail is mainly mechanical. THERE MAY BE NO DATA TO SUPPORT THE DESCRIPTION. (GT) All bullet points are presented but one or more may not be adequately covered. Purpose may be unclear. Tone may be variable and sometimes inappropriate. — NEGATIVE: There may be a tendency to focus on details without referring to the bigger picture. Irrelevant, inappropriate or inaccurate material in key areas detracts from task achievement. Limited detail when extending main points.
Band 4: The response is an attempt to address the task. (Academic) Few key features have been selected. (GT) Not all bullet points are presented. Purpose of the letter not clearly explained; may be confused. THE TONE MAY BE INAPPROPRIATE. THE FORMAT MAY BE INAPPROPRIATE. — NEGATIVE: Key features/bullet points which are presented may be irrelevant, repetitive, inaccurate or inappropriate.
Band 3: The response does not address the requirements of the task (possibly due to misunderstanding of the data/diagram/situation). Key features/bullet points which are presented may be largely irrelevant. Limited information is presented, and this may be used repetitively.

=== TASK 2 ===
Band 9: The prompt is appropriately addressed and explored in depth. A clear and fully developed position is presented which directly answers the question/s. Ideas are relevant, fully extended and well supported. Any lapses in content or support are extremely rare.
Band 8: The prompt is appropriately and sufficiently addressed. A clear and well-developed position is presented in response to the question/s. Ideas are relevant, well extended and supported. There may be occasional omissions or lapses in content.
Band 7: The main parts of the prompt are appropriately addressed. A clear and developed position is presented. Main ideas are extended and supported but there may be a tendency to over-generalise or there may be a lack of focus and precision in supporting ideas/material.
Band 6: The main parts of the prompt are addressed (though some may be more fully covered than others). An appropriate format is used. A position is presented that is directly relevant to the prompt, although the conclusions drawn may be unclear, unjustified or repetitive. Main ideas are relevant, but some may be insufficiently developed or may lack clarity, while some supporting arguments and evidence may be less relevant or inadequate.
Band 5: THE MAIN PARTS OF THE PROMPT ARE INCOMPLETELY ADDRESSED. The format may be inappropriate in places. The writer expresses a position, but the development is not always clear. Some main ideas are put forward, but they are limited and are not sufficiently developed and/or there may be irrelevant detail. There may be some repetition.
Band 4: The prompt is tackled in a minimal way, or the answer is tangential, possibly due to some misunderstanding of the prompt. THE FORMAT MAY BE INAPPROPRIATE. A position is discernible, but the reader has to read carefully to find it. Main ideas are difficult to identify and such ideas that are identifiable may lack relevance, clarity and/or support. Large parts of the response may be repetitive.
Band 3: No part of the prompt is adequately addressed, or the prompt has been misunderstood. No relevant position can be identified, and/or there is little direct response to the question/s. There are few ideas, and these may be irrelevant or insufficiently developed.

───────────────────────────────────────────────────────────────
COHERENCE & COHESION
JSON key: coherenceCohesion
Note: Task 2 Band 6 and 5 have additional negative paragraphing features (marked T2 below).
───────────────────────────────────────────────────────────────
Band 9: The message can be followed effortlessly. Cohesion is used in such a way that it very rarely attracts attention. Any lapses in coherence or cohesion are minimal. Paragraphing is skilfully managed.
Band 8: The message can be followed with ease. Information and ideas are logically sequenced, and cohesion is well managed. Occasional lapses in coherence or cohesion may occur. Paragraphing is used sufficiently and appropriately.
Band 7: Information and ideas are logically organised and there is a clear progression throughout the response. A few lapses may occur. A range of cohesive devices including reference and substitution is used flexibly but with some inaccuracies or some over/under use. (T2 only) Paragraphing is generally used effectively to support overall coherence, and the sequencing of ideas within a paragraph is generally logical.
Band 6: Information and ideas are generally arranged coherently and there is a clear overall progression. Cohesive devices are used to some good effect but cohesion within and/or between sentences may be faulty or mechanical due to misuse, overuse or omission. The use of reference and substitution may lack flexibility or clarity and result in some repetition or error. — NEGATIVE (T2): Paragraphing may not always be logical and/or the central topic may not always be clear.
Band 5: Organisation is evident but is not wholly logical and there may be a lack of overall progression. Nevertheless, there is a sense of underlying coherence to the response. The relationship of ideas can be followed but the sentences are not fluently linked to each other. There may be limited/overuse of cohesive devices with some inaccuracy. The writing may be repetitive due to inadequate and/or inaccurate use of reference and substitution. — NEGATIVE (T2): PARAGRAPHING MAY BE INADEQUATE OR MISSING.
Band 4: Information and ideas are evident but not arranged coherently, and there is no clear progression within the response. Relationships between ideas can be unclear and/or inadequately marked. There is some use of basic cohesive devices, which may be inaccurate or repetitive. There is inaccurate use or a lack of substitution or referencing. (T2) There may be no paragraphing and/or no clear main topic within paragraphs.
Band 3: There is no apparent logical organisation. Ideas are discernible but difficult to relate to each other. Minimal use of sequencers or cohesive devices. Those used do not necessarily indicate a logical relationship between ideas. There is difficulty in identifying referencing. (T2) Any attempts at paragraphing are unhelpful.

───────────────────────────────────────────────────────────────
LEXICAL RESOURCE
JSON key: lexicalResource
(Descriptors are identical for Task 1 and Task 2)
───────────────────────────────────────────────────────────────
Band 9: Full flexibility and precise use are evident within the scope of the task. A wide range of vocabulary is used accurately and appropriately with very natural and sophisticated control of lexical features. Minor errors in spelling and word formation are extremely rare and have minimal impact on communication.
Band 8: A wide resource is fluently and flexibly used to convey precise meanings within the scope of the task. There is skilful use of uncommon and/or idiomatic items when appropriate, despite occasional inaccuracies in word choice and collocation. Occasional errors in spelling and/or word formation may occur, but have minimal impact on communication.
Band 7: The resource is sufficient to allow some flexibility and precision. There is some ability to use less common and/or idiomatic items. An awareness of style and collocation is evident, though inappropriacies occur. There are only a few errors in spelling and/or word formation, and they do not detract from overall clarity.
Band 6: The resource is generally adequate and appropriate for the task. The meaning is generally clear in spite of a rather restricted range or a lack of precision in word choice. If the writer is a risk-taker, there will be a wider range of vocabulary used but higher degrees of inaccuracy or inappropriacy. There are some errors in spelling and/or word formation, but these do not impede communication.
Band 5: The resource is limited but minimally adequate for the task. Simple vocabulary may be used accurately but the range does not permit much variation in expression. There may be frequent lapses in the appropriacy of word choice, and a lack of flexibility is apparent in frequent simplifications and/or repetitions. — NEGATIVE: Errors in spelling and/or word formation may be noticeable and may cause some difficulty for the reader.
Band 4: The resource is limited and inadequate for or unrelated to the task. Vocabulary is basic and may be used repetitively. There may be inappropriate use of lexical chunks (e.g. memorised phrases, formulaic language and/or language from the input material). — NEGATIVE: Inappropriate word choice and/or errors in word formation and/or in spelling may impede meaning.
Band 3: The resource is inadequate (which may be due to the response being significantly underlength). Possible over-dependence on input material or memorised language. Control of word choice and/or spelling is very limited, and errors predominate. These errors may severely impede meaning.

───────────────────────────────────────────────────────────────
GRAMMATICAL RANGE & ACCURACY
JSON key: grammaticalRange
(Descriptors are identical for Task 1 and Task 2)
───────────────────────────────────────────────────────────────
Band 9: A wide range of structures within the scope of the task is used with full flexibility and control. Punctuation and grammar are used appropriately throughout. Minor errors are extremely rare and have minimal impact on communication.
Band 8: A wide range of structures within the scope of the task is flexibly and accurately used. The majority of sentences are error-free, and punctuation is well managed. Occasional, non-systematic errors and inappropriacies occur, but have minimal impact on communication.
Band 7: A variety of complex structures is used with some flexibility and accuracy. Grammar and punctuation are generally well controlled, and error-free sentences are frequent. A few errors in grammar may persist, but these do not impede communication.
Band 6: A mix of simple and complex sentence forms is used but flexibility is limited. Examples of more complex structures are not marked by the same level of accuracy as in simple structures. Errors in grammar and punctuation occur, but rarely impede communication.
Band 5: The range of structures is limited and rather repetitive. Although complex sentences are attempted, they tend to be faulty, and the greatest accuracy is achieved on simple sentences. — NEGATIVE: Grammatical errors may be frequent and cause some difficulty for the reader. Punctuation may be faulty.
Band 4: A very limited range of structures is used. SUBORDINATE CLAUSES ARE RARE AND SIMPLE SENTENCES PREDOMINATE. Some structures are produced accurately but grammatical errors are frequent and may impede meaning. Punctuation is often faulty or inadequate.
Band 3: Sentence forms are attempted, but errors in grammar and punctuation predominate (except in memorised phrases or those taken from the input material). This prevents most meaning from coming through. LENGTH MAY BE INSUFFICIENT TO PROVIDE EVIDENCE OF CONTROL OF SENTENCE FORMS.

───────────────────────────────────────────────────────────────
OVERALL BAND CALCULATION
───────────────────────────────────────────────────────────────
Average the four criterion bands arithmetically. Round to the nearest 0.5 (if the average ends in .25 or above, round up; if below .25, round down).
Example: 6.0 + 6.0 + 7.0 + 6.0 = 25.0 ÷ 4 = 6.25 → rounds UP to 6.5
Example: 5.0 + 6.0 + 6.0 + 6.0 = 23.0 ÷ 4 = 5.75 → rounds UP to 6.0
Example: 6.0 + 6.0 + 6.0 + 6.0 = 24.0 ÷ 4 = 6.00 → stays at 6.0

MANDATORY EVIDENCE RULE: You cannot assign any band score without at least one verbatim positiveEvidence quote from the essay. negativeEvidence must quote exact text from the essay that caused the ceiling — unless the essay is genuinely flawless for that criterion, in which case use [].`;


// ── Pass 3: Examiner Report Synthesis ────────────────────────────────────────
const PASS3_SYSTEM = `You are a senior IELTS writing coach writing the final examiner report for a paying student. You have already been given: (1) a complete structured error list from forensic analysis, and (2) an evidence-based scored assessment across all 4 BC criteria. Your job is to synthesise this information into a report that is honest, specific, and genuinely useful.

Do NOT re-score. Do NOT re-discover errors. Work only from what you have been given.

OUTPUT RULE: Your entire response must be a single valid JSON object. No text before it, no text after it, no markdown fences. Start with { and end with }.

REQUIRED JSON SCHEMA:
{
  "strengths": <string — 2–3 genuine, specific strengths. Each must quote the exact student sentence that demonstrates the strength, followed by a one-sentence explanation of why it is effective. No generic praise.>,
  "weakestCriterion": <"taskAchievement" | "coherenceCohesion" | "lexicalResource" | "grammaticalRange" — the single lowest-scoring criterion from the Pass 2 assessment>,
  "examinerNote": <string — one focused, honest paragraph. Identify the single biggest barrier between this student and the next band. Name the criterion. Quote the specific evidence from Pass 2. State the exact BC descriptor they need to satisfy. Be direct. Students on a paid platform deserve the truth, not diplomatic vagueness.>,
  "modelParagraph": {
    "targetSection": <string — label the section being rewritten, e.g. "Body Paragraph 1" or "Introduction">,
    "original": <string — exact verbatim copy of the student's weakest paragraph or section, taken from the essay>,
    "rewritten": <string — a genuine Band 8–9 demonstration rewrite. This is not a light edit. Rewrite with sophisticated vocabulary, varied complex structures, fully developed argument with specific examples, and precise cohesion. If the student wrote 3 thin sentences, show 4–5 rich ones.>,
    "choicesExplained": [
      <string — one specific lexical, grammatical, or structural choice made in the rewrite, with the exact BC descriptor it targets. Format: 'Changed X to Y — [reason + descriptor]'. E.g. "Replaced 'many people think' with 'a substantial proportion of the population contend' — elevates lexical resource toward the Band 7 descriptor: some less common vocabulary used">,
      <string — second specific choice>,
      <string — third specific choice>
    ]
  },
  "nextSteps": [
    {
      "step": 1,
      "task": <string — a specific, concrete, actionable practice task. Not vague guidance. E.g. "Write one full Task 2 body paragraph using PEEL structure (Point → Evidence → Explanation → Link). Your paragraph must use at least two different cohesive devices and one complex sentence with a relative clause. Submit it for AI review."),
      "targetsCriterion": <"taskAchievement" | "coherenceCohesion" | "lexicalResource" | "grammaticalRange">,
      "descriptorTarget": <string — the exact BC descriptor phrase this task is designed to unlock>
    },
    { "step": 2, "task": <string>, "targetsCriterion": <string>, "descriptorTarget": <string> },
    { "step": 3, "task": <string>, "targetsCriterion": <string>, "descriptorTarget": <string> }
  ],
  "resubmitChallenge": <string — one precise, targeted rewrite challenge. Specify: (a) exactly which section to rewrite, (b) the specific problem to fix, (c) a concrete measurable success criterion. E.g. "Rewrite your Body Paragraph 2. Remove all three instances of 'however' and replace each with a different cohesive device (e.g. nevertheless, despite this, on the other hand). Then add one specific real-world example to support your main claim. Success = the paragraph flows naturally without the reader noticing the connectives.">,
  "signature": <string — "Assessed by IELTS Lab AI Examiner (v2 · Multi-Pass Analysis) — [taskType] | For personalised coaching, book a session with your IELTS Lab tutor.">
}

QUALITY STANDARDS — these apply to every field:
1. strengths: Must quote exact student text. Must explain WHY the quoted text is effective in BC terms. Never use phrases like "good structure" or "well done" without specifics.
2. modelParagraph.rewritten: Must be a genuine Band 8–9 demonstration — not cosmetic edits. Richer vocabulary, complex syntax, fully developed argument, precise cohesion. A student reading this should think "I see the gap now."
3. choicesExplained: Each entry must name the specific BC descriptor it targets. Generic explanations are not acceptable.
4. nextSteps: Ordered by impact — the highest-leverage improvement first. All three must target different criteria if possible. Tasks must be specific enough that a student can complete them without further instructions.
5. examinerNote: Must be honest. If the essay is a Band 5, say so and explain exactly why. Vague encouragement helps no one.`;


// ── P1-D: Cross-pass consistency ceilings ────────────────────────────────────
// Enforces band ceilings derived from the Pass 1 error list onto Pass 2 scores.
// Prevents AI inflation when hard error evidence contradicts the awarded band.
// Returns { scores, ceilingsApplied[] } — ceilingsApplied is logged and returned
// to the client so the UI can surface "Score adjusted from X to Y" if needed.
function applyConsistencyCeilings(pass1Errors, pass2Scores) {
  const scores      = JSON.parse(JSON.stringify(pass2Scores)); // deep clone
  const ceilingsApplied = [];

  const criterionMap = {
    grammaticalRange:  ['grammar',  'grammaticalRange'],
    lexicalResource:   ['lexical',  'lexicalResource'],
    coherenceCohesion: ['cohesion', 'coherenceCohesion'],
  };

  for (const [scoreKey, [errorType, criterionKey]] of Object.entries(criterionMap)) {
    const relevant = pass1Errors.filter(
      e => e.type === errorType || e.criterion === criterionKey
    );
    const criticalCount = relevant.filter(e => e.severity === 'critical').length;

    // Only recurring major errors count toward ceilings — isolated slips are
    // consistent with Band 7-8 per BC descriptors ("a few errors may persist",
    // "occasional, non-systematic errors"). Non-recurring majors are excluded.
    const recurringMajorCount = relevant.filter(
      e => e.severity === 'major' && e.isRecurring === true
    ).length;
    const heavyCount = criticalCount + recurringMajorCount;

    const criterion = scores[scoreKey];
    if (!criterion) continue;

    let ceiling = null;
    if (criticalCount >= 2)   ceiling = 5.5;  // 2 critical = systemic structural failure
    else if (heavyCount >= 5) ceiling = 6.0;  // 5 recurring major = pervasive pattern

    if (ceiling !== null && criterion.band > ceiling) {
      ceilingsApplied.push({
        criterion:      scoreKey,
        originalBand:   criterion.band,
        appliedCeiling: ceiling,
        reason: `Pass 1 found ${criticalCount} critical + ${recurringMajorCount} recurring major ${errorType} errors`,
      });
      criterion.band = ceiling;
    }
  }

  // Recalculate overall if any ceiling was applied
  if (ceilingsApplied.length > 0) {
    const bands = ['taskAchievement', 'coherenceCohesion', 'lexicalResource', 'grammaticalRange']
      .map(k => scores[k]?.band ?? 0);
    const avg = bands.reduce((a, b) => a + b, 0) / bands.length;
    scores.overall = Math.round(avg * 2) / 2; // round to nearest 0.5
    console.log(`[v2] Consistency ceilings applied:`, JSON.stringify(ceilingsApplied));
  }

  return { scores, ceilingsApplied };
}


// ── P2-B: Detect essay type from the question prompt ─────────────────────────
// Derives essayType from the question string before any AI call so Pass 1
// receives a constraint rather than having to guess from the student's response.
// Returns null if the prompt is absent or ambiguous — Pass 1 then falls back
// to its own detection.
function detectEssayTypeFromPrompt(taskLabel, question) {
  const label = (taskLabel || '').toLowerCase();

  // Task 1 types are determined entirely by taskLabel, not question content
  if (label.includes('task 1') || label.includes('task1')) {
    return label.includes('general') ? 'General Training Letter' : 'Academic Report';
  }

  if (!question) return null;

  // Task 2 — keyword matching against the question prompt
  if (/discuss\s+both\s+(views|sides|opinions?)|both\s+views|some\s+people.*others?\s+(believe|think|argue|feel)/i.test(question)) {
    // A "discuss both views" prompt that also asks about advantages/disadvantages
    // is still a Discussion essay — advantages prompts always say "advantages AND disadvantages"
    if (/advantage[s]?\s+and\s+disadvantage[s]?|disadvantage[s]?\s+and\s+advantage[s]?/i.test(question)) {
      return 'Advantages & Disadvantages';
    }
    return 'Discussion';
  }

  if (/advantage[s]?\s+and\s+disadvantage[s]?|disadvantage[s]?\s+and\s+advantage[s]?/i.test(question)) {
    return 'Advantages & Disadvantages';
  }

  if (/agree\s+or\s+disagree|to\s+what\s+extent\s+(do\s+you\s+)?agree|what\s+is\s+your\s+(view|opinion|position)|outweigh|do\s+you\s+think/i.test(question)) {
    return 'Opinion';
  }

  if (/(what\s+are\s+the?\s+)?(problem[s]?|cause[s]?|reason[s]?).*\n.*(solution[s]?|measure[s]?|step[s]?|tackle|solve|address)/is.test(question) ||
      /(problem[s]?\s+and\s+solution[s]?|cause[s]?\s+and\s+solution[s]?)/i.test(question)) {
    return 'Problem & Solution';
  }

  // Two-part question: two distinct "?" marks in the prompt
  const qMarks = (question.match(/\?/g) || []).length;
  if (qMarks >= 2) return 'Two-Part Question';

  return null; // ambiguous — let Pass 1 detect from the essay
}


// ── POST /api/correct-essay-v2 ────────────────────────────────────────────────
app.post('/api/correct-essay-v2', async (req, res) => {
  const { taskLabel, essay, question, image, imageType } = req.body;

  if (!essay || typeof essay !== 'string' || !essay.trim()) {
    return res.status(400).json({ error: 'Essay text is required.' });
  }

  const essayTrimmed  = essay.trim();
  const wordCount     = essayTrimmed.split(/\s+/).length;
  const isTask1       = (taskLabel || '').includes('1');
  const minWords      = isTask1 ? 150 : 250;
  const underMinimum  = wordCount < minWords;

  // P2-B: derive essay type from the prompt before any AI call
  const promptEssayType = detectEssayTypeFromPrompt(taskLabel, question);

  const taskInfo =
    `Task Type: ${taskLabel || 'Task 2 Essay'}\n` +
    (question ? `Question/Prompt: ${question}\n` : '') +
    `Word count: ${wordCount} words\n` +
    `Minimum required: ${minWords} words\n` +
    `Under minimum: ${underMinimum}\n` +
    (promptEssayType ? `Prompt-Derived Essay Type: ${promptEssayType}\n` : '');

  try {
    // ── PASS 1: Forensic Error Extraction ──────────────────────────────────
    console.log('[v2] Starting Pass 1 — Error Extraction');

    const buildPass1Content = (capErrors = false) => {
      const suffix = capErrors
        ? `\n\nIMPORTANT: Return at most 15 of the most impactful errors — prioritise critical and major ones. Keep each explanation under 1 sentence. Return ONLY valid JSON.`
        : `\n\nExtract all errors as specified. Return ONLY valid JSON.`;
      return image
        ? [
            { type: 'image', source: { type: 'base64', media_type: imageType || 'image/jpeg', data: image } },
            { type: 'text', text: `${taskInfo}\nStudent Essay:\n${essayTrimmed}${suffix}` },
          ]
        : `${taskInfo}\nStudent Essay:\n${essayTrimmed}${suffix}`;
    };

    let pass1;
    try {
      console.log('[Pass 1] max_tokens:', MAX_TOKENS_PASS1);
      const pass1Raw = await callAnthropic({
        system:      PASS1_SYSTEM,
        messages:    [{ role: 'user', content: buildPass1Content(false) }],
        maxTokens:   MAX_TOKENS_PASS1,
        temperature: 0.3,
      });
      pass1 = extractJSON(pass1Raw, 'Pass 1');
    } catch (e1) {
      console.warn('[v2] Pass 1 attempt 1 failed:', e1.message, '— retrying with capped errors');
      try {
        const pass1RawRetry = await callAnthropic({
          system:      PASS1_SYSTEM,
          messages:    [{ role: 'user', content: buildPass1Content(true) }],
          maxTokens:   MAX_TOKENS_PASS1,
          temperature: 0.3,
        });
        pass1 = extractJSON(pass1RawRetry, 'Pass 1 retry');
      } catch (e2) {
        console.warn('[v2] Pass 1 retry failed:', e2.message, '— proceeding with empty error list');
        pass1 = {
          wordCount: essayTrimmed.split(/\s+/).length,
          taskType:  taskLabel?.includes('1') ? (taskLabel.includes('General') ? 'Task 1 General Training' : 'Task 1 Academic') : 'Task 2',
          essayType: 'Opinion',
          errors:    [],
        };
      }
    }

    if (!Array.isArray(pass1.errors)) pass1.errors = [];
    console.log(`[v2] Pass 1 complete — ${pass1.errors.length} errors, essay type: ${pass1.essayType}`);


    // ── PASS 2: Evidence-Based Holistic Scoring ─────────────────────────────
    console.log('[v2] Starting Pass 2 — Evidenced Scoring');

    const pass2TextBody =
      `${taskInfo}Detected Essay Type: ${pass1.essayType || 'Unknown'}\n` +
      `Word Count: ${pass1.wordCount}\n\n` +
      (image ? `The chart/graph/diagram image for this Task 1 question is attached above. Use it to verify data accuracy in the student's essay when scoring taskAchievement.\n\n` : '') +
      `Student Essay:\n${essayTrimmed}\n\n` +
      (pass1.errors.length > 0
        ? `PRE-EXTRACTED ERROR LIST (from forensic Pass 1):\n${JSON.stringify(pass1.errors, null, 2)}\n\n`
        : '') +
      `Apply the 4 BC criteria holistically and verify the essay's structural format. Return ONLY valid JSON.`;

    // P2-A: send image to Pass 2 so taskAchievement can verify data accuracy
    const buildPass2Content = (extraInstruction = '') => {
      const text = pass2TextBody + extraInstruction;
      return image
        ? [
            { type: 'image', source: { type: 'base64', media_type: imageType || 'image/jpeg', data: image } },
            { type: 'text', text },
          ]
        : text;
    };

    let pass2;
    try {
      const pass2Raw = await callAnthropic({
        system:      PASS2_SYSTEM,
        messages:    [{ role: 'user', content: buildPass2Content() }],
        maxTokens:   MAX_TOKENS_PASS2,
        temperature: 0.3,
      });
      pass2 = extractJSON(pass2Raw, 'Pass 2');
    } catch (e2) {
      console.warn('[v2] Pass 2 failed:', e2.message, '— retrying');
      const pass2Raw = await callAnthropic({
        system:      PASS2_SYSTEM,
        messages:    [{ role: 'user', content: buildPass2Content('\n\nKeep each evidence array to 1 item maximum to save space.') }],
        maxTokens:   MAX_TOKENS_PASS2,
        temperature: 0.3,
      });
      pass2 = extractJSON(pass2Raw, 'Pass 2 retry');
    }

    if (!pass2.scores || typeof pass2.scores.overall === 'undefined') {
      return res.status(502).json({ error: 'Pass 2 did not return valid scores. Please try again.' });
    }

    // P1-D: apply server-side consistency ceilings before Pass 3 sees the scores
    const { scores: adjustedScores, ceilingsApplied } = applyConsistencyCeilings(
      pass1.errors,
      pass2.scores
    );
    pass2.scores = adjustedScores;

    console.log(`[v2] Pass 2 complete — Overall: ${pass2.scores.overall}`);


    // ── PASS 3: Synthesis ───────────────────────────────────────────────────
    console.log('[v2] Starting Pass 3 — Synthesis');

    const pass3UserText =
      `${taskInfo}Essay Type: ${pass1.essayType}\n\n` +
      `Student Essay:\n${essayTrimmed}\n\n` +
      (pass1.errors.length > 0
        ? `STRUCTURED ERROR LIST (Pass 1 — ${pass1.errors.length} errors):\n${JSON.stringify(pass1.errors, null, 2)}\n\n`
        : '') +
      `EVIDENCE-BASED SCORING (Pass 2):\n${JSON.stringify(pass2, null, 2)}\n\n` +
      `Generate the full synthesis report. Return ONLY valid JSON.`;

    let pass3;
    try {
      const pass3Raw = await callAnthropic({
        system:      PASS3_SYSTEM,
        messages:    [{ role: 'user', content: pass3UserText }],
        maxTokens:   MAX_TOKENS_PASS3,
        temperature: 0.3,
      });
      pass3 = extractJSON(pass3Raw, 'Pass 3');
    } catch (e3) {
      console.warn('[v2] Pass 3 failed:', e3.message, '— retrying with shorter choicesExplained');
      const pass3Raw = await callAnthropic({
        system:      PASS3_SYSTEM,
        messages:    [{ role: 'user', content: pass3UserText + '\n\nKeep choicesExplained to 2 items and nextSteps tasks under 50 words each.' }],
        maxTokens:   MAX_TOKENS_PASS3,
        temperature: 0.3,
      });
      pass3 = extractJSON(pass3Raw, 'Pass 3 retry');
    }
    console.log('[v2] Pass 3 complete — Synthesis done');


    // ── Merge and return ────────────────────────────────────────────────────
    const result = {
      // Meta
      wordCount:            pass1.wordCount ?? wordCount,
      taskType:             pass1.taskType,
      essayType:            pass1.essayType,
      underMinimum,
      minWords,
      wordCountStatus:      underMinimum
                              ? `FLAG: only ${pass1.wordCount ?? wordCount} words — minimum is ${minWords}`
                              : 'PASS — meets minimum',

      // Pass 1 — drives colour-coded annotation UI
      errors:               pass1.errors,
      totalErrorsDetected:  pass1.totalErrorsDetected ?? pass1.errors.length,

      // P1-D — ceiling audit trail (empty array if no ceilings were triggered)
      ceilingsApplied,

      // Pass 2 — holistic scores with evidence
      formatVerification: pass2.formatVerification,
      scores:             pass2.scores,

      // Pass 2 → scoreLabels shim (keeps v1 frontend keys working)
      scoreLabels: {
        taskAchievement:   pass2.scores.taskAchievement?.label   || '',
        coherenceCohesion: pass2.scores.coherenceCohesion?.label  || '',
        lexicalResource:   pass2.scores.lexicalResource?.label    || '',
        grammaticalRange:  pass2.scores.grammaticalRange?.label   || '',
      },

      // Pass 3 — narrative report
      strengths:          pass3.strengths,
      weakestCriterion:   pass3.weakestCriterion,
      examinerNote:       pass3.examinerNote,
      modelParagraph:     pass3.modelParagraph,
      nextSteps:          pass3.nextSteps,
      resubmitChallenge:  pass3.resubmitChallenge,
      signature:          pass3.signature,
    };

    res.json(result);

  } catch (err) {
    console.error('[correct-essay-v2]', err.message);
    res.status(502).json({ error: err.message });
  }
});


// ════════════════════════════════════════════════════════════════════════════
//  IELTS EXPERT CHAT AGENT
// ════════════════════════════════════════════════════════════════════════════

const EXPERT_SYSTEM = `You are a Senior IELTS Expert Advisor working exclusively for IELTS Lab — a premium IELTS preparation platform.

YOUR IDENTITY:
- 15+ years experience as a certified IELTS trainer
- Deep knowledge of Academic and General Training formats
- Expert in all 4 skills: Reading, Writing, Listening, Speaking
- You know every IDP and British Council guideline by heart

YOUR STRICT RULES:
1. You ONLY answer questions related to IELTS preparation, exam strategy, band scores, skills improvement, and English language learning for IELTS purposes.
2. If a student asks ANYTHING not related to IELTS or English learning respond ONLY with:
   "I'm your dedicated IELTS Expert at The Writing Clinic. I can only help you with IELTS preparation, exam strategy, and English skills. What would you like to improve today?"
3. Never break character. Never discuss other topics.
4. Always address the student warmly and directly.
5. Always end every response with one actionable next step.

WHAT YOU CAN HELP WITH:
- IELTS band score requirements and how to achieve them
- Reading strategies (skimming, scanning, question types)
- Listening strategies (note-taking, traps, accents)
- Speaking tips (fluency, pronunciation, Part 1/2/3 strategy)
- Writing Task 1 and Task 2 structure and approach
- Grammar and vocabulary specifically for IELTS
- Exam day tips, timing strategies, registration advice
- Academic vs General Training comparison
- Latest exam format updates from IDP and British Council

TONE: Warm, encouraging, expert. Like the best teacher the student has ever had.`;

app.post('/api/ielts-expert', async (req, res) => {
  const { messages, essayContext } = req.body;

  if (!Array.isArray(messages) || messages.length === 0) {
    return res.status(400).json({ error: 'messages array is required.' });
  }

  const sanitised = messages
    .filter(m => m && typeof m.content === 'string' && m.content.trim())
    .map(m => ({
      role:    m.role === 'assistant' ? 'assistant' : 'user',
      content: m.content.trim(),
    }));

  if (sanitised.length === 0) {
    return res.status(400).json({ error: 'No valid messages provided.' });
  }

  const lastContent = sanitised[sanitised.length - 1]?.content?.toLowerCase() || '';
  const offTopicPatterns = [/\bpolitic/,/\bcode\b/,/\bprogram/,/\bhack/,/\bjavascript/,/\bpython/,/\bcrypto/];
  if (offTopicPatterns.some(p => p.test(lastContent))) {
    console.warn('[ielts-expert] off-topic attempt:', lastContent.slice(0, 80));
  }

  // Inject essay context from the student's most recent correction (if provided)
  const systemPrompt = (essayContext && typeof essayContext === 'string')
    ? `${EXPERT_SYSTEM}\n\n${essayContext}`
    : EXPERT_SYSTEM;

  try {
    const reply = await callAnthropic({
      system:    systemPrompt,
      messages:  sanitised,
      maxTokens: 1200,
    });
    res.json({ reply });
  } catch (err) {
    console.error('[ielts-expert]', err.message);
    res.status(502).json({ error: err.message });
  }
});


// ════════════════════════════════════════════════════════════════════════════
//  MOCK TESTS — QUESTION GENERATION & GRADING
// ════════════════════════════════════════════════════════════════════════════

const MOCK_QUESTION_SYSTEM = `You are an expert IELTS test designer. Generate a brand-new, unique IELTS question for the specified skill and training type. Return ONLY valid JSON matching the schema below — no text before or after.`;

function buildQuestionPrompt(skill, trainingType, _mode) {
  const type = trainingType === 'academic' ? 'Academic' : 'General Training';
  if (skill === 'writing') {
    return `Generate a complete IELTS Writing test (${type}).
Return JSON:
{
  "task1": {
    "prompt": "<full Task 1 question text — Academic: describe a graph/chart/process diagram/map; General Training: write a letter in a realistic scenario>",
    "tip": "<one practical tip for this specific task>"
  },
  "task2": {
    "prompt": "<full Task 2 essay question — a complete IELTS-style question with clear task requirements>",
    "tip": "<one practical tip>"
  }
}
Make the questions realistic, contemporary, and varied. Do not reuse common example topics.`;
  }
  if (skill === 'reading') {
    return `Generate a complete IELTS Reading test (${type}).
Return JSON:
{
  "title": "<passage title>",
  "passage": "<full reading passage, 600–750 words, academic or general training style, on a contemporary non-fiction topic>",
  "questions": [
    {"type": "multiple_choice", "question": "<question text>", "options": ["A. ...", "B. ...", "C. ...", "D. ..."], "answer": "A. ..."},
    {"type": "true_false_ng", "question": "<True/False/Not Given statement>", "answer": "True"},
    {"type": "short_answer", "question": "<short answer question>", "answer": "<expected answer>"}
  ]
}
Include 8–10 questions, a mix of multiple choice, True/False/Not Given, and short answer. Vary the types.`;
  }
  if (skill === 'listening') {
    return `Generate a complete IELTS Listening test simulation.
Return JSON:
{
  "scenario": "<2–3 sentence description of the listening scenario: who is speaking, context, setting>",
  "transcript": "<full realistic dialogue or monologue transcript, 400–500 words, written exactly as spoken — include speaker labels like 'Agent:', 'Customer:', etc. or just present the monologue directly>",
  "questions": [
    {"type": "gap_fill", "question": "<sentence with a blank, e.g. 'The booking is for ___ people'>", "answer": "<expected answer>"},
    {"type": "multiple_choice", "question": "<question text>", "options": ["A. ...", "B. ...", "C. ...", "D. ..."], "answer": "A. ..."}
  ]
}
Include 8 questions, a mix of gap fill and multiple choice. All answers must be findable in the transcript.`;
  }
  if (skill === 'speaking') {
    return `Generate a complete IELTS Speaking test (${type}).
Return JSON:
{
  "part1": {
    "topic": "<general topic e.g. hometown, hobbies, food>",
    "questions": [
      "<Question 1>",
      "<Question 2>",
      "<Question 3>",
      "<Question 4>"
    ]
  },
  "part2": {
    "topic": "<what the candidate should talk about>",
    "points": [
      "<You should say: point 1>",
      "<point 2>",
      "<point 3>",
      "<And explain: point 4>"
    ]
  },
  "part3": {
    "topic": "<abstract theme linked to Part 2>",
    "questions": [
      "<Discussion question 1 — requires extended abstract response>",
      "<Discussion question 2>",
      "<Discussion question 3>"
    ]
  }
}`;
  }
  return `Generate an IELTS ${skill} question for ${type} training. Return JSON.`;
}

app.post('/api/mock/generate-question', async (req, res) => {
  const { skill, trainingType, mode } = req.body;
  if (!skill || !trainingType) {
    return res.status(400).json({ error: 'skill and trainingType are required.' });
  }
  try {
    const prompt = buildQuestionPrompt(skill, trainingType, mode);
    const rawText = await callAnthropic({
      system: MOCK_QUESTION_SYSTEM,
      messages: [{ role: 'user', content: prompt }],
      maxTokens: 4000,
    });
    const question = extractJSON(rawText, `mock-question-${skill}`);
    res.json(question);
  } catch (err) {
    console.error('[mock/generate-question]', err.message);
    res.status(502).json({ error: err.message });
  }
});


const MOCK_GRADING_SYSTEM = `You are a certified IELTS examiner. Grade the student's response according to official IELTS band descriptors.

OUTPUT RULE: Your entire response must be a single valid JSON object. No text before or after it. Start with { and end with }.

Return this JSON schema (omit fields that don't apply to the skill being graded):
{
  "overall_band": <number 1–9 in 0.5 steps — overall band score for this skill>,
  "skill_scores": {
    "listening": <number or null>,
    "reading": <number or null>,
    "writing": <number or null>,
    "speaking": <number or null>
  },
  "writing_feedback": {
    "task_achievement": <number 1–9 in 0.5 steps or null>,
    "coherence": <number 1–9 in 0.5 steps or null>,
    "lexical_resource": <number 1–9 in 0.5 steps or null>,
    "grammar": <number 1–9 in 0.5 steps or null>
  },
  "speaking_feedback": {
    "fluency": <number 1–9 in 0.5 steps or null>,
    "vocabulary": <number 1–9 in 0.5 steps or null>,
    "grammar": <number 1–9 in 0.5 steps or null>,
    "pronunciation": <number 1–9 in 0.5 steps or null>
  },
  "strengths": ["<specific strength with example from student's response>", "..."],
  "improvements": ["<specific area to improve with actionable advice>", "..."],
  "examiner_note": "<one paragraph: the single biggest barrier between this student and the next band>",
  "score_breakdown": "<brief explanation of how the overall_band was calculated>"
}

For Listening and Reading: count correct answers and convert to band score using standard IELTS conversion tables (approximately: 40 correct = 9.0, 35 = 8.0, 30 = 7.0, 23 = 6.0, 16 = 5.0, 10 = 4.0). Set only the relevant skill score and set others to null.

Be honest, specific, and encouraging. Use IELTS band descriptor language.`;

app.post('/api/mock/grade', async (req, res) => {
  const { skill, trainingType, question, answers } = req.body;
  if (!skill || !answers) {
    return res.status(400).json({ error: 'skill and answers are required.' });
  }

  const type = trainingType === 'academic' ? 'Academic' : 'General Training';
  let userContent = `Skill: ${skill.toUpperCase()}\nTraining Type: ${type}\n\n`;

  if (skill === 'writing') {
    userContent += `Task 1 Question:\n${question?.task1?.prompt || 'N/A'}\n\nTask 1 Answer:\n${answers.task1 || '(blank)'}\n\nTask 2 Question:\n${question?.task2?.prompt || 'N/A'}\n\nTask 2 Answer:\n${answers.task2 || '(blank)'}\n\nGrade both tasks. The overall_band should be weighted: Task 1 = 1/3, Task 2 = 2/3 of the writing score.`;
  } else if (skill === 'reading') {
    const correctAnswers = question?.questions?.map(q => q.answer) || [];
    const studentAnswers = Object.values(answers);
    let correct = 0;
    correctAnswers.forEach((ans, i) => {
      if (ans && studentAnswers[i] && studentAnswers[i].toLowerCase().trim() === ans.toLowerCase().trim()) correct++;
    });
    userContent += `Total questions: ${correctAnswers.length}\nStudent correct answers: ${correct}\n\nQuestion-by-question:\n`;
    (question?.questions || []).forEach((q, i) => {
      userContent += `Q${i+1}: "${q.question}" — Expected: "${q.answer}" — Student: "${studentAnswers[i] || '(blank)'}"\n`;
    });
    userContent += `\nConvert ${correct}/${correctAnswers.length} correct to a band score.`;
  } else if (skill === 'listening') {
    const correctAnswers = question?.questions?.map(q => q.answer) || [];
    const studentAnswers = Object.values(answers);
    let correct = 0;
    correctAnswers.forEach((ans, i) => {
      if (ans && studentAnswers[i] && studentAnswers[i].toLowerCase().trim() === ans.toLowerCase().trim()) correct++;
    });
    userContent += `Total questions: ${correctAnswers.length}\nStudent correct answers: ${correct}\n\nQuestion-by-question:\n`;
    (question?.questions || []).forEach((q, i) => {
      userContent += `Q${i+1}: "${q.question}" — Expected: "${q.answer}" — Student: "${studentAnswers[i] || '(blank)'}"\n`;
    });
  } else if (skill === 'speaking') {
    userContent += `Part 1 Questions:\n${(question?.part1?.questions || []).join('\n')}\n\nPart 1 Response:\n${answers.part1 || '(blank)'}\n\n`;
    userContent += `Part 2 Topic: ${question?.part2?.topic || 'N/A'}\n\nPart 2 Response:\n${answers.part2 || '(blank)'}\n\n`;
    userContent += `Part 3 Questions:\n${(question?.part3?.questions || []).join('\n')}\n\nPart 3 Response:\n${answers.part3 || '(blank)'}`;
  }

  try {
    const rawText = await callAnthropic({
      system: MOCK_GRADING_SYSTEM,
      messages: [{ role: 'user', content: userContent }],
      maxTokens: 2500,
    });
    const result = extractJSON(rawText, `mock-grade-${skill}`);
    res.json(result);
  } catch (err) {
    console.error('[mock/grade]', err.message);
    res.status(502).json({ error: err.message });
  }
});


// ════════════════════════════════════════════════════════════════════════════
//  EMAIL REPORT — POST /api/send-report
//  Uses Resend (resend.com). Requires RESEND_API_KEY in .env.
//  Optional: RESEND_FROM_EMAIL (defaults to onboarding@resend.dev for testing)
// ════════════════════════════════════════════════════════════════════════════

function buildEmailHtml(r) {
  const cLabels = {
    taskAchievement:   'Task Achievement',
    coherenceCohesion: 'Coherence & Cohesion',
    lexicalResource:   'Lexical Resource',
    grammaticalRange:  'Grammar & Accuracy',
  };
  const getBand = k => {
    const v = r.scores?.[k];
    return (v && typeof v === 'object') ? v.band : (v ?? '—');
  };
  const criteriaHtml = Object.entries(cLabels).map(([k, label]) => `
    <td style="width:25%;text-align:center;padding:14px 8px;border-right:1px solid #e5e0d8;">
      <div style="font-size:10px;font-weight:700;text-transform:uppercase;letter-spacing:0.12em;color:#6b7280;margin-bottom:4px;">${label}</div>
      <div style="font-size:24px;font-weight:700;color:#0f1e3c;font-family:Georgia,serif;">${getBand(k)}</div>
    </td>`).join('');

  const nextStepsHtml = Array.isArray(r.nextSteps)
    ? r.nextSteps.map(s => `<li style="margin-bottom:10px;line-height:1.7;">${s.task || s}</li>`).join('')
    : `<li style="line-height:1.7;">${r.nextSteps || ''}</li>`;

  return `<!DOCTYPE html><html><head><meta charset="UTF-8"></head>
  <body style="margin:0;padding:0;background:#faf7f2;font-family:'Helvetica Neue',Arial,sans-serif;color:#1a1a2e;">
    <table width="100%" cellpadding="0" cellspacing="0" style="background:#faf7f2;padding:40px 16px;">
      <tr><td align="center">
        <table width="600" cellpadding="0" cellspacing="0" style="max-width:600px;width:100%;background:#ffffff;border-radius:16px;overflow:hidden;box-shadow:0 4px 24px rgba(0,0,0,0.08);">

          <tr><td style="background:#0f1e3c;padding:28px 36px;">
            <div style="font-size:20px;font-weight:700;color:#fff;letter-spacing:1px;">IELTS <span style="color:#c9a84c;">Lab</span></div>
            <div style="font-size:12px;color:rgba(255,255,255,0.55);margin-top:4px;letter-spacing:0.06em;">AI Writing Corrector Report</div>
          </td></tr>

          <tr><td style="padding:32px 36px;text-align:center;border-bottom:1px solid #e5e0d8;">
            <div style="font-size:11px;font-weight:700;text-transform:uppercase;letter-spacing:0.15em;color:#6b7280;margin-bottom:6px;">Overall Band Score</div>
            <div style="font-size:72px;font-weight:700;color:#0f1e3c;line-height:1;font-family:Georgia,serif;">${r.scores?.overall || '—'}</div>
            <div style="font-size:13px;color:#6b7280;margin-top:8px;">${r.taskType || ''}${r.essayType ? ' · ' + r.essayType : ''}</div>
          </td></tr>

          <tr><td style="border-bottom:1px solid #e5e0d8;">
            <table width="100%" cellpadding="0" cellspacing="0"><tr>${criteriaHtml}</tr></table>
          </td></tr>

          ${r.examinerNote ? `<tr><td style="padding:24px 36px;border-bottom:1px solid #e5e0d8;">
            <div style="font-size:10px;font-weight:700;text-transform:uppercase;letter-spacing:0.14em;color:#6b7280;margin-bottom:10px;">Examiner Note</div>
            <div style="font-size:14px;line-height:1.8;background:#f0f4ff;border-left:3px solid #0f1e3c;border-radius:0 8px 8px 0;padding:14px 18px;">${r.examinerNote}</div>
          </td></tr>` : ''}

          ${r.nextSteps ? `<tr><td style="padding:24px 36px;border-bottom:1px solid #e5e0d8;">
            <div style="font-size:10px;font-weight:700;text-transform:uppercase;letter-spacing:0.14em;color:#6b7280;margin-bottom:10px;">Your Next Steps</div>
            <ol style="font-size:14px;line-height:1.8;margin:0;padding-left:20px;">${nextStepsHtml}</ol>
          </td></tr>` : ''}

          <tr><td style="padding:28px 36px;text-align:center;background:#faf7f2;">
            <a href="http://localhost:3000/writing-clinic/corrector.html"
               style="display:inline-block;background:#0f1e3c;color:#ffffff;text-decoration:none;padding:13px 30px;border-radius:12px;font-size:12px;font-weight:700;letter-spacing:0.08em;text-transform:uppercase;">
              Submit Another Essay →
            </a>
            <div style="font-size:11px;color:#9ca3af;margin-top:18px;">IELTS Lab · AI Writing Corrector</div>
          </td></tr>

        </table>
      </td></tr>
    </table>
  </body></html>`;
}

app.post('/api/send-report', async (req, res) => {
  const { email, reportData } = req.body;
  if (!email || !reportData) {
    return res.status(400).json({ error: 'email and reportData are required.' });
  }

  const apiKey = process.env.RESEND_API_KEY;
  if (!apiKey) {
    return res.status(503).json({
      error: 'Email service not configured. Add RESEND_API_KEY=re_xxxx to your .env file (get a free key at resend.com).',
    });
  }

  const from    = process.env.RESEND_FROM_EMAIL || 'IELTS Lab <onboarding@resend.dev>';
  const subject = `Your IELTS Writing Report — Band ${reportData.scores?.overall || '—'}`;
  const html    = buildEmailHtml(reportData);

  try {
    const r = await fetch('https://api.resend.com/emails', {
      method:  'POST',
      headers: { 'Authorization': `Bearer ${apiKey}`, 'Content-Type': 'application/json' },
      body:    JSON.stringify({ from, to: [email], subject, html }),
    });
    const body = await r.json().catch(() => ({}));
    if (!r.ok) {
      return res.status(502).json({ error: body.message || `Resend API error ${r.status}` });
    }
    console.log(`[send-report] Sent to ${email} — Resend ID: ${body.id}`);
    res.json({ success: true, id: body.id });
  } catch (err) {
    console.error('[send-report]', err.message);
    res.status(502).json({ error: err.message });
  }
});


// ════════════════════════════════════════════════════════════════════════════
//  VOCABULARY BUILDER — LEXICAL UPGRADE ENGINE
// ════════════════════════════════════════════════════════════════════════════

const VOCAB_UPGRADE_SYSTEM = `You are a senior IELTS examiner and lexical resource specialist with 20+ years of experience assessing IELTS Writing. Your sole job is to audit a student's text for Lexical Resource quality and return a structured JSON upgrade report.

WHAT YOU ARE LOOKING FOR:
- Overused / generic verbs: show, get, make, do, give, have, say, go, use, need, think
- Vague / basic adjectives: big, small, good, bad, important, interesting, many, lots of
- Weak nouns: thing, stuff, people, situation, problem, area, way
- Incorrect collocations: "do a mistake", "make a research", "strong opinion"
- Repetition of the same word within the same paragraph
- Informal register for an academic essay

FOR EACH WEAK ITEM:
- Quote the exact word or short phrase from the text
- Explain in one sentence why it lowers the band score
- Provide ONE best Band 7–8 replacement that fits the context
- Provide the natural collocation or phrase it belongs in
- Show a short improved example sentence using the replacement
- Rate it: 7 or 8 (8 = sophisticated, low-frequency academic word; 7 = clear upgrade, appropriate for IELTS)

ALSO:
- List any strong vocabulary the student already used correctly (positive reinforcement)
- Give a one-sentence overall Lexical Resource assessment
- Estimate the current LR band based purely on vocabulary quality (0.5 steps, 5.0–8.5)

IMPORTANT CALIBRATION:
- Only flag genuinely weak choices — do not over-flag. A Band 7 essay should have 4–8 flags.
- Do not flag subject-specific technical terms (globalisation, sustainability, infrastructure).
- Do not flag words that are appropriate and not easily improved.
- Prioritise verbs and collocations — these have the most examiner impact.

Return ONLY valid JSON in this exact schema:
{
  "lrEstimate": 6.0,
  "overallNote": "string — one sentence, direct, examiner tone",
  "upgrades": [
    {
      "original": "shows",
      "issue": "Generic verb that signals limited vocabulary range",
      "replacement": "demonstrates",
      "definition": "to prove or show something clearly and without doubt",
      "collocation": "demonstrates that / demonstrates the need for",
      "example": "This clearly demonstrates that governments must take immediate action.",
      "band": 7
    }
  ],
  "strongWords": ["furthermore", "significant", "deteriorate"]
}`;

app.post('/api/vocab/upgrade', async (req, res) => {
  const { text } = req.body;
  if (!text || typeof text !== 'string' || text.trim().length < 20) {
    return res.status(400).json({ error: 'Please provide at least one full sentence to analyse.' });
  }
  if (text.trim().length > 3000) {
    return res.status(400).json({ error: 'Text is too long. Please submit up to 3000 characters at a time.' });
  }

  const userMessage = `Please analyse the following student text for Lexical Resource quality and return the upgrade JSON:\n\n"${text.trim()}"`;

  try {
    let raw = await callAnthropic({
      system:      VOCAB_UPGRADE_SYSTEM,
      messages:    [{ role: 'user', content: userMessage }],
      maxTokens:   2000,
      temperature: 0.2,
    });

    let result = extractJSON(raw, 'vocab-upgrade');

    if (!result || !Array.isArray(result.upgrades)) {
      raw = await callAnthropic({
        system:      VOCAB_UPGRADE_SYSTEM,
        messages:    [{ role: 'user', content: userMessage }],
        maxTokens:   2000,
        temperature: 0.2,
      });
      result = extractJSON(raw, 'vocab-upgrade-retry');
    }

    if (!result || !Array.isArray(result.upgrades)) {
      return res.status(502).json({ error: 'Could not parse vocabulary analysis. Please try again.' });
    }

    console.log(`[vocab-upgrade] ${result.upgrades.length} upgrades found, LR estimate: ${result.lrEstimate}`);
    res.json(result);
  } catch (err) {
    console.error('[vocab-upgrade]', err.message);
    res.status(502).json({ error: err.message });
  }
});

const VOCAB_PRACTICE_SYSTEM = `You are an IELTS Writing examiner specialising in collocation and lexical accuracy. A student is practising a specific vocabulary word in a sentence. Your job is to check whether they have used it correctly — right collocation, right grammar, right register for academic writing.

Be encouraging but precise. If the collocation is correct, confirm it warmly. If wrong, explain the exact issue in one sentence and rewrite it correctly.

Return ONLY valid JSON:
{
  "correct": true,
  "feedback": "One specific sentence of feedback in an encouraging examiner tone.",
  "improvedSentence": "Your corrected version if needed — null if the sentence is already correct."
}`;

app.post('/api/vocab/practice-check', async (req, res) => {
  const { word, collocation, userSentence } = req.body;
  if (!word || !userSentence || userSentence.trim().length < 5) {
    return res.status(400).json({ error: 'word and userSentence are required.' });
  }

  const prompt = `Word being practised: "${word}"
Target collocation pattern: "${collocation || 'general academic use'}"
Student's sentence: "${userSentence.trim()}"

Check the student's use of this word and return your JSON assessment.`;

  try {
    const raw = await callAnthropic({
      system:      VOCAB_PRACTICE_SYSTEM,
      messages:    [{ role: 'user', content: prompt }],
      maxTokens:   400,
      temperature: 0.2,
    });
    const result = extractJSON(raw, 'vocab-practice');
    if (!result || typeof result.correct === 'undefined') {
      return res.status(502).json({ error: 'Could not parse feedback. Please try again.' });
    }
    res.json(result);
  } catch (err) {
    console.error('[vocab-practice]', err.message);
    res.status(502).json({ error: err.message });
  }
});


// ── Start ─────────────────────────────────────────────────────────────────────
app.listen(PORT, () => {
  const keyOk = !!process.env.ANTHROPIC_API_KEY;
  console.log(`\n✅  IELTS Lab server running`);
  console.log(`\n    Main site:      http://localhost:${PORT}/IELTS-Lab.html`);
  console.log(`    Writing Clinic: http://localhost:${PORT}/writing-clinic/index.html`);
  console.log(`    Health check:   http://localhost:${PORT}/api/health\n`);
  if (!keyOk) {
    console.warn(`⚠️   ANTHROPIC_API_KEY is not set!`);
    console.warn(`    Create a .env file with: ANTHROPIC_API_KEY=sk-ant-...\n`);
  } else {
    console.log(`✅  ANTHROPIC_API_KEY loaded\n`);
  }
});
