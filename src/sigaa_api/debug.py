"""."""

from playwright.sync_api import sync_playwright
from src.sigaa_api.models import StudentPortal


def main():
    with sync_playwright() as p:
        browser = p.webkit.launch(headless=False)
        page = browser.new_page()
        page.goto("https://sig.ifsc.edu.br/sigaa/verTelaLogin.do")

        # Fill "name=user.name" and "name=user.senha" inputs
        page.locator(selector="input[name='user.login']").fill(value="raphael.pg")
        page.locator(selector="input[name='user.senha']").fill(value="30201510rR?")

        # Click on button to submit form
        page.locator(
            selector='//*[@id="loginForm"]/table/tfoot/tr[2]/td/button'
        ).click()

        portal = StudentPortal(page=page)
        classes_portal = portal.get_classes_portal()
        print(classes_portal.div)

        # Get the classes table header
        header = classes_portal.get_header()
        print(header)

        # Get the classes table body
        body = classes_portal.get_body_raw_texts()
        print(body)

        # Get the classes table content
        content = classes_portal.get_classes_content()
        print(content)


main()
test = 2
