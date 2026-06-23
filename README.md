<div align="center">

# Lead Enrichment Tool

**Turn a raw CSV of leads into a fully enriched, scored, outreach-ready list.**

![Python](https://img.shields.io/badge/Python-3.9+-blue?style=flat-square&logo=python&logoColor=white)
![Hunter.io](https://img.shields.io/badge/Hunter.io-Integrated-orange?style=flat-square)
![Clearbit](https://img.shields.io/badge/Clearbit-Integrated-purple?style=flat-square)
![License](https://img.shields.io/badge/License-MIT-green?style=flat-square)
![Status](https://img.shields.io/badge/Status-Active-brightgreen?style=flat-square)

</div>

---

## What it does

Takes a CSV of raw leads — just names and companies, no emails needed — and enriches each one with:

- **Verified email addresses** via Hunter.io (with pattern-based fallback)
- **Company metadata** via Clearbit — industry, headcount, LinkedIn
- **Lead scores** (0–100) based on data completeness and ICP signals
- **Deduplication** before any API calls are made

Output is a ranked CSV ready to import into Instantly, Apollo, or your CRM.

---

## Table of Contents

- [Quickstart](#quickstart)
- [How It Works](#how-it-works)
- [Input Format](#input-format)
- [Output](#output)
- [Lead Scoring](#lead-scoring)
- [Configuration](#configuration)
- [CLI Reference](#cli-reference)
- [Project Structure](#project-structure)
- [Running Tests](#running-tests)
- [Contributing](#contributing)

---

## Quickstart

```bash
git clone https://github.com/MVP-03/lead-enrichment-tool.git
cd lead-enrichment-tool
pip install -r requirements.txt

# Copy and fill in your API keys
cp .env.example .env

# Run enrichment
python -m enricher.cli enrich data/sample_leads.csv --output enriched.csv --stats
```

---

## How It Works

```
Input CSV
    │
    ▼
Clean + Deduplicate
    │
    ▼
Domain Inference (if domain missing)
    │
    ▼
Email Discovery ──► Hunter.io API
    │                   │ (if not found)
    │               Pattern Generator
    │               + MX Validation
    ▼
Company Enrichment ──► Clearbit API
    │
    ▼
Lead Scoring (0–100)
    │
    ▼
Output CSV / JSON / Table
```

---

## Input Format

Minimum required: a `company` or `domain` column. Everything else improves match rate.

```csv
first_name,last_name,company,domain,title
Sarah,Chen,Notion,,Head of Growth
Marcus,Webb,Stripe,stripe.com,VP of Sales
Priya,Sharma,Linear,linear.app,Product Lead
```

---

## Output

```csv
first_name,last_name,company,domain,email,email_confidence,linkedin_url,industry,company_size,lead_score
Sarah,Chen,Notion,notion.so,sarah.chen@notion.so,88,linkedin.com/company/notionhq,Productivity,501-1000,93
Marcus,Webb,Stripe,stripe.com,marcus.webb@stripe.com,91,linkedin.com/company/stripe,Fintech,1001-5000,98
Priya,Sharma,Linear,linear.app,priya.sharma@linear.app,76,linkedin.com/company/linear,DevTools,51-200,86
```

---

## Lead Scoring

Each lead is scored 0–100 based on enrichment completeness:

| Signal | Points |
|---|---|
| Email found | +40 |
| Email confidence > 80 | +10 |
| LinkedIn URL found | +20 |
| Company size data | +15 |
| Title populated | +15 |

Use `--min-score 70` before importing to your sequencer to filter out low-quality records.

---

## Configuration

Copy `.env.example` to `.env` and set your keys:

| Variable | Required | Description |
|---|---|---|
| `HUNTER_API_KEY` | Yes | Hunter.io — free tier gives 25 searches/month |
| `CLEARBIT_API_KEY` | No | Clearbit — enables company metadata |
| `RATE_LIMIT_DELAY` | No | Seconds between API calls (default: `1.0`) |
| `MIN_EMAIL_CONFIDENCE` | No | Drop emails below this score (default: `60`) |

---

## CLI Reference

```bash
# Basic enrichment — outputs to terminal
python -m enricher.cli enrich leads.csv

# Save to file
python -m enricher.cli enrich leads.csv --output enriched.csv

# JSON output
python -m enricher.cli enrich leads.csv --format json

# Pretty table in terminal
python -m enricher.cli enrich leads.csv --format table

# Only output high-quality leads
python -m enricher.cli enrich leads.csv --min-score 70 --output qualified.csv

# Show summary stats after run
python -m enricher.cli enrich leads.csv --stats

# Validate input without using API credits
python -m enricher.cli enrich leads.csv --dry-run
```

---

## Project Structure

```
lead-enrichment-tool/
├── enricher/
│   ├── core.py                  # Main enrichment pipeline
│   ├── cli.py                   # Click-based CLI
│   ├── sources/
│   │   ├── hunter.py            # Hunter.io email finder + verifier
│   │   ├── clearbit.py          # Clearbit company enrichment
│   │   └── email_patterns.py    # Pattern-based email generation fallback
│   └── utils/
│       ├── validator.py         # Email syntax + MX record validation
│       └── formatter.py         # CSV / JSON / table output
├── data/
│   └── sample_leads.csv
├── tests/
│   ├── test_core.py
│   └── test_validator.py
├── .env.example
└── requirements.txt
```

---

## Running Tests

```bash
pip install pytest
pytest tests/
```

Tests run with `dry_run=True` — no API calls, no keys needed.

---

## Contributing

Ideas for next iterations:

- LinkedIn URL resolution via Proxycurl
- Apollo.io as an additional email source
- Batch mode with checkpoint/resume for large lists (1k+)
- Streamlit UI for non-technical users

---

## License

MIT
