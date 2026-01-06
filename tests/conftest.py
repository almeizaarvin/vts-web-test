import os
import pytest
import pytest_html
import base64
from datetime import datetime
from selenium.webdriver.support.ui import WebDriverWait
from .helper.browser_setup import create_driver
from .helper.login_helper import *

@pytest.fixture(scope="session")
def driver():
    """Setup WebDriver Chrome """
    driver = create_driver()
    yield driver
    driver.quit()

@pytest.fixture(scope="function")
def login_as_admin_fixture(driver):
    """Fixture untuk login sebagai Admin sebelum setiap test"""
    login_as_admin(driver)
    return driver

@pytest.fixture(scope="function")
def login_as_instructor_fixture(driver):
    """Fixture BARU untuk login sebagai Instructor sebelum setiap test"""
    login_as_instructor(driver)
    return driver

# ---------------------------------------------------------------------------
# ---------------------------------------------------------------------------
@pytest.hookimpl(hookwrapper=True)
def pytest_runtest_makereport(item, call):
    outcome = yield
    rep = outcome.get_result()

    if rep.when == "call" and rep.failed:
        driver = (
            item.funcargs.get("login_as_admin_fixture")
            or item.funcargs.get("login_as_instructor_fixture")
            or item.funcargs.get("driver")
        )

        if not driver:
            return

        screenshot = driver.get_screenshot_as_png()
        encoded = base64.b64encode(screenshot).decode()

        extra = getattr(rep, "extra", [])
        extra.append(
            pytest_html.extras.html(
                f"""
                <div style="margin-top:10px">
                    <b>📸 Screenshot on Failure</b><br>
                    <img src="data:image/png;base64,{encoded}"
                         style="width:700px;border:1px solid #ccc;border-radius:6px"/>
                </div>
                """
            )
        )
        rep.extra = extra
