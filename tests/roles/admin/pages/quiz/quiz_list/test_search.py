import pytest
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from tests.helper.general_helper import navigate_to_page_button, perform_search_and_verify

@pytest.mark.usefixtures("login_as_admin_fixture")
def test_search_user_instructor(login_as_admin_fixture):
    """
    Mencari user di subpage Instructor.
    """
    driver = login_as_admin_fixture
    wait = WebDriverWait(driver, 15)

    navigate_to_page_button(driver, wait, "Quiz")
    perform_search_and_verify(driver, wait, query_text="Esai")