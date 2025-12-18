from time import time
import pytest
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC

from tests.helper.edit_group_helper import safe_click, wait_for_toast
from tests.helper.quiz_list_helper import navigate_to_page_button

def add_course_to_assignment(driver, wait, course_name):
    """
    Menavigasi ke halaman Assignment, membuka modal Add Course,
    mengisi input dengan name='nama' secara robust, mengklik tombol 'CREATE NEW',
    dan memverifikasi course baru di dalam tabel.
    """

    print(f"\n{'='*60}")
    print(f"🎯 Memulai Skenario Add Course: {course_name}")
    
    try:
        # 1. Navigasi ke page Assignment
        navigate_to_page_button(driver, wait, "Assignments") 
        print("✅ Berhasil navigasi ke Halaman Assignments.")

        # 2. Cari button yang contain 'Course', lalu klik (Membuka Modal)
        add_course_btn_locator = (By.XPATH, "//button[contains(text(), 'Course')]")
        add_course_btn = wait.until(EC.element_to_be_clickable(add_course_btn_locator))
        safe_click(driver, add_course_btn)
        print("➡️ Mengklik tombol yang mengandung 'Course'. Modal Add Course terbuka.")
        
        # Tambahkan wait untuk modal visibility
        modal_locator = (By.XPATH, "//div[@role='dialog' and @aria-modal='true']")
        wait.until(EC.visibility_of_element_located(modal_locator))

        # 3. Cari input dengan name='nama', lalu isi Course Name (Robust Input)
        course_input_locator = (By.NAME, 'nama')
        
        try:
            course_input = wait.until(EC.presence_of_element_located(course_input_locator))
            wait.until(EC.element_to_be_clickable(course_input))

        except TimeoutException:
            raise NoSuchElementException(
                "Gagal menemukan elemen INPUT untuk nama Course dengan name='nama'."
            )
        
        print("📝 Mencoba clear input field...")
        
        # 1. Coba clear normal
        course_input.clear()

        # 2. Clear paksa (Ctrl+A + Delete) jika clear normal tidak cukup
        current_value = course_input.get_attribute('value')
        if current_value and len(current_value.strip()) > 0:
             print("⚠️ Clear normal gagal, menggunakan Ctrl+A + Delete.")
             course_input.send_keys(Keys.CONTROL + 'a')
             course_input.send_keys(Keys.DELETE)
             time.sleep(0.1) 

        # 3. Masukkan teks baru
        course_input.send_keys(course_name)
        print(f"✅ Mengisi input Course dengan: '{course_name}'.")

        # 4. Klik tombol 'Create New'
        print("💾 Mencari dan mengklik tombol 'CREATE NEW' di modal...")
        
        # Menggunakan XPath yang mencari BUTTON yang berisi SPAN dengan teks 'Create New' (Case Sensitive)
        create_new_btn_locator = (
            By.XPATH, 
            "//button[.//span[contains(text(), 'Create New')]]"
        ) 
        
        create_new_btn = wait.until(EC.element_to_be_clickable(create_new_btn_locator))

        safe_click(driver, create_new_btn)
        print("➡️ Mengklik tombol 'Create New'.")

        
        # =======================================================================
        # 5. VERIFIKASI BARU: Cari nama course di tabel
        # =======================================================================
        print(f"🔍 Memverifikasi course baru di tabel: '{course_name}'...")
        
        # Locator untuk mencari <td> yang mengandung nama course yang baru dibuat
        course_in_table_locator = (
            By.XPATH,
            f"//table//tbody//td[contains(., '{course_name}')]"
        )
        
        try:
            # Tunggu hingga nama course baru muncul di tabel
            wait.until(EC.presence_of_element_located(course_in_table_locator))
            print("🎉 Course berhasil ditambahkan. Course baru ditemukan di tabel!")
            
        except TimeoutException:
            # Jika tidak ditemukan setelah batas waktu tunggu
            raise TimeoutException(f"❌ Verifikasi GAGAL: Course '{course_name}' tidak ditemukan di tabel Assignment.")

        return True

    except Exception as e:
        print(f"❌ Skenario Add Course GAGAL Total: {e}")
        # Jika terjadi kegagalan, raise exception agar test fail
        raise

