# import pytest
# from selenium.webdriver.common.by import By
# from selenium.webdriver.support.ui import WebDriverWait
# from selenium.webdriver.support import expected_conditions as EC

# @pytest.mark.usefixtures("login_as_admin")
# class TestAddQuizList:
#     def test_add_quiz_list(self, driver):
#         """Admin membuat quiz list baru"""
#         driver.get("http://192.168.100.33:3003/#/quiz/quiz-list")

#         driver.find_element(By.ID, "btnAddQuiz").click()
#         driver.find_element(By.ID, "inputQuizName").send_keys("Quiz Automation 1")
#         driver.find_element(By.ID, "btnSubmitQuiz").click()

#         notif = WebDriverWait(driver, 10).until(
#             EC.presence_of_element_located((By.CLASS_NAME, "alert-success"))
#         )
#         assert "berhasil" in notif.text.lower()
