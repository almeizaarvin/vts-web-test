import pytest
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from tests.helper.edit_group_helper import *

@pytest.mark.usefixtures("login_as_admin_fixture")
def test_search_user_instructor(login_as_admin_fixture):
    """
    Mencari user di subpage Instructor.
    """
    driver = login_as_admin_fixture
    wait = WebDriverWait(driver, 15)

    navigate_to_instructor_subpage(driver, wait)

    perform_search_and_verify(driver, wait, query_text="Instructor")