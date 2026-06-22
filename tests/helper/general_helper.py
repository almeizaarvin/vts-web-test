import re
import time
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException
from selenium.webdriver.common.keys import Keys # Pastikan ini sudah diimpor

def navigate_to_page_button(driver, wait, button_text):
    """
    Menavigasi ke subpage yang dituju dengan mengklik tombol tab yang sesuai.
    
    Args:
        driver: WebDriver instance
        wait: WebDriverWait instance
        button_text: Teks yang terdapat pada tombol tab halaman tujuan (misal: 'Instructor', 'Trainee', dll.)
    
    Raises:
        RuntimeError: Jika gagal navigasi ke subpage yang dituju
    """
    print(f"➡️ Navigasi ke Subpage: '{button_text}'...")
    
    # Menggunakan f-string untuk memasukkan parameter ke dalam XPath
    # Mencari tombol yang mengandung teks yang sesuai
    page_tab_locator = (By.XPATH, f"//button[contains(text(), '{button_text}')]")
    
    try:
        page_tab = wait.until(
            EC.element_to_be_clickable(page_tab_locator)
        )
        
        # Scroll ke view dan klik (menggunakan click() standar, tapi safe_click lebih disarankan jika ada)
        # Jika kamu punya helper 'safe_click', lebih baik ganti baris ini:
        # safe_click(driver, page_tab)
        
        driver.execute_script("arguments[0].scrollIntoView(true);", page_tab)
        page_tab.click() 
        
        print(f"✅ Berhasil pindah ke subpage '{button_text}'.")
        
    except TimeoutException:
        print(f"❌ Gagal menemukan atau mengklik tab '{button_text}'.")
        raise RuntimeError(f"Gagal navigasi ke subpage '{button_text}'.")
    except Exception as e:
        print(f"⚠️ Error saat klik tab '{button_text}': {e}")
        raise


def perform_search_and_verify(driver, wait, query_text):
    """
    Fungsi inti: Mengetik query, mengirimkannya (dengan ENTER), dan memverifikasi hasilnya.
    Verifikasi: Memastikan setiap hasil MENGANDUNG teks query (case insensitive).
    """
    print(f"\n{'='*60}")
    print(f"🎯 Memulai Core Action: Pencarian user dengan query '{query_text}'")
    print(f"{'='*60}")

    # 1. Cari input search
    try:
        search_input = wait.until(
            EC.presence_of_element_located((By.CSS_SELECTOR, "form input[name='query']"))
        )
    except TimeoutException:
        raise RuntimeError("❌ Tidak menemukan input search (form input[name='query']).")

    # 2. Ketik query dan KIRIM dengan ENTER
    print(f"🔍 Mengetik query pencarian: '{query_text}' dan menekan ENTER...")
    search_input.clear()
    search_input.send_keys(query_text)
    search_input.send_keys(Keys.ENTER)

    # Beri waktu agar data baru dimuat
    time.sleep(2) 

    # 3. Ambil baris tabel
    try:
        table = wait.until(EC.presence_of_element_located((By.TAG_NAME, "table")))
        rows = table.find_elements(By.CSS_SELECTOR, "tbody tr")
        assert rows, f"❌ Tidak ada row ditemukan di tabel setelah pencarian dengan query '{query_text}'!"
    except Exception as e:
        raise AssertionError(f"Gagal mengambil/memverifikasi baris tabel: {e}")

    # 4. Verifikasi setiap baris
    matched_all = True
    
    # === PERBAIKAN PENTING DI SINI ===
    # 4a. Ubah pola regex. Hilangkan '^' (start of string) agar menjadi substring match (mengandung)
    # Kita menggunakan re.search() di bawah, jadi pola tidak perlu mengandung '^' atau '$'
    pattern = re.compile(rf"{query_text}", re.IGNORECASE)
    
    print(f"🔎 Memverifikasi {len(rows)} hasil...")

    for i, row in enumerate(rows, start=1):
        cells = row.find_elements(By.TAG_NAME, "td")
        if not cells: continue

        # Asumsi kolom nama ada di kolom pertama
        cell_text = cells[0].text.strip() 
        
        # 4b. Menggunakan re.search() untuk mencari pola di mana pun dalam string
        if not pattern.search(cell_text):
            matched_all = False
            print(f"❌ Row {i} ('{cell_text}') TIDAK MENGANDUNG query '{query_text}'")

    # 5. Hasil Akhir
    assert matched_all, "❌ Ada hasil pencarian yang tidak sesuai query!"
    print(f"✅ Semua {len(rows)} hasil pencarian MENGANDUNG kata kunci '{query_text}'.")
    print(f"{'='*60}\n")


