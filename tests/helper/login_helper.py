import os
import dotenv
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
            # Locator untuk tombol switch
            switch_button = driver.find_element(By.XPATH, "//div[contains(@class, 'absolute top-4 right-4')]//button")
            switch_button.click()

            # Tunggu teks berubah menjadi selain "MASUK"
            wait.until(
                lambda d: d.find_element(By.CSS_SELECTOR, "button[type='submit']").text.strip().upper() != "MASUK"
            )
            print("✅ Bahasa berhasil diganti ke English")
        else:
            print("✅ Halaman sudah berbahasa Inggris")
    except Exception as e:
        print(f"⚠️ Tidak dapat memeriksa/menukar bahasa: {e}")

def perform_login(driver, user_type):
    """
    Fungsi inti untuk melakukan login berdasarkan tipe user.
    user_type harus 'ADMIN' atau 'INSTRUCTOR'.
    """
    dotenv.load_dotenv()

    # Tentukan Environment Variable berdasarkan tipe user
    url = os.getenv("LOGIN_URL")
    username = os.getenv(f"{user_type}_USER")
    password = os.getenv(f"{user_type}_PASS")

    if not all([url, username, password]):
        raise ValueError(f"LOGIN_URL, {user_type}_USER, dan {user_type}_PASS harus diisi di .env")

    driver.get(url)
    wait = WebDriverWait(driver, 15)

    ensure_english_language(driver, wait)

    # Isi form login
    username_input = wait.until(EC.presence_of_element_located((By.NAME, "username")))
    password_input = wait.until(EC.presence_of_element_located((By.NAME, "password")))

    print(f"🔑 Mencoba login sebagai {user_type}...")
    username_input.clear()
    username_input.send_keys(username)
    password_input.clear()
    password_input.send_keys(password)

    # Klik tombol login
    login_btn = wait.until(EC.element_to_be_clickable((By.CSS_SELECTOR, "button[type='submit']")))
    login_btn.click()

    # Verifikasi URL (Asumsi: Admin/Instructor sama-sama diarahkan ke userlist setelah login)
    wait.until(EC.url_contains("userlist?pageId=0"))
    assert "userlist?pageId=0" in driver.current_url, (
        f"Login {user_type} gagal: URL sekarang ({driver.current_url}) tidak sesuai"
    )
    print(f"✅ Login {user_type} Berhasil!")

    return driver

def login_as_admin(driver):
    return perform_login(driver, "ADMIN")

def login_as_instructor(driver):
    return perform_login(driver, "INSTRUCTOR")