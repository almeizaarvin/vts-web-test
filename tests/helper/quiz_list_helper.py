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


def perform_add_new_quiz_and_delete_question(driver, wait):
    """
    Membuat kuis baru → LANGSUNG Edit pertanyaan default (Native Click) → Save → Verify toast success.
    """

    print("\n" + "="*60)
    print("🎯 Memulai: Edit Pertanyaan Default (Native Only)")
    print("="*60)

    # 1. Klik tombol Create New Quiz (Ini akan membuka quiz detail dan menampilkan tabel dengan 1 pertanyaan default)
    print("➡️ Membuat/Membuka Quiz Baru untuk mencapai tabel pertanyaan...")
    try:
        click_create_new_quiz(driver, wait)
        print("✅ Berada di halaman detail quiz.")
    except Exception as e:
        print(f"❌ Gagal membuat/membuka quiz baru: {e}")
        return False
    
    time.sleep(1) # Tunggu sebentar untuk loading konten tabel

    # 2. Cari row terakhir pada tabel (yang merupakan pertanyaan default)
    print("🔍 Mencari row tabel (pertanyaan default/terakhir)...")
    table_row_locator = (By.XPATH, "//table//tbody/tr")
    
    # Tunggu setidaknya satu baris muncul
    try:
        rows = wait.until(EC.presence_of_all_elements_located(table_row_locator))
    except TimeoutException:
        raise RuntimeError("❌ Tabel pertanyaan tidak ditemukan atau pertanyaan default tidak muncul.")

    if not rows:
        raise RuntimeError("❌ Tidak ada row pada tabel. Pertanyaan default tidak ditemukan.")

    # Ambil row pertama (atau terakhir, jika kamu yakin pertanyaan default selalu dihitung sebagai baris pertama/terakhir)
    # Kita ambil yang pertama/default, yaitu rows[0]
    default_row = rows[0]
    print(f"✅ Row default ditemukan. Total {len(rows)} pertanyaan.")

    # 3. KLIK TOMBOL EDIT (Hanya Native Click)
    print("✏️ Mencari tombol Edit (Ikon) pada row default...")
    
    # LOCATOR NATIVE UNTUK TOMBOL IKON EDIT: Target BUTTON yang berisi SVG EditIcon
    edit_btn_locator_relative = (
        By.XPATH,
        ".//button[.//svg[@data-testid='EditIcon'] or .//svg[@data-testid='ModeEditIcon']]"
    )
    
    # Cari elemen BUTTON di dalam scope default_row
    edit_btn = default_row.find_element(*edit_btn_locator_relative)
    
    # Tunggu hingga tombol benar-benar clickable
    wait.until(EC.element_to_be_clickable(edit_btn))
    
    safe_click(driver, edit_btn)
    print("📝 Tombol Edit diklik secara Native. Menunggu Modal Edit muncul...")
    
    # 4. Tunggu modal/dialog Edit muncul
    modal_locator = (By.XPATH, "//div[@role='dialog' and @aria-modal='true']")
    wait.until(EC.visibility_of_element_located(modal_locator))
    print("✅ Modal Edit Question berhasil muncul.")
    
    # 5. KLIK TOMBOL SAVE (Tanpa mengubah input apapun, hanya menyimpan ulang)
    print("💾 Mengklik tombol 'Save' di modal Edit...")

    # Locator Tombol Save (berdasarkan posisi button[2] di DialogActions)
    save_btn_locator = (By.XPATH, "//div[contains(@class, 'MuiDialogActions-root')]/button[2]")
    
    # Wait dan Klik Save
    save_btn = wait.until(EC.element_to_be_clickable(save_btn_locator))
    safe_click(driver, save_btn)
    print("✅ Tombol Save diklik.")

    # 6. WAJIB: Tunggu MODAL menghilang 
    wait.until(EC.invisibility_of_element_located(modal_locator))
    print("✅ Modal Edit Question berhasil ditutup.")
    time.sleep(1) # Tunggu sebentar untuk transisi DOM

    # 7. Tunggu toast success
    print("🔎 Menunggu Toast Success...")
    wait_for_toast(wait)
    print("✅ Toast Success muncul — Pertanyaan default berhasil diedit/disimpan ulang.")

    print("="*60 + "\n")

    return True

