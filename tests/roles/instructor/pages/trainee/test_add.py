# import pytest
# from selenium.webdriver.common.by import By
# from selenium.webdriver.support.ui import WebDriverWait
# from selenium.webdriver.support import expected_conditions as EC

# @pytest.mark.usefixtures("login_as_admin")
# class TestAddInstructor:
#     def test_add_instructor(self, driver):
#         """Admin menambahkan instructor baru"""
#         driver.get("http://192.168.100.33:3003/#/user/instructor/add")

#         driver.find_element(By.ID, "inputName").send_keys("Automation Instructor 1")
#         driver.find_element(By.ID, "inputEmail").send_keys("instructor_auto1@test.com")
#         driver.find_element(By.ID, "btnAddInstructor").click()

#         notif = WebDriverWait(driver, 10).until(
#             EC.presence_of_element_located((By.CLASS_NAME, "alert-success"))
#         )
#         assert "berhasil" in notif.text.lower()
