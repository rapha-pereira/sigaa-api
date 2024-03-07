"""This module contains the profile section of the portal."""
# TODO: Improve dinamic get of info from profile.

from urllib.parse import urljoin
from app.core.config import SIGAA_SITE_ENTRYPOINT
from app.sigaa.schemas import Profile

from typing import Union, List

from selectolax.lexbor import LexborHTMLParser, LexborNode


class PortalProfile:
    def __init__(self, parser: LexborHTMLParser) -> None:
        self._parser = parser
        self._portal_selector = "#perfil-docente"
        self._photo_selector = "div.pessoal-docente > div.foto > img"
        self._name_selector = "p.info-docente > span > small > b"
        self._additional_info_selector = "#agenda-docente"
        self._additional_info_table_selector = "table > tbody"
        pass

    def _get_profile_name(self) -> Union[str, None]:
        """Method to get the profile name."""
        selector = f"{self._portal_selector} > {self._name_selector}"
        name_node = self._parser.css_first(selector)
        if name_node:
            return name_node.text(deep=True, separator="", strip=True)
        else:
            return None

    def _get_profile_photo(self) -> Union[str, None]:
        """Method to get the profile photo."""
        selector = f"{self._portal_selector} > {self._photo_selector}"
        photo_node = self._parser.css_first(selector)
        if photo_node:
            return urljoin(
                base=SIGAA_SITE_ENTRYPOINT, url=photo_node.attributes.get("src")
            )
        else:
            return None

    def _get_additional_info(self) -> Union[List[str], None]:
        """Method to get the additional info."""
        def _get_student_id(main_node: LexborNode) -> int:
            pass

        selector = f"{self._portal_selector} > {self._additional_info_selector} > {self._additional_info_table_selector}"
        additional_info_node = self._parser.css_first(selector)
        if additional_info_node:
            return [
                info.text(deep=True, separator="", strip=True)
                for info in additional_info_node.css("tr > td")
                if info
            ]
        else:
            return None

    def get_profile_with_basic_info(self) -> Profile:
        """Method to get the profile basic info."""
        name = self._get_profile_name()
        photo = self._get_profile_photo()
        return Profile(name=name, photo=photo)

    def get_profile_with_additional_info(self) -> Profile:
        """Method to get the profile with additional info."""
        name = self._get_profile_name()
        photo = self._get_profile_photo()
        additional_info = self._get_additional_info()
        return Profile(name=name, photo=photo, additional_info=additional_info)
