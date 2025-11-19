# import pytest
# from selenium.webdriver.support.ui import WebDriverWait
# from selenium.webdriver.common.by import By
# from selenium.webdriver.support import expected_conditions as EC
# # Asumsi semua helper sudah diimport.
# # Contoh:
# # from your_module.base_helper import safe_click, wait_for_toast
# # from your_module.user_list_helper import select_current_date_in_dialog, select_mui_dropdown_option 
# from tests.helper.edit_group_helper import * # Menggunakan import yang kamu sediakan

# # Pastikan Anda sudah menambahkan fungsi select_mui_dropdown_option ke file helper Anda!

# # ======================================================
# # TEST ADD TRAINEE (PENGISIAN DATA LENGKAP)
# # ======================================================
# @pytest.mark.usefixtures("login_as_admin_fixture")
# def test_add_trainee_data_entry(login_as_admin_fixture):
#     driver = login_as_admin_fixture
#     wait = WebDriverWait(driver, 15)

#     # Pastikan kita di halaman userlist
#     wait.until(lambda d: "userlist?pageId=0" in d.current_url)
#     print("📄 Halaman userlist terbuka")

#     # 1. Cari dan klik tombol "Add Trainee"
#     print("🔍 Mencari dan mengklik tombol 'Add Trainee'…")
#     add_trainee_btn = wait.until(
#         EC.element_to_be_clickable((By.XPATH, "//button[.//span[contains(text(), 'Add Trainee')]]"))
#     )
#     safe_click(driver, add_trainee_btn)
#     print("🟩 Tombol 'Add Trainee' diklik. Menunggu form muncul...")

#     # Tunggu form dialog muncul
#     wait.until(EC.presence_of_element_located((By.NAME, "nama")))

#     # 2. Isi Semua Input Field Biasa
#     print("✍️ Mengisi data Trainee...")
    
#     fields = {
#         "nama": "Trainee Test Auto",
#         "identityNumber": "123",
#         "email": "test@gmail.com",
#         "username": "traineetest",
#         "password": "testuser"
#     }

#     for name, value in fields.items():
#         input_field = wait.until(EC.presence_of_element_located((By.NAME, name)))
#         input_field.clear()
#         input_field.send_keys(value)
#         print(f"    -> Input {name} diisi: {value}")
        
#     # 3. Handle Date Picker (birthDate)
#     select_current_date_in_dialog(driver, wait) 
    
#     # 4. Handle Dropdown Gender (TAMBAHAN BARU)
#     # Kita pilih 'Male' sesuai dengan opsi di screenshot
#     select_mui_dropdown_option(driver, wait, input_name="gender", option_text="Male")
    
#     print("\n✅ Semua isian form (termasuk dropdown) berhasil diisi.")
    
#     # --- Opsional: Klik Save dan Verifikasi ---
#     # print("💾 Mengklik tombol Save...")
#     # save_btn = wait.until(EC.element_to_be_clickable((By.XPATH, "//button[.//span[text()='Save']]")))
#     # safe_click(driver, save_btn)
#     # wait_for_toast(wait)
    
#     # close_dialog(driver, wait) # Tutup jika berhasil save