def perform_add_new_quiz_and_edit_question(driver, wait):
    """
    Membuat quiz baru → Edit pertanyaan default → Save → Verifikasi teks di tabel.
    Hanya menggunakan native click (safe_click).
    """

    print("\n" + "="*60)
    print("🎯 Memulai: Edit Pertanyaan Default (Native Only)")
    print("="*60)

    NEW_QUESTION_TEXT = " Edited"

    # ============================================================
    # 1. Buat New Quiz / Masuk ke Detail Quiz
    # ============================================================
    print("➡️ Membuat/Membuka quiz baru...")

    try:
        click_create_new_quiz(driver, wait)
        print("✅ Berada di halaman detail quiz.")
    except Exception as e:
        print(f"❌ Gagal membuat/membuka quiz baru: {e}")
        return False

    time.sleep(1)

    # ============================================================
    # 2. Ambil row pertama (default question)
    # ============================================================
    print("🔍 Mencari pertanyaan default di tabel...")

    try:
        rows = wait.until(
            EC.presence_of_all_elements_located((By.XPATH, "//table//tbody/tr"))
        )
    except TimeoutException:
        raise RuntimeError("❌ Tabel pertanyaan tidak ditemukan.")

    if not rows:
        raise RuntimeError("❌ Tidak ada pertanyaan default di tabel.")

    default_row = rows[0]
    print(f"✅ Pertanyaan default ditemukan. Total pertanyaan: {len(rows)}")

    # ============================================================
    # 3. Klik tombol Edit di row pertama
    # ============================================================
    print("✏️ Klik tombol Edit pada row default...")

    edit_btn = default_row.find_element(By.XPATH, ".//button[contains(text(),'Edit')]")
    wait.until(EC.element_to_be_clickable(edit_btn))
    safe_click(driver, edit_btn)

    print("📝 Menunggu modal Edit muncul...")

    # ============================================================
    # 4. Isi Textarea Pertanyaan
    # ============================================================
    wait.until(
        EC.visibility_of_element_located(
            (By.XPATH, "//div[@role='dialog' and @aria-modal='true']")
        )
    )
    print("✅ Modal Edit terbuka.")

    print("📝 Mengedit pertanyaan...")

    textarea = wait.until(
        EC.presence_of_element_located(
            (By.XPATH, "//textarea[contains(text(),'Pertanyaan')]")
        )
    )

    textarea.clear()
    textarea.send_keys(NEW_QUESTION_TEXT)

    print(f"✅ Teks pertanyaan diubah menjadi: 'Pertanyaan {NEW_QUESTION_TEXT}'")

    # ============================================================
    # 5. Klik tombol Save
    # ============================================================
    print("💾 Klik tombol Save di modal...")

    save_btn = wait.until(
        EC.element_to_be_clickable(
            (By.XPATH, "//div[contains(@class, 'MuiDialogActions-root')]/button[2]")
        )
    )
    safe_click(driver, save_btn)

    print("✅ Perubahan disimpan.")

    # ============================================================
    # 6. Verifikasi hasil di tabel
    # ============================================================
    print("🔍 Verifikasi apakah teks edit muncul di tabel...")

    try:
        wait.until(
            EC.presence_of_element_located(
                (By.XPATH, "//table//td[contains(., 'Pertanyaan Edited')]")
            )
        )
        print("✅ Verifikasi BERHASIL.")
        return True

    except TimeoutException:
        print("❌ Verifikasi GAGAL: Teks tidak muncul di tabel setelah Save.")
        return False

    finally:
        print("="*60 + "\n")


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