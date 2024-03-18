"""This module represents the student portal login process."""

from fastapi.security import HTTPBasicCredentials

from sigaa_api.http import HttpClient
from sigaa_api.sigaa.models import SIGAALogin

from sigaa_api.core.config import (
    RECAPTCHA_ANCHOR,
    RECAPTCHA_PAYLOAD,
    RECAPTCHA_RELOAD,
    SIGAA_SITE_ENTRYPOINT,
    SIGAA_LOGIN_ENDPOINT,
    SIGAA_LOGIN_FORM_ENDPOINT,
    SIGAA_LOGIN_FORM_HEADER,
)


class PortalLogin:
    """Execute the login process on SIGAA."""

    def __init__(self, credentials: HTTPBasicCredentials) -> None:
        self._http = HttpClient(base_url=SIGAA_SITE_ENTRYPOINT)
        self._username = credentials.username
        self._password = credentials.password
        pass

    def _generate_recaptcha(self) -> str:
        """Generate recaptcha token for active session.\n
        NOTE: Code from: https://github.com/blaannk/Recaptcha-Invisible-Bypass.git
        """
        session = self._http.session

        response1 = session.get(url=RECAPTCHA_ANCHOR).text
        token1 = response1.split('recaptcha-token" value="')[1].split('">')[0]

        payload = RECAPTCHA_PAYLOAD.replace("<token>", str(token1))
        response2 = session.post(
            url=RECAPTCHA_RELOAD,
            data=payload,
            headers={"Content-Type": "application/x-www-form-urlencoded"},
        )

        try:
            token2 = str(response2.text.split('"rresp","')[1].split('"')[0])
            return token2 if token2 else ""

        except IndexError:
            return ""

    def login(self) -> SIGAALogin:
        """Login into the SIGAA portal."""
        recaptcha_token = self._generate_recaptcha()
        login_response = self._http.get(endpoint=SIGAA_LOGIN_ENDPOINT)
        login_cookies = login_response.cookies.get_dict()

        form_payload = {
            "width": "1920",
            "height": "1080",
            "user.login": self._username,
            "user.senha": self._password,
            "g-recaptcha-response": recaptcha_token,
        }
        form_response = self._http.post(
            endpoint=SIGAA_LOGIN_FORM_ENDPOINT,
            headers=SIGAA_LOGIN_FORM_HEADER,
            cookies=login_cookies,
            data=form_payload,
            allow_redirects=True,
        )

        return SIGAALogin(response=form_response)
