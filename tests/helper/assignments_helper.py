from time import time
import pytest
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC


from tests.helper.edit_group_helper import safe_click
from tests.helper.general_helper import navigate_to_page_button, wait_for_toast
from tests.helper.quiz_list_helper import navigate_to_page_button
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException
from selenium.webdriver.common.keys import Keys
import time

from tests.helper.general_helper import navigate_to_page_button
from tests.helper.edit_group_helper import safe_click

from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.keys import Keys
from selenium.common.exceptions import TimeoutException
import time

from tests.helper.general_helper import navigate_to_page_button
from tests.helper.general_helper import safe_click


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
    Ensure course exists → delete → verify removed
    """

    print(f"\n{'='*60}")
    print(f"🎯 Memulai Skenario Delete Course: {course_name}")
    print("="*60)

    try:
        # ==========================================================
        # 1. NAVIGATE
        # ==========================================================
        navigate_to_page_button(driver, wait, "Assignments")

        # ==========================================================
        # 2. CHECK EXISTENCE
        # ==========================================================
        print(f"🔍 Checking if course exists: {course_name}")

        course_locator = (
            By.XPATH,
            f"//td[contains(normalize-space(.), '{course_name}')]"
        )

        course_exists = True
        try:
            wait.until(EC.presence_of_element_located(course_locator))
            print("✅ Course already exists")
        except TimeoutException:
            course_exists = False
            print("⚠️ Course not found → creating new one")

        # ==========================================================
        # 3. CREATE IF NOT EXISTS
        # ==========================================================
        if not course_exists:
            add_course_to_assignment(driver, wait, course_name)
            print("✅ Course created for delete test")

        # ==========================================================
        # 4. RE-FIND ROW (IMPORTANT)
        # ==========================================================
        course_row = wait.until(
            EC.presence_of_element_located(
                (By.XPATH, f"//tr[.//td[contains(normalize-space(.), '{course_name}')]]")
            )
        )

        # ==========================================================
        # 5. CLICK DELETE
        # ==========================================================
        delete_btn = wait.until(
            EC.element_to_be_clickable((
                By.XPATH,
                "/html/body/div[1]/main/div/div/div[1]/div/div[2]/div[2]/div/div/div/div[2]/div/div/div/div/table/tbody/tr/td[1]/div/button[1]"
            ))
        )

        driver.execute_script("arguments[0].click();", delete_btn)
        print("🗑️ Delete clicked (fixed xpath)")
        
        # ==========================================================
        # 6. CONFIRM MODAL
        # ==========================================================
        wait.until(
            EC.visibility_of_element_located((By.XPATH, "//div[@role='dialog']"))
        )

        confirm_btn = wait.until(
            EC.element_to_be_clickable(
                (By.XPATH, "//button[contains(., 'Delete') or contains(., 'Hapus')]")
            )
        )

        safe_click(driver, confirm_btn)

        # ==========================================================
        # 7. VERIFY DISAPPEAR
        # ==========================================================
        print("🔎 Waiting for course to disappear...")

        wait.until(
            EC.invisibility_of_element_located(course_locator)
        )

        print(f"🎉 SUCCESS: {course_name} deleted")

        return True

    except Exception as e:
        print(f"❌ Delete flow failed: {e}")
        raise

def perform_edit_course(driver, wait, old_course_name, new_course_name):
    """
    Edit course name + verify + rollback ke kondisi awal
    """

    print(f"\n{'='*60}")
    print(f"🎯 Memulai Skenario Edit Course")
    print(f"Old Name: {old_course_name}")
    print(f"New Name: {new_course_name}")
    print(f"{'='*60}")

    try:
        # ==========================================================
        # 1. ke Assignments
        # ==========================================================
        navigate_to_page_button(driver, wait, "Assignments")

        # ==========================================================
        # 2. cari row
        # ==========================================================
        course_row_locator = (
            By.XPATH,
            f"//table//tbody//tr[.//td[contains(normalize-space(.), '{old_course_name}')]]"
        )

        course_row = wait.until(
            EC.presence_of_element_located(course_row_locator)
        )

        print(f"✅ Row found: {old_course_name}")

        # ==========================================================
        # 3. klik edit
        # ==========================================================
        edit_btn = course_row.find_element(By.XPATH, ".//button[2]")
        safe_click(driver, edit_btn)

        wait.until(EC.visibility_of_element_located((By.XPATH, "//div[@role='dialog']")))

        # ==========================================================
        # 4. input edit
        # ==========================================================
        course_input = wait.until(
            EC.element_to_be_clickable((By.NAME, "nama"))
        )

        # clean input TOTAL (biar ga concat)
        course_input.click()
        course_input.send_keys(Keys.CONTROL, "a")
        course_input.send_keys(Keys.BACKSPACE)

        # extra safety
        driver.execute_script("arguments[0].value = '';", course_input)

        course_input.send_keys(new_course_name)

        print(f"✏️ Changed to: {new_course_name}")

        # ==========================================================
        # 5. save
        # ==========================================================
        save_btn = wait.until(
            EC.element_to_be_clickable((By.XPATH, "//button[contains(., 'Save')]"))
        )

        safe_click(driver, save_btn)

        # ==========================================================
        # 6. toast
        # ==========================================================
        wait_for_toast(wait)

        # ==========================================================
        # 7. VERIFY UPDATED NAME (IMPORTANT)
        # ==========================================================
        print("🔍 Verifying updated name...")

        updated_locator = (
            By.XPATH,
            f"//table//tbody//td[contains(normalize-space(.), '{new_course_name}')]"
        )

        wait.until(EC.presence_of_element_located(updated_locator))

        print(f"✅ Verified: {new_course_name}")

        # ==========================================================
        # 8. ROLLBACK (balikin ke nama awal)
        # ==========================================================
        print("🔁 Rolling back to original name...")

        # IMPORTANT: re-fetch table row AFTER re-render
        old_row_locator = (
            By.XPATH,
            f"//table//tbody//tr[.//td[contains(normalize-space(.), '{new_course_name}')]]"
        )

        old_row = wait.until(EC.presence_of_element_located(old_row_locator))

        edit_btn = old_row.find_element(By.XPATH, ".//button[2]")
        safe_click(driver, edit_btn)

        wait.until(EC.visibility_of_element_located((By.XPATH, "//div[@role='dialog']")))

        course_input = wait.until(
            EC.element_to_be_clickable((By.NAME, "nama"))
        )

        course_input.click()
        course_input.send_keys(Keys.CONTROL, "a")
        course_input.send_keys(Keys.BACKSPACE)
        driver.execute_script("arguments[0].value = '';", course_input)

        course_input.send_keys(old_course_name)

        save_btn = wait.until(
            EC.element_to_be_clickable((By.XPATH, "//button[contains(., 'Save')]"))
        )

        safe_click(driver, save_btn)

        wait_for_toast(wait)

        # ==========================================================
        # 9. FINAL VERIFY rollback
        # ==========================================================
        wait.until(
            EC.presence_of_element_located(
                (By.XPATH, f"//td[contains(normalize-space(.), '{old_course_name}')]")
            )
        )

        print(f"🔁 Rollback success: {old_course_name}")

        print("=" * 60)
        return True

    except Exception as e:
        print(f"❌ FAILED edit course flow: {e}")
        raise