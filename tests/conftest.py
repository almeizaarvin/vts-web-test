from dotenv import load_dotenv
import os
import pytest
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from webdriver_manager.chrome import ChromeDriverManager
from datetime import datetime
import base64

# --- Load environment variables ---
load_dotenv()

@pytest.fixture(scope="session")
def driver():
    """Setup WebDriver Chrome (headless) untuk seluruh sesi test"""
    chrome_options = Options()
    chrome_options.add_argument("--no-sandbox")
    chrome_options.add_argument("--disable-dev-shm-usage")
    chrome_options.add_argument("--headless")
    chrome_options.add_argument("--window-size=1366,768")
    chrome_options.binary_location = "/usr/bin/google-chrome"

    driver = webdriver.Chrome(
        service=Service(ChromeDriverManager().install()),
        options=chrome_options
    )
    yield driver
    driver.quit()


@pytest.fixture(scope="function")
def login_as_admin(driver):
    """Login sebagai admin, ambil credential dari .env"""
    url = os.getenv("LOGIN_URL")
    username = os.getenv("ADMIN_USER")
    password = os.getenv("ADMIN_PASS")

    if not all([url, username, password]):
        raise ValueError("LOGIN_URL, ADMIN_USER, dan ADMIN_PASS harus diisi di .env")

    driver.get(url)
    wait = WebDriverWait(driver, 15)

    # ✅ Username
    username_input = wait.until(EC.presence_of_element_located((By.NAME, "username")))
    username_input.clear()
    username_input.send_keys(username)

    # ✅ Password
    password_input = wait.until(EC.presence_of_element_located((By.NAME, "password")))
    password_input.clear()
    password_input.send_keys(password)

    # ✅ Klik tombol LOGIN
    login_btn = wait.until(EC.element_to_be_clickable((By.CSS_SELECTOR, "button[type='submit']")))
    login_btn.click()

    # ✅ Tunggu redirect
    wait.until(EC.url_contains("userlist?pageId=0"))
    assert "userlist?pageId=0" in driver.current_url, (
        f"Login gagal: URL sekarang ({driver.current_url}) tidak sesuai"
    )

    return driver


# ---------------------------------------------------------------------------
# 🧩 HOOK UNTUK TAMBAHKAN SCREENSHOT DI REPORT HTML (INLINE DALAM DETAIL TEST)
# ---------------------------------------------------------------------------
@pytest.hookimpl(hookwrapper=True)
def pytest_runtest_makereport(item, call):
    """Hook untuk menambahkan screenshot ke report HTML pytest"""
    outcome = yield
    rep = outcome.get_result()

    # Hanya jalankan setelah test selesai ("call" phase)
    if rep.when == "call":
        driver = item.funcargs.get("login_as_admin") or item.funcargs.get("driver")
        if driver:
            # Buat folder screenshot
            screenshot_dir = "screenshots"
            os.makedirs(screenshot_dir, exist_ok=True)

            # Nama file
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            filename = f"{item.name}_{timestamp}.png"
            screenshot_path = os.path.join(screenshot_dir, filename)

            # Simpan screenshot
            driver.save_screenshot(screenshot_path)

            # Konversi ke base64 biar bisa tampil inline
            with open(screenshot_path, "rb") as image_file:
                encoded = base64.b64encode(image_file.read()).decode()

            # Tambahkan ke HTML report
            pytest_html = item.config.pluginmanager.getplugin("html")
            extra = getattr(rep, "extra", [])

            extra.append(pytest_html.extras.html(
                f'<div><b>Screenshot:</b><br><img src="data:image/png;base64,{encoded}" '
                f'style="width:600px;border:1px solid #ccc;border-radius:8px;"/></div>'
            ))
            rep.extra = extra
