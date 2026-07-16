"""
General helper functions for VTS UI Test automation.
Contains reusable utilities for navigation, search, click, and toast verification.
"""

import re
import time
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException
from selenium.webdriver.common.keys import Keys


def navigate_to_page_button(driver, wait, button_text):
    """
    Navigate to a subpage by clicking the corresponding tab button.

    Args:
        driver: WebDriver instance
        wait: WebDriverWait instance
        button_text: Text on the tab button (e.g., 'Instructor', 'Trainee', 'Quiz')

    Raises:
        RuntimeError: If navigation fails
    """
    print(f"➡️ Navigasi ke Subpage: '{button_text}'...")

    page_tab_locator = (By.XPATH, f"//button[contains(text(), '{button_text}')]")

    try:
        page_tab = wait.until(EC.element_to_be_clickable(page_tab_locator))
        driver.execute_script("arguments[0].scrollIntoView({block:'center'});", page_tab)
        safe_click(driver, page_tab)
        print(f"✅ Berhasil pindah ke subpage '{button_text}'.")
    except TimeoutException:
        print(f"❌ Gagal menemukan atau mengklik tab '{button_text}'.")
        raise RuntimeError(f"Gagal navigasi ke subpage '{button_text}'.")
    except Exception as e:
        print(f"⚠️ Error saat klik tab '{button_text}': {e}")
        raise


def perform_search_and_verify(driver, wait, query_text):
    """
    Perform search on the input field and verify results.
    Ensures each result CONTAINS the query text (case insensitive).

    Args:
        driver: WebDriver instance
        wait: WebDriverWait instance
        query_text: Search query string

    Raises:
        AssertionError: If verification fails
    """
    print(f"\n{'='*60}")
    print(f"🎯 Memulai Pencarian dengan Query: '{query_text}'")
    print(f"{'='*60}")

    # 1. Find search input
    search_locator = (By.CSS_SELECTOR, "form input[name='query']")
    try:
        search_input = wait.until(EC.presence_of_element_located(search_locator))
    except TimeoutException:
        raise RuntimeError(f"❌ Tidak menemukan input search dengan locator: {search_locator}.")

    # 2. Type query and submit (ENTER)
    print(f"🔍 Mengetik query: '{query_text}' dan menekan ENTER...")
    search_input.clear()
    search_input.send_keys(query_text)
    search_input.send_keys(Keys.ENTER)

    time.sleep(2)

    # 3. Get table rows
    try:
        table = wait.until(EC.presence_of_element_located((By.TAG_NAME, "table")))
        rows = table.find_elements(By.CSS_SELECTOR, "tbody tr")
        assert rows, f"❌ Tidak ada hasil (row) ditemukan setelah pencarian dengan query '{query_text}'!"
    except Exception as e:
        raise AssertionError(f"Gagal mengambil/memverifikasi baris tabel: {e}")

    # 4. Verify each row
    matched_all = True
    pattern = re.compile(rf"{query_text}", re.IGNORECASE)

    print(f"🔎 Memverifikasi {len(rows)} hasil pencarian...")

    for i, row in enumerate(rows, start=1):
        cells = row.find_elements(By.TAG_NAME, "td")
        if not cells:
            continue
        cell_text = cells[0].text.strip()
        if not pattern.search(cell_text):
            matched_all = False
            print(f"❌ Row {i} ('{cell_text}') TIDAK mengandung query '{query_text}'")

    # 5. Final Result
    assert matched_all, f"❌ Ditemukan hasil yang tidak sesuai query!"
    print(f"✅ Semua {len(rows)} hasil pencarian MENGANDUNG kata kunci '{query_text}'.")
    print(f"{'='*60}\n")


def find_row_by_name(driver, wait, name):
    """
    Find a table row by name text, supporting nested elements inside TD.

    Args:
        driver: WebDriver instance
        wait: WebDriverWait instance
        name: Text to search for in the row

    Returns:
        WebElement: The found row element

    Raises:
        Exception: If row is not found
    """
    print(f"🔍 Mencari row dengan nama '{name}' menggunakan XPath yang robust...")

    row_locator = (
        By.XPATH,
        f"//table//tbody/tr[.//td[contains(normalize-space(.), '{name}')]]"
    )

    try:
        row = wait.until(EC.presence_of_element_located(row_locator))
        print(f"✅ Row dengan teks '{name}' ditemukan.")
        return row
    except TimeoutException:
        raise Exception(f"❌ Row dengan nama '{name}' tidak ditemukan!")


def wait_for_toast(wait, timeout=5):
    """
    Wait for and verify Toastify success message.

    Args:
        wait: WebDriverWait instance
        timeout: Maximum wait time in seconds (default: 5)

    Returns:
        WebElement: Toast success element

    Raises:
        AssertionError: If toast does not appear within timeout
    """
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


def safe_click(driver, element, retries=3, wait_time=0.8):
    """
    Click an element with retry and scroll into view.
    Uses JavaScript to avoid ElementClickInterceptedException.

    Args:
        driver: WebDriver instance
        element: WebElement to click
        retries: Number of attempts (default: 3)
        wait_time: Wait time between retries in seconds (default: 0.8)

    Raises:
        RuntimeError: If click fails after all retries
    """
    for i in range(retries):
        try:
            driver.execute_script("arguments[0].scrollIntoView(true);", element)
            driver.execute_script("arguments[0].click();", element)
            return
        except Exception as e:
            print(f"⚠️ Click intercepted (attempt {i+1}/{retries}): {e}")
            time.sleep(wait_time)
    raise RuntimeError("Gagal klik elemen setelah beberapa percobaan.")
