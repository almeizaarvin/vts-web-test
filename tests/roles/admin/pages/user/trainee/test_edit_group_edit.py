import pytest
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from tests.helper.edit_group_helper import *

@pytest.mark.usefixtures("login_as_admin_fixture")
def test_edit_group(login_as_admin_fixture):
    driver = login_as_admin_fixture
    wait = WebDriverWait(driver, 15)

    original_name = "Group D"
    edited_name = "Group D Edited"

    # --- Step 1: Pastikan group ada (add dulu jika belum)
    open_edit_dialog(driver, wait)
    delete_group_if_exists(driver, wait, original_name)
    delete_group_if_exists(driver, wait, edited_name) 

    print("➕ Menambahkan group baru untuk diedit...")
    add_btn = wait.until(EC.element_to_be_clickable((By.XPATH, "//button[contains(., 'Add New Group')]")))
    safe_click(driver, add_btn)

    group_input = wait.until(EC.presence_of_element_located((By.NAME, "groupname")))
    group_input.clear()
    group_input.send_keys(original_name)

    save_icon = wait.until(EC.presence_of_element_located((By.XPATH, "//*[@aria-label='Simpan']")))
    parent = save_icon.find_element(By.XPATH, "./ancestor::*[self::button or self::div][1]")
    driver.execute_script("arguments[0].click();", parent)

    # tutup dan buka ulang dialog
    close_dialog(driver, wait)
    open_edit_dialog(driver, wait)

    # pastikan group muncul
    names = get_group_names(driver, wait)
    assert original_name in names, f"❌ '{original_name}' tidak ditemukan setelah add."

    # --- Step 2: Klik icon Edit (pensil)
    print(f"✏️ Mengedit '{original_name}' menjadi '{edited_name}'...")
    edit_btn = wait.until(EC.element_to_be_clickable((
        By.XPATH,
        f"//div[normalize-space(text())='{original_name}']/following::button[.//*[@data-testid='EditIcon']][1]"
    )))
    driver.execute_script("arguments[0].click();", edit_btn)

    # --- Step 3: Edit nama di input field
    input_field = wait.until(EC.presence_of_element_located((By.NAME, "groupname")))
    input_field.clear()
    input_field.send_keys(edited_name)

    # Klik ikon checklist (aria-label='Simpan')
    check_icon = wait.until(EC.presence_of_element_located((By.XPATH, "//*[@aria-label='Simpan']")))
    parent_check = check_icon.find_element(By.XPATH, "./ancestor::*[self::button or self::div][1]")
    driver.execute_script("arguments[0].click();", parent_check)

    # --- Step 4: Verifikasi perubahan
    close_dialog(driver, wait)
    open_edit_dialog(driver, wait)

    names_after = get_group_names(driver, wait)
    assert edited_name in names_after, f"❌ '{edited_name}' tidak ditemukan setelah edit!"
    assert original_name not in names_after, f"❌ '{original_name}' masih muncul setelah edit!"

    print(f"✅ Group '{original_name}' berhasil diubah menjadi '{edited_name}'.")
