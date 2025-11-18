import time
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC

def safe_click(driver, element, retries=3, wait_time=0.8):
    """Klik elemen dengan retry dan scroll ke view"""
    for i in range(retries):
        try:
            driver.execute_script("arguments[0].scrollIntoView(true);", element)
            driver.execute_script("arguments[0].click();", element)
            return
        except Exception as e:
            print(f"⚠️ Click intercepted (attempt {i+1}/{retries}): {e}")
            time.sleep(wait_time)
    raise RuntimeError("Gagal klik elemen setelah beberapa percobaan.")


def open_edit_dialog(driver, wait):
    print("🟦 Membuka Edit Group List...")
    edit_btn = wait.until(
        EC.element_to_be_clickable((By.XPATH, "//button[.//span[contains(text(), 'Edit Group List')]]"))
    )
    safe_click(driver, edit_btn)
    wait.until(EC.presence_of_element_located((By.CLASS_NAME, "MuiDialogContent-root")))


def close_dialog(driver, wait):
    print("🟥 Menutup dialog...")
    try:
        close_icon = wait.until(EC.presence_of_element_located((By.XPATH, "//*[@data-testid='CloseIcon']")))
        parent_btn = close_icon.find_element(By.XPATH, "./ancestor::button[1]")
        driver.execute_script("arguments[0].click();", parent_btn)
        wait.until(EC.invisibility_of_element_located((By.CLASS_NAME, "MuiDialogContent-root")))
        print("✅ Dialog berhasil tertutup.")
    except Exception as e:
        print(f"⚠️ Gagal menutup dialog: {e}")


def get_group_names(driver, wait):
    dialog = wait.until(EC.presence_of_element_located((By.CLASS_NAME, "MuiDialogContent-root")))
    divs = dialog.find_elements(By.TAG_NAME, "div")
    return [d.text.strip() for d in divs if d.text.strip()]


def delete_group_if_exists(driver, wait, group_name):
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


def find_row_by_name(driver, wait, name):
    """
    Cari row dalam table yg kolom pertamanya sama dengan 'name'.
    Return WebElement row.
    """
    rows = wait.until(EC.presence_of_all_elements_located(
        (By.XPATH, "//table//tbody/tr")
    ))

    for row in rows:
        first_col = row.find_element(By.XPATH, "./td[1]//div")
        if first_col.text.strip() == name:
            return row

    raise Exception(f"Row dengan nama '{name}' tidak ditemukan!")


def click_edit_group_button(driver, wait, row):
    """
    Dari row yg ditemukan, klik tombol dengan svg aria-label 'Ubah Kelompok'
    """
    edit_btn = row.find_element(
        By.XPATH,
        ".//button[.//svg[@aria-label='Ubah Kelompok']]"
    )

    driver.execute_script("arguments[0].click();", edit_btn)


def open_group_edit_dropdown(driver, wait):
    """
    Cari popup form edit-group-form lalu buka dropdown (listbox button)
    """
    form = wait.until(EC.presence_of_element_located(
        (By.ID, "edit-group-form")
    ))

    dropdown_btn = form.find_element(
        By.XPATH,
        ".//div[@aria-haspopup='listbox']"
    )

    driver.execute_script("arguments[0].click();", dropdown_btn)


def wait_for_toast(wait, timeout=5):
    """Menunggu dan memverifikasi Toastify success message."""
    toast_class = "Toastify__toast--success"
    try:
        success_toast = wait.until(
            EC.presence_of_element_located((By.CLASS_NAME, toast_class)),
            f"❌ Timeout: Toast sukses ({toast_class}) tidak muncul dalam {timeout} detik."
        )
        print("✅ Success Toast muncul!")
        return success_toast
    except TimeoutException as e:
        raise AssertionError(f"❌ Gagal memverifikasi Toast sukses: {e}")
    

def find_row_by_name(driver, wait, name):
    rows = wait.until(EC.presence_of_all_elements_located(
        (By.XPATH, "//table//tbody/tr")
    ))

    for row in rows:
        # Mencari teks di kolom pertama (td[1])
        first_col = row.find_element(By.XPATH, "./td[1]") 
        if first_col.text.strip() == name:
            return row

    raise Exception(f"❌ Row dengan nama '{name}' tidak ditemukan!")


def find_peserta_row(driver, wait):
    """Helper spesifik untuk mencari, misalnya 'Peserta 6'."""
    print("🔍 Mencari row Peserta 6…")
    row = find_row_by_name(driver, wait, "Peserta 6")
    print("🟩 Row Peserta 6 ditemukan.")
    return row


