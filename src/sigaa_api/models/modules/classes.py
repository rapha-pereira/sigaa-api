"""This module contains the classes section of the portal."""

from src.sigaa_api.utils.aux_functions import remove_newlines_and_tabs

from dataclasses import dataclass, field
from typing import Union, List

from selectolax.lexbor import LexborHTMLParser, LexborNode


@dataclass(init=True, frozen=True, slots=True)
class Classes:
    """
    A class that represents the classes section of the portal.
    """

    parser: LexborHTMLParser
    _portal_selector: str = field(default="#turmas-portal", init=False)
    _table_selector: str = field(default="table:nth-child(3)", init=False)
    _header_selector: str = field(default="thead > tr", init=False)
    _body_selector: str = field(default="tbody > tr", init=False)

    def get_classes_header(self) -> Union[List[str], None]:
        """Method to get the header of the classes table."""
        selector = f"{self._portal_selector} > {self._table_selector} > {self._header_selector}"
        header_node = self.parser.css_first(selector)
        if header_node:
            headers_text: list = [
                header.text(deep=True, separator="", strip=True)
                for header in header_node.css("th")
                if header
            ]
            return list(filter(None, headers_text))
        else:
            return None

    def get_classes_body(self) -> Union[List[str], None]:
        """Method to get the body of the classes table."""
        selector = (
            f"{self._portal_selector} > {self._table_selector} > {self._body_selector}"
        )
        body_nodes = self.parser.css(selector)
        if body_nodes:
            classes = []
            for node in body_nodes:

                def _handle_td_info(td: LexborNode) -> str:
                    # Handles duplicated td.info elements (local and schedule info)
                    center_selector = td.css_first("center")
                    if center_selector:
                        schedule_content = center_selector.text_lexbor()
                        schedule_content_normalized = remove_newlines_and_tabs(
                            schedule_content
                        )
                        return schedule_content_normalized

                    # When there is no center tag, it means it's the local info
                    if not center_selector:
                        return td.text()

                name_selector = node.css_first("td.descricao>form>a")
                local_schedule_selector = node.css("td.info")

                if name_selector:
                    tds_info = [
                        _handle_td_info(td)
                        for td in local_schedule_selector
                        if td and local_schedule_selector
                    ]
                    classes.append([name_selector.text(), *tds_info])

            return classes

        else:
            return None

    def get_classes(self) -> Union[dict, None]:
        """Method to get the classes table."""
        header = self.get_classes_header()
        body = self.get_classes_body()
        classes = []
        if header and body:
            for _, row in enumerate(body):
                classes.append(dict(zip(header, row)))
            return classes
        else:
            return None
