"""
Helper functions untuk VTS UI Test
Berisi semua fungsi pembantu yang digunakan dalam automation testing
"""

import re
import time
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException, StaleElementReferenceException

from tests.helper.general_helper import find_row_by_name, safe_click, wait_for_toast


# ============================================================================
# SECTION 1: BASE HELPER - Fungsi Dasar untuk Interaksi WebDriver
# ============================================================================



def close_dialog(driver, wait):
    """
    Menutup dialog saat ini menggunakan ikon 'CloseIcon'.
    
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
    Mengklik input date, memilih tanggal hari ini (aria-current='date'),
    dan mengklik tombol 'OK' di dalam dialog kalender.
    
    Args:
        driver: WebDriver instance
        wait: WebDriverWait instance
    """
    print("🗓️ Memilih tanggal lahir (hari ini)...")
    
    # Klik input 'birthDate' untuk membuka kalender
    birth_date_input = wait.until(
        EC.presence_of_element_located((By.NAME, "birthDate"))
    )
    safe_click(driver, birth_date_input)

    # Tunggu dan cari tombol tanggal hari ini
    try:
        current_date_btn = wait.until(
            EC.element_to_be_clickable((By.CSS_SELECTOR, "button[aria-current='date']"))
        )
        safe_click(driver, current_date_btn)
    except TimeoutException:
        print("⚠️ Gagal menemukan tombol tanggal hari ini. Melanjutkan...")

    # Klik tombol 'OK'
    ok_btn = wait.until(
        EC.element_to_be_clickable((By.XPATH, "//button[text()='OK']"))
    )
    safe_click(driver, ok_btn)
    print("✅ Tanggal dan 'OK' berhasil diklik.")


def select_mui_dropdown_option(driver, wait, input_name, option_text):
    """
    Menangani dropdown MUI dengan Scroll-to-View, klik trigger, dan JS Force Click.
    
    Args:
        driver: WebDriver instance
        wait: WebDriverWait instance
        input_name: Nama label dropdown (contoh: 'Gender')
        option_text: Teks opsi yang akan dipilih
    
    Raises:
        RuntimeError: Jika gagal membuka atau memilih opsi dropdown
    """
    print(f"🔄 Memilih opsi '{option_text}' untuk input '{input_name}'...")
    
    # STEP 1: Scroll ke trigger dan klik
    try:
        select_trigger = wait.until(
            EC.element_to_be_clickable((
                By.XPATH, 
                f"//label[text()='{input_name}']/following-sibling::div//div[@role='combobox']"
            )),
            timeout=5
        )
        
        # Scroll ke trigger agar ada di viewport
        driver.execute_script("arguments[0].scrollIntoView({block: 'center'});", select_trigger)
        time.sleep(0.5)
        
        safe_click(driver, select_trigger)
        print(f"   -> Trigger dropdown '{input_name}' diklik.")

    except TimeoutException:
        print("⚠️ Gagal klik combobox.")
        raise RuntimeError(f"Gagal membuka menu dropdown {input_name}.")

    # STEP 2: Tunggu popup, scroll ke opsi, dan klik dengan JS
    option_locator = f'//ul[@role="listbox"]//li[@role="option" and normalize-space()="{option_text}"]'
    listbox_locator = By.XPATH, '//ul[@role="listbox"]'
    
    try:
        # Tunggu listbox muncul
        wait.until(EC.presence_of_element_located(listbox_locator))
        
        # Tunggu opsi muncul di DOM
        option_element = wait.until(
            EC.presence_of_element_located((By.XPATH, option_locator)),
            f"❌ Opsi '{option_text}' tidak ditemukan."
        )

        # Scroll agar opsi terlihat
        driver.execute_script("arguments[0].scrollIntoView({block: 'nearest'});", option_element)
        time.sleep(0.3)
        
        # Force click dengan JavaScript
        driver.execute_script("arguments[0].click();", option_element)
        print(f"   -> Opsi '{option_text}' berhasil diklik.")
        
        # Verifikasi menu tertutup
        wait.until(EC.invisibility_of_element_located(listbox_locator))
        print("✅ Dropdown berhasil ditutup.")

    except (TimeoutException, StaleElementReferenceException) as e:
        print(f"❌ Gagal klik opsi: {e}")
        raise RuntimeError("Gagal memilih opsi dropdown.")


# ============================================================================
# SECTION 2: GROUP HELPER - Fungsi untuk Manajemen Group
# ============================================================================

