import pytest
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from tests.helper.edit_group_helper import *

@pytest.mark.usefixtures("login_as_instructor_fixture")
def test_edit_group_edit(login_as_instructor_fixture):
    driver = login_as_instructor_fixture
    wait = WebDriverWait(driver, 15)
    original_name = "Group_Edit_Test"
    edited_name = "Group_Edit_Test_Updated"
    
    # 1. SETUP: Pastikan group yang akan diedit ada
    create_group_for_edit(driver, wait, original_name)
    
    # 2. CORE ACTION: Lakukan Edit dan Verifikasi
    perform_edit_group_and_verify(driver, wait, original_name, edited_name)