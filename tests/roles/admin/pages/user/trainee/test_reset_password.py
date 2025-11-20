import pytest
import time
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC

from tests.helper.edit_group_helper import *


@pytest.mark.usefixtures("login_as_admin_fixture")
def test_reset_password(login_as_admin_fixture):
    """
    Menguji fungsionalitas reset password untuk user Trainee 
    (yang berada di halaman default setelah login).
    """
    driver = login_as_admin_fixture
    wait = WebDriverWait(driver, 15)

    # ⚙️ Data User Trainee
    username = "Peserta 6"  # Asumsi ini adalah Trainee/Peserta
    password_baru = "traineepass456"

    # --- ACTION ---
    # Karena ini halaman default (Trainee), kita langsung panggil core action.
    # Tidak perlu memanggil navigate_to_instructor_subpage.
    perform_reset_password_and_verify(driver, wait, username, password_baru)