def open_edit_dialog(driver, wait):
    """
    Membuka dialog 'Edit Group List'.
    
    Args:
        driver: WebDriver instance
        wait: WebDriverWait instance
    """
    print("🟦 Membuka Edit Group List...")
    edit_btn = wait.until(
        EC.element_to_be_clickable((By.XPATH, "//button[.//span[contains(text(), 'Edit Group List')]]"))
    )
    safe_click(driver, edit_btn)
    wait.until(EC.presence_of_element_located((By.CLASS_NAME, "MuiDialogContent-root")))
    print("✅ Dialog Edit Group List terbuka.")


def open_group_edit_dialog(driver, wait):
    """Membuka dialog "Edit Group List"."""
    print("🟦 Membuka Edit Group List...")
    edit_btn = wait.until(
        EC.element_to_be_clickable((By.XPATH, "//button[.//span[contains(text(), 'Edit Group List')]]"))
    )
    safe_click(driver, edit_btn)
    wait.until(EC.presence_of_element_located((By.CLASS_NAME, "MuiDialogContent-root")))
    print("✅ Dialog terbuka.")



def get_group_names(driver, wait):
    """
    Mengambil semua nama group yang ditampilkan di dalam dialog.
    
    Args:
        driver: WebDriver instance
        wait: WebDriverWait instance
    
    Returns:
        list: Daftar nama group (string)
    """
    dialog = wait.until(EC.presence_of_element_located((By.CLASS_NAME, "MuiDialogContent-root")))
    divs = dialog.find_elements(By.TAG_NAME, "div")
    
    # Filter hanya div yang berisi teks dan bukan tombol
    names = []
    for d in divs:
        text = d.text.strip()
        if text and not d.find_elements(By.TAG_NAME, 'button'):
            names.append(text)
    
    return names


def click_add_new_group(driver, wait):
    """
    Mengklik tombol 'Add New Group' dan menunggu input muncul.
    
    Args:
        driver: WebDriver instance
        wait: WebDriverWait instance
    """
    print("➕ Klik tombol 'Add New Group'...")
    add_btn = wait.until(EC.element_to_be_clickable((By.XPATH, "//button[contains(., 'Add New Group')]")))
    safe_click(driver, add_btn)
    wait.until(EC.presence_of_element_located((By.NAME, "groupname")))
    print("✅ Input group name muncul.")


def click_save_button(driver, wait):
    """
    Mengklik tombol 'Simpan' (dengan aria-label='Simpan').
    
    Args:
        driver: WebDriver instance
        wait: WebDriverWait instance
    """
    print("💾 Klik tombol Simpan...")
    save_icon = wait.until(EC.presence_of_element_located((By.XPATH, "//*[@aria-label='Simpan']")))
    parent_btn = save_icon.find_element(By.XPATH, "./ancestor::*[self::button or self::div][1]")
    safe_click(driver, parent_btn)
    print("✅ Tombol Simpan diklik.")


