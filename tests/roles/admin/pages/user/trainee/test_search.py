import pytest
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from tests.helper.edit_group_helper import *
from tests.helper.general_helper import perform_search_and_verify

@pytest.mark.usefixtures("login_as_admin_fixture")
def test_search_user_trainee(login_as_admin_fixture):
    """
    Mencari user di halaman default (Trainee).
    """
    driver = login_as_admin_fixture
    wait = WebDriverWait(driver, 15)
    
    # Prasyarat: Pastikan halaman sudah dimuat (userlist)
    wait.until(lambda d: "userlist?pageId=0" in d.current_url)

    # ACTION: Langsung panggil core action
    perform_search_and_verify(driver, wait, query_text="Trainee")