def perform_delete_course(driver, wait, course_name):
    """
    Mencari Course berdasarkan nama (menggunakan locator yang sama dengan Add), 
    mengklik tombol Delete (Icon) via JavaScript Executor, dan memverifikasi 
    course hilang dari tabel.
    """

    print(f"\n{'='*60}")
    print(f"🎯 Memulai Skenario Delete Course: {course_name} (Perbaikan Tracing Row)")
    print("="*60)
    
    # 1. Navigasi ke page Assignment (Jika belum di sana)
    try:
        navigate_to_page_button(driver, wait, "Assignments") 
        print("✅ Berhasil navigasi ke Halaman Assignments.")
    except Exception as e:
        print(f"❌ Gagal navigasi ke Assignment Page: {e}")
        return False
    
    # =======================================================================
    # 2. PERBAIKAN: Cari elemen TD yang mengandung Course Name, lalu dapatkan TR parent
    # =======================================================================
    print(f"🔍 Mencari cell (TD) yang mengandung course: '{course_name}'...")
    
    # Locator untuk TD
    course_cell_locator = (
        By.XPATH, 
        f"//table//tbody//td[contains(., '{course_name}')]"
    )
    
    try:
        # 2a. Temukan TD yang berisi nama course (locator yang sama dengan verifikasi ADD)
        course_cell = wait.until(EC.presence_of_element_located(course_cell_locator))
        
        # 2b. Dari TD, naik ke parent TR
        course_row = course_cell.find_element(By.XPATH, "./parent::tr")
        print(f"✅ Row (TR) untuk course '{course_name}' ditemukan melalui cell.")
        
    except TimeoutException:
        print(f"❌ Gagal menemukan cell course '{course_name}'. Tidak dapat menghapus.")
        return False
    
    # 3. Solusi Terakhir: Cari Tombol Delete (SVG Icon data-testid) dan Klik Paksa
    print("🗑️ Mencari dan mengklik tombol Delete (JS Executor)...")
    
    # Target: BUTTON yang berisi SVG Ikon dengan data-testid="DeleteForeverIcon"
    delete_btn_locator_relative = (
        By.XPATH, 
            f".//button[contains(@aria-label, 'Hapus Kelas Test Course') or contains(@aria-label, 'Hapus Kelas Test Course')]"
    )

    try:
        # Kita cari tombol Delete relatif terhadap course_row
        delete_btn = course_row.find_element(*delete_btn_locator_relative)
        
        # JIKA SAFE_CLICK GAGAL TERUS, GANTI DENGAN JAVASCRIPT EXECUTOR
        driver.execute_script("arguments[0].click();", delete_btn)
        print("✅ Tombol Delete (JS Click) dieksekusi. Menunggu modal konfirmasi...")
        
    except Exception as e:
        print(f"❌ Tombol Delete (JS Click) gagal: {e}")
        return False
    
    # 4. Konfirmasi Delete di Modal
    confirmation_modal_locator = (By.XPATH, "//div[@role='dialog' and .//h2[contains(text(), 'Delete') or contains(text(), 'Hapus')]]")
    wait.until(EC.visibility_of_element_located(confirmation_modal_locator))
    print("✅ Modal Konfirmasi Delete muncul.")

    # Mencari tombol konfirmasi "Delete" di dalam modal 
    confirm_delete_btn_locator = (
        By.XPATH, 
        "//div[contains(@class, 'MuiDialogActions-root')]//button[contains(translate(normalize-space(.), 'ABCDEFGHIJKLMNOPQRSTUVWXYZ', 'abcdefghijklmnopqrstuvwxyz'), 'delete') or contains(text(), 'Hapus')]"
    )

    try:
        confirm_delete_btn = wait.until(EC.element_to_be_clickable(confirm_delete_btn_locator))
        safe_click(driver, confirm_delete_btn)
        print("✅ Tombol konfirmasi Delete diklik.")

    except TimeoutException:
        print("❌ Tombol konfirmasi Delete tidak ditemukan di modal.")
        return False
    
    # 5. Verifikasi: Course harus hilang dari tabel
    print("🔎 Menunggu Course menghilang dari tabel...")
    
    try:
        # Tunggu hingga row course hilang (Staleness of element)
        # Kita menggunakan course_row yang ditemukan di Langkah 2
        wait.until(EC.staleness_of(course_row)) 
        print(f"🎉 Verifikasi BERHASIL: Course '{course_name}' berhasil dihapus dari tabel.")
        result = True
        
    except TimeoutException:
        print(f"❌ Verifikasi GAGAL: Course '{course_name}' masih terlihat di tabel setelah dihapus.")
        result = False

    print("="*60 + "\n")
    return True