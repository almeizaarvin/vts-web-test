import pytest
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from .edit_group_helper import *

@pytest.mark.usefixtures("login_as_admin")
def test_add_new_group(login_as_admin):
    """
    Skenario: Tambah Group Baru (Group D)
    """
    driver = login_as_admin
    wait = WebDriverWait(driver, 15)
    group_name = "Group D"

    # --- Buka dialog & bersihkan jika ada ---
    open_edit_dialog(driver, wait)
    delete_group_if_exists(driver, wait, group_name)

    # --- Tambah baru ---
    print("➕ Klik tombol 'Add New Group'...")
    add_btn = wait.until(EC.element_to_be_clickable((By.XPATH, "//button[contains(., 'Add New Group')]")))
    safe_click(driver, add_btn)

    group_input = wait.until(EC.presence_of_element_located((By.NAME, "groupname")))
    group_input.clear()
    group_input.send_keys(group_name)

    save_icon = wait.until(EC.presence_of_element_located((By.XPATH, "//*[@aria-label='Simpan']")))
    parent = save_icon.find_element(By.XPATH, "./ancestor::*[self::button or self::div][1]")
    driver.execute_script("arguments[0].click();", parent)
    print("💾 Tombol Simpan diklik, menunggu dialog stabil...")

    close_dialog(driver, wait)
    open_edit_dialog(driver, wait)

    group_names = get_group_names(driver, wait)
    print(f"📋 Daftar group terbaru: {group_names}")
    assert group_name in group_names, f"❌ '{group_name}' tidak ditemukan setelah tambah baru!"
    print(f"✅ '{group_name}' berhasil ditambahkan dan terverifikasi.")
