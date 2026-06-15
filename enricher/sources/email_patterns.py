def generate_email_candidates(first: str, last: str, domain: str) -> list[str]:
    first = first.lower().strip()
    last = last.lower().strip()

    if not first or not last or not domain:
        return []

    fi = first[0]
    li = last[0]

    patterns = [
        f"{first}.{last}@{domain}",
        f"{fi}{last}@{domain}",
        f"{first}{li}@{domain}",
        f"{first}@{domain}",
        f"{last}@{domain}",
        f"{first}_{last}@{domain}",
        f"{fi}.{last}@{domain}",
        f"{first}.{li}@{domain}",
    ]

    return patterns
