"""
Helper functions for VTS UI Test - Quiz List Management.
Contains functions for quiz CRUD, question editing, and quiz row actions.
"""

import time
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException
from selenium.webdriver.common.keys import Keys

from tests.helper.general_helper import safe_click, wait_for_toast, find_row_by_name


def click_create_new_quiz(driver, wait):
    """Click the 'Create New Quiz' button and wait for the form to open."""
    print("➕ Mengklik tombol 'Create New Quiz'...")
    create_btn_locator = (By.XPATH, "//button[contains(text(), 'Create New Quiz')]")
    create_btn = wait.until(EC.element_to_be_clickable(create_btn_locator))
    safe_click(driver, create_btn)
    print("✅ Halaman Create New Quiz terbuka.")


def click_save_quiz_button(driver, wait):
    """Click the 'Save' or 'Simpan' button on the quiz form."""
    print("💾 Mengklik tombol 'Save' untuk menyimpan kuis...")
    save_btn_locator = (By.XPATH, "//button[normalize-space()='Save' or normalize-space()='Simpan']")
    save_btn = wait.until(EC.element_to_be_clickable(save_btn_locator))
    safe_click(driver, save_btn)
    print("✅ Tombol Save diklik.")


def perform_add_new_quiz_and_verify(driver, wait):
    """
    Core function: Delete old template, create new quiz, save, and verify toast success.
    """
    quiz_name = "Template Kuis Baru"

    print(f"\n{'='*60}")
    print(f"🎯 Memulai: Menambahkan Kuis Baru ('{quiz_name}')")
    print(f"{'='*60}")

    delete_quiz_template_if_exists(driver, wait, quiz_name)
    click_create_new_quiz(driver, wait)

    print(f"✍️ Mencari input name='quiz' dan memastikan nama kuis terisi...")
    quiz_name_input_locator = (By.NAME, "quiz")

    click_save_quiz_button(driver, wait)

    print("🔎 Menunggu verifikasi Toast Success...")
    wait_for_toast(wait)
    print("✅ Kuis baru berhasil dibuat dan diverifikasi dengan Toast Success.")
    print(f"{'='*60}\n")

    return quiz_name


def perform_add_new_quiz_and_delete_question(driver, wait):
    """
    Create new quiz → Edit default question (Native Click) → Save → Verify toast success.
    """
    print("\n" + "=" * 60)
    print("🎯 Memulai: Edit Pertanyaan Default (Native Only)")
    print("=" * 60)

    print("➡️ Membuat/Membuka Quiz Baru untuk mencapai tabel pertanyaan...")
    try:
        click_create_new_quiz(driver, wait)
        print("✅ Berada di halaman detail quiz.")
    except Exception as e:
        print(f"❌ Gagal membuat/membuka quiz baru: {e}")
        return False

    time.sleep(1)

    print("🔍 Mencari row tabel (pertanyaan default/terakhir)...")
    table_row_locator = (By.XPATH, "//table//tbody/tr")

    try:
        rows = wait.until(EC.presence_of_all_elements_located(table_row_locator))
    except TimeoutException:
        raise RuntimeError("❌ Tabel pertanyaan tidak ditemukan atau pertanyaan default tidak muncul.")

    if not rows:
        raise RuntimeError("❌ Tidak ada row pada tabel. Pertanyaan default tidak ditemukan.")

    default_row = rows[0]
    print(f"✅ Row default ditemukan. Total {len(rows)} pertanyaan.")

    print("✏️ Mencari tombol Edit (Ikon) pada row default...")
    edit_btn_locator_relative = (
        By.XPATH,
        "/html/body/div[1]/main/div/div/div[1]/div/div[2]/div[2]/div/div/div[2]/table/tbody/tr/td[3]/div/button[1]"
    )

    edit_btn = default_row.find_element(*edit_btn_locator_relative)
    wait.until(EC.element_to_be_clickable(edit_btn))
    safe_click(driver, edit_btn)
    print("📝 Tombol Edit diklik secara Native. Menunggu Modal Edit muncul...")

    modal_locator = (By.XPATH, "//div[@role='dialog' and @aria-modal='true']")
    wait.until(EC.visibility_of_element_located(modal_locator))
    print("✅ Modal Edit Question berhasil muncul.")

    print("💾 Mengklik tombol 'Save' di modal Edit...")
    save_btn_locator = (By.XPATH, "//div[contains(@class, 'MuiDialogActions-root')]/button[2]")
    save_btn = wait.until(EC.element_to_be_clickable(save_btn_locator))
    safe_click(driver, save_btn)
    print("✅ Tombol Save diklik.")

    wait.until(EC.invisibility_of_element_located(modal_locator))
    print("✅ Modal Edit Question berhasil ditutup.")
    time.sleep(1)

    print("=" * 60 + "\n")
    return True


