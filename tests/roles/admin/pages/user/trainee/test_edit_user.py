import pytest
from selenium.webdriver.support.ui import WebDriverWait
from tests.helper.edit_user_helper import perform_edit_trainee_name_and_verify


@pytest.mark.usefixtures("login_as_admin_fixture")
def test_edit_user(login_as_admin_fixture):
    """
    Test edit trainee name and revert back.
    """
    driver = login_as_admin_fixture
    wait = WebDriverWait(driver, 15)

    # pastikan di halaman user list trainee
    wait.until(lambda d: "userlist?pageId=0" in d.current_url)

    perform_edit_trainee_name_and_verify(
        driver,
        wait,
        original_name="Peserta",
        edited_name="Peserta Edited"
    )