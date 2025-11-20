import pytest
from selenium.webdriver.support.ui import WebDriverWait
from tests.helper.edit_group_helper import * 


@pytest.mark.usefixtures("login_as_admin_fixture")
def test_edit_group_add(login_as_admin_fixture):
    driver = login_as_admin_fixture
    wait = WebDriverWait(driver, 15)
    group_name = "Group E (After Nav)"

    navigate_to_instructor_subpage(driver, wait) 

    perform_add_group_and_verify(driver, wait, group_name)