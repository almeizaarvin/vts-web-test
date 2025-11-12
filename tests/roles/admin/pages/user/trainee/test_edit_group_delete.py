import pytest
from selenium.webdriver.support.ui import WebDriverWait
from tests.helper.edit_group_helper import *

@pytest.mark.usefixtures("login_as_admin_fixture")
def test_delete_group(login_as_admin_fixture):
    driver = login_as_admin_fixture
    wait = WebDriverWait(driver, 15)
    group_name = "Group D"

    open_edit_dialog(driver, wait)
    deleted = delete_group_if_exists(driver, wait, group_name)

    close_dialog(driver, wait)
    open_edit_dialog(driver, wait)

    assert group_name not in get_group_names(driver, wait), f"❌ '{group_name}' masih ada!"
    print(f"✅ '{group_name}' {'berhasil dihapus' if deleted else 'memang sudah tidak ada sejak awal'}.")
