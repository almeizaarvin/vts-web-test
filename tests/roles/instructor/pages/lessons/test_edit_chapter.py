import pytest
from selenium.webdriver.support.ui import WebDriverWait
from tests.helper.lesson_helper import perform_edit_chapter


@pytest.mark.usefixtures("login_as_instructor_fixture")
def test_edit_chapter(login_as_instructor_fixture):

    driver = login_as_instructor_fixture
    wait = WebDriverWait(driver, 15)

    result = perform_edit_chapter(
        driver,
        wait,
        original_name="Chapter Testing",
        edited_name="Chapter Testing Edited"
    )

    assert result is True