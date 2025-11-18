import pytest
import time
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC

from tests.helper.edit_group_helper import *


@pytest.mark.usefixtures("login_as_admin_fixture")
def test_reset_password_peserta(login_as_admin_fixture):
    driver = login_as_admin_fixture
    wait = WebDriverWait(driver, 15)

    # 1. Setup: Pastikan halaman userlist dan Cari row Peserta 6
    wait.until(lambda d: "userlist?pageId=0" in d.current_url)
    row = find_peserta_row(driver, wait)

    # 2. Klik See Details untuk membuka dialog
    open_user_details_dialog(driver, wait, row)
    
    # 3. Cari dan klik tombol "Reset Password"
    print("🔍 Mencari dan mengklik tombol 'Reset Password'…")
    reset_btn = wait.until(
        EC.presence_of_element_located((
            By.XPATH,
            "//button[text()='Reset Password']" 
        ))
    )
    safe_click(driver, reset_btn)
    print("🟩 Tombol Reset Password diklik")

    # 4 & 5. Cari input id="new-password" dan masukkan teks
    print("🔍 Mencari input 'new-password' dan memasukkan password…")
    new_password_input = wait.until(EC.presence_of_element_located((By.ID, "new-password")))
    new_password_input.send_keys("newpassword")
    print("🟩 Password 'newpassword' dimasukkan")

    # 6. Klik tombol Save (menggunakan locator XPath)
    print("🔍 Mencari dan mengklik tombol 'Save'…")
    save_btn = wait.until(
        EC.presence_of_element_located((
            By.XPATH,
            "//button[text()='Save']"
        ))
    )
    safe_click(driver, save_btn)
    print("🟩 Tombol Save diklik")

    # 7. Assert Success Toast
    wait_for_toast(wait)
    
    # Cleanup: Tutup dialog
    close_dialog(driver, wait)