import os
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

def ensure_english_language(driver, wait):
    """Pastikan halaman login sudah berbahasa Inggris"""
    try:
        login_button = wait.until(
            EC.presence_of_element_located((By.CSS_SELECTOR, "button[type='submit']"))
        )

        if login_button.text.strip().upper() == "MASUK":
            print("🌐 Bahasa masih Indonesia → ganti ke English...")
            switch_div = driver.find_element(By.CSS_SELECTOR, "div.absolute.top-4.right-4")
            switch_button = switch_div.find_element(By.CSS_SELECTOR, "div > button")
            switch_button.click()

            wait.until(
                lambda d: d.find_element(By.CSS_SELECTOR, "button[type='submit']").text.strip().upper() != "MASUK"
            )
            print("✅ Bahasa berhasil diganti ke English")
        else:
            print("✅ Halaman sudah berbahasa Inggris")
    except Exception as e:
        print(f"⚠️ Tidak dapat memeriksa/menukar bahasa: {e}")


def login_as_admin(driver):
    """Login sebagai admin, memastikan bahasa & autentikasi"""
    import dotenv
    dotenv.load_dotenv()

    url = os.getenv("LOGIN_URL")
    username = os.getenv("ADMIN_USER")
    password = os.getenv("ADMIN_PASS")

    if not all([url, username, password]):
        raise ValueError("LOGIN_URL, ADMIN_USER, dan ADMIN_PASS harus diisi di .env")

    driver.get(url)
    wait = WebDriverWait(driver, 15)

    ensure_english_language(driver, wait)

    # Isi form login
    username_input = wait.until(EC.presence_of_element_located((By.NAME, "username")))
    password_input = wait.until(EC.presence_of_element_located((By.NAME, "password")))

    username_input.clear()
    username_input.send_keys(username)
    password_input.clear()
    password_input.send_keys(password)

    # Klik tombol login
    login_btn = wait.until(EC.element_to_be_clickable((By.CSS_SELECTOR, "button[type='submit']")))
    login_btn.click()

    wait.until(EC.url_contains("userlist?pageId=0"))
    assert "userlist?pageId=0" in driver.current_url, (
        f"Login gagal: URL sekarang ({driver.current_url}) tidak sesuai"
    )

    return driver
