import pytest
from selenium.webdriver.support.ui import WebDriverWait
from tests.helper.lesson_helper import perform_add_chapter

@pytest.mark.usefixtures("login_as_instructor_fixture")
def test_add_chapter(login_as_instructor_fixture):

    driver = login_as_instructor_fixture
    wait = WebDriverWait(driver, 15)

    CHAPTER_NAME = "Chapter Testing"
    MODULE_NAME = "Module Testing"

    result = perform_add_chapter(
        driver,
        wait,
        chapter_name=CHAPTER_NAME,
        module_name=MODULE_NAME
    )

    assert result is True, "❌ Failed to create lesson"