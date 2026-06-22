import pytest
from selenium.webdriver.support.ui import WebDriverWait
from tests.helper.assignments_helper import perform_edit_course


@pytest.mark.usefixtures("login_as_admin_fixture")
def test_edit_course(login_as_admin_fixture):

    driver = login_as_admin_fixture
    wait = WebDriverWait(driver, 15)

    OLD_COURSE_NAME = "Course Testing"
    NEW_COURSE_NAME = "Course Testing Edited"

    result = perform_edit_course(
        driver,
        wait,
        old_course_name=OLD_COURSE_NAME,
        new_course_name=NEW_COURSE_NAME
    )

    assert result is True, "Failed to edit course"