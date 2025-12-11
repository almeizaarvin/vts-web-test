# --- File: test_add_quiz.py ---

import pytest
from selenium.webdriver.support.ui import WebDriverWait

# Asumsi: navigate_to_page_button ada di tests.helper.general_helper
from tests.helper.general_helper import navigate_to_page_button
from tests.helper.quiz_list_helper import perform_add_new_quiz_and_delete_question
# Asumsi: perform_add_new_quiz_and_verify ada di tests.helper.quiz_helper


@pytest.mark.usefixtures("login_as_instructor_fixture")
def test_add_new_quiz_delete_question(login_as_instructor_fixture):
    """
    Test case untuk menambah kuis baru dan memverifikasi.
    """
    driver = login_as_instructor_fixture
    wait = WebDriverWait(driver, 15)

    navigate_to_page_button(driver, wait, "Quiz")
    
    perform_add_new_quiz_and_delete_question(driver, wait)