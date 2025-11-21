
import pytest
from selenium.webdriver.support.ui import WebDriverWait
from tests.helper.general_helper import navigate_to_page_button
from tests.helper.quiz_list_helper import perform_add_new_quiz_and_verify, perform_delete_quiz_and_verify


@pytest.mark.usefixtures("login_as_admin_fixture")
def test_delete_quiz(login_as_admin_fixture):
    """
    Test case untuk menambah kuis baru dan memverifikasi.
    """
    driver = login_as_admin_fixture
    wait = WebDriverWait(driver, 15)

    navigate_to_page_button(driver, wait, "Quiz")
    
    perform_delete_quiz_and_verify(driver, wait)