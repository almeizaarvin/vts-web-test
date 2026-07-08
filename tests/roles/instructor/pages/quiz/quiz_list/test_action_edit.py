import pytest
from selenium.webdriver.support.ui import WebDriverWait

from tests.helper.edit_quiz_helper import (
    perform_edit_quiz_question_and_verify
)
from tests.helper.general_helper import navigate_to_page_button


@pytest.mark.usefixtures("login_as_instructor_fixture")
def test_edit_quiz(login_as_instructor_fixture):
    driver = login_as_instructor_fixture
    wait = WebDriverWait(driver, 15)

    # masuk dulu ke page Quiz
    navigate_to_page_button(driver, wait, "Quiz")

    perform_edit_quiz_question_and_verify(
        driver,
        wait,
        quiz_name="Pilihan Ganda",
        old_question="Pertanyaan 1 esai",
        new_question="Pertanyaan Edited"
    )

    print("QUIZ =", "Pilihan Ganda")
    print("OLD =", "Pertanyaan 1 esai")