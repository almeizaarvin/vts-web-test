import pytest
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from tests.helper.edit_group_helper import *


@pytest.mark.usefixtures("login_as_admin_fixture")
def test_toggle_status_trainee(login_as_admin_fixture):
    """
    Menguji fungsionalitas toggle status untuk user Trainee (di halaman default).
    """
    driver = login_as_admin_fixture
    wait = WebDriverWait(driver, 15)
    
    # Prasyarat: Pastikan di halaman userlist
    wait.until(lambda d: "userlist?pageId=0" in d.current_url)

    # ACTION: Langsung panggil core action
    perform_toggle_status_and_verify(driver, wait, username="Peserta 6")