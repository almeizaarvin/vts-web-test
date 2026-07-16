"""
Helper functions for VTS UI Test - Group and User Management.
Contains functions for group CRUD, user status toggle, and dialog interactions.
"""

import time
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException, StaleElementReferenceException

from tests.helper.general_helper import find_row_by_name, safe_click, wait_for_toast


# ============================================================================
# SECTION 1: DIALOG HELPERS
# ============================================================================

def close_dialog(driver, wait):
    """
    Close the current dialog using the 'CloseIcon'.

    Args:
        driver: WebDriver instance
        wait: WebDriverWait instance
    """
    print("🟥 Menutup dialog...")
    try:
        close_icon = wait.until(EC.presence_of_element_located((By.XPATH, "//*[@data-testid='CloseIcon']")))
        parent_btn = close_icon.find_element(By.XPATH, "./ancestor::button[1]")
        safe_click(driver, parent_btn)
        wait.until(EC.invisibility_of_element_located((By.CLASS_NAME, "MuiDialogContent-root")))
        print("✅ Dialog berhasil tertutup.")
    except Exception as e:
        print(f"⚠️ Gagal menutup dialog: {e}")


def select_current_date_in_dialog(driver, wait):
    """
    Click the date input, select today's date (aria-current='date'),
    and click the 'OK' button in the calendar dialog.

    Args:
        driver: WebDriver instance
        wait: WebDriverWait instance
    """
    print("🗓️ Memilih tanggal lahir (hari ini)...")
    birth_date_input = wait.until(EC.presence_of_element_located((By.NAME, "birthDate")))
    safe_click(driver, birth_date_input)

    try:
        current_date_btn = wait.until(
            EC.element_to_be_clickable((By.CSS_SELECTOR, "button[aria-current='date']"))
        )
        safe_click(driver, current_date_btn)
    except TimeoutException:
        print("⚠️ Gagal menemukan tombol tanggal hari ini. Melanjutkan...")

    ok_btn = wait.until(EC.element_to_be_clickable((By.XPATH, "//button[text()='OK']")))
    safe_click(driver, ok_btn)
    print("✅ Tanggal dan 'OK' berhasil diklik.")


def select_mui_dropdown_option(driver, wait, input_name, option_text):
    """
    Handle MUI dropdown with Scroll-to-View and JS Force Click.

    Args:
        driver: WebDriver instance
        wait: WebDriverWait instance
        input_name: Label name of the dropdown (e.g., 'Gender')
        option_text: Text of the option to select

    Raises:
        RuntimeError: If dropdown cannot be opened or option selected
    """
    print(f"🔄 Memilih opsi '{option_text}' untuk input '{input_name}'...")

    # STEP 1: Scroll to trigger and click
    try:
        select_trigger = wait.until(
            EC.element_to_be_clickable((
                By.XPATH,
                f"//label[text()='{input_name}']/following-sibling::div//div[@role='combobox']"
            )),
            timeout=5
        )
        driver.execute_script("arguments[0].scrollIntoView({block: 'center'});", select_trigger)
        time.sleep(0.5)
        safe_click(driver, select_trigger)
        print(f"   -> Trigger dropdown '{input_name}' diklik.")
    except TimeoutException:
        raise RuntimeError(f"Gagal membuka menu dropdown {input_name}.")

    # STEP 2: Wait for popup, scroll to option, and click with JS
    option_locator = f'//ul[@role="listbox"]//li[@role="option" and normalize-space()="{option_text}"]'
    listbox_locator = By.XPATH, '//ul[@role="listbox"]'

    try:
        wait.until(EC.presence_of_element_located(listbox_locator))
        option_element = wait.until(
            EC.presence_of_element_located((By.XPATH, option_locator)),
            f"❌ Opsi '{option_text}' tidak ditemukan."
        )
        driver.execute_script("arguments[0].scrollIntoView({block: 'nearest'});", option_element)
        time.sleep(0.3)
        driver.execute_script("arguments[0].click();", option_element)
        print(f"   -> Opsi '{option_text}' berhasil diklik.")
        wait.until(EC.invisibility_of_element_located(listbox_locator))
        print("✅ Dropdown berhasil ditutup.")
    except (TimeoutException, StaleElementReferenceException) as e:
        raise RuntimeError("Gagal memilih opsi dropdown.")


