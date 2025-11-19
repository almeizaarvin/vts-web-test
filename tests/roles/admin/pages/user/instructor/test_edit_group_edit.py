import pytest
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from tests.helper.edit_group_helper import *

@pytest.mark.usefixtures("login_as_admin_fixture")
def test_edit_group_edit(login_as_admin_fixture):
    driver = login_as_admin_fixture
    wait = WebDriverWait(driver, 15)

    # ⚙️ Nama unik untuk skenario ini
    original_name = "Group_Edit_Inst_Nav"
    edited_name = "Group_Edit_Inst_Nav_EDITED"

    # --- STEP 1: NAVIGASI ---
    navigate_to_instructor_subpage(driver, wait) 

    # --- STEP 2: CORE ACTION ---
    # Panggil fungsi inti untuk melakukan ADD -> EDIT -> VERIFY -> CLEANUP
    perform_edit_group_and_verify(driver, wait, original_name, edited_name)