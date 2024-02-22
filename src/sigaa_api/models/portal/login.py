"""Module to represent the SIGAA portal login."""

from src.settings import BASE_URL, LOGIN_URL

from dataclasses import dataclass, field
from typing import Tuple

from playwright.sync_api import Page
from getpass import getpass


@dataclass(init=True, frozen=True, slots=True)
class StudentPortalLogin:
    """
    A class that represents the SIGAA login page.
    https://sig.ifsc.edu.br/sigaa/
    """

    page: Page

    _input_username_selector: str = field(
        default="#loginForm > table > tbody > tr:nth-child(1) > td > input[type=text]",
        init=False,
    )
    _input_password_selector: str = field(
        default="#loginForm > table > tbody > tr:nth-child(2) > td > input[type=password]",
        init=False,
    )
    _form_button_selector: str = field(
        default="#loginForm > table > tfoot > tr:nth-child(2) > td > button",
        init=False,
    )

    def login(self) -> bool:
        """Method to login into the SIGAA portal."""
        # Go to login page
        self.page.goto(f"{BASE_URL}/{LOGIN_URL}")

        # Get the user credentials
        username, password = self._get_user_credentials()

        # Fill the username and password inputs
        self.page.locator(selector=self._input_username_selector).fill(value=username)
        self.page.locator(selector=self._input_password_selector).fill(value=password)

        # Delete the user credentials from memory
        del username, password

        # Click on the button to submit the form
        self.page.locator(selector=self._form_button_selector).click()

        # Wait until the page loads
        try:
            resolver = self.page.wait_for_selector("#turmas-portal")
            if resolver:
                return True
        except Exception:
            return False

    def _get_user_credentials(self) -> Tuple[str, str]:
        """Method to get the user credentials."""
        print("Enter your SIGAA credentials.")
        username = input("Username: ")
        password = getpass("Password: ")
        return username, password
