import pytest
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from tests.helper.edit_group_helper import *
from tests.helper.quiz_list_helper import navigate_to_page_button

@pytest.mark.usefixtures("login_as_admin_fixture")
def test_edit_group_add(login_as_admin_fixture):
    driver = login_as_admin_fixture
    wait = WebDriverWait(driver, 15)
    group_name = "Group D"

    navigate_to_page_button(driver, wait, "Quiz")


    # Panggil fungsi core action
    perform_add_group_and_verify(driver, wait, group_name)