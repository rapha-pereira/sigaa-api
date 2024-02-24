"""This module represents the student portal login process."""

from src.sigaa_api.utils.http_client import HttpClient
from src.sigaa_api.core.login.login_model import LoginModel

from src.sigaa_api.core.login.config import (
    RECAPTCHA_ANCHOR,
    RECAPTCHA_PAYLOAD,
    RECAPTCHA_RELOAD,
    SIGAA_BASE_URL,
    SIGAA_LOGIN_URL,
    SIGAA_LOGIN_FORM_URL,
    SIGAA_LOGIN_FORM_HEADER,
)

from typing import Tuple

import requests
import getpass


class PortalLogin:
    """Class to represent the login process on SIGAA."""

    def __init__(self) -> None:
        self._http = HttpClient(base_url=SIGAA_BASE_URL)
        pass

    def _get_user_credentials(self) -> Tuple[str, str]:
        """Get the user credentials."""
        print("Enter your SIGAA credentials.")
        username = input("Username: ")
        password = getpass.getpass("Password: ")
        return username, password

    def _generate_recaptcha(self) -> str:
        """Generate recaptcha token for active session."""
        # NOTE.:
        # Script taken from: https://github.com/blaannk/Recaptcha-Invisible-Bypass.git
        # Minor modifications were made on this.
        s = self._http.session
        r1 = s.get(url=RECAPTCHA_ANCHOR).text
        token1 = r1.split('recaptcha-token" value="')[1].split('">')[0]
        payload = RECAPTCHA_PAYLOAD.replace("<token>", str(token1))
        r2 = s.post(
            url=RECAPTCHA_RELOAD,
            data=payload,
            headers={"Content-Type": "application/x-www-form-urlencoded"},
        )
        try:
            token2 = str(r2.text.split('"rresp","')[1].split('"')[0])
            return token2
        except:  # noqa: E722
            return ""

    def _get_login_page(self) -> requests.Response:
        """Get the login page."""
        return self._http.get(endpoint=SIGAA_LOGIN_URL)

    @staticmethod
    def _get_cookies(response: requests.Response) -> dict:
        """Get the cookies from the login page."""
        return response.cookies.get_dict()

    def login(self) -> LoginModel:
        """Login into the SIGAA portal."""
        username, password = self._get_user_credentials()
        recaptcha_token = self._generate_recaptcha()
        response = self._get_login_page()
        cookies = self._get_cookies(response)

        payload = {
            "width": "1920",
            "height": "1080",
            "user.login": username,
            "user.senha": password,
            "recaptcha-token": recaptcha_token,
        }
        response = self._http.post(
            endpoint=SIGAA_LOGIN_FORM_URL,
            data=payload,
            headers=SIGAA_LOGIN_FORM_HEADER,
            cookies=cookies,
            allow_redirects=True,
        )

        del username, password, recaptcha_token, cookies, payload
        return LoginModel(response=response)
