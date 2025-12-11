
import pytest
from selenium.webdriver.support.ui import WebDriverWait
from tests.helper.assignments_helper import add_course_to_assignment
from tests.helper.general_helper import navigate_to_page_button
from tests.helper.quiz_list_helper import delete_quiz_template_if_exists


@pytest.mark.usefixtures("login_as_admin_fixture")
def test_add_new_course(login_as_admin_fixture):
    """
    Test case untuk menambah course baru dari halaman Assignment dan memverifikasi notifikasi sukses.
    """
    driver = login_as_admin_fixture
    wait = WebDriverWait(driver, 15) # Default wait 15 detik

    # Tentukan nama course yang akan diuji
    TEST_COURSE_NAME = "Course Testing"
    
    # Panggil fungsi helper untuk melakukan seluruh skenario Add Course
    result = perform_delete_course(driver, wait, course_name=TEST_COURSE_NAME)

    # Verifikasi hasil: memastikan helper function mengembalikan True
    assert result is True, f"Failed to add course"