# ============================================================================
# SECTION 2: GROUP HELPERS
# ============================================================================

def open_edit_dialog(driver, wait):
    """Open the 'Edit Group List' dialog."""
    print("🟦 Membuka Edit Group List...")
    edit_btn = wait.until(
        EC.element_to_be_clickable((By.XPATH, "//button[.//span[contains(text(), 'Edit Group List')]]"))
    )
    safe_click(driver, edit_btn)
    wait.until(EC.presence_of_element_located((By.CLASS_NAME, "MuiDialogContent-root")))
    print("✅ Dialog Edit Group List terbuka.")


def open_group_edit_dialog(driver, wait):
    """Open the 'Edit Group List' dialog (alias for open_edit_dialog)."""
    return open_edit_dialog(driver, wait)


def get_group_names(driver, wait):
    """
    Get all group names displayed in the dialog.

    Args:
        driver: WebDriver instance
        wait: WebDriverWait instance

    Returns:
        list: List of group name strings
    """
    dialog = wait.until(EC.presence_of_element_located((By.CLASS_NAME, "MuiDialogContent-root")))
    divs = dialog.find_elements(By.TAG_NAME, "div")
    names = []
    for d in divs:
        text = d.text.strip()
        if text and not d.find_elements(By.TAG_NAME, 'button'):
            names.append(text)
    return names


def click_add_new_group(driver, wait):
    """Click the 'Add New Group' button and wait for input to appear."""
    print("➕ Klik tombol 'Add New Group'...")
    add_btn = wait.until(EC.element_to_be_clickable((By.XPATH, "//button[contains(., 'Add New Group')]")))
    safe_click(driver, add_btn)
    wait.until(EC.presence_of_element_located((By.NAME, "groupname")))
    print("✅ Input group name muncul.")


def click_save_button(driver, wait):
    """Click the 'Simpan' button (with aria-label='Simpan')."""
    print("💾 Klik tombol Simpan...")
    save_icon = wait.until(EC.presence_of_element_located((By.XPATH, "//*[@aria-label='Simpan']")))
    parent_btn = save_icon.find_element(By.XPATH, "./ancestor::*[self::button or self::div][1]")
    safe_click(driver, parent_btn)
    print("✅ Tombol Simpan diklik.")


def delete_group_if_exists(driver, wait, group_name):
    """
    Delete a group if it already exists in the list.

    Args:
        driver: WebDriver instance
        wait: WebDriverWait instance
        group_name: Name of the group to delete

    Returns:
        bool: True if group was deleted, False if it didn't exist
    """
    print(f"🕵️ Mengecek apakah '{group_name}' sudah ada...")
    names = get_group_names(driver, wait)

    if group_name not in names:
        print(f"✅ '{group_name}' belum ada, tidak perlu dihapus.")
        return False

    print(f"⚠️ '{group_name}' ditemukan, proses hapus...")
    delete_btn = wait.until(EC.element_to_be_clickable((
        By.XPATH,
        f"//div[normalize-space(text())='{group_name}']/following::button[.//*[@data-testid='DeleteIcon']][1]"
    )))
    driver.execute_script("arguments[0].click();", delete_btn)

    confirm_btn = wait.until(
        EC.element_to_be_clickable((By.XPATH, "//*[name()='svg' and @aria-label='Ya']/ancestor::button[1]"))
    )
    driver.execute_script("arguments[0].click();", confirm_btn)

    wait.until_not(EC.text_to_be_present_in_element((By.CLASS_NAME, "MuiDialogContent-root"), group_name))
    print(f"✅ '{group_name}' berhasil dihapus.")
    return True


