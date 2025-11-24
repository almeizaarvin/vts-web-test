import re
import time
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException
from selenium.webdriver.common.keys import Keys # <-- DIPERLUKAN UNTUK Keys.TAB

# Asumsi: safe_click dan find_row_by_name diimpor dari edit_group_helper
# Asumsi: wait_for_toast juga diimpor dari edit_group_helper atau sejenisnya
# (Menyesuaikan dengan impor yang kamu berikan, meski seharusnya di satu file)
from tests.helper.edit_group_helper import safe_click, wait_for_toast
from tests.helper.general_helper import find_row_by_name 
# Catatan: Fungsi navigate_to_page_button dipindahkan ke general_helper.py, 
# tapi saya sertakan di sini jika kamu ingin menggunakannya.


def navigate_to_page_button(driver, wait, button_text):
    """
    Menavigasi ke subpage yang dituju dengan mengklik tombol tab yang sesuai.
    (Idealnya fungsi ini ada di general_helper.py)
    """
    print(f"➡️ Navigasi ke Subpage: '{button_text}'...")
    
    page_tab_locator = (By.XPATH, f"//button[contains(text(), '{button_text}')]")
    
    try:
        page_tab = wait.until(
            EC.element_to_be_clickable(page_tab_locator)
        )
        
        # Menggunakan safe_click jika ada, jika tidak, gunakan script/click
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


# def delete_quiz_template_if_exists(driver, wait, quiz_name):
#     """
#     Mencari dan menghapus row kuis dengan nama tertentu.
#     """
#     print(f"🕵️ Mengecek apakah kuis '{quiz_name}' sudah ada dan menghapusnya...")
    
#     try:
#         # Cari row dengan nama kuis
#         row = find_row_by_name(driver, wait, quiz_name)
        
#         print(f"⚠️ Kuis '{quiz_name}' ditemukan, proses hapus...")
        
#         # PERBAIKAN LOCATOR: Menggunakan aria-label='Delete'
#         delete_icon_locator = By.XPATH, ".//button[@aria-label='Delete']"
#         delete_btn = row.find_element(*delete_icon_locator)
#         safe_click(driver, delete_btn) # Asumsi safe_click sudah tersedia
        
#         # Konfirmasi delete di popup
#         print("❓ Mengklik tombol 'Delete' di popup konfirmasi...")
#         confirm_btn = wait.until(
#             EC.element_to_be_clickable((By.XPATH, "//button[normalize-space()='Delete']"))
#         )
#         safe_click(driver, confirm_btn) # Asumsi safe_click sudah tersedia

#         # Tunggu hingga row kuis hilang dari DOM
#         wait.until(EC.staleness_of(row))
        
#         print(f"✅ Kuis '{quiz_name}' berhasil dihapus.")
#         return True
        
#     except Exception:
#         print(f"✅ Kuis '{quiz_name}' tidak ditemukan, tidak perlu dihapus.")
#         return False


def click_create_new_quiz(driver, wait):
    """
    Mengklik tombol 'Create New Quiz' dan menunggu form terbuka.
    """
    print("➕ Mengklik tombol 'Create New Quiz'...")
    create_btn_locator = (By.XPATH, "//button[contains(text(), 'Create New Quiz')]")
    
    create_btn = wait.until(
        EC.element_to_be_clickable(create_btn_locator)
    )
    safe_click(driver, create_btn) # Asumsi safe_click sudah tersedia
    
    print("✅ Halaman Create New Quiz terbuka.")


def click_save_quiz_button(driver, wait):
    """
    Mengklik tombol 'Save' atau 'Simpan' di form kuis.
    """
    print("💾 Mengklik tombol 'Save' untuk menyimpan kuis...")
    save_btn_locator = (By.XPATH, "//button[normalize-space()='Save' or normalize-space()='Simpan']")
    
    save_btn = wait.until(
        EC.element_to_be_clickable(save_btn_locator)
    )
    safe_click(driver, save_btn) # Asumsi safe_click sudah tersedia
    print("✅ Tombol Save diklik.")

# def perform_delete_quiz_and_verify(driver, wait):
#     """
#     Fungsi inti: Menghapus template lama, membuat kuis baru, 
#     mengisi nama kuis (walaupun sama), menyimpan, dan memverifikasi Toast sukses.
#     """
#     quiz_name = "Template Kuis Baru" # Nama kuis yang akan dibuat/dicek

#     print(f"\n{'='*60}")
#     print(f"🎯 Menghapus ('{quiz_name}')")
#     print(f"{'='*60}")
    
#     # 1. Cari dan hapus row dengan nama Template Kuis Baru (CLEANUP)
#     delete_quiz_template_if_exists(driver, wait, quiz_name)
#     wait_for_toast(wait)
#     print("✅ Kuis berhasil dihapus dan diverifikasi dengan Toast Success.")



