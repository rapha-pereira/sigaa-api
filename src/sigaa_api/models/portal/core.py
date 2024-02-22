"""Module to represent the SIGAA portal core."""

from src.sigaa_api.models.portal.login import StudentPortalLogin
from src.sigaa_api.models.modules.classes import Classes
from src.sigaa_api.models.exceptions import LoginFailed
from src.sigaa_api.utils.playwright_utils import prepare_playwright

from selectolax.lexbor import LexborHTMLParser
from playwright.sync_api import sync_playwright


class StudentPortal:
    """
    A class that represents the SIGAA main page.
    https://sig.ifsc.edu.br/sigaa/portais/discente/
    """

    def __init__(self) -> None:
        with sync_playwright() as playwright:
            self.browser, self.context, self.page = prepare_playwright(playwright)

            # Login user into the portal
            if not self._login():
                self.context.close()
                self.browser.close()
                raise LoginFailed()
            else:
                # Get the HTML parser and close playwright
                self.parser = LexborHTMLParser(self.page.content())
                self.context.close()
                self.browser.close()

    def _login(self) -> bool:
        """Method to login into the SIGAA portal."""
        return StudentPortalLogin(page=self.page).login()

    def get_classes_portal(self) -> Classes:
        return Classes(parser=self.parser)

    # def get_profile_portal(self) -> Profile:
    #     return Profile(page=self.page)
