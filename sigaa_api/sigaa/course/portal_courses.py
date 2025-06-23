"""This module contains the courses section of the portal."""

from sigaa_api.utils import remove_newlines_and_tabs
from sigaa_api.sigaa.models import Course

from typing import Union, List

from selectolax.lexbor import LexborHTMLParser, LexborNode


class PortalCourses:
    def __init__(self, parser: LexborHTMLParser) -> None:
        self._parser = parser
        self._portal_selector = "#turmas-portal"
        self._table_selector = "table:nth-child(3)"
        self._header_selector = "thead > tr"
        self._body_selector = "tbody > tr"
        pass

    def _get_courses_header(self) -> Union[List[str], None]:
        """Method to get the header of the courses table."""
        selector = f"{self._portal_selector} > {self._table_selector} > {self._header_selector}"
        header_node = self._parser.css_first(selector)
        if header_node:
            headers_text: list = [
                header.text(deep=True, separator="", strip=True)
                for header in header_node.css("th")
                if header
            ]
            return list(filter(None, headers_text))
        else:
            return None

    def _get_courses_body(self) -> Union[List[str], None]:
        """Method to get the body of the courses table."""
        selector = (
            f"{self._portal_selector} > {self._table_selector} > {self._body_selector}"
        )
        body_nodes = self._parser.css(selector)
        if body_nodes:
            courses = []
            for node in body_nodes:

                def _handle_td_info(td: LexborNode) -> str: # type: ignore
                    # Handles duplicated td.info elements (local and schedule info)
                    center_selector = td.css_first("center")
                    if center_selector:
                        schedule_content = center_selector.text(
                            deep=True, separator="", strip=True
                        )
                        schedule_content_normalized = remove_newlines_and_tabs(
                            schedule_content
                        )
                        return schedule_content_normalized

                    # When there is no center tag, it means it's the local info
                    if not center_selector:
                        return td.text(deep=True, separator="", strip=True)

                name_selector = node.css_first("td.descricao>form>a")
                local_schedule_selector = node.css("td.info")

                if name_selector:
                    tds_info = [
                        _handle_td_info(td)
                        for td in local_schedule_selector
                        if td and local_schedule_selector
                    ]
                    courses.append(
                        [
                            name_selector.text(deep=True, separator="", strip=True),
                            *tds_info,
                        ]
                    )

            return courses

        else:
            return None

    def get_courses(self) -> Union[List[Course], None]:
        """Method to get courses."""
        body = self._get_courses_body()
        courses = []
        if body:
            for course in body:
                courses.append(
                    Course(name=course[0], location=course[1], schedule=course[2])
                )
            return courses
        else:
            return None
