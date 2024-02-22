"""Module to represent Playwright utilities."""

from playwright.sync_api import Playwright, Browser, BrowserContext, Page, Route
from typing import Tuple

BLOCK_RESOURCE_TYPES = [
    "beacon",
    "csp_report",
    "font",
    "image",
    "imageset",
    "media",
    "object",
    "texttrack",
]


@staticmethod
def prepare_playwright(playwright: Playwright) -> Tuple[Browser, BrowserContext, Page]:
    """Run browser, context and page and return them in a dictionary."""
    browser = playwright.webkit.launch(headless=True)
    context = browser.new_context(viewport={"width": 1920, "height": 1080})
    page = browser.new_page()
    page.route("**/*", intercept_route)
    return browser, context, page


@staticmethod
def intercept_route(route: Route):
    """Intercept all requests and abort blocked ones."""
    if route.request.resource_type in BLOCK_RESOURCE_TYPES:
        return route.abort(error_code="aborted")
    return route.continue_()
