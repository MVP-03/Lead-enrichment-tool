# Usage Guide

## Prerequisites

- Python 3.9+
- A [Hunter.io](https://hunter.io) API key (free tier: 25 searches/month)
- Optional: A [Clearbit](https://clearbit.com) API key for company metadata

## Installation

```bash
git clone https://github.com/YOUR_USERNAME/lead-enrichment-tool.git
cd lead-enrichment-tool
pip install -r requirements.txt
```

## Configuration

Copy the example env file and fill in your keys:

```bash
cp .env.example .env
```

```
HUNTER_API_KEY=your_key_here
CLEARBIT_API_KEY=your_key_here  # optional
RATE_LIMIT_DELAY=1.0
MIN_EMAIL_CONFIDENCE=60
```

## Preparing Your Input

Create a CSV with at minimum a `company` or `domain` column:

```csv
first_name,last_name,company,domain,title
Sarah,Chen,Notion,,Head of Growth
Marcus,Webb,Stripe,stripe.com,VP Sales
```

The more columns you provide, the higher the email match rate.

## Running Enrichment

```bash
# Basic run — outputs to terminal
python -m enricher.cli enrich data/sample_leads.csv

# Save results to a file
python -m enricher.cli enrich data/sample_leads.csv --output enriched.csv

# JSON output
python -m enricher.cli enrich data/sample_leads.csv --format json

# Pretty table in terminal
python -m enricher.cli enrich data/sample_leads.csv --format table

# Only keep high-quality leads
python -m enricher.cli enrich data/sample_leads.csv --min-score 70 --output qualified.csv

# See summary stats
python -m enricher.cli enrich data/sample_leads.csv --stats

# Test without using API credits
python -m enricher.cli enrich data/sample_leads.csv --dry-run
```

## Understanding Lead Scores

| Score Range | Meaning |
|---|---|
| 90–100 | Email verified, full profile data |
| 70–89 | Email found, most fields populated |
| 50–69 | Email found, partial company data |
| Below 50 | No email, low data completeness |

Use `--min-score 70` before importing into your CRM or sequencer.

## Running Tests

```bash
pip install pytest
pytest tests/
```
