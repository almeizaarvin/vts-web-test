
import pytest
from selenium.webdriver.support.ui import WebDriverWait
from tests.helper.general_helper import navigate_to_page_button
from tests.helper.quiz_list_helper import delete_quiz_template_if_exists


@pytest.mark.usefixtures("login_as_instructor_fixture")
def test_delete_quiz(login_as_instructor_fixture):
    """
    Test case untuk menambah kuis baru dan memverifikasi.
    """
    driver = login_as_instructor_fixture
    wait = WebDriverWait(driver, 15)

    navigate_to_page_button(driver, wait, "Quiz")
    
    delete_quiz_template_if_exists(driver, wait, quiz_name="Template Kuis Baru")