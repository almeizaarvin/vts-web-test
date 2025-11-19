import re
import time
import pytest
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException

@pytest.mark.usefixtures("login_as_instructor_fixture")
def test_search_user(login_as_instructor_fixture):
    driver = login_as_instructor_fixture
    wait = WebDriverWait(driver, 15)

    query_text = "Trainee"

    # --- Step 1: Pastikan halaman userlist sudah muncul
    wait.until(lambda d: "userlist?pageId=0" in d.current_url)
    print("✅ Berada di halaman userlist.")

    # --- Step 2: Cari input search dan ketik query
    try:
        search_input = wait.until(
            EC.presence_of_element_located((By.CSS_SELECTOR, "form input[name='query']"))
        )
    except TimeoutException:
        pytest.fail("❌ Tidak menemukan input search.")

    print(f"🔍 Mengetik query pencarian: '{query_text}'...")
    search_input.clear()
    search_input.send_keys(query_text)

    time.sleep(2) 

    # --- Step 3 & 4: Ambil semua baris tabel dan verifikasi
    try:
        table = wait.until(EC.presence_of_element_located((By.TAG_NAME, "table")))
        rows = table.find_elements(By.CSS_SELECTOR, "tbody tr")
        assert rows, "❌ Tidak ada row ditemukan di tabel setelah pencarian!"
    except TimeoutException:
        pytest.fail("❌ Tidak menemukan tabel user setelah pencarian.")

    matched_all = True
    # Mencari pola yang diawali dengan query_text (case insensitive)
    pattern = re.compile(rf"^{query_text}", re.IGNORECASE)

    for i, row in enumerate(rows, start=1):
        cells = row.find_elements(By.TAG_NAME, "td")
        if not cells: continue

        # Asumsi kolom nama ada di kolom pertama
        cell_text = cells[0].text.strip()
        
        if not pattern.match(cell_text):
            matched_all = False
            print(f"❌ Row {i} ('{cell_text}') tidak sesuai dengan query '{query_text}'")

    # --- Step 5: Verifikasi hasil
    assert matched_all, "❌ Ada hasil pencarian yang tidak sesuai query!"
    print(f"✅ Semua hasil pencarian cocok dengan '{query_text}'.")