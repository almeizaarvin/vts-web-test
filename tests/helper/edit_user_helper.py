from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.keys import Keys

def perform_edit_trainee_name_and_verify(
    driver,
    wait,
    original_name: str,
    edited_name: str
):
    """
    Cari trainee berdasarkan nama, edit, verify, lalu revert.
    """

    def edit_name(old_name, new_name):
        rows = wait.until(
            EC.presence_of_all_elements_located(
                (By.XPATH, "//table/tbody/tr")
            )
        )

        target_row = None

        for row in rows:
            if old_name in row.text:
                target_row = row
                break

        assert target_row is not None, f"Trainee '{old_name}' tidak ditemukan"

        # klik detail button (button pertama di kolom action)
        detail_button = target_row.find_element(
            By.XPATH, ".//td[last()]//button[1]"
        )
        detail_button.click()

        # klik edit
        edit_button = wait.until(
            EC.element_to_be_clickable(
                (By.XPATH, "/html/body/div[1]/div/div[3]/div/div[2]/div/button[3]")
            )
        )
        edit_button.click()

        # input nama
        name_input = wait.until(
            EC.element_to_be_clickable(
                (By.XPATH, '//*[@id="nama"]')
            )
        )

        # tunggu sampai enabled
        wait.until(lambda d: name_input.is_enabled())

        # clear pakai ctrl+a biar lebih stabil
        name_input.click()
        name_input.send_keys(Keys.CONTROL, "a")
        name_input.send_keys(Keys.BACKSPACE)

        name_input.send_keys(new_name)


        # save
        save_button = wait.until(
            EC.element_to_be_clickable(
                (By.XPATH, "/html/body/div[1]/div/div[3]/div/div[2]/div/button[2]")
            )
        )
        save_button.click()

        # verify updated
        updated_input = wait.until(
            EC.presence_of_element_located(
                (By.XPATH, '//*[@id="nama"]')
            )
        )

        actual_value = updated_input.get_attribute("value")

        assert actual_value == new_name, (
            f"Expected '{new_name}', got '{actual_value}'"
        )

        # close modal
        close_button = wait.until(
            EC.element_to_be_clickable(
                (By.XPATH, "/html/body/div[1]/div/div[3]/div/div[2]/div/button[1]")
            )
        )
        close_button.click()

    try:
        edit_name(original_name, edited_name)
        edit_name(edited_name, original_name)
    finally:
        # force close modal kalau masih kebuka
        try:
            close_button = driver.find_element(
                By.XPATH,
                "/html/body/div[1]/div/div[3]/div/div[2]/div/button[1]"
            )
            close_button.click()
        except:
            pass