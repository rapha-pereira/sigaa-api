"""."""

from playwright.sync_api import sync_playwright
from playwright.sync_api import Page
from src.sigaa_api.models.portal.core import StudentPortal
from selectolax.lexbor import LexborHTMLParser, LexborNode
import re


def remove_newlines_and_tabs(input_string: str) -> str:
    cleaned_string = re.sub(r"[\n\t]", "", input_string)
    return cleaned_string


# block pages by resource type. e.g. image, stylesheet
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


def intercept_route(route):
    """intercept all requests and abort blocked ones"""
    if route.request.resource_type in BLOCK_RESOURCE_TYPES:
        return route.abort()
    return route.continue_()


def main():
    with sync_playwright() as p:
        browser = p.webkit.launch(headless=True)
        context = browser.new_context(viewport={"width": 1920, "height": 1080})
        page: Page = context.new_page()
        # enable intercepting for this page, **/* stands for all requests
        page.route("**/*", intercept_route)

        # Login
        portal = StudentPortal(page=page)
        login = portal.login()

        if login:
            print("Login successful.")
            classes_portal = portal.get_classes_portal()

            # Get classes main div
            print("Div:")
            print(classes_portal.div)

            # Get the classes table header
            header = classes_portal.get_normalized_header()
            print("Header:")
            print(header)

            page_c = page.content()

            nodes = LexborHTMLParser(page_c).css(
                "#turmas-portal > table:nth-child(3) > tbody > tr"
            )
            for node in nodes if nodes else []:

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
                    class_name = name_selector.text()

                if local_schedule_selector:
                    class_local_and_schedule = [
                        _handle_td_info(td)
                        for td in local_schedule_selector
                        if td and local_schedule_selector
                    ]

                if class_name:
                    print("---- Class Name ----")
                    print(class_name)
                if class_local_and_schedule:
                    print("---- Class local & schedule ----")
                    print(class_local_and_schedule)

            browser.close()


def test():
    x = StudentPortal()
    classes_p = x.get_classes_portal()
    header = classes_p.get_classes_header()
    body = classes_p.get_classes_body()
    classes = classes_p.get_classes()
    print("Header:")
    print(header)
    print("Body:")
    print(body)
    print("Classes:")
    print(classes)

test()
