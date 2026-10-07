"""US-specific configuration for the Narwal Cloud US build."""

from __future__ import annotations

API_BASE_URL = "https://us-app.narwaltech.com"
COUNTRY_CODE = "US"
BROKER_DISCOVERY_COUNTRY = "US"


def build_login_payload(email: str, password: str) -> dict[str, str]:
    """Build the payload accepted by Narwal's US login endpoint.

    The US endpoint, like the EU one, accepts the plain password field inside
    verified HTTPS (confirmed against loginByEmail on us-app.narwaltech.com).
    """
    return {"email": email, "password": password}