def perform_add_new_quiz_and_edit_question(driver, wait):
    """
    Create new quiz → Edit default question → Save → Verify text in table.
    Only uses native click (safe_click).
    """
    print("\n" + "=" * 60)
    print("🎯 Memulai: Edit Pertanyaan Default (Native Only)")
    print("=" * 60)

    NEW_QUESTION_TEXT = " Edited"

    print("➡️ Membuat/Membuka quiz baru...")
    try:
        click_create_new_quiz(driver, wait)
        print("✅ Berada di halaman detail quiz.")
    except Exception as e:
        print(f"❌ Gagal membuat/membuka quiz baru: {e}")
        return False

    time.sleep(1)

    print("🔍 Mencari pertanyaan default di tabel...")
    try:
        rows = wait.until(EC.presence_of_all_elements_located((By.XPATH, "//table//tbody/tr")))
    except TimeoutException:
        raise RuntimeError("❌ Tabel pertanyaan tidak ditemukan.")

    if not rows:
        raise RuntimeError("❌ Tidak ada pertanyaan default di tabel.")

    default_row = rows[0]
    print(f"✅ Pertanyaan default ditemukan. Total pertanyaan: {len(rows)}")

    print("✏️ Klik tombol Edit pada row default...")
    edit_btn = default_row.find_element(By.XPATH, ".//button[contains(text(),'Edit')]")
    wait.until(EC.element_to_be_clickable(edit_btn))
    safe_click(driver, edit_btn)
    print("📝 Menunggu modal Edit muncul...")

    wait.until(EC.visibility_of_element_located((By.XPATH, "//div[@role='dialog' and @aria-modal='true']")))
    print("✅ Modal Edit terbuka.")

    print("📝 Mengedit pertanyaan...")
    textarea = wait.until(EC.presence_of_element_located((By.XPATH, "//textarea[contains(text(),'Pertanyaan')]")))
    textarea.clear()
    textarea.send_keys(NEW_QUESTION_TEXT)
    print(f"✅ Teks pertanyaan diubah menjadi: 'Pertanyaan {NEW_QUESTION_TEXT}'")

    print("💾 Klik tombol Save di modal...")
    save_btn = wait.until(
        EC.element_to_be_clickable((By.XPATH, "//div[contains(@class, 'MuiDialogActions-root')]/button[2]"))
    )
    safe_click(driver, save_btn)
    print("✅ Perubahan disimpan.")

    print("🔍 Verifikasi apakah teks edit muncul di tabel...")
    try:
        wait.until(EC.presence_of_element_located((By.XPATH, "//table//td[contains(., 'Pertanyaan Edited')]")))
        print("✅ Verifikasi BERHASIL.")
        return True
    except TimeoutException:
        print("❌ Verifikasi GAGAL: Teks tidak muncul di tabel setelah Save.")
        return False
    finally:
        print("=" * 60 + "\n")


def perform_quiz_row_action(driver, wait, quiz_name, action_label, verification_type="navigate"):
    """
    Modular function to perform actions (Delete, Submission, Preview) on a quiz row.

    Args:
        quiz_name (str): Name of the quiz.
        action_label (str): Value of the 'aria-label' attribute of the button to click
                           (e.g., 'Delete', 'Quiz Submission', 'Preview').
        verification_type (str): Type of verification ('navigate' or 'delete').
    """
    print(f"\n{'='*60}")
    print(f"🎯 Memulai Aksi '{action_label}' pada kuis '{quiz_name}'")

    print(f"🔍 Mencari row kuis dengan nama '{quiz_name}'...")
    try:
        row = find_row_by_name(driver, wait, quiz_name)
    except Exception as e:
        if verification_type == 'delete':
            print(f"✅ Kuis '{quiz_name}' tidak ditemukan, tidak perlu dihapus.")
            return True
        raise RuntimeError(f"❌ Row kuis dengan nama '{quiz_name}' tidak ditemukan: {e}")

    print(f"✅ Row kuis '{quiz_name}' ditemukan.")

    print(f"➡️ Mengklik tombol '{action_label}'...")
    action_btn_locator = By.XPATH, f".//button[@aria-label='{action_label}']"

    try:
        action_btn = row.find_element(*action_btn_locator)
        safe_click(driver, action_btn)
    except Exception as e:
        raise RuntimeError(f"❌ Gagal menemukan atau mengklik tombol '{action_label}': {e}")

    if verification_type == 'navigate':
        print("🔎 Memverifikasi header (H1) di halaman tujuan...")
        header_locator = (By.XPATH, f"//h1[contains(normalize-space(.), '{quiz_name}')]")

        try:
            header = wait.until(EC.visibility_of_element_located(header_locator))
        except TimeoutException:
            raise AssertionError(
                f"❌ Gagal menemukan header H1 yang mengandung teks: '{quiz_name}' setelah navigasi.")

        header_text = header.text.strip()
        assert quiz_name in header_text, \
            f"❌ Header mismatch! Diharapkan mengandung: '{quiz_name}', Ditemukan: '{header_text}'"

        print(f"✅ Navigasi berhasil. Header halaman: '{header_text}' diverifikasi.")

    elif verification_type == 'delete':
        print("❓ Mengklik tombol 'Delete' di popup konfirmasi...")
        confirm_btn = wait.until(
            EC.element_to_be_clickable((By.XPATH, "//button[normalize-space()='Delete']"))
        )
        safe_click(driver, confirm_btn)
        wait.until(EC.staleness_of(row))
        print(f"✅ Kuis '{quiz_name}' berhasil dihapus.")

    print(f"{'='*60}\n")
    return True


def delete_quiz_template_if_exists(driver, wait, quiz_name):
    """
    Delete a quiz if it exists. Leverages modular perform_quiz_row_action.
    """
    try:
        return perform_quiz_row_action(driver, wait, quiz_name, "Delete", verification_type="delete")
    except RuntimeError:
        return False


def quiz_submission_navigate_and_verify(driver, wait, quiz_name):
    """
    Navigate to the Submission page. Leverages modular perform_quiz_row_action.
    """
    return perform_quiz_row_action(driver, wait, quiz_name, "Quiz Submission", verification_type="navigate")


def quiz_preview_navigate_and_verify(driver, wait, quiz_name):
    """
    Navigate to the Preview page. Leverages modular perform_quiz_row_action.
    """
    return perform_quiz_row_action(driver, wait, quiz_name, "Preview", verification_type="navigate")
