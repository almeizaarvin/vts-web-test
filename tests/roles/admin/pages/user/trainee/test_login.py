import os
from datetime import datetime
import pytest
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC


@pytest.mark.usefixtures("login_as_admin")
def test_login(login_as_admin):
    """Pastikan login berhasil dan halaman user list tampil"""

    driver = login_as_admin
    wait = WebDriverWait(driver, 10)

    # ✅ Verifikasi URL sudah benar
    assert "userlist?pageId=0" in driver.current_url, (
        f"URL tidak sesuai: {driver.current_url}"
    )

    # ✅ Pastikan tabel user muncul
    table = wait.until(EC.presence_of_element_located((By.TAG_NAME, "table")))
    assert table is not None, "Tabel user tidak ditemukan!"