def click_edit_group_button(driver, row):
    """
    From the found row, click the button with svg aria-label 'Ubah Kelompok'.

    Args:
        driver: WebDriver instance
        row: WebElement row containing the edit button
    """
    edit_btn = row.find_element(
        By.XPATH,
        ".//button[.//svg[@aria-label='Ubah Kelompok']]"
    )
    driver.execute_script("arguments[0].click();", edit_btn)


def open_group_edit_dropdown(driver, wait):
    """
    Find the 'edit-group-form' popup and open the dropdown (listbox button).

    Args:
        driver: WebDriver instance
        wait: WebDriverWait instance
    """
    form = wait.until(EC.presence_of_element_located((By.ID, "edit-group-form")))
    dropdown_btn = form.find_element(By.XPATH, ".//div[@aria-haspopup='listbox']")
    driver.execute_script("arguments[0].click();", dropdown_btn)


# ============================================================================
# SECTION 3: USER HELPERS
# ============================================================================

def open_user_details_dialog(driver, wait, row):
    """
    From the found row, click the 'See Details' button to open the dialog.

    Args:
        driver: WebDriver instance
        wait: WebDriverWait instance
        row: WebElement row containing the See Details button
    """
    print("🔍 Mencari dan mengklik tombol See Details…")
    details_btn = row.find_element(By.CSS_SELECTOR, "button[aria-label='See Details']")
    safe_click(driver, details_btn)
    print("✅ Dialog detail Peserta terbuka.")


def get_status_button(row):
    """
    Find the 'Active' or 'Inactive' button within a row.

    Args:
        row: WebElement row containing the status button

    Returns:
        WebElement: The status button (Active/Inactive)

    Raises:
        Exception: If status button is not found
    """
    buttons = row.find_elements(By.TAG_NAME, "button")
    for btn in buttons:
        txt = btn.text.strip()
        if txt in ("Active", "Inactive"):
            return btn
    raise Exception("❌ Tidak menemukan tombol Active/Inactive pada row.")


def click_status_action(driver, wait, current_status):
    """
    Click the action button (Activate/Deactivate) in the confirmation popup.

    Args:
        driver: WebDriver instance
        wait: WebDriverWait instance
        current_status: Current status ('Active' or 'Inactive')

    Returns:
        str: Target status after the action
    """
    target_status = "Inactive" if current_status == "Active" else "Active"
    action_button_label = "Deactivate" if current_status == "Active" else "Activate"

    print(f"🎯 Target: {target_status} (aksi: {action_button_label})")

    action_btn = wait.until(
        EC.element_to_be_clickable((By.XPATH, f"//button[normalize-space()='{action_button_label}']"))
    )
    safe_click(driver, action_btn)
    print(f"✅ Tombol {action_button_label} diklik.")

    return target_status


# ============================================================================
# SECTION 4: NAVIGATION HELPERS
# ============================================================================

def navigate_to_instructor_subpage(driver, wait):
    """
    Navigate from the main 'userlist' page to the Instructor subpage.

    Args:
        driver: WebDriver instance
        wait: WebDriverWait instance

    Raises:
        RuntimeError: If navigation fails
    """
    print("➡️ Navigasi ke Subpage Instructor...")
    instructor_tab_locator = (By.XPATH, "//button[contains(text(), 'Instructor')]")

    try:
        instructor_tab = wait.until(EC.element_to_be_clickable(instructor_tab_locator))
        driver.execute_script("arguments[0].scrollIntoView(true);", instructor_tab)
        instructor_tab.click()
        print("✅ Berhasil pindah ke subpage Instructor.")
    except TimeoutException:
        raise RuntimeError("Gagal navigasi ke subpage Instructor.")
    except Exception as e:
        print(f"⚠️ Error saat klik Instructor tab: {e}")
        raise


# ============================================================================
# SECTION 5: GROUP ACTION HELPERS
# ============================================================================

