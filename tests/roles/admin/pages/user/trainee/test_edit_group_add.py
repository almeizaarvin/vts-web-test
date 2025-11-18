import pytest
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from tests.helper.edit_group_helper import *

@pytest.mark.usefixtures("login_as_admin_fixture")
def test_add_new_group(login_as_admin_fixture):
    driver = login_as_admin_fixture
    wait = WebDriverWait(driver, 15)
    group_name = "Group D"

    # Setup: Pastikan group yang akan ditambahkan tidak ada
    open_group_edit_dialog(driver, wait)
    delete_group_if_exists(driver, wait, group_name)
    
    # 1. Klik 'Add New Group' dan tunggu input muncul
    click_add_new_group(driver, wait)

    # 2. Isi Nama Group
    group_input = driver.find_element(By.NAME, "groupname")
    group_input.clear()
    group_input.send_keys(group_name)

    # 3. Simpan
    click_save_button(driver, wait)
    
    # 4. Verifikasi (tutup, buka, dan cek daftar)
    close_dialog(driver, wait)
    open_group_edit_dialog(driver, wait)

    assert group_name in get_group_names(driver, wait), f"❌ '{group_name}' tidak ditemukan setelah ditambahkan!"
    print(f"✅ '{group_name}' berhasil ditambahkan.")

    # Cleanup: Tutup dialog
    close_dialog(driver, wait)