def delete_group_if_exists(driver, wait, group_name):
    """
    Menghapus group jika sudah ada dalam daftar.
    
    Args:
        driver: WebDriver instance
        wait: WebDriverWait instance
        group_name: Nama group yang akan dihapus
    
    Returns:
        bool: True jika group dihapus, False jika tidak ada
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

    # Konfirmasi delete
    confirm_btn = wait.until(
        EC.element_to_be_clickable((By.XPATH, "//*[name()='svg' and @aria-label='Ya']/ancestor::button[1]"))
    )
    driver.execute_script("arguments[0].click();", confirm_btn)

    # Tunggu hingga nama group hilang dari list
    wait.until_not(EC.text_to_be_present_in_element((By.CLASS_NAME, "MuiDialogContent-root"), group_name))
    print(f"✅ '{group_name}' berhasil dihapus.")
    return True


def click_edit_group_button(driver, row):
    """
    Dari row yang ditemukan, klik tombol dengan svg aria-label 'Ubah Kelompok'.
    
    Args:
        driver: WebDriver instance
        row: WebElement row yang berisi tombol edit
    """
    edit_btn = row.find_element(
        By.XPATH,
        ".//button[.//svg[@aria-label='Ubah Kelompok']]"
    )
    driver.execute_script("arguments[0].click();", edit_btn)


def open_group_edit_dropdown(driver, wait):
    """
    Cari popup form 'edit-group-form' lalu buka dropdown (listbox button).
    
    Args:
        driver: WebDriver instance
        wait: WebDriverWait instance
    """
    form = wait.until(EC.presence_of_element_located((By.ID, "edit-group-form")))
    
    dropdown_btn = form.find_element(
        By.XPATH,
        ".//div[@aria-haspopup='listbox']"
    )
    driver.execute_script("arguments[0].click();", dropdown_btn)


# ============================================================================
# SECTION 3: USER HELPER - Fungsi untuk Manajemen User
# ============================================================================

def open_user_details_dialog(driver, wait, row):
    """
    Dari row yang ditemukan, klik tombol 'See Details' untuk membuka dialog.
    
    Args:
        driver: WebDriver instance
        wait: WebDriverWait instance
        row: WebElement row yang berisi tombol See Details
    """
    print("🔍 Mencari dan mengklik tombol See Details…")
    details_btn = row.find_element(By.CSS_SELECTOR, "button[aria-label='See Details']")
    safe_click(driver, details_btn)
    print("✅ Dialog detail Peserta terbuka.")


def get_status_button(row):
    """
    Mencari tombol 'Active' atau 'Inactive' di dalam row.
    
    Args:
        row: WebElement row yang berisi tombol status
    
    Returns:
        WebElement: Tombol status (Active/Inactive)
    
    Raises:
        Exception: Jika tombol status tidak ditemukan
    """
    buttons = row.find_elements(By.TAG_NAME, "button")
    for btn in buttons:
        txt = btn.text.strip()
        if txt in ("Active", "Inactive"):
            return btn
    raise Exception("❌ Tidak menemukan tombol Active/Inactive pada row.")


def click_status_action(driver, wait, current_status):
    """
    Mengklik tombol aksi (Activate/Deactivate) di popup konfirmasi.
    
    Args:
        driver: WebDriver instance
        wait: WebDriverWait instance
        current_status: Status saat ini ('Active' atau 'Inactive')
    
    Returns:
        str: Target status setelah aksi
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
# SECTION 4: NAVIGATION HELPER - Fungsi untuk Navigasi Halaman
# ============================================================================



def navigate_to_instructor_subpage(driver, wait):
    """
    Menavigasi dari halaman utama 'userlist' ke subpage Instructor.
    
    Args:
        driver: WebDriver instance
        wait: WebDriverWait instance
    
    Raises:
        RuntimeError: Jika gagal navigasi ke subpage Instructor
    """
    print("➡️ Navigasi ke Subpage Instructor...")
    
    instructor_tab_locator = (By.XPATH, "//button[contains(text(), 'Instructor')]")
    
    try:
        instructor_tab = wait.until(
            EC.element_to_be_clickable(instructor_tab_locator)
        )
        driver.execute_script("arguments[0].scrollIntoView(true);", instructor_tab)
        instructor_tab.click()
        print("✅ Berhasil pindah ke subpage Instructor.")
        
    except TimeoutException:
        print("❌ Gagal menemukan atau mengklik tab Instructor.")
        raise RuntimeError("Gagal navigasi ke subpage Instructor.")
    except Exception as e:
        print(f"⚠️ Error saat klik Instructor tab: {e}")
        raise


# ============================================================================
# SECTION 5: GROUP ACTION HELPER - Fungsi Aksi Lengkap untuk Group
# ============================================================================

def perform_add_group_and_verify(driver, wait, group_name):
    """
    Fungsi inti: Setup, Add Group, Save, dan Verification.
    
    Args:
        driver: WebDriver instance
        wait: WebDriverWait instance
        group_name: Nama group yang akan ditambahkan
    
    Raises:
        AssertionError: Jika group tidak ditemukan setelah ditambahkan
    """
    print(f"\n{'='*60}")
    print(f"🎯 Memulai: Menambahkan Group '{group_name}'")
    print(f"{'='*60}")

    # Setup: Pastikan group tidak ada
    open_edit_dialog(driver, wait)
    delete_group_if_exists(driver, wait, group_name)
    
    # Klik 'Add New Group'
    click_add_new_group(driver, wait)

    # Isi Nama Group
    print(f"✍️ Mengisi nama group: '{group_name}'...")
    group_input = driver.find_element(By.NAME, "groupname")
    group_input.clear()
    group_input.send_keys(group_name)

    # Simpan
    click_save_button(driver, wait)
    
    # Verifikasi
    close_dialog(driver, wait)
    open_edit_dialog(driver, wait)

    names = get_group_names(driver, wait)
    assert group_name in names, f"❌ '{group_name}' tidak ditemukan setelah ditambahkan!"
    print(f"✅ '{group_name}' berhasil ditambahkan dan diverifikasi.")

    # Cleanup
    close_dialog(driver, wait)
    print(f"{'='*60}\n")