def perform_add_group_and_verify(driver, wait, group_name):
    """
    Core function: Setup, Add Group, Save, and Verification.

    Args:
        driver: WebDriver instance
        wait: WebDriverWait instance
        group_name: Name of the group to add

    Raises:
        AssertionError: If group is not found after adding
    """
    print(f"\n{'='*60}")
    print(f"🎯 Memulai: Menambahkan Group '{group_name}'")
    print(f"{'='*60}")

    open_edit_dialog(driver, wait)
    delete_group_if_exists(driver, wait, group_name)

    click_add_new_group(driver, wait)

    print(f"✍️ Mengisi nama group: '{group_name}'...")
    group_input = driver.find_element(By.NAME, "groupname")
    group_input.clear()
    group_input.send_keys(group_name)

    click_save_button(driver, wait)

    close_dialog(driver, wait)
    open_edit_dialog(driver, wait)

    names = get_group_names(driver, wait)
    assert group_name in names, f"❌ '{group_name}' tidak ditemukan setelah ditambahkan!"
    print(f"✅ '{group_name}' berhasil ditambahkan dan diverifikasi.")

    close_dialog(driver, wait)
    print(f"{'='*60}\n")


def perform_edit_group_and_verify(driver, wait, original_name, edited_name):
    """
    Core function: Setup (Add), Edit, Save, and Verification.

    Args:
        driver: WebDriver instance
        wait: WebDriverWait instance
        original_name: Original group name
        edited_name: Edited group name

    Raises:
        AssertionError: If verification fails
    """
    print(f"\n{'='*60}")
    print(f"🎯 Memulai: Mengedit Group '{original_name}' → '{edited_name}'")
    print(f"{'='*60}")

    # SETUP: Ensure group doesn't exist
    open_edit_dialog(driver, wait)
    delete_group_if_exists(driver, wait, original_name)
    delete_group_if_exists(driver, wait, edited_name)

    # Add original group
    print(f"➕ Menambahkan group '{original_name}' untuk diedit...")
    click_add_new_group(driver, wait)
    group_input = driver.find_element(By.NAME, "groupname")
    group_input.send_keys(original_name)
    click_save_button(driver, wait)

    close_dialog(driver, wait)
    open_edit_dialog(driver, wait)

    names = get_group_names(driver, wait)
    assert original_name in names, f"❌ '{original_name}' tidak ditemukan setelah add."
    print(f"✅ Group '{original_name}' berhasil ditambahkan.")

    # Click edit icon
    print(f"✏️ Mengedit '{original_name}'...")
    edit_btn_locator = (
        By.XPATH,
        f"//div[normalize-space(text())='{original_name}']/following::button[.//*[@data-testid='EditIcon']][1]"
    )
    edit_btn = wait.until(EC.element_to_be_clickable(edit_btn_locator))
    safe_click(driver, edit_btn)

    # Edit name
    print(f"✍️ Mengubah nama menjadi: '{edited_name}'...")
    input_field = wait.until(EC.presence_of_element_located((By.NAME, "groupname")))
    input_field.clear()
    input_field.send_keys(edited_name)

    click_save_button(driver, wait)

    close_dialog(driver, wait)
    open_edit_dialog(driver, wait)

    names_after = get_group_names(driver, wait)

    assert edited_name in names_after, f"❌ '{edited_name}' tidak ditemukan setelah edit!"
    assert original_name not in names_after, f"❌ '{original_name}' masih muncul setelah edit!"

    print(f"✅ Group berhasil diubah dari '{original_name}' menjadi '{edited_name}'.")

    delete_group_if_exists(driver, wait, edited_name)
    close_dialog(driver, wait)
    print(f"{'='*60}\n")


