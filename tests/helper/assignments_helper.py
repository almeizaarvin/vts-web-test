import pytest
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC

from tests.helper.edit_group_helper import safe_click, wait_for_toast
from tests.helper.quiz_list_helper import navigate_to_page_button

def add_course_to_assignment(driver, wait, course_name):
    # Implementasi helper Add Course (diadaptasi dari respons sebelumnya)
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
        print("➡️ Mengklik tombol yang mengandung 'Course'. Modal terbuka.")

        # 3. Cari input dengan placeholder/label/testid, lalu isi Course Testing
        # OPSI A: Mencari input berdasarkan name='nama' (berdasarkan trace HTML modal lain)

        # OPSI A: Mencari input berdasarkan name='nama' (berdasarkan trace HTML modal lain)
        course_input_locator = (By.NAME, 'nama')
        
        # OPSI B: Fallback XPATH (Jika name='nama' salah, gunakan type='text')
        # course_input_locator = (By.XPATH, "//input[@type='text' and not(@id='rnk')]")
        
        try:
            course_input = wait.until(EC.presence_of_element_located(course_input_locator))
            
            # Tambahkan wait untuk memastikan elemen dapat di-interact (clickable/writable)
            wait.until(EC.element_to_be_clickable(course_input))

        except TimeoutException:
            # Jika OPSI A gagal, coba lagi dengan OPSI B jika diperlukan, atau langsung raise error
            raise NoSuchElementException(
                "Gagal menemukan elemen INPUT untuk nama Course. Coba cek name/id/placeholder yang benar."
            )
        
        course_input.clear()
        course_input.send_keys(course_name)
        print(f"✅ Mengisi input Course dengan: '{course_name}'.")

        # 4. Cari tombol contain 'Create New' (case insensitive), lalu klik
        create_new_btn_locator = (By.XPATH, "//button[contains(translate(normalize-space(.), 'ABCDEFGHIJKLMNOPQRSTUVWXYZ', 'abcdefghijklmnopqrstuvwxyz'), 'create new')]")
        create_new_btn = wait.until(EC.element_to_be_clickable(create_new_btn_locator))
        
        safe_click(driver, create_new_btn)
        print("➡️ Mengklik tombol 'Create New'.")

        # 5. Pastikan keluar toast hijau
        wait_for_toast(wait)
        print("🎉 Course berhasil ditambahkan. Toast sukses diverifikasi!")
        
        return True

    except Exception as e:
        print(f"❌ Skenario Add Course GAGAL Total: {e}")
        raise