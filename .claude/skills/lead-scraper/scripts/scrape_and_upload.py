#!/usr/bin/env python3
"""
Lead Scraper — Hunter.io domain email enrichment
Usage:
  python3 scrape_and_upload.py --input domains.txt
  python3 scrape_and_upload.py --input leads.csv --column domain --min-confidence 70
"""

import argparse
import csv
import os
import sys
import time
from datetime import datetime
from pathlib import Path

import requests
from dotenv import load_dotenv

# ── Config ────────────────────────────────────────────────────────────────────

load_dotenv()

HUNTER_API_KEY = os.getenv("HUNTER_API_KEY", "")
HUNTER_URL     = "https://api.hunter.io/v2/domain-search"
REQUEST_DELAY  = 1.1  # seconds between requests (stay within free-tier rate limit)

EXPORTS_DIR = Path(__file__).resolve().parents[3] / "exports"
EXPORTS_DIR.mkdir(parents=True, exist_ok=True)

OUTPUT_COLUMNS = [
    "domain", "first_name", "last_name", "email",
    "position", "confidence", "linkedin", "twitter", "scraped_at",
]

# ── Helpers ───────────────────────────────────────────────────────────────────

def load_domains(input_path: str, column: str) -> list[str]:
    """Return a deduplicated list of domains from a .txt or .csv file."""
    path = Path(input_path)
    if not path.exists():
        sys.exit(f"[ERROR] Input file not found: {input_path}")

    domains = []
    if path.suffix.lower() == ".csv":
        with open(path, newline="", encoding="utf-8") as f:
            reader = csv.DictReader(f)
            if column not in (reader.fieldnames or []):
                sys.exit(f"[ERROR] Column '{column}' not found in CSV. Available: {reader.fieldnames}")
            for row in reader:
                domain = row[column].strip().lower()
                if domain:
                    domains.append(domain)
    else:
        with open(path, encoding="utf-8") as f:
            for line in f:
                domain = line.strip().lower()
                if domain and not domain.startswith("#"):
                    domains.append(domain)

    # Deduplicate while preserving order
    seen = set()
    unique = []
    for d in domains:
        if d not in seen:
            seen.add(d)
            unique.append(d)
    return unique


def hunter_lookup(domain: str, api_key: str, min_confidence: int) -> list[dict]:
    """
    Call Hunter.io domain-search for one domain.
    Returns a list of email rows (may be empty if no results or API error).
    """
    try:
        resp = requests.get(
            HUNTER_URL,
            params={"domain": domain, "api_key": api_key},
            timeout=15,
        )
        if resp.status_code == 429:
            print(f"  [WARN] Rate limited on {domain} — sleeping 30s")
            time.sleep(30)
            return []
        if resp.status_code != 200:
            print(f"  [WARN] Hunter API error {resp.status_code} for {domain}: {resp.text[:120]}")
            return []

        data     = resp.json().get("data", {})
        emails   = data.get("emails", [])
        rows     = []
        ts       = datetime.utcnow().strftime("%Y-%m-%dT%H:%M:%SZ")

        for hit in emails:
            confidence = hit.get("confidence", 0)
            if confidence < min_confidence:
                continue
            rows.append({
                "domain":      domain,
                "first_name":  hit.get("first_name", ""),
                "last_name":   hit.get("last_name", ""),
                "email":       hit.get("value", ""),
                "position":    hit.get("position", ""),
                "confidence":  confidence,
                "linkedin":    hit.get("linkedin", ""),
                "twitter":     hit.get("twitter", ""),
                "scraped_at":  ts,
            })

        # If domain was found but produced 0 qualifying emails, write a blank-email row
        # so coverage tracking shows the domain was attempted.
        if not rows:
            rows.append({
                "domain":     domain,
                "first_name": "", "last_name": "", "email": "",
                "position":   "", "confidence": 0,
                "linkedin":   "", "twitter":    "",
                "scraped_at": datetime.utcnow().strftime("%Y-%m-%dT%H:%M:%SZ"),
            })

        return rows

    except requests.RequestException as exc:
        print(f"  [ERROR] Network error for {domain}: {exc}")
        return []


def append_rows(output_path: Path, rows: list[dict]) -> None:
    """Append rows to the CSV, writing header only if the file is new."""
    is_new = not output_path.exists()
    with open(output_path, "a", newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(f, fieldnames=OUTPUT_COLUMNS)
        if is_new:
            writer.writeheader()
        writer.writerows(rows)

# ── Main ──────────────────────────────────────────────────────────────────────

def main() -> None:
    parser = argparse.ArgumentParser(description="Scrape emails from domains via Hunter.io")
    parser.add_argument("--input",          required=True,  help="Path to domain list (.txt or .csv)")
    parser.add_argument("--column",         default="domain", help="CSV column name containing domains (default: domain)")
    parser.add_argument("--min-confidence", type=int, default=0, help="Minimum Hunter.io confidence score to include (0–100)")
    parser.add_argument("--output",         default=None,   help="Output CSV path (default: exports/leads_YYYY-MM-DD.csv)")
    args = parser.parse_args()

    if not HUNTER_API_KEY:
        sys.exit("[ERROR] HUNTER_API_KEY is not set. Add it to your .env file.")

    domains = load_domains(args.input, args.column)
    if not domains:
        sys.exit("[ERROR] No domains found in input file.")

    output_path = Path(args.output) if args.output else EXPORTS_DIR / f"leads_{datetime.utcnow().strftime('%Y-%m-%d')}.csv"

    print(f"\n[Lead Scraper] Starting enrichment")
    print(f"  Domains     : {len(domains)}")
    print(f"  Min conf.   : {args.min_confidence}")
    print(f"  Output file : {output_path}\n")

    total_emails = 0
    total_errors = 0
    seen_emails  = set()

    for i, domain in enumerate(domains, 1):
        print(f"[{i}/{len(domains)}] {domain} ...", end=" ", flush=True)

        rows = hunter_lookup(domain, HUNTER_API_KEY, args.min_confidence)

        # Deduplicate emails across the full run
        unique_rows = []
        for row in rows:
            email = row["email"]
            if email and email in seen_emails:
                continue
            if email:
                seen_emails.add(email)
            unique_rows.append(row)

        found = sum(1 for r in unique_rows if r["email"])
        total_emails += found
        if not rows:
            total_errors += 1

        print(f"{found} email(s) found")
        append_rows(output_path, unique_rows)

        if i < len(domains):
            time.sleep(REQUEST_DELAY)

    print(f"\n── Summary ──────────────────────────────")
    print(f"  Domains processed : {len(domains)}")
    print(f"  Unique emails     : {total_emails}")
    print(f"  API errors        : {total_errors}")
    print(f"  Output            : {output_path}")
    print(f"─────────────────────────────────────────\n")


if __name__ == "__main__":
    main()
