# # File: tests/roles/admin/test_lesson_management.py

# import pytest
# from selenium.webdriver.support.ui import WebDriverWait

# # Asumsi kamu mengimpor fungsi helper dari lokasi yang sesuai
# from tests.helper.lesson_helper import delete_lesson_by_name_and_verify 

# @pytest.mark.lessons
# @pytest.mark.usefixtures("login_as_admin_fixture")
# def test_delete_multi_function_display_lesson(login_as_admin_fixture):
#     """
#     Skenario: Menghapus lesson 'Multi Function Display' sebagai Admin.
#     """
#     driver = login_as_admin_fixture
#     wait = WebDriverWait(driver, 15)

#     # Nama lesson yang akan dihapus
#     LESSON_NAME = "Multi Function Display"

#     # Panggil fungsi helper
#     delete_lesson_by_name_and_verify(driver, wait, lesson_name=LESSON_NAME)

#     # Jika fungsi helper berjalan tanpa error, test dianggap PASSED