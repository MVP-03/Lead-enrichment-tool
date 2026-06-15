import time
import pandas as pd
from tqdm import tqdm

from enricher.sources.hunter import HunterClient
from enricher.sources.clearbit import ClearbitClient
from enricher.sources.email_patterns import generate_email_candidates
from enricher.utils.validator import validate_email_syntax, validate_mx_record
from enricher.utils.formatter import format_output


REQUIRED_COLUMNS = {"company", "domain"}


class EnrichmentPipeline:
    def __init__(self, config: dict):
        self.hunter = HunterClient(config.get("hunter_api_key"))
        self.clearbit = ClearbitClient(config.get("clearbit_api_key"))
        self.rate_limit_delay = float(config.get("rate_limit_delay", 1.0))
        self.min_confidence = int(config.get("min_email_confidence", 60))
        self.dry_run = config.get("dry_run", False)

    def load(self, filepath: str) -> pd.DataFrame:
        df = pd.read_csv(filepath)
        df.columns = [c.strip().lower().replace(" ", "_") for c in df.columns]

        if not REQUIRED_COLUMNS.intersection(set(df.columns)):
            raise ValueError(
                "Input CSV must have at least a 'company' or 'domain' column."
            )

        df = self._clean(df)
        return df

    def _clean(self, df: pd.DataFrame) -> pd.DataFrame:
        df = df.drop_duplicates()
        df = df.dropna(how="all")
        for col in ["first_name", "last_name", "company", "domain", "title"]:
            if col in df.columns:
                df[col] = df[col].astype(str).str.strip()
                df[col] = df[col].replace("nan", "")
        return df.reset_index(drop=True)

    def run(self, df: pd.DataFrame) -> pd.DataFrame:
        results = []

        for _, row in tqdm(df.iterrows(), total=len(df), desc="Enriching leads"):
            record = row.to_dict()
            record = self._enrich_record(record)
            record["lead_score"] = self._score(record)
            results.append(record)

            if not self.dry_run:
                time.sleep(self.rate_limit_delay)

        return pd.DataFrame(results)

    def _enrich_record(self, record: dict) -> dict:
        domain = record.get("domain", "")
        first = record.get("first_name", "")
        last = record.get("last_name", "")

        if not domain and record.get("company"):
            domain = self._infer_domain(record["company"])
            record["domain"] = domain

        record.setdefault("email", "")
        record.setdefault("email_confidence", 0)
        record.setdefault("linkedin_url", "")
        record.setdefault("industry", "")
        record.setdefault("company_size", "")

        if self.dry_run or not domain:
            return record

        # Email discovery — Hunter first, fallback to pattern generation
        if first and last and domain:
            hunter_result = self.hunter.find_email(first, last, domain)
            if hunter_result and hunter_result["confidence"] >= self.min_confidence:
                record["email"] = hunter_result["email"]
                record["email_confidence"] = hunter_result["confidence"]

        if not record["email"] and first and last and domain:
            candidates = generate_email_candidates(first, last, domain)
            for candidate in candidates:
                if validate_email_syntax(candidate) and validate_mx_record(domain):
                    record["email"] = candidate
                    record["email_confidence"] = 50
                    break

        # Company enrichment via Clearbit
        if domain:
            company_data = self.clearbit.enrich_company(domain)
            if company_data:
                record["industry"] = company_data.get("industry", "")
                record["company_size"] = company_data.get("employees_range", "")
                record["linkedin_url"] = company_data.get("linkedin_handle", "")

        return record

    def _infer_domain(self, company_name: str) -> str:
        slug = company_name.lower().strip()
        slug = "".join(c for c in slug if c.isalnum())
        return f"{slug}.com"

    def _score(self, record: dict) -> int:
        score = 0
        if record.get("email"):
            score += 40
            if int(record.get("email_confidence", 0)) > 80:
                score += 10
        if record.get("linkedin_url"):
            score += 20
        if record.get("company_size"):
            score += 15
        if record.get("title"):
            score += 15
        return min(score, 100)
