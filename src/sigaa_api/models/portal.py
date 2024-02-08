import time
from typing import List, Tuple, Union
from dataclasses import dataclass, field

from re import split as re_split
from re import search as re_search

from playwright.sync_api import Locator, Page


@dataclass(frozen=True)
class StudentPortalLogin:
    """
    A class that represents the SIGAA login page.
    https://sig.ifsc.edu.br/sigaa/
    """

    username: str
    password: str


@dataclass(frozen=True)
class Classes:
    """
    A class that represents classes section of the portal.
    """

    page: Page
    portal_div_selector: str = field(default="#turmas-portal", init=False)
    portal_table_selector: str = field(default="table:nth-child(3)", init=False)
    portal_header_selector: str = field(default="thead > tr", init=False)
    portal_body_selector: str = field(default="tbody", init=False)

    @property
    def div(self) -> Locator:
        return self.page.locator(selector=self.portal_div_selector)

    @property
    def table(self) -> Locator:
        return self.div.locator(selector_or_locator=self.portal_table_selector)

    @property
    def header(self) -> Locator:
        return self.table.locator(selector_or_locator=self.portal_header_selector)

    @property
    def body(self) -> Locator:
        return self.table.locator(selector_or_locator=self.portal_body_selector)

    def get_header(self) -> List[str]:
        """Method to get the header of the classes table as text."""
        return list(filter(None, re_split(r"\t|\n+", self.header.inner_text())))

    def get_body_raw_texts(self) -> List[str]:
        """Method to get the body of the classes table as text."""
        return self.body.locator(selector_or_locator="tr").all_inner_texts()

    def get_classes_content(self) -> List[Union[Tuple[str, str, str], None]]:
        """Method to get the content of the classes table."""
        body_tr_inner_texts = self.get_body_raw_texts()

        def group_courses_content(string: str) -> Union[Tuple[str, str, str], None]:
            match = re_search(r"(.+?)\n(.+?)\t\n([*]?)\n\n", string)
            if match:
                course_name, course_code, course_schedule = match.group(1, 2, 3)
                return course_name, course_code, course_schedule

        return [group_courses_content(_str) for _str in body_tr_inner_texts]


@dataclass(frozen=True)
class StudentPortal:
    """
    A class that represents the SIGAA main page.
    https://sig.ifsc.edu.br/sigaa/portais/discente/
    """

    page: Page

    def get_classes_portal(self) -> Classes:
        time.sleep(10)
        return Classes(page=self.page)