# --- Dialog/Action Handlers ---

def open_user_details_dialog(driver, wait, row):
    """
    Dari row yang ditemukan, klik tombol "See Details" untuk membuka dialog.
    """
    print("🔍 Mencari dan mengklik tombol See Details…")
    
    # Mencari tombol "See Details" berdasarkan aria-label
    details_btn = row.find_element(By.CSS_SELECTOR, "button[aria-label='See Details']")
    
    safe_click(driver, details_btn)
    print("🟩 Dialog detail Peserta terbuka.")


def get_status_button(row):
    """Mencari tombol 'Active' atau 'Inactive' di dalam row."""
    buttons = row.find_elements(By.TAG_NAME, "button")
    for btn in buttons:
        txt = btn.text.strip()
        if txt in ("Active", "Inactive"):
            return btn
    raise Exception("❌ Tidak menemukan tombol Active/Inactive pada row.")


def click_status_action(driver, wait, current_status):
    """
    Mengklik tombol aksi (Activate/Deactivate) di popup konfirmasi.
    """
    target_status = "Inactive" if current_status == "Active" else "Active"
    action_button_label = "Deactivate" if current_status == "Active" else "Activate"
    
    print(f"🎯 Target: {target_status} (aksi: {action_button_label})")

    action_btn = wait.until(
        EC.element_to_be_clickable((By.XPATH, f"//button[normalize-space()='{action_button_label}']"))
    )
    safe_click(driver, action_btn)
    print(f"🟩 Tombol {action_button_label} diklik.")

    return target_status


def open_group_edit_dialog(driver, wait):
    """Membuka dialog "Edit Group List"."""
    print("🟦 Membuka Edit Group List...")
    edit_btn = wait.until(
        EC.element_to_be_clickable((By.XPATH, "//button[.//span[contains(text(), 'Edit Group List')]]"))
    )
    safe_click(driver, edit_btn)
    wait.until(EC.presence_of_element_located((By.CLASS_NAME, "MuiDialogContent-root")))
    print("✅ Dialog terbuka.")


def close_dialog(driver, wait):
    """Menutup dialog saat ini menggunakan ikon 'CloseIcon'."""
    print("🟥 Menutup dialog...")
    try:
        # Mencari ikon dan naik ke parent button
        close_icon = wait.until(EC.presence_of_element_located((By.XPATH, "//*[@data-testid='CloseIcon']")))
        parent_btn = close_icon.find_element(By.XPATH, "./ancestor::button[1]")
        safe_click(driver, parent_btn)
        # Menunggu dialog menghilang
        wait.until(EC.invisibility_of_element_located((By.CLASS_NAME, "MuiDialogContent-root")))
        print("✅ Dialog berhasil tertutup.")
    except Exception as e:
        print(f"⚠️ Gagal menutup dialog: {e}")


def get_group_names(driver, wait):
    """Mengambil semua nama group yang ditampilkan di dalam dialog."""
    dialog = wait.until(EC.presence_of_element_located((By.CLASS_NAME, "MuiDialogContent-root")))
    # Asumsi nama group ada di div dengan teks yang tidak kosong
    divs = dialog.find_elements(By.XPATH, "//div[contains(@class, 'MuiDialogContent-root')]//div[normalize-space()]")
    
    # Filter dan ambil teks dari elemen yang benar-benar berisi nama group, biasanya elemen pertama di setiap baris group
    names = []
    for d in divs:
        text = d.text.strip()
        if text and not d.find_elements(By.TAG_NAME, 'button'): # Pastikan bukan tombol
             names.append(text)
    
    return names

# --- Group Action Handlers ---

def click_add_new_group(driver, wait):
    """Mengklik tombol 'Add New Group' dan menunggu input muncul."""
    print("➕ Klik tombol 'Add New Group'...")
    add_btn = wait.until(EC.element_to_be_clickable((By.XPATH, "//button[contains(., 'Add New Group')]")))
    safe_click(driver, add_btn)
    # Menunggu input field muncul
    wait.until(EC.presence_of_element_located((By.NAME, "groupname")))


def click_save_button(driver, wait):
    """Mengklik tombol 'Simpan' (dengan aria-label='Simpan')."""
    save_icon = wait.until(EC.presence_of_element_located((By.XPATH, "//*[@aria-label='Simpan']")))
    # Naik ke parent button/div
    parent_btn = save_icon.find_element(By.XPATH, "./ancestor::*[self::button or self::div][1]")
    safe_click(driver, parent_btn)
