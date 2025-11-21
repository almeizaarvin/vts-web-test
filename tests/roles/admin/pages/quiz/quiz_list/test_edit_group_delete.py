import pytest
from selenium.webdriver.support.ui import WebDriverWait
from tests.helper.edit_group_helper import *
from tests.helper.quiz_list_helper import navigate_to_page_button

@pytest.mark.usefixtures("login_as_admin_fixture")
def test_delete_group(login_as_admin_fixture):
    driver = login_as_admin_fixture
    wait = WebDriverWait(driver, 15)
    group_name = "Group_Untuk_Hapus"
    
    navigate_to_page_button(driver, wait, "Quiz")

    # -----------------------------------------------------------
    # 🎯 STEP 1: SETUP (Pastikan Group ada sebelum Dihapus)
    # -----------------------------------------------------------
    print(f"\n--- SETUP: Mempersiapkan '{group_name}' untuk dihapus ---")
    open_edit_dialog(driver, wait)
    
    # 1a. Bersihkan jika sudah ada (untuk memastikan kita mulai dari kondisi bersih)
    delete_group_if_exists(driver, wait, group_name)
    
    # 1b. Tambahkan Group baru
    click_add_new_group(driver, wait)
    group_input = driver.find_element(By.NAME, "groupname")
    group_input.send_keys(group_name)
    click_save_button(driver, wait)
    
    # 1c. Refresh dan verifikasi Group berhasil dibuat
    close_dialog(driver, wait)
    open_edit_dialog(driver, wait)
    assert group_name in get_group_names(driver, wait), f"❌ SETUP GAGAL: '{group_name}' tidak ditemukan setelah add!"
    print(f"✅ Group '{group_name}' berhasil dibuat untuk test delete.")
    
    # -----------------------------------------------------------
    # 🎯 STEP 2: ACTION (Hapus Group)
    # -----------------------------------------------------------
    print(f"\n--- ACTION: Menghapus '{group_name}' ---")
    # Panggil helper delete yang sudah kita yakin akan menemukan group_name
    deleted = delete_group_if_exists(driver, wait, group_name)
    
    # -----------------------------------------------------------
    # 🎯 STEP 3: VERIFICATION
    # -----------------------------------------------------------
    print("\n--- VERIFIKASI: Memastikan group hilang ---")
    close_dialog(driver, wait)
    open_edit_dialog(driver, wait)
    
    names_after_delete = get_group_names(driver, wait)
    
    # ASSERTION 1: Group harusnya sudah tidak ada
    assert group_name not in names_after_delete, f"❌ '{group_name}' masih ditemukan setelah penghapusan!"
    
    # ASSERTION 2: Pastikan aksi delete benar-benar terjadi
    assert deleted is True, f"❌ Fungsi delete_group_if_exists mengindikasikan group tidak dihapus."
    
    print(f"✅ '{group_name}' berhasil dihapus dan diverifikasi.")
    close_dialog(driver, wait)