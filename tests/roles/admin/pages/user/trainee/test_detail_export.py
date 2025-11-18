# import pytest
# import os
# import time
# from selenium.webdriver.support.ui import WebDriverWait
# from selenium.webdriver.common.by import By
# from selenium.webdriver.support import expected_conditions as EC


# # ======================================================
# # Helper: cari row Peserta 6
# # ======================================================
# def find_peserta_row(driver, wait):
#     table = wait.until(EC.presence_of_element_located((By.TAG_NAME, "table")))
#     rows = table.find_elements(By.CSS_SELECTOR, "tbody tr")
#     assert rows, "❌ Tidak ada satupun baris data di tabel"

#     for row in rows:
#         cells = row.find_elements(By.TAG_NAME, "td")
#         if cells and cells[0].text.strip() == "Peserta 6":
#             return row

#     raise Exception("❌ Tidak menemukan row Peserta 6")


# # ======================================================
# # TEST EXPORT CSV
# # ======================================================
# # ======================================================
# # TEST EXPORT CSV (Kode yang sudah di-EDIT dengan SVG Test ID)
# # ======================================================
# @pytest.mark.usefixtures("login_as_admin_fixture")
# def test_export_csv_peserta(login_as_admin_fixture):
#     driver = login_as_admin_fixture
#     wait = WebDriverWait(driver, 15)

#     DOWNLOAD_DIR = "./downloads"  # sesuaikan kalau beda

#     # Pastikan halaman userlist
#     wait.until(lambda d: "userlist?pageId=0" in d.current_url)
#     print("📄 Halaman userlist terbuka")

#     # ======================================================
#     # 1) Cari row Peserta
#     # ======================================================
#     print("🔍 Mencari row Peserta 6…")
#     row = find_peserta_row(driver, wait)
#     print("🟩 Row Peserta 6 ditemukan")

#     # ======================================================
#     # 2) Klik See Details
#     # ======================================================
#     print("🔍 Mencari tombol See Details…")

#     details_btn = None

#     for td in row.find_elements(By.TAG_NAME, "td"):
#         try:
#             div = td.find_element(By.TAG_NAME, "div")
#             # Mencari tombol See Details berdasarkan aria-label
#             btn = div.find_element(By.CSS_SELECTOR, "button[aria-label='See Details']")
#             details_btn = btn
#             break
#         except:
#             continue

#     assert details_btn, "❌ Tidak menemukan button dengan aria-label='See Details' di dalam td/div"

#     driver.execute_script("arguments[0].scrollIntoView({block:'center'});", details_btn)
#     driver.execute_script("arguments[0].click();", details_btn)

#     print("🟩 Tombol See Details diklik")

#     # ======================================================
#     # 3) Cari tombol Export (dengan mencari SVG Icon dan naik 2 parent)
#     # ======================================================
#     print("🔍 Mencari tombol Export via SVG Icon…")

#     # 1. Cari elemen SVG dengan data-testid="FileDownloadIcon"
#     svg_icon = wait.until(
#         EC.presence_of_element_located((
#             By.XPATH,
#             "//svg[@data-testid='FileDownloadIcon']"
#         ))
#     )
    
#     # 2. Naik dua tingkat parent (dari SVG ke span, dari span ke button)
#     # Gunakan .find_element(By.XPATH, "./..") atau "../.."
#     export_btn = svg_icon.find_element(By.XPATH, "./..").find_element(By.XPATH, "./..")
    
#     # Pastikan elemen yang ditemukan adalah tombol (opsional tapi disarankan)
#     if export_btn.tag_name != 'button':
#         raise Exception("❌ Gagal mendapatkan elemen tombol 'Export' yang benar!")


#     # Eksekusi klik
#     driver.execute_script("arguments[0].scrollIntoView({block:'center'});", export_btn)
#     driver.execute_script("arguments[0].click();", export_btn)

#     print("🟩 Tombol Export (via SVG) diklik")

#     # ======================================================
#     # 4) Cek file CSV terdownload
#     # ======================================================
#     print("📥 Menunggu file CSV ter-download…")

#     timeout = time.time() + 10
#     downloaded_file = None

#     while time.time() < timeout:
#         time.sleep(0.5)
#         for filename in os.listdir(DOWNLOAD_DIR):
#             if filename.endswith(".csv"):
#                 downloaded_file = filename
#                 break
#         if downloaded_file:
#             break

#     assert downloaded_file, "❌ CSV tidak ditemukan di folder download!"

#     print(f"🟩 File CSV berhasil di-download: {downloaded_file}")