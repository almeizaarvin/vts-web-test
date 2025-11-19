import pytest
import time
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from tests.helper.edit_group_helper import *


@pytest.mark.usefixtures("login_as_admin_fixture")
def test_toggle_status(login_as_admin_fixture):
    driver = login_as_admin_fixture
    wait = WebDriverWait(driver, 15)

    # Pastikan kita di halaman userlist
    wait.until(lambda d: "userlist?pageId=0" in d.current_url)
    print("📄 Halaman userlist terbuka")

    # 1. Cari row Peserta 6
    row = find_peserta_row(driver, wait) 

    # 2. Deteksi status saat ini dan klik tombol status
    current_status_btn = get_status_button(row)
    current_status = current_status_btn.text.strip()
    safe_click(driver, current_status_btn)
    print(f"🟩 Tombol status '{current_status}' diklik")

    # 3. Klik tombol Aksi (Activate / Deactivate) di popup konfirmasi
    target_status = click_status_action(driver, wait, current_status)
    
    # Beri waktu update backend
    # Note: idealnya, tunggu toast sukses (jika ada) atau tunggu hilangnya tombol konfirmasi
    # Kita pakai sleep sementara, tapi bisa diganti wait_for_toast jika toast-nya muncul di sini.
    wait_for_toast(wait, timeout=5) 

    # 4. Cari ulang row Peserta 6 (fresh DOM)
    print("🔄 Reload row Peserta 6 untuk verifikasi…")
    row = find_peserta_row(driver, wait)

    # 5. Pastikan status berubah sesuai target
    print(f"🔍 Mengecek apakah status berubah menjadi {target_status}…")
    
    updated_btn = get_status_button(row)
    assert updated_btn.text.strip() == target_status, f"❌ Status tidak berubah menjadi {target_status}"

    print(f"🟩 Status Peserta 6 berhasil berubah menjadi {target_status}!")