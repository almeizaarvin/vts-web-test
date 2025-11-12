import os
import time
from datetime import datetime
import pytest
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import (
    TimeoutException,
    NoSuchElementException,
    ElementClickInterceptedException,
    StaleElementReferenceException,
)

SCREENSHOT_DIR = os.environ.get("SCREENSHOT_DIR", "/tmp")

@pytest.mark.usefixtures("login_as_admin_fixture")
def test_login(login_as_admin_fixture):

    driver = login_as_admin_fixture
    wait = WebDriverWait(driver, 10)

    def take_screenshot(name="screenshot"):
        ts = datetime.now().strftime("%Y%m%d_%H%M%S")
        filename = os.path.join(SCREENSHOT_DIR, f"{name}_{ts}.png")
        try:
            driver.save_screenshot(filename)
            print(f"📸 Screenshot saved: {filename}")
        except Exception as e:
            print(f"⚠️ Gagal simpan screenshot: {e}")

    # -------------------------
    # 1) Cek apakah tombol submit ada (login page)
    # -------------------------
    try:
        login_btn = wait.until(
            EC.presence_of_element_located((By.CSS_SELECTOR, "button[type='submit']"))
        )
    except TimeoutException:
        # Jika tombol submit nggak ditemukan, kemungkinan sudah otomatis login oleh fixture.
        # Ambil screenshot dan gagalkan test agar flow lebih jelas.
        take_screenshot("no_submit_button_found")
        pytest.fail("Tombol submit tidak ditemukan — fixture mungkin sudah melakukan login.")

    # Ambil teks tombol (robust: coba .text, fallback cari child)
    def get_button_text(el):
        try:
            txt = el.text.strip()
            if txt:
                return txt
        except StaleElementReferenceException:
            return ""
        # fallback: cek innerText via JS
        try:
            return driver.execute_script("return arguments[0].innerText || '';", el).strip()
        except Exception:
            return ""

    btn_text = get_button_text(login_btn).upper()
    print(f"Debug: login button text = '{btn_text}'")

    # -------------------------
    # 2) Jika masih 'MASUK', lakukan switch language
    # -------------------------
    if btn_text == "MASUK":
        print("Detected Indonesian UI — attempting to switch language...")

        try:
            switch_div = wait.until(
                EC.presence_of_element_located((By.CSS_SELECTOR, "div.absolute.top-4.right-4"))
            )
        except TimeoutException:
            take_screenshot("switch_div_not_found")
            pytest.fail("Tidak menemukan container switch language (div.absolute.top-4.right-4).")

        # cari button di dalam struktur yang disebutkan: div > button
        try:
            switch_button = switch_div.find_element(By.CSS_SELECTOR, "div > button")
        except NoSuchElementException:
            # fallback: cari button descendant apa pun
            try:
                switch_button = switch_div.find_element(By.CSS_SELECTOR, "button")
            except NoSuchElementException:
                take_screenshot("switch_button_not_found")
                pytest.fail("Tidak menemukan tombol switch language di dalam container.")

        clicked = False
        last_err = None
        for attempt in range(3):
            try:
                wait.until(EC.element_to_be_clickable((By.CSS_SELECTOR, "div.absolute.top-4.right-4 div > button")))
                try:
                    switch_button.click()
                except (ElementClickInterceptedException, StaleElementReferenceException):
                    driver.execute_script("arguments[0].click();", switch_button)
                clicked = True
                print(f"Clicked switch button (attempt {attempt + 1})")
                break
            except Exception as e:
                last_err = e
                print(f"Attempt {attempt + 1} to click switch button failed: {e}")
                time.sleep(0.5)
                # try re-find element to avoid stale reference
                try:
                    switch_button = switch_div.find_element(By.CSS_SELECTOR, "div > button")
                except Exception:
                    pass

        if not clicked:
            take_screenshot("switch_click_failed")
            pytest.fail(f"Gagal klik switch language button: {last_err}")

        try:
            wait.until(
                lambda d: get_button_text(d.find_element(By.CSS_SELECTOR, "button[type='submit']")).upper()
                != "MASUK"
            )
            print("✅ Language switched to English (login button text changed).")
        except TimeoutException:
            print("Switch click didn't change text quickly, trying refresh...")
            driver.refresh()
            try:
                wait.until(
                    lambda d: get_button_text(d.find_element(By.CSS_SELECTOR, "button[type='submit']")).upper()
                    != "MASUK"
                )
                print("✅ Language switched after refresh.")
            except TimeoutException:
                take_screenshot("still_masuk_after_switch")
                pytest.fail("Setelah klik switch (dan refresh) teks tombol masih 'MASUK'.")
    else:
        print("✅ UI already English or login button not 'MASUK'.")

    # -------------------------
    # 3) Lanjutkan ke verifikasi halaman userlist
    # -------------------------
    try:
        wait.until(lambda d: "userlist?pageId=0" in d.current_url)
    except TimeoutException:
        take_screenshot("url_not_userlist")
        pytest.fail(f"URL tidak mengarah ke userlist: {driver.current_url}")

    # Pastikan tabel user muncul
    try:
        table = wait.until(EC.presence_of_element_located((By.TAG_NAME, "table")))
    except TimeoutException:
        take_screenshot("table_not_found")
        pytest.fail("Tabel user tidak ditemukan!")

    assert table is not None, "Tabel user tidak ditemukan!"