def perform_edit_group_and_verify(driver, wait, original_name, edited_name):
    """
    Fungsi inti: Setup (Add), Edit, Save, dan Verification.
    
    Args:
        driver: WebDriver instance
        wait: WebDriverWait instance
        original_name: Nama group awal
        edited_name: Nama group setelah diedit
    
    Raises:
        AssertionError: Jika verifikasi edit gagal
    """
    print(f"\n{'='*60}")
    print(f"🎯 Memulai: Mengedit Group '{original_name}' → '{edited_name}'")
    print(f"{'='*60}")

    # SETUP: Pastikan group tidak ada
    open_edit_dialog(driver, wait)
    delete_group_if_exists(driver, wait, original_name)
    delete_group_if_exists(driver, wait, edited_name)

    # Tambahkan group awal
    print(f"➕ Menambahkan group '{original_name}' untuk diedit...")
    click_add_new_group(driver, wait)
    group_input = driver.find_element(By.NAME, "groupname")
    group_input.send_keys(original_name)
    click_save_button(driver, wait)
    
    # Refresh dialog
    close_dialog(driver, wait)
    open_edit_dialog(driver, wait)
    
    # Verifikasi group awal
    names = get_group_names(driver, wait)
    assert original_name in names, f"❌ '{original_name}' tidak ditemukan setelah add."
    print(f"✅ Group '{original_name}' berhasil ditambahkan.")

    # Klik icon Edit (pensil)
    print(f"✏️ Mengedit '{original_name}'...")
    edit_btn_locator = (
        By.XPATH,
        f"//div[normalize-space(text())='{original_name}']/following::button[.//*[@data-testid='EditIcon']][1]"
    )
    edit_btn = wait.until(EC.element_to_be_clickable(edit_btn_locator))
    safe_click(driver, edit_btn)

    # Edit nama
    print(f"✍️ Mengubah nama menjadi: '{edited_name}'...")
    input_field = wait.until(EC.presence_of_element_located((By.NAME, "groupname")))
    input_field.clear()
    input_field.send_keys(edited_name)

    # Simpan
    click_save_button(driver, wait)

    # Verifikasi perubahan
    close_dialog(driver, wait)
    open_edit_dialog(driver, wait)

    names_after = get_group_names(driver, wait)
    
    # ASSERTIONS
    assert edited_name in names_after, f"❌ '{edited_name}' tidak ditemukan setelah edit!"
    assert original_name not in names_after, f"❌ '{original_name}' masih muncul setelah edit!"

    print(f"✅ Group berhasil diubah dari '{original_name}' menjadi '{edited_name}'.")
    
    # CLEANUP
    delete_group_if_exists(driver, wait, edited_name)
    close_dialog(driver, wait)
    print(f"{'='*60}\n")


def create_group_for_edit(driver, wait, group_name):
    """
    Setup: Menambahkan group baru untuk persiapan test edit.
    
    Args:
        driver: WebDriver instance
        wait: WebDriverWait instance
        group_name: Nama group yang akan disiapkan
    
    Raises:
        AssertionError: Jika setup gagal
    """
    print(f"\n{'='*60}")
    print(f"🔧 SETUP: Menyiapkan '{group_name}' untuk diedit")
    print(f"{'='*60}")
    
    # Buka dialog
    open_edit_dialog(driver, wait)
    
    # Bersihkan duplikat
    delete_group_if_exists(driver, wait, group_name)
    delete_group_if_exists(driver, wait, group_name + "_Edited")
    
    # Tambahkan group
    click_add_new_group(driver, wait)
    group_input = driver.find_element(By.NAME, "groupname")
    group_input.clear()
    group_input.send_keys(group_name)
    
    click_save_button(driver, wait)
    
    # Verifikasi
    close_dialog(driver, wait)
    open_edit_dialog(driver, wait)
    assert group_name in get_group_names(driver, wait), f"❌ SETUP GAGAL: '{group_name}' tidak ditemukan."
    close_dialog(driver, wait)
    
    print(f"✅ SETUP BERHASIL: '{group_name}' sudah tersedia.")
    print(f"{'='*60}\n")


