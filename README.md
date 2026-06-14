# Lead Enrichment Tool

![Python](https://img.shields.io/badge/Python-3.9+-blue?style=flat-square&logo=python)
![License](https://img.shields.io/badge/License-MIT-green?style=flat-square)
![Status](https://img.shields.io/badge/Status-Active-brightgreen?style=flat-square)

A lightweight CLI tool that takes a CSV of raw leads (name + company/domain) and enriches them with verified emails, LinkedIn URLs, company metadata, and lead scores — ready to drop into any outreach sequence.

---

## Features

- **Email Discovery** — generates pattern-based emails and validates via Hunter.io
- **Company Enrichment** — pulls industry, size, and LinkedIn from Clearbit
- **Lead Scoring** — scores each lead 0–100 based on data completeness and ICP fit
- **Deduplication** — cleans and dedupes the input before processing
- **Multiple Output Formats** — CSV, JSON, or pretty-printed table
- **Batch Processing** — handles large lists with rate-limit-aware throttling

---

## Quickstart

```bash
# 1. Clone and install
git clone https://github.com/YOUR_USERNAME/lead-enrichment-tool.git
cd lead-enrichment-tool
pip install -r requirements.txt

# 2. Set your API keys
cp .env.example .env
# Edit .env with your Hunter.io and Clearbit keys

# 3. Run enrichment
python -m enricher.cli enrich data/sample_leads.csv --output results.csv
```

---

## Input Format

Your CSV needs at minimum a `company` or `domain` column. Everything else is optional but improves match rates.

```csv
first_name,last_name,company,domain,title
Sarah,Chen,Acme Corp,acme.com,Head of Growth
Marcus,Webb,Stripe,,VP of Sales
,, Notion,notion.so,
```

---

## Output

```csv
first_name,last_name,company,domain,email,email_confidence,linkedin_url,industry,company_size,lead_score
Sarah,Chen,Acme Corp,acme.com,sarah.chen@acme.com,92,linkedin.com/in/sarahchen,SaaS,51-200,88
Marcus,Webb,Stripe,stripe.com,marcus.webb@stripe.com,87,linkedin.com/in/marcuswebb,Fintech,1001-5000,91
```

---

## CLI Reference

```bash
# Basic enrichment
python -m enricher.cli enrich leads.csv

# Specify output file and format
python -m enricher.cli enrich leads.csv --output enriched.csv --format csv

# Filter by minimum lead score
python -m enricher.cli enrich leads.csv --min-score 70

# Dry run (validate input only, no API calls)
python -m enricher.cli enrich leads.csv --dry-run

# Show stats summary after enrichment
python -m enricher.cli enrich leads.csv --stats
```

---

## Configuration

| Variable | Required | Description |
|---|---|---|
| `HUNTER_API_KEY` | Yes | Hunter.io API key — free tier gives 25 searches/month |
| `CLEARBIT_API_KEY` | No | Clearbit key for company metadata |
| `RATE_LIMIT_DELAY` | No | Seconds between API calls (default: 1.0) |
| `MIN_EMAIL_CONFIDENCE` | No | Drop emails below this confidence score (default: 60) |

---

## How Lead Scoring Works

Each lead is scored out of 100 based on:

| Signal | Points |
|---|---|
| Email found + verified | 40 |
| Email confidence > 80 | +10 |
| LinkedIn URL resolved | 20 |
| Company size data available | 15 |
| Title/role populated | 15 |

---

## Project Structure

```
lead-enrichment-tool/
├── enricher/
│   ├── core.py           # Main enrichment pipeline
│   ├── cli.py            # Click-based CLI
│   ├── sources/
│   │   ├── hunter.py     # Hunter.io email finder
│   │   ├── clearbit.py   # Clearbit company data
│   │   └── email_patterns.py  # Pattern-based email generation
│   └── utils/
│       ├── validator.py  # Email syntax + MX validation
│       └── formatter.py  # Output formatting
├── data/
│   └── sample_leads.csv  # Sample input file
├── tests/
├── docs/
│   └── usage.md
├── .env.example
└── requirements.txt
```

---

## License

MIT
