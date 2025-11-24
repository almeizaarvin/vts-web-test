from concurrent.futures import wait
import pytest
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from tests.helper.general_helper import find_row_by_name
from tests.helper.quiz_list_helper import navigate_to_page_button, quiz_submission_navigate_and_verify

@pytest.mark.usefixtures("login_as_admin_fixture")
def test_action_quiz_submission(login_as_admin_fixture):
    """
    1. Mencari row kuis 'Auxiliary Console'.
    2. Mengklik tombol dengan ikon ChecklistRtlIcon di dalam row tersebut.
    3. Memverifikasi header (H1) di halaman tujuan.
    """
    driver = login_as_admin_fixture
    wait = WebDriverWait(driver, 15)
    
    navigate_to_page_button(driver, wait, "Quiz")

    quiz_submission_navigate_and_verify(driver, wait, quiz_name="Auxiliary Console")


