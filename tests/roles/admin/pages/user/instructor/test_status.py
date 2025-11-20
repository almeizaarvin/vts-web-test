import pytest
from selenium.webdriver.support.ui import WebDriverWait
from tests.helper.edit_group_helper import navigate_to_instructor_subpage, perform_toggle_status_and_verify 


@pytest.mark.usefixtures("login_as_admin_fixture")
def test_toggle_status_instructor(login_as_admin_fixture):
    """
    Menguji fungsionalitas toggle status untuk user Instructor (setelah navigasi).
    """
    driver = login_as_admin_fixture
    wait = WebDriverWait(driver, 15)

    navigate_to_instructor_subpage(driver, wait)

    perform_toggle_status_and_verify(driver, wait, username="Instruktur 1")