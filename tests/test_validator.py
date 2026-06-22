import pytest
from enricher.utils.validator import validate_email_syntax


@pytest.mark.parametrize("email,expected", [
    ("john.doe@acme.com", True),
    ("j.doe+tag@sub.domain.co.uk", True),
    ("notanemail", False),
    ("missing@tld", False),
    ("@nodomain.com", False),
    ("spaces @domain.com", False),
    ("", False),
])
def test_validate_email_syntax(email, expected):
    assert validate_email_syntax(email) == expected