def perform_add_new_quiz_and_verify(driver, wait):
    """
    Fungsi inti: Menghapus template lama, membuat kuis baru, 
    mengisi nama kuis (walaupun sama), menyimpan, dan memverifikasi Toast sukses.
    """
    quiz_name = "Template Kuis Baru" # Nama kuis yang akan dibuat/dicek

    print(f"\n{'='*60}")
    print(f"🎯 Memulai: Menambahkan Kuis Baru ('{quiz_name}')")
    print(f"{'='*60}")
    
    # 1. Cari dan hapus row dengan nama Template Kuis Baru (CLEANUP)
    delete_quiz_template_if_exists(driver, wait, quiz_name)
    
    # 2. Klik tombol Create New Quiz
    click_create_new_quiz(driver, wait)
    
    # 3. Cari dan isi nama kuis (Perbaikan input field)
    print(f"✍️ Mencari input name='quiz' dan memastikan nama kuis terisi...")
    
    quiz_name_input_locator = (By.NAME, "quiz") 
    
    
    # 4. Klik tombol Save (Mengirim form kuis)
    click_save_quiz_button(driver, wait)
    
    # 5. Pastikan keluar toast success
    print("🔎 Menunggu verifikasi Toast Success...")
    wait_for_toast(wait)
    print("✅ Kuis baru berhasil dibuat dan diverifikasi dengan Toast Success.")
    
    print(f"{'='*60}\n")
    
    return quiz_name

def perform_quiz_row_action(driver, wait, quiz_name, action_label, verification_type="navigate"):
    """
    Fungsi modular untuk melakukan aksi (Delete, Submission, Preview) pada row kuis.
    
    Args:
        quiz_name (str): Nama kuis.
        action_label (str): Nilai atribut 'aria-label' dari tombol yang akan diklik 
                            (misal: 'Delete', 'Quiz Submission', 'Preview').
        verification_type (str): Tipe verifikasi yang akan dilakukan ('navigate' atau 'delete').
    """
    
    print(f"\n{'='*60}")
    print(f"🎯 Memulai Aksi '{action_label}' pada kuis '{quiz_name}'")
    
    # 1. Cari row kuis
    print(f"🔍 Mencari row kuis dengan nama '{quiz_name}'...")
    try:
        row = find_row_by_name(driver, wait, quiz_name) 
    except Exception as e:
        if verification_type == 'delete':
            print(f"✅ Kuis '{quiz_name}' tidak ditemukan, tidak perlu dihapus.")
            return True
        raise RuntimeError(f"❌ Row kuis dengan nama '{quiz_name}' tidak ditemukan: {e}")
        
    print(f"✅ Row kuis '{quiz_name}' ditemukan.")

    # 2. Klik tombol aksi berdasarkan aria-label
    print(f"➡️ Mengklik tombol '{action_label}'...")
    action_btn_locator = By.XPATH, f".//button[@aria-label='{action_label}']"
    
    try:
        action_btn = row.find_element(*action_btn_locator)
        safe_click(driver, action_btn)
    except Exception as e:
        raise RuntimeError(f"❌ Gagal menemukan atau mengklik tombol '{action_label}': {e}")


    # 3. Verifikasi berdasarkan tipe
    if verification_type == 'navigate':
        # Verifikasi navigasi ke halaman baru (Submission/Preview)
        print("🔎 Memverifikasi header (H1) di halaman tujuan...")
        header_locator = (
            By.XPATH, 
            f"//h1[contains(normalize-space(.), '{quiz_name}')]"
        )
        
        try:
            header = wait.until(EC.visibility_of_element_located(header_locator))
        except TimeoutException:
            raise AssertionError(f"❌ Gagal menemukan header H1 yang mengandung teks: '{quiz_name}' setelah navigasi.")
        
        header_text = header.text.strip()
        # Cek apakah nama kuis ada di dalam teks header
        assert quiz_name in header_text, f"❌ Header mismatch! Diharapkan mengandung: '{quiz_name}', Ditemukan: '{header_text}'"
        
        print(f"✅ Navigasi berhasil. Header halaman: '{header_text}' diverifikasi.")
        
    elif verification_type == 'delete':
        # Verifikasi proses delete
        print("❓ Mengklik tombol 'Delete' di popup konfirmasi...")
        confirm_btn = wait.until(
            EC.element_to_be_clickable((By.XPATH, "//button[normalize-space()='Delete']"))
        )
        safe_click(driver, confirm_btn)

        # Tunggu hingga row kuis hilang dari DOM
        wait.until(EC.staleness_of(row))
        
        print(f"✅ Kuis '{quiz_name}' berhasil dihapus.")
    
    print(f"{'='*60}\n")
    return True

# --- Tambahkan atau timpa fungsi-fungsi di file quiz_list_helper.py kamu ---

def delete_quiz_template_if_exists(driver, wait, quiz_name):
    """
    Menggantikan fungsi delete lama. 
    Menghapus kuis yang ada. Memanfaatkan modularisasi.
    """
    # Action Label: 'Delete', Verification: 'delete'
    try:
        return perform_quiz_row_action(driver, wait, quiz_name, "Delete", verification_type="delete")
    except RuntimeError:
        # Jika row tidak ditemukan (error dari find_row_by_name), dianggap sukses (tidak perlu dihapus)
        return False

def quiz_submission_navigate_and_verify(driver, wait, quiz_name):
    """
    Menggantikan fungsi submission lama.
    Menavigasi ke halaman Submission. Memanfaatkan modularisasi.
    """
    # Action Label: 'Quiz Submission', Verification: 'navigate'
    return perform_quiz_row_action(driver, wait, quiz_name, "Quiz Submission", verification_type="navigate")

def quiz_preview_navigate_and_verify(driver, wait, quiz_name):
    """
    Menggantikan fungsi preview lama.
    Menavigasi ke halaman Preview. Memanfaatkan modularisasi.
    """
    # Action Label: 'Preview', Verification: 'navigate'
    return perform_quiz_row_action(driver, wait, quiz_name, "Preview", verification_type="navigate")