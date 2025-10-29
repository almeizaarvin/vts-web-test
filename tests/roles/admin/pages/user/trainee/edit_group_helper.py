import time
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC

def safe_click(driver, element, retries=3, wait_time=0.8):
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
        close_icon = wait.until(
            EC.presence_of_element_located((By.XPATH, "//*[@data-testid='CloseIcon']"))
        )
        parent_btn = close_icon.find_element(By.XPATH, "./ancestor::button[1]")
        driver.execute_script("arguments[0].click();", parent_btn)
        print("✅ Tombol close diklik (via CloseIcon).")
    except Exception as e:
        print(f"❌ Gagal menemukan atau klik tombol close: {e}")
        raise

    try:
        wait.until(EC.invisibility_of_element_located((By.CLASS_NAME, "MuiDialogContent-root")))
        print("✅ Dialog berhasil tertutup.")
    except Exception:
        print("⚠️ Dialog belum hilang, coba tunggu fallback.")
        wait.until_not(EC.presence_of_element_located((By.XPATH, "//*[@data-testid='CloseIcon']")))
        print("✅ Dialog tertutup (fallback).")

def get_group_names(driver, wait):
    dialog = wait.until(EC.presence_of_element_located((By.CLASS_NAME, "MuiDialogContent-root")))
    divs = dialog.find_elements(By.TAG_NAME, "div")
    names = [d.text.strip() for d in divs if d.text.strip()]
    return names

def delete_group_if_exists(driver, wait, group_name):
    print(f"🕵️ Mengecek apakah '{group_name}' sudah ada...")
    names = get_group_names(driver, wait)
    print(f"📋 Daftar group saat ini: {names}")

    if group_name not in names:
        print(f"✅ '{group_name}' belum ada, tidak perlu dihapus.")
        return False

    print(f"⚠️ '{group_name}' ditemukan, proses hapus...")
    delete_btn = wait.until(EC.element_to_be_clickable((
        By.XPATH,
        f"//div[normalize-space(text())='{group_name}']/following::button[.//*[@data-testid='DeleteIcon']][1]"
    )))
    driver.execute_script("arguments[0].click();", delete_btn)
    print("🗑️ Tombol hapus diklik.")

    confirm_btn = wait.until(
        EC.element_to_be_clickable((By.XPATH, "//*[name()='svg' and @aria-label='Ya']/ancestor::button[1]"))
    )
    driver.execute_script("arguments[0].click();", confirm_btn)
    print("✅ Konfirmasi hapus diklik, menunggu refresh...")

    wait.until_not(EC.text_to_be_present_in_element((By.CLASS_NAME, "MuiDialogContent-root"), group_name))
    print(f"✅ '{group_name}' berhasil dihapus.")
    return True
