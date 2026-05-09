# IELTS Lab

AI-powered IELTS preparation platform with essay correction, mock tests, and chat coaching — built with HTML/JS and Claude API.

## Features

- **Essay Corrector** — AI grades Task 1 & Task 2 essays with band scores for all 4 criteria (Task Achievement, Coherence & Cohesion, Lexical Resource, Grammatical Range & Accuracy)
- **Mock Tests** — Full practice exams for Listening, Reading, Writing, and Speaking
- **AI Chat Coach** — IELTS expert chat powered by Claude for personalized writing guidance
- **Vocabulary Builder** — Curated vocabulary practice for IELTS-level language

## Stack

| Layer | Technology |
|-------|-----------|
| Frontend | HTML5, Tailwind CSS (CDN), Vanilla JavaScript |
| Backend | Node.js + Express (ESM) |
| AI | Anthropic Claude API (`claude-sonnet-4-6`) |
| Auth | localStorage-based session (`ielts_session`) |

## Project Structure

```
/IELTS-Lab.html          ← Public landing page
/server.js               ← Express backend + Claude API routes
/js/components.js        ← Shared nav, auth, and theme component
/writing-clinic/
  corrector.html         ← Essay corrector (3-pass AI pipeline)
  chat.html              ← IELTS expert chat
  vocabulary.html        ← Vocabulary practice
/mock-tests/
  index.html             ← Mock test dashboard
  listening.html
  reading.html
  writing.html
  speaking.html
  results.html
/about/
/privacy/
/terms/
```

## API Endpoints

| Method | Route | Purpose |
|--------|-------|---------|
| GET | `/api/health` | Server + API key status |
| POST | `/api/correct-essay` | Single-pass essay correction |
| POST | `/api/correct-essay-v2` | Three-pass multi-agent pipeline |
| POST | `/api/ielts-expert` | IELTS chat coach |
| POST | `/api/mock/generate-question` | Generate mock test question |
| POST | `/api/mock/grade` | Grade mock test answer |

## Setup

**1. Install dependencies:**
```bash
npm install
```

**2. Configure environment:**
```bash
cp .env.example .env
```
Then add your `ANTHROPIC_API_KEY` inside `.env`.

**3. Run the server:**
```bash
# Production
npm start

# Development (auto-restart on file change)
npm run dev
```

The server runs on `http://localhost:3000` by default.

## Environment Variables

| Variable | Required | Description |
|----------|----------|-------------|
| `ANTHROPIC_API_KEY` | Yes | Get from [console.anthropic.com](https://console.anthropic.com/) |
| `PORT` | No | Server port (default: 3000) |

## Notes

- Frontend uses localStorage for auth — no database required
- All AI calls go through the backend (`server.js`) — the API key is never exposed to the browser
- IELTS band scores follow official May 2023 British Council descriptors (1–9 in 0.5 steps)
