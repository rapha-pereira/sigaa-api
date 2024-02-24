"""A module that represents the SIGAA login model"""

from src.sigaa_api.core.exceptions import LoginFailed

from selectolax.lexbor import LexborHTMLParser

from dataclasses import dataclass, field

import requests


@dataclass(init=True, frozen=True, slots=True)
class LoginModel:
    """A class that represents the SIGAA login after the POST on the form URL."""

    response: requests.Response = field(init=True)
    _is_response_ok: bool = field(init=False)

    def __post_init__(self):
        if not self.response.ok:
            raise LoginFailed()
        else:
            pass

    def parse_response(self) -> LexborHTMLParser:
        """Method to parse the response."""
        return LexborHTMLParser(self.response.text)
