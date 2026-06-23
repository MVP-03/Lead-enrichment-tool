import requests


HUNTER_BASE_URL = "https://api.hunter.io/v2"


class HunterClient:
    def __init__(self, api_key: str):
        self.api_key = api_key
        self.session = requests.Session()

    def find_email(self, first_name: str, last_name: str, domain: str) -> dict | None:
        if not self.api_key:
            return None

        params = {
            "first_name": first_name,
            "last_name": last_name,
            "domain": domain,
            "api_key": self.api_key,
        }

        try:
            response = self.session.get(
                f"{HUNTER_BASE_URL}/email-finder", params=params, timeout=10
            )
            response.raise_for_status()
            data = response.json().get("data", {})

            email = data.get("email")
            confidence = data.get("score", 0)

            if email:
                return {"email": email, "confidence": confidence}

        except requests.RequestException:
            pass

        return None

    def verify_email(self, email: str) -> dict | None:
        if not self.api_key:
            return None

        params = {"email": email, "api_key": self.api_key}

        try:
            response = self.session.get(
                f"{HUNTER_BASE_URL}/email-verifier", params=params, timeout=10
            )
            response.raise_for_status()
            data = response.json().get("data", {})
            return {
                "status": data.get("status"),
                "score": data.get("score", 0),
            }
        except requests.RequestException:
            return None

    def domain_search(self, domain: str, limit: int = 10) -> list[dict]:
        if not self.api_key:
            return []

        params = {"domain": domain, "limit": limit, "api_key": self.api_key}

        try:
            response = self.session.get(
                f"{HUNTER_BASE_URL}/domain-search", params=params, timeout=10
            )
            response.raise_for_status()
            emails = response.json().get("data", {}).get("emails", [])
            return [
                {
                    "first_name": e.get("first_name", ""),
                    "last_name": e.get("last_name", ""),
                    "email": e.get("value", ""),
                    "confidence": e.get("confidence", 0),
                    "title": e.get("position", ""),
                }
                for e in emails
            ]
        except requests.RequestException:
            return []
