import pandas as pd
import pytest
from enricher.core import EnrichmentPipeline


@pytest.fixture
def pipeline():
    config = {
        "hunter_api_key": "",
        "clearbit_api_key": "",
        "rate_limit_delay": "0",
        "min_email_confidence": "60",
        "dry_run": True,
    }
    return EnrichmentPipeline(config)


def test_load_valid_csv(pipeline, tmp_path):
    csv = tmp_path / "leads.csv"
    csv.write_text("first_name,last_name,company,domain\nJane,Doe,Acme,acme.com\n")
    df = pipeline.load(str(csv))
    assert len(df) == 1
    assert df.iloc[0]["company"] == "Acme"


def test_load_missing_required_columns(pipeline, tmp_path):
    csv = tmp_path / "bad.csv"
    csv.write_text("name,email\nJane,jane@test.com\n")
    with pytest.raises(ValueError, match="company.*domain"):
        pipeline.load(str(csv))


def test_clean_deduplicates(pipeline):
    df = pd.DataFrame([
        {"company": "Acme", "domain": "acme.com"},
        {"company": "Acme", "domain": "acme.com"},
    ])
    cleaned = pipeline._clean(df)
    assert len(cleaned) == 1


def test_score_full_record(pipeline):
    record = {
        "email": "jane@acme.com",
        "email_confidence": 90,
        "linkedin_url": "linkedin.com/in/jane",
        "company_size": "51-200",
        "title": "VP Sales",
    }
    assert pipeline._score(record) == 100


def test_score_empty_record(pipeline):
    record = {"email": "", "linkedin_url": "", "company_size": "", "title": ""}
    assert pipeline._score(record) == 0


def test_infer_domain(pipeline):
    assert pipeline._infer_domain("Acme Corp") == "acmecorp.com"
    assert pipeline._infer_domain("Stripe") == "stripe.com"
