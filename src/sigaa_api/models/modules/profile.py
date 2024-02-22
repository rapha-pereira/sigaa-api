"""This module contains the profile section of the portal."""

from src.sigaa_api.utils.aux_functions import remove_newlines_and_tabs

from dataclasses import dataclass, field
from typing import Union, List

from selectolax.lexbor import LexborHTMLParser, LexborNode


@dataclass(frozen=True, slots=True)
class Profile:
    """
    A class that represents the profile section of the portal.
    """

    page: Page
    _portal_main_div_selector: str = field(default="#perfil-docente", init=False)
    _portal_photo_selector: str = field(
        default="div.pessoal-docente > div.foto > img", init=False
    )
    _portal_name_selector: str = field(
        default="p.info-docente > span > small > b",
        init=False,
    )
    _portal_institutional_data_selector: str = field(
        default="#agenda-docente",
        init=False,
    )

    @property
    def div(self) -> Locator:
        return self.page.locator(selector=self._portal_main_div_selector)

    def get_name(self) -> str:
        """Method to get the name of the user."""
        return self.div.locator(
            selector_or_locator=self._portal_name_selector
        ).inner_text()

    def get_photo_url(self) -> str:
        """Method to get the photo of the user."""
        # .evaluate() is used to get the src *property* of the img tag
        # .get_attribute() would return the attribute, that doesn't contain the base URL
        return self.div.locator(
            selector_or_locator=self._portal_photo_selector
        ).evaluate("el => el.src")
