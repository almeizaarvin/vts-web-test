from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support import expected_conditions as EC

from tests.helper.general_helper import safe_click, wait_for_toast


def perform_edit_quiz_question_and_verify(
    driver,
    wait,
    quiz_name: str,
    old_question: str,
    new_question: str
):
    """
    Cari quiz by name -> buka detail -> edit question -> save -> verify toast.
    """

    print("\n" + "=" * 60)
    print(f"🎯 Edit Quiz '{quiz_name}'")
    print("=" * 60)

    # cari row quiz
    row = find_quiz_row(driver, wait, quiz_name)

    # klik tombol edit quiz (button ke-2)
    edit_quiz_button = row.find_element(
        By.XPATH,
        ".//td[last()]//button[2]"
    )
    safe_click(driver, edit_quiz_button)

    print("✅ Quiz detail opened")

    # klik tombol edit question (button pertama di tabel question)
    edit_question_button = wait.until(
        EC.element_to_be_clickable((
            By.XPATH,
            "/html/body/div[1]/main/div/div/div[1]/div/div[2]/div[2]/div/div/div[2]/table/tbody/tr/td[3]/div/button[1]"
        ))
    )
    safe_click(driver, edit_question_button)

    print("✅ Edit question modal opened")

    # cari textarea question
    question_input = wait.until(
        EC.element_to_be_clickable((
            By.XPATH,
            "//textarea[@name='question']"
        ))
    )

    # verify old value
    current_value = question_input.get_attribute("value").strip()

    assert current_value == old_question, (
        f"Expected '{old_question}', got '{current_value}'"
    )

    # replace text
    question_input.click()
    question_input.send_keys(Keys.CONTROL, "a")
    question_input.send_keys(Keys.DELETE)
    question_input.send_keys(new_question)

    # verify updated
    wait.until(
        lambda d: question_input.get_attribute("value").strip() == new_question
    )

    print(f"✅ Question changed: {old_question} -> {new_question}")

    # klik save
    save_button = wait.until(
        EC.element_to_be_clickable((
            By.XPATH,
            "/html/body/div[1]/div/div[3]/div/div[2]/button[2]"
        ))
    )
    safe_click(driver, save_button)

    # verify toast success
    wait_for_toast(wait)

    print("✅ Quiz updated successfully")
    print("=" * 60 + "\n")


def find_quiz_row(driver, wait, quiz_name):
    """
    Cari row quiz berdasarkan text row.
    """

    rows = wait.until(
        EC.presence_of_all_elements_located(
            (By.XPATH, "//table/tbody/tr")
        )
    )

    for row in rows:
        row_text = row.text.strip()
        print("ROW:", row_text)

        if quiz_name.lower() in row_text.lower():
            return row

    raise AssertionError(f"Quiz '{quiz_name}' tidak ditemukan")