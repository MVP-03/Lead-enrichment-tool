import os
import sys
import click
from dotenv import load_dotenv

from enricher.core import EnrichmentPipeline
from enricher.utils.formatter import format_output, print_stats

load_dotenv()


def _build_config(min_score, dry_run):
    return {
        "hunter_api_key": os.getenv("HUNTER_API_KEY", ""),
        "clearbit_api_key": os.getenv("CLEARBIT_API_KEY", ""),
        "rate_limit_delay": os.getenv("RATE_LIMIT_DELAY", "1.0"),
        "min_email_confidence": os.getenv("MIN_EMAIL_CONFIDENCE", "60"),
        "dry_run": dry_run,
    }


@click.group()
def cli():
    """Lead Enrichment Tool — enrich a CSV of leads with emails, LinkedIn, and company data."""
    pass


@cli.command()
@click.argument("input_file", type=click.Path(exists=True))
@click.option("--output", "-o", default=None, help="Output file path (default: prints to stdout)")
@click.option("--format", "-f", "fmt", default="csv", type=click.Choice(["csv", "json", "table"]), help="Output format")
@click.option("--min-score", default=0, help="Only output leads with lead_score >= this value")
@click.option("--dry-run", is_flag=True, default=False, help="Validate input and show plan without making API calls")
@click.option("--stats", is_flag=True, default=False, help="Print enrichment stats summary after processing")
def enrich(input_file, output, fmt, min_score, dry_run, stats):
    """Enrich leads from INPUT_FILE with emails, LinkedIn URLs, and company data."""

    if dry_run:
        click.echo("Dry run mode — no API calls will be made.\n")

    config = _build_config(min_score, dry_run)
    pipeline = EnrichmentPipeline(config)

    try:
        click.echo(f"Loading {input_file}...")
        df = pipeline.load(input_file)
        click.echo(f"Found {len(df)} leads.\n")
    except (ValueError, FileNotFoundError) as e:
        click.echo(f"Error: {e}", err=True)
        sys.exit(1)

    result_df = pipeline.run(df)

    if min_score > 0:
        result_df = result_df[result_df["lead_score"] >= min_score]
        click.echo(f"\nFiltered to {len(result_df)} leads with score >= {min_score}.")

    if stats:
        print_stats(result_df)

    formatted = format_output(result_df, fmt=fmt)

    if output:
        with open(output, "w", newline="", encoding="utf-8") as f:
            f.write(formatted)
        click.echo(f"Results saved to {output}")
    else:
        click.echo(formatted)
