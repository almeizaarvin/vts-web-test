# # --- Tambahkan atau modifikasi fungsi ini di file helper yang sesuai ---

# import pytest
# from selenium.webdriver.common.by import By
# from selenium.webdriver.support import expected_conditions as EC
# from selenium.common.exceptions import TimeoutException
# import time

# from tests.helper.edit_group_helper import safe_click, wait_for_toast
# from tests.helper.quiz_list_helper import navigate_to_page_button # (Hanya jika time.sleep masih dibutuhkan di safe_click atau find_row_by_name)
# from selenium.webdriver.support.ui import WebDriverWait

# # Asumsi: safe_click, find_row_by_name, navigate_to_page_button sudah diimpor/tersedia
# # Asumsi: wait_for_toast juga sudah tersedia untuk verifikasi sukses.



# @pytest.mark.usefixtures("login_as_admin_fixture")
# def test_action_quiz_submission(login_as_admin_fixture):
#     """
#     1. Mencari row kuis 'Auxiliary Console'.
#     2. Mengklik tombol dengan ikon ChecklistRtlIcon di dalam row tersebut.
#     3. Memverifikasi header (H1) di halaman tujuan.
#     """
#     driver = login_as_admin_fixture
#     wait = WebDriverWait(driver, 15)
    
#     navigate_to_page_button(driver, wait, "Quiz")

#     test_perform_review_edit_score_and_verify(driver, wait, quiz_name="Auxiliary Console")



# def test_perform_review_edit_score_and_verify(driver, wait, quiz_name):
#     """
#     Skenario End-to-End: Edit Skor pada Quiz Result (Kolom Terakhir).
#     1. Navigasi ke Quiz -> Result.
#     2. Ambil TD paling kanan di row pertama.
#     3. Klik tombol 'Review' di row tersebut.
#     4. Di halaman detail, klik tombol 'EditIcon' pertama.
#     5. Isi input 'score' dengan nilai baru.
#     6. Klik tombol 'Save'.
#     7. Ulangi klik 'EditIcon' dan verifikasi placeholder 'score' sudah berubah.
#     """
    
#     print(f"\n{'='*60}")
#     print(f"🎯 Memulai Skenario: Edit Skor Quiz Result ({quiz_name})")
    
#     try:
#         # 1. Navigasi ke Quiz -> Result
#         # (Asumsi sudah berada di halaman Quiz List atau Group Detail)
#         navigate_to_page_button(driver, wait, "Result")
#         print("✅ Berhasil navigasi ke Subpage: Result.")

#         # --- Aksi di Halaman Result ---
        
#         # 2. Ambil TD terakhir (kolom paling kanan) di row pertama
#         table_result_locator = (By.TAG_NAME, "table")
#         wait.until(EC.presence_of_element_located(table_result_locator))
        
#         # LOKATOR DIPERBAIKI: Mengambil TD terakhir (paling kanan) di TR pertama
#         last_td_locator = (By.CSS_SELECTOR, "tbody tr:first-child td:last-child")
#         first_row_last_td = wait.until(EC.presence_of_element_located(last_td_locator))
        
#         # 3. Cari tombol 'Review' dan klik
#         print(f"🔍 Mencari dan mengklik tombol 'Review' di row pertama...")
        
#         # LOKATOR DIPERBAIKI: Menggunakan wait.until untuk memastikan tombol siap diklik
#         review_btn_locator = (By.XPATH, "//button[.//svg[@aria-label='Review']]")
#         review_btn = wait.until(EC.element_to_be_clickable(review_btn_locator)) 
        
#         safe_click(driver, review_btn)
#         print("➡️ Berhasil mengklik tombol 'Review'. Pindah ke halaman detail...")

#         # --- Aksi di Halaman Detail Review ---

#         # 4. Cari tombol edit (EditIcon)
#         # LOKATOR DIPERBAIKI: Menggunakan data-testid="EditIcon" (sesuai prompt)
#         edit_icon_locator = (By.XPATH, "//button[.//svg[@data-testid='EditIcon']]")
        
#         # Ambil tombol edit pertama
#         edit_buttons = wait.until(EC.presence_of_all_elements_located(edit_icon_locator))
#         first_edit_btn = edit_buttons[0]
        
#         # Klik tombol edit
#         safe_click(driver, first_edit_btn)
#         print("✅ Berhasil mengklik tombol EditIcon pertama.")

#         # 5. Cari input 'score', simpan nilai lama, dan isi nilai baru
#         score_input_locator = (By.NAME, "score")
#         score_input = wait.until(EC.visibility_of_element_located(score_input_locator))
        
#         old_score = score_input.get_attribute("placeholder")
        
#         # Logika nilai baru
#         if old_score and old_score.isdigit():
#              new_score = "100" if int(old_score) < 100 else "90"
#         else:
#              new_score = "100"
             
#         print(f"✍️ Mengisi skor baru: Old Score='{old_score}', New Score='{new_score}'...")
#         score_input.clear()
#         score_input.send_keys(new_score)

#         # 6. Klik tombol Save
#         save_btn_locator = (By.XPATH, "//button[normalize-space()='Save']")
#         save_btn = driver.find_element(*save_btn_locator)
#         safe_click(driver, save_btn)
        
#         # VERIFIKASI DIBALIKKAN: Tunggu Toast sukses
#         wait_for_toast(wait) 
#         print("✅ Skor berhasil disimpan dan Toast Success diverifikasi.")

#         # --- Verifikasi Perubahan ---

#         # 7. Ulangi klik icon edit
#         wait.until(EC.element_to_be_clickable(first_edit_btn)) 
#         safe_click(driver, first_edit_btn)
#         print("🔎 Membuka kembali form edit untuk verifikasi...")

#         # 8. Cek apakah nilai di placeholder sudah berubah
#         score_input_recheck = wait.until(EC.visibility_of_element_located(score_input_locator))
#         verified_score = score_input_recheck.get_attribute("placeholder")
        
#         assert verified_score == new_score, f"❌ Verifikasi GAGAL! Diharapkan skor '{new_score}', Ditemukan '{verified_score}'."
        
#         print(f"🎉 Skenario SUKSES! Skor baru '{verified_score}' sudah tersimpan di placeholder.")
#         return True

#     except Exception as e:
#         print(f"❌ Skenario Edit Skor GAGAL Total: {e}")
#         raise