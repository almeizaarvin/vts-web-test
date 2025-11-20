import pytest
import time
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC

from tests.helper.edit_group_helper import *


@pytest.mark.usefixtures("login_as_admin_fixture")
def test_reset_password_instructor_nav(login_as_admin_fixture):
    driver = login_as_admin_fixture
    wait = WebDriverWait(driver, 15)

    # ⚙️ Asumsi: Ada user dengan nama "Instructor X" yang bisa direset
    username = "Instruktur 2" 
    password_baru = "instructorpass123"

    # Pindah ke subpage Instructor
    navigate_to_instructor_subpage(driver, wait) 

    # Panggil fungsi inti yang sudah modular
    perform_reset_password_and_verify(driver, wait, username, password_baru)