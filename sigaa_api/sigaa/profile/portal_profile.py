"""This module contains the profile section of the portal."""

from urllib.parse import urljoin
from typing import Optional
from selectolax.lexbor import LexborHTMLParser

from sigaa_api.core.config import SIGAA_SITE_ENTRYPOINT
from sigaa_api.sigaa.models import AcademicIndexes, Profile, Workload
from sigaa_api.utils import (
    convert_semester_to_date,
    clean_paid_workload_string,
    remove_newlines_and_tabs,
)


_PORTAL_SELECTOR = "#perfil-docente"
_PHOTO_SELECTOR = "div.pessoal-docente > div.foto > img"
_NAME_SELECTOR = "p.info-docente > span > small > b"
_ADDITIONAL_INFO_SELECTOR = "#agenda-docente"
_ADDITIONAL_INFO_TABLE_SELECTOR = "table > tbody"


class PortalProfile:
    def __init__(self, parser: LexborHTMLParser) -> None:
        self._parser = parser
        pass

    def _get_profile_name(self) -> Optional[str]:
        """Method to get the profile name."""
        selector = f"{_PORTAL_SELECTOR} > {_NAME_SELECTOR}"
        name_node = self._parser.css_first(selector)
        if name_node:
            return name_node.text(deep=True, separator="", strip=True)
        else:
            return None

    def _get_profile_photo(self) -> Optional[str]:
        """Method to get the profile photo."""
        selector = f"{_PORTAL_SELECTOR} > {_PHOTO_SELECTOR}"
        photo_node = self._parser.css_first(selector)
        if photo_node:
            return urljoin(
                base=SIGAA_SITE_ENTRYPOINT, url=photo_node.attributes.get("src")
            )
        else:
            return None

    def _get_profile_info(self) -> dict:
        """Method to get profile info."""
        node = self._parser.css_first(_PORTAL_SELECTOR)
        enrollment = node.css_first("tr:nth-child(1) > td:nth-child(2)").text()
        course_summary = remove_newlines_and_tabs(
            node.css_first("tr:nth-child(2) > td:nth-child(2)").text()
        )
        course_level = node.css_first("tr:nth-child(3) > td:nth-child(2)").text()
        course_status = node.css_first("tr:nth-child(4) > td:nth-child(2)").text()
        course_joined_at = node.css_first("tr:nth-child(6) > td:nth-child(2)").text()

        return {
            "enrollment_id": int(enrollment),
            "course_summary": course_summary,
            "course_level": course_level,
            "course_status": course_status,
            "course_joined_at": convert_semester_to_date(course_joined_at),
        }

    def _get_additional_info(self) -> dict:
        """Method to get the additional info."""
        # TODO: Improve the dinamic way to get the additional info
        selector = f"{_PORTAL_SELECTOR} > {_ADDITIONAL_INFO_SELECTOR} > {_ADDITIONAL_INFO_TABLE_SELECTOR}"
        additional_info_node = self._parser.css_first(selector)
        if additional_info_node:
            # AcademicIndexes
            grades_table = self._parser.css_first(
                f"{selector} > tr:nth-child(9) > td > table > tbody"
            )
            mc = grades_table.css_first(
                "tr:nth-child(2) > td:nth-child(2) > div"
            ).text()
            ira = grades_table.css_first(
                "tr:nth-child(2) > td:nth-child(4) > div"
            ).text()
            iech = grades_table.css_first(
                "tr:nth-child(3) > td:nth-child(2) > div"
            ).text()
            iepl = grades_table.css_first(
                "tr:nth-child(3) > td:nth-child(4) > div"
            ).text()
            iea = grades_table.css_first(
                "tr:nth-child(4) > td:nth-child(2) > div"
            ).text()
            caa = grades_table.css_first(
                "tr:nth-child(4) > td:nth-child(4) > div"
            ).text()
            # Workload
            workload_table = self._parser.css_first(
                "tr:nth-child(10) > td > table > tbody"
            )
            mandatory_workload = workload_table.css_first(
                "tr:nth-child(1) > td:nth-child(2)"
            ).text()
            optional_workload = workload_table.css_first(
                "tr:nth-child(2) > td:nth-child(2)"
            ).text()
            total_workload = workload_table.css_first(
                "tr:nth-child(3) > td:nth-child(2)"
            ).text()
            paid_workload = clean_paid_workload_string(
                workload_table.css_first("tr:nth-child(5) > td").text()
            )
            # Init models
            academic_indexes = AcademicIndexes(
                mc=float(mc),
                ira=float(ira),
                iech=float(iech),
                iepl=float(iepl),
                iea=float(iea),
                caa=float(caa),
            )
            workload = Workload(
                mandatory=float(mandatory_workload),
                optional=float(optional_workload),
                total=float(total_workload),
                progress=float(paid_workload),
            )
            return {"academic_indexes": academic_indexes, "workload": workload}
        else:
            return None

    def get_profile(self) -> Profile:
        """Method to get the profile with additional info."""
        profile_name = self._get_profile_name()
        profile_photo = self._get_profile_photo()
        profile_info = self._get_profile_info()
        profile_additional_info = self._get_additional_info()
        return Profile(
            name=profile_name,
            photo=profile_photo,
            **profile_info,
            **profile_additional_info,
        )
