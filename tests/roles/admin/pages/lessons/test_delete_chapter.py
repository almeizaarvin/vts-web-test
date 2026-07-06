import pytest
from selenium.webdriver.support.ui import WebDriverWait

from tests.helper.lesson_helper import perform_delete_chapter_and_restore


@pytest.mark.usefixtures("login_as_admin_fixture")
def test_delete_chapter(login_as_admin_fixture):

    driver = login_as_admin_fixture
    wait = WebDriverWait(driver, 15)

    perform_delete_chapter_and_restore(
        driver,
        wait,
        chapter_name="Chapter Testing",
        module_name="Module Testing"
    )