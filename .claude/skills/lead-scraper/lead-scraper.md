---
name: Lead Scraper
description: Scrape business domains from a source list and harvest verified emails via Hunter.io enrichment API. Appends results into a timestamped CSV in /exports/.
trigger: When the user asks to scrape leads, find emails for a list of domains, or enrich a company list with contact info.
script: scripts/scrape_and_upload.py
---

# Lead Scraper Skill

Orchestrates domain-to-email enrichment using the Hunter.io Domain Search API. Reads a domain list, looks up verified emails per domain, deduplicates, and writes clean rows to `/exports/`.

## Process Checklist

- [ ] **1. Validate inputs** — confirm `HUNTER_API_KEY` is set in `.env` and the source domain list file exists
- [ ] **2. Load domains** — read domain list from CSV or plain text file (one domain per line or a `domain` column)
- [ ] **3. Hunter.io lookup loop** — for each domain, call `GET https://api.hunter.io/v2/domain-search?domain={domain}&api_key={key}`
- [ ] **4. Parse results** — extract `first_name`, `last_name`, `value` (email), `position`, `confidence`, `linkedin`, `twitter` from each hit
- [ ] **5. Deduplicate** — skip exact email addresses already seen in this run
- [ ] **6. Rate limiting** — respect Hunter.io free tier (1 req/s); sleep 1.1s between requests
- [ ] **7. Append to CSV** — write enriched rows to `/exports/leads_YYYY-MM-DD.csv` (append mode, write header only if file is new)
- [ ] **8. Summary report** — print total domains processed, emails found, API errors, and output file path

## Environment Variables Required

| Variable | Description |
|----------|-------------|
| `HUNTER_API_KEY` | Hunter.io API key (get from hunter.io/api-keys) |

## Input Formats Accepted

- Plain text file: one domain per line (`example.com`)
- CSV file with a `domain` column header

## Output

`/exports/leads_YYYY-MM-DD.csv` with columns:
`domain, first_name, last_name, email, position, confidence, linkedin, twitter, scraped_at`

## Usage

```bash
python3 .claude/skills/lead-scraper/scripts/scrape_and_upload.py --input domains.txt
python3 .claude/skills/lead-scraper/scripts/scrape_and_upload.py --input leads.csv --column domain
```

## Known Constraints

- Hunter.io free tier: 25 searches/month. Paid plans unlock higher limits.
- Confidence < 50 means the email is a pattern guess, not verified — filter with `--min-confidence 70` if needed.
- Some domains return 0 results (no indexed emails); these are logged but still written as a row with empty email fields so you can track coverage.