def create_group_for_edit(driver, wait, group_name):
    """
    Setup: Add a new group for edit test preparation.

    Args:
        driver: WebDriver instance
        wait: WebDriverWait instance
        group_name: Name of the group to prepare

    Raises:
        AssertionError: If setup fails
    """
    print(f"\n{'='*60}")
    print(f"🔧 SETUP: Menyiapkan '{group_name}' untuk diedit")
    print(f"{'='*60}")

    open_edit_dialog(driver, wait)
    delete_group_if_exists(driver, wait, group_name)
    delete_group_if_exists(driver, wait, group_name + "_Edited")

    click_add_new_group(driver, wait)
    group_input = driver.find_element(By.NAME, "groupname")
    group_input.clear()
    group_input.send_keys(group_name)

    click_save_button(driver, wait)

    close_dialog(driver, wait)
    open_edit_dialog(driver, wait)
    assert group_name in get_group_names(driver, wait), f"❌ SETUP GAGAL: '{group_name}' tidak ditemukan."
    close_dialog(driver, wait)

    print(f"✅ SETUP BERHASIL: '{group_name}' sudah tersedia.")
    print(f"{'='*60}\n")


def perform_reset_password_and_verify(driver, wait, username, new_password):
    """
    Core function: Find user, Reset Password, Save, and Verify Toast.

    Args:
        driver: WebDriver instance
        wait: WebDriverWait instance
        username: Username to reset password for
        new_password: New password

    Raises:
        AssertionError: If Toast verification fails
    """
    print(f"\n{'='*60}")
    print(f"🎯 Memulai: Reset Password untuk User '{username}'")
    print(f"{'='*60}")

    row = find_row_by_name(driver, wait, username)
    open_user_details_dialog(driver, wait, row)

    print("🔍 Mengklik tombol 'Reset Password'...")
    reset_btn = wait.until(EC.presence_of_element_located((By.XPATH, "//button[text()='Reset Password']")))
    safe_click(driver, reset_btn)

    print(f"✍️ Memasukkan password baru: '{new_password}'...")
    new_password_input = wait.until(EC.presence_of_element_located((By.ID, "new-password")))
    new_password_input.send_keys(new_password)

    print("💾 Mengklik tombol 'Save'...")
    save_btn = wait.until(EC.presence_of_element_located((By.XPATH, "//button[text()='Save']")))
    safe_click(driver, save_btn)

    wait_for_toast(wait)
    print(f"✅ Password untuk '{username}' berhasil direset.")

    close_dialog(driver, wait)
    print(f"{'='*60}\n")


def get_table_rows(driver, wait):
    """Get all rows (<tr>) from the table tbody."""
    try:
        table = wait.until(EC.presence_of_element_located((By.TAG_NAME, "table")))
        rows = table.find_elements(By.CSS_SELECTOR, "tbody tr")
        return rows
    except TimeoutException:
        raise RuntimeError("❌ Tidak menemukan tabel user di halaman.")


def perform_toggle_status_and_verify(driver, wait, username):
    """
    Core function: Find user, detect status, toggle status (Activate/Deactivate),
    and verify status change and success toast.

    Args:
        driver: WebDriver instance
        wait: WebDriverWait instance
        username: Username to toggle status for

    Raises:
        AssertionError: If status or toast verification fails
    """
    print(f"\n{'='*60}")
    print(f"🎯 Memulai Core Action: Toggle Status untuk User '{username}'")
    print(f"{'='*60}")

    row = find_row_by_name(driver, wait, username)
    current_status_btn = get_status_button(row)
    current_status = current_status_btn.text.strip()
    safe_click(driver, current_status_btn)
    print(f"🟩 Tombol status '{current_status}' diklik")

    target_status = click_status_action(driver, wait, current_status)
    wait_for_toast(wait, timeout=10)

    print("🔄 Reload row untuk verifikasi status baru…")
    row = find_row_by_name(driver, wait, username)

    print(f"🔍 Mengecek apakah status berubah menjadi {target_status}…")
    updated_btn = get_status_button(row)

    assert updated_btn.text.strip() == target_status, \
        f"❌ Status tidak berubah dari {current_status} menjadi {target_status}"

    print(f"✅ Status '{username}' berhasil diubah menjadi {target_status}!")
    print(f"{'='*60}\n")

    return target_status
