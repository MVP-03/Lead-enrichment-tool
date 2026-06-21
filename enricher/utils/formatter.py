import json
import pandas as pd
from tabulate import tabulate


OUTPUT_COLUMNS = [
    "first_name",
    "last_name",
    "company",
    "domain",
    "title",
    "email",
    "email_confidence",
    "linkedin_url",
    "industry",
    "company_size",
    "lead_score",
]


def format_output(df: pd.DataFrame, fmt: str = "csv") -> str:
    df = _reorder_columns(df)

    if fmt == "csv":
        return df.to_csv(index=False)

    if fmt == "json":
        return json.dumps(df.to_dict(orient="records"), indent=2)

    if fmt == "table":
        return tabulate(df, headers="keys", tablefmt="rounded_outline", showindex=False)

    raise ValueError(f"Unsupported format: {fmt}. Choose csv, json, or table.")


def print_stats(df: pd.DataFrame) -> None:
    total = len(df)
    with_email = df["email"].notna() & (df["email"] != "")
    avg_score = df["lead_score"].mean()

    print("\n── Enrichment Summary ──────────────────")
    print(f"  Total leads processed : {total}")
    print(f"  Emails found          : {with_email.sum()} ({with_email.mean()*100:.0f}%)")
    print(f"  Avg lead score        : {avg_score:.1f} / 100")
    print(f"  High-quality (≥70)    : {(df['lead_score'] >= 70).sum()}")
    print("────────────────────────────────────────\n")


def _reorder_columns(df: pd.DataFrame) -> pd.DataFrame:
    cols = [c for c in OUTPUT_COLUMNS if c in df.columns]
    extra = [c for c in df.columns if c not in OUTPUT_COLUMNS]
    return df[cols + extra]
