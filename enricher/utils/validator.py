import re
import dns.resolver


EMAIL_REGEX = re.compile(r"^[a-zA-Z0-9._%+\-]+@[a-zA-Z0-9.\-]+\.[a-zA-Z]{2,}$")

_mx_cache: dict[str, bool] = {}


def validate_email_syntax(email: str) -> bool:
    return bool(EMAIL_REGEX.match(email.strip()))


def validate_mx_record(domain: str) -> bool:
    if domain in _mx_cache:
        return _mx_cache[domain]

    try:
        dns.resolver.resolve(domain, "MX")
        _mx_cache[domain] = True
    except (dns.resolver.NoAnswer, dns.resolver.NXDOMAIN, dns.exception.DNSException):
        _mx_cache[domain] = False

    return _mx_cache[domain]