def perform_reset_password_and_verify(driver, wait, username, new_password):
    """
    Fungsi inti: Mencari user, Reset Password, Save, dan Verifikasi Toast.
    
    Args:
        driver: WebDriver instance
        wait: WebDriverWait instance
        username: Nama user yang akan direset passwordnya (contoh: "Peserta 6")
        new_password: Password baru
        
    Raises:
        AssertionError: Jika verifikasi Toast gagal
    """
    print(f"\n{'='*60}")
    print(f"🎯 Memulai: Reset Password untuk User '{username}'")
    print(f"{'='*60}")
    
    # 1. Cari row User
    row = find_row_by_name(driver, wait, username) # Menggunakan helper yang sudah ada
    
    # 2. Klik See Details
    open_user_details_dialog(driver, wait, row)
    
    # 3. Cari dan klik tombol "Reset Password"
    print("🔍 Mengklik tombol 'Reset Password'...")
    reset_btn = wait.until(
        EC.presence_of_element_located((By.XPATH, "//button[text()='Reset Password']")) 
    )
    safe_click(driver, reset_btn)
    
    # 4. Cari input "new-password" dan masukkan password
    print(f"✍️ Memasukkan password baru: '{new_password}'...")
    new_password_input = wait.until(EC.presence_of_element_located((By.ID, "new-password")))
    new_password_input.send_keys(new_password)
    
    # 5. Klik tombol Save
    print("💾 Mengklik tombol 'Save'...")
    save_btn = wait.until(
        EC.presence_of_element_located((By.XPATH, "//button[text()='Save']"))
    )
    safe_click(driver, save_btn)
    
    # 6. Assert Success Toast
    wait_for_toast(wait)
    print(f"✅ Password untuk '{username}' berhasil direset.")
    
    # Cleanup: Tutup dialog
    close_dialog(driver, wait)
    print(f"{'='*60}\n")

def get_table_rows(driver, wait):
    """Mendapatkan semua baris (<tr>) dari tbody tabel user."""
    try:
        table = wait.until(EC.presence_of_element_located((By.TAG_NAME, "table")))
        # Cari semua baris <tr> di dalam <tbody>
        rows = table.find_elements(By.CSS_SELECTOR, "tbody tr")
        return rows
    except TimeoutException:
        raise RuntimeError("❌ Tidak menemukan tabel user di halaman.")


def perform_toggle_status_and_verify(driver, wait, username):
    """
    Fungsi inti: Mencari user, mendeteksi status, toggle status (Activate/Deactivate), 
    dan memverifikasi perubahan status serta toast sukses.
    
    Args:
        driver: WebDriver instance
        wait: WebDriverWait instance
        username: Nama user yang statusnya akan diubah
        
    Raises:
        AssertionError: Jika verifikasi status atau toast gagal.
    """
    print(f"\n{'='*60}")
    print(f"🎯 Memulai Core Action: Toggle Status untuk User '{username}'")
    print(f"{'='*60}")
    
    # 1. Cari row User
    row = find_row_by_name(driver, wait, username) 
    
    # 2. Deteksi status saat ini dan klik tombol status
    current_status_btn = get_status_button(row)
    current_status = current_status_btn.text.strip()
    safe_click(driver, current_status_btn)
    print(f"🟩 Tombol status '{current_status}' diklik")

    # 3. Klik tombol Aksi (Activate / Deactivate) di popup konfirmasi
    target_status = click_status_action(driver, wait, current_status)
    
    # 4. Assert Success Toast
    wait_for_toast(wait, timeout=10) # Ditingkatkan timeout-nya karena ini adalah verifikasi kunci

    # 5. Cari ulang row User (fresh DOM)
    print("🔄 Reload row untuk verifikasi status baru…")
    # Asumsi: Halaman tidak berpindah, hanya refresh DOM/data
    row = find_row_by_name(driver, wait, username)

    # 6. Pastikan status berubah sesuai target
    print(f"🔍 Mengecek apakah status berubah menjadi {target_status}…")
    updated_btn = get_status_button(row)
    
    assert updated_btn.text.strip() == target_status, f"❌ Status tidak berubah dari {current_status} menjadi {target_status}"

    print(f"✅ Status '{username}' berhasil diubah menjadi {target_status}!")
    print(f"{'='*60}\n")
    
    return target_status