def perform_search_and_verify(driver, wait, query_text):
    """
    Melakukan pencarian pada input field dan memverifikasi hasilnya.
    """
    print(f"\n{'='*60}")
    print(f"🎯 Memulai Pencarian User dengan Query: '{query_text}'")
    print(f"{'='*60}")

    # 1. Cari input search
    search_locator = (By.CSS_SELECTOR, "form input[name='query']")
    try:
        search_input = wait.until(EC.presence_of_element_located(search_locator))
    except TimeoutException:
        raise RuntimeError(f"❌ Tidak menemukan input search dengan locator: {search_locator}.")

    # 2. Ketik query dan KIRIM (ENTER)
    print(f"🔍 Mengetik query: '{query_text}' dan menekan ENTER...")
    search_input.clear()
    search_input.send_keys(query_text)
    search_input.send_keys(Keys.ENTER)

    time.sleep(2) 

    # 3. Ambil baris tabel
    try:
        table = wait.until(EC.presence_of_element_located((By.TAG_NAME, "table")))
        rows = table.find_elements(By.CSS_SELECTOR, "tbody tr")
        
        assert rows, f"❌ Tidak ada hasil (row) ditemukan setelah pencarian dengan query '{query_text}'!"
    except Exception as e:
        raise AssertionError(f"Gagal mengambil/memverifikasi baris tabel: {e}")

    # 4. Verifikasi setiap baris
    matched_all = True
    
    # Kompilasi pola regex untuk pencarian substring (case insensitive)
    pattern = re.compile(rf"{query_text}", re.IGNORECASE)
    
    print(f"🔎 Memverifikasi {len(rows)} hasil pencarian...")

    for i, row in enumerate(rows, start=1):
        cells = row.find_elements(By.TAG_NAME, "td")
        if not cells: 
            continue # Lewati jika row kosong (misal: row placeholder loading)

        # Asumsi kolom nama/teks yang diverifikasi ada di kolom pertama (index 0)
        cell_text = cells[0].text.strip() 
        
        # Menggunakan re.search() untuk mencari pola di mana pun dalam string
        if not pattern.search(cell_text):
            matched_all = False
            print(f"❌ Row {i} ('{cell_text}') TIDAK mengandung query '{query_text}'")
            # Tidak perlu break; lanjutkan untuk log semua kegagalan

    # 5. Hasil Akhir
    assert matched_all, f"❌ Ditemukan {len(rows) - sum(not matched_all for row in rows)} hasil yang tidak sesuai query!"
    print(f"✅ Semua {len(rows)} hasil pencarian MENGANDUNG kata kunci '{query_text}'.")
    print(f"{'='*60}\n")


def find_row_by_name(driver, wait, name):
    """
    Mencari row berdasarkan nama, mendukung teks yang berada langsung di dalam TD
    maupun di dalam elemen anak (seperti <p> atau <div>) di dalam TD.
    """
    print(f"🔍 Mencari row dengan nama '{name}' menggunakan XPath yang robust...")
    
    # PERUBAHAN UTAMA DI SINI:
    # Menggunakan 'contains(., ...)' untuk mencari teks di dalam node saat ini (.) 
    # dan semua keturunannya, termasuk elemen anak (P, DIV, dll.).
    # Namun, karena kita ingin mencocokkan nama secara eksak (tidak hanya mengandung), 
    # kita gabungkan dengan 'normalize-space()' pada seluruh node.
    # Sayangnya, mencocokkan teks eksak dengan elemen anak seringkali sulit.
    
    # SOLUSI PALING STABIL (Mencari di dalam TD mana pun yang mengandung teks eksak):
    row_locator = (
        By.XPATH, 
        # Mencari TR yang memiliki TD yang mengandung (contains) teks nama
        # Catatan: Ini akan bekerja jika nama unik, namun bisa memuat 'Nama' yang merupakan 
        # substring dari 'Nama Lain'. Jika nama unik, ini aman.
        f"//table//tbody/tr[.//td[contains(normalize-space(.), '{name}')]]"
    )
    
    # Alternatif jika nama harus benar-benar eksak (lebih ketat, tapi bisa rentan spasi)
    # row_locator_strict = (
    #    By.XPATH, 
    #    f"//table//tbody/tr[.//td[normalize-space(.)='{name}']]"
    # )
    
    try:
        # Menggunakan locator yang lebih fleksibel: contains(normalize-space(.), ...)
        row = wait.until(EC.presence_of_element_located(row_locator))
        print(f"✅ Row dengan teks '{name}' ditemukan.")
        return row
    except TimeoutException:
        raise Exception(f"❌ Row dengan nama '{name}' tidak ditemukan!")    



def wait_for_toast(wait, timeout=5):
    """
    Menunggu dan memverifikasi Toastify success message.
    
    Args:
        wait: WebDriverWait instance
        timeout: Waktu tunggu maksimal (default: 5 detik)
    
    Returns:
        WebElement: Toast success element
    
    Raises:
        AssertionError: Jika toast tidak muncul dalam waktu timeout
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
    Klik elemen dengan retry dan scroll ke view.
    Menggunakan JavaScript untuk menghindari ElementClickInterceptedException.
    
    Args:
        driver: WebDriver instance
        element: WebElement yang akan diklik
        retries: Jumlah percobaan (default: 3)
        wait_time: Waktu tunggu antar retry dalam detik (default: 0.8)
    
    Raises:
        RuntimeError: Jika gagal klik setelah beberapa percobaan
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
