import pytest
from selenium.webdriver.support.ui import WebDriverWait
from .edit_group_helper import *

@pytest.mark.usefixtures("login_as_admin")
def test_delete_group(login_as_admin):
    """
    Skenario: Hapus Group (Group D)
    """
    driver = login_as_admin
    wait = WebDriverWait(driver, 15)
    group_name = "Group D"

    open_edit_dialog(driver, wait)
    deleted = delete_group_if_exists(driver, wait, group_name)

    close_dialog(driver, wait)
    open_edit_dialog(driver, wait)

    names = get_group_names(driver, wait)
    print(f"📋 Daftar group terbaru: {names}")
    assert group_name not in names, f"❌ '{group_name}' masih ada setelah dihapus!"
    if deleted:
        print(f"✅ '{group_name}' berhasil dihapus dan terverifikasi.")
    else:
        print(f"✅ '{group_name}' memang sudah tidak ada sejak awal.")
