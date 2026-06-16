import requests


CLEARBIT_BASE_URL = "https://company.clearbit.com/v2"


EMPLOYEE_RANGES = {
    (1, 10): "1-10",
    (11, 50): "11-50",
    (51, 200): "51-200",
    (201, 500): "201-500",
    (501, 1000): "501-1000",
    (1001, 5000): "1001-5000",
    (5001, float("inf")): "5001+",
}


def _employee_range(count: int | None) -> str:
    if not count:
        return ""
    for (low, high), label in EMPLOYEE_RANGES.items():
        if low <= count <= high:
            return label
    return ""


class ClearbitClient:
    def __init__(self, api_key: str):
        self.api_key = api_key
        self.session = requests.Session()
        if api_key:
            self.session.headers.update({"Authorization": f"Bearer {api_key}"})

    def enrich_company(self, domain: str) -> dict | None:
        if not self.api_key:
            return None

        try:
            response = self.session.get(
                f"{CLEARBIT_BASE_URL}/companies/find",
                params={"domain": domain},
                timeout=10,
            )
            if response.status_code == 404:
                return None
            response.raise_for_status()
            data = response.json()

            linkedin = data.get("linkedin", {}).get("handle", "")
            if linkedin:
                linkedin = f"linkedin.com/company/{linkedin}"

            return {
                "industry": data.get("category", {}).get("industry", ""),
                "employees_range": _employee_range(data.get("metrics", {}).get("employees")),
                "linkedin_handle": linkedin,
                "description": data.get("description", ""),
                "location": data.get("location", ""),
            }

        except requests.RequestException:
            return None
