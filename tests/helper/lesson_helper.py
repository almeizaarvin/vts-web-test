# # File: tests/helper/lesson_helper.py (FINAL & TERSIMPLIFIKASI)

# from selenium.webdriver.common.by import By
# from selenium.webdriver.support import expected_conditions as EC
# from selenium.common.exceptions import NoSuchElementException, TimeoutException
# from selenium.webdriver.support.ui import WebDriverWait

# from tests.helper.edit_group_helper import safe_click, wait_for_toast
# from tests.helper.general_helper import navigate_to_page_button

# # Asumsi: safe_click, wait_for_toast, navigate_to_page_button sudah diimpor

# def delete_lesson_by_name_and_verify(driver, wait, lesson_name):
    
#     print(f"\n{'='*60}")
#     print(f"🎯 Memulai Skenario Hapus Lesson: {lesson_name}")
    
#     try:
#         navigate_to_page_button(driver, wait, "Lessons")
#         print("✅ Berhasil navigasi ke Halaman Lessons.")

#         # =================================================================
#         # 1. CEK DULU ROW DENGAN XPATH FLEKSIBEL (Case/Whitespace Tolerant)
#         # =================================================================
#         lower_lesson_name = lesson_name.lower()
        
#         # XPATH BARIS (Fleksibel): Menggunakan translate/normalize-space
#         row_xpath_template = (
#             "//tr[./td[contains("
#             "translate(normalize-space(.), 'ABCDEFGHIJKLMNOPQRSTUVWXYZ', 'abcdefghijklmnopqrstuvwxyz'), "
#             f"'{lower_lesson_name}'"
#             ")]]"
#         )
#         row_locator = (By.XPATH, row_xpath_template)
        
#         try:
#             # Tunggu dan temukan row
#             target_row = wait.until(EC.presence_of_element_located(row_locator))
#             print(f"🔍 Baris Lesson '{lesson_name}' berhasil ditemukan.")
#         except TimeoutException:
#             # Jika row tidak ditemukan, raise error spesifik
#             raise NoSuchElementException(
#                 f"Baris Lesson '{lesson_name}' GAGAL DITEMUKAN. Periksa apakah nama Lesson sudah benar di UI/DB (XPATH: {row_xpath_template})."
#             )
        
#         # =================================================================
#         # 2. CARI SVG DI DALAM ROW DENGAN XPATH GABUNGAN
#         # =================================================================
        
#         # XPATH SVG: Target akurat dari HTML
#         svg_locator_value = "//svg[@data-testid='DeleteIcon']" 
        
#         # Gabungkan XPATH menjadi satu string yang VALID
#         full_svg_xpath = row_xpath_template + svg_locator_value
        
#         print(f"DEBUG XPATH GABUNGAN: {full_svg_xpath}")
        
#         try:
#             # Tunggu hingga SVG muncul menggunakan XPath gabungan yang VALID
#             delete_svg = wait.until(EC.presence_of_element_located((By.XPATH, full_svg_xpath)))
            
#             # Mendapatkan parent element (Button) dari SVG
#             action_btn = delete_svg.find_element(By.XPATH, "./ancestor::button[1]")
            
#             # Pastikan tombol parent siap diklik
#             wait.until(EC.element_to_be_clickable(action_btn))
#             print("✅ Tombol Delete ditemukan (via XPath gabungan) dan siap diklik.")

#         except TimeoutException:
#              # Jika gagal, raise error yang jelas
#              raise NoSuchElementException(
#                  f"Gagal menemukan elemen SVG dengan data-testid='DeleteIcon' di baris Lesson: '{lesson_name}' setelah menunggu. "
#                  f"Periksa kembali data-testid atau masalah timing loading."
#              )

#         # =================================================================
#         # 3. Klik Tombol Aksi (Native dengan Fallback JS)
#         # =================================================================
#         try:
#             action_btn.click() 
#             print("➡️ Mengklik tombol DeleteIcon secara Native.")
#         except Exception:
#             # Fallback ke JavaScript jika klik native gagal
#             driver.execute_script("arguments[0].click();", action_btn)
#             print("➡️ Mengklik tombol DeleteIcon via JavaScript.")

#         # 4. Konfirmasi dialog
#         confirm_btn_locator = (By.XPATH, "//button[normalize-space()='Delete']")
#         confirm_btn = wait.until(EC.element_to_be_clickable(confirm_btn_locator))
        
#         safe_click(driver, confirm_btn) 
#         print("➡️ Mengklik tombol 'Delete' di dialog konfirmasi.")

#         # 5. Verifikasi Toast
#         wait_for_toast(wait)
#         print("🎉 Lesson berhasil dihapus. Toast sukses diverifikasi!")
        
#         return True

#     except Exception as e:
#         print(f"❌ Skenario Hapus Lesson GAGAL Total: {e}")
#         raise