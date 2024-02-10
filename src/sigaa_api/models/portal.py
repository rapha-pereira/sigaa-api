from typing import List, Tuple, Union
from dataclasses import dataclass, field

from re import split as re_split
from re import search as re_search

from playwright.sync_api import Locator, Page


@dataclass(frozen=True, slots=True)
class StudentPortalLogin:
    """
    A class that represents the SIGAA login page.
    https://sig.ifsc.edu.br/sigaa/
    """

    username: str
    password: str


@dataclass(frozen=True, slots=True)
class Classes:
    """
    A class that represents the classes section of the portal.
    """

    page: Page
    _portal_div_selector: str = field(default="#turmas-portal", init=False)
    _portal_table_selector: str = field(default="table:nth-child(3)", init=False)
    _portal_header_selector: str = field(default="thead > tr", init=False)
    _portal_body_selector: str = field(default="tbody", init=False)

    @property
    def div(self) -> Locator:
        return self.page.locator(selector=self._portal_div_selector)

    @property
    def table(self) -> Locator:
        return self.div.locator(selector_or_locator=self._portal_table_selector)

    @property
    def header(self) -> Locator:
        return self.table.locator(selector_or_locator=self._portal_header_selector)

    @property
    def body(self) -> Locator:
        return self.table.locator(selector_or_locator=self._portal_body_selector)

    def get_normalized_header(self) -> List[str]:
        """Method to get the header of the classes table as text."""
        return list(filter(None, re_split(r"\t|\n+", self.header.inner_text())))

    def get_body_raw_texts(self) -> List[str]:
        """Method to get the body of the classes table as text."""
        return self.body.locator(selector_or_locator="tr").all_inner_texts()

    def get_classes_content(self) -> List[Union[Tuple[str, str, str], None]]:
        """Method to get the content of the classes table."""
        body_tr_inner_texts = filter(None, self.get_body_raw_texts())

        def group_courses_content(string: str) -> Union[Tuple[str, str, str], None]:
            match = re_search(r"(.+?)\n(.+?)\t\n([*]?)\n\n", string)
            if match:
                course_name, course_code, course_schedule = match.group(1, 2, 3)
                return course_name, course_code, course_schedule
            else:
                return None

        return [group_courses_content(_str) for _str in body_tr_inner_texts]

    def get_classes_content_with_header(self) -> Union[List[dict], None]:
        """Method to get the content of the classes table with header."""
        header = self.get_normalized_header()
        content = self.get_classes_content()
        if header and content:
            return [dict(zip(header, _tuple)) for _tuple in content]
        else:
            return None


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
        return self.div.locator(
            selector_or_locator=self._portal_photo_selector
        ).get_attribute("src")


@dataclass(frozen=True, slots=True)
class StudentPortal:
    """
    A class that represents the SIGAA main page.
    https://sig.ifsc.edu.br/sigaa/portais/discente/
    """

    page: Page

    def __post_init__(self) -> None:
        resolver: None = self.page.wait_for_load_state("load")
        # Wait until Playwright loads the page, then init the class.
        if resolver is None:
            del resolver
            pass

    def get_classes_portal(self) -> Classes:
        return Classes(page=self.page)

    def get_profile_portal(self) -> Profile:
        return Profile(page=self.page)
