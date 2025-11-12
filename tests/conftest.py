import os
import pytest
import base64
from datetime import datetime
from selenium.webdriver.support.ui import WebDriverWait
from .helper.browser_setup import create_driver
from .helper.login_helper import login_as_admin

@pytest.fixture(scope="session")
def driver():
    """Setup WebDriver Chrome """
    driver = create_driver()
    yield driver
    driver.quit()


@pytest.fixture(scope="function")
def login_as_admin_fixture(driver):
    """Login sebelum test"""
    login_as_admin(driver)
    return driver


# ---------------------------------------------------------------------------
# ---------------------------------------------------------------------------
@pytest.hookimpl(hookwrapper=True)
def pytest_runtest_makereport(item, call):
    """Hook untuk menambahkan screenshot ke report HTML pytest"""
    outcome = yield
    rep = outcome.get_result()

    if rep.when == "call":
        driver = item.funcargs.get("login_as_admin_fixture") or item.funcargs.get("driver")
        if driver:
            screenshot_dir = "screenshots"
            os.makedirs(screenshot_dir, exist_ok=True)

            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            filename = f"{item.name}_{timestamp}.png"
            path = os.path.join(screenshot_dir, filename)

            driver.save_screenshot(path)

            with open(path, "rb") as image_file:
                encoded = base64.b64encode(image_file.read()).decode()

            pytest_html = item.config.pluginmanager.getplugin("html")
            extra = getattr(rep, "extra", [])
            extra.append(pytest_html.extras.html(
                f'<div><b>Screenshot:</b><br>'
                f'<img src="data:image/png;base64,{encoded}" '
                f'style="width:600px;border:1px solid #ccc;border-radius:8px;"/></div>'
            ))
            rep.extra = extra
