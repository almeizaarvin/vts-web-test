import time
from selenium.webdriver import Keys
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException

from tests.helper.general_helper import navigate_to_page_button, wait_for_toast


# =========================================================
# NAVIGATE LESSONS → OTHERS
# =========================================================
def navigate_to_lessons_others(driver, wait):
    print("➡️ Navigasi ke Subpage 'Others' dalam Lessons...")

    others_tab_locator = (
        By.XPATH,
        "//button[contains(text(), 'Others')]"
    )

    try:
        others_tab = wait.until(
            EC.element_to_be_clickable(others_tab_locator)
        )

        driver.execute_script("arguments[0].scrollIntoView(true);", others_tab)
        driver.execute_script("arguments[0].click();", others_tab)

        print("✅ Berhasil pindah ke subpage 'Others'.")

    except TimeoutException:
        raise RuntimeError("❌ Gagal navigasi ke Lessons → Others")


# =========================================================
# ADD LESSON
# =========================================================
def perform_add_chapter(driver, wait, chapter_name, module_name):

    print("\n" + "=" * 60)
    print("🎯 LESSONS - ADD FLOW")
    print(f"Chapter: {chapter_name}")
    print(f"Module : {module_name}")
    print("=" * 60)

    try:
        # =====================================================
        # 1. Main tab Lessons
        # =====================================================
        navigate_to_page_button(driver, wait, "Lessons")
        time.sleep(1)

        # =====================================================
        # 2. Subtab Others
        # =====================================================
        navigate_to_lessons_others(driver, wait)
        time.sleep(1)

        # =====================================================
        # 3. Add Chapter button (contains Chapter)
        # =====================================================
        add_btn = wait.until(
            EC.element_to_be_clickable((
                By.XPATH,
                "//button[contains(., 'Chapter')]"
            ))
        )

        driver.execute_script("arguments[0].click();", add_btn)

        print("➕ Modal Add Chapter opened")

        # =====================================================
        # 4. Get all inputs with id containing ':r'
        # input[0] = chapter
        # input[1] = module
        # =====================================================
        inputs = wait.until(
            EC.presence_of_all_elements_located((
                By.XPATH,
                "//input[contains(@id, ':r')]"
            ))
        )

        if len(inputs) < 2:
            raise Exception("❌ Input Chapter / Module tidak ditemukan")

        chapter_input = inputs[0]
        module_input = inputs[1]

        # =====================================================
        # 5. Fill Chapter
        # =====================================================
        chapter_input.click()
        chapter_input.clear()
        chapter_input.send_keys(chapter_name)

        print(f"✅ Chapter filled: {chapter_name}")

        # =====================================================
        # 6. Fill Module
        # =====================================================
        module_input.click()
        module_input.clear()
        module_input.send_keys(module_name)

        print(f"✅ Module filled: {module_name}")

        # =====================================================
        # 7. Click Create
        # =====================================================
        create_btn = wait.until(
            EC.element_to_be_clickable((
                By.XPATH,
                "//button[contains(., 'Create')]"
            ))
        )

        driver.execute_script("arguments[0].click();", create_btn)

        print("🚀 Create clicked")

        # =====================================================
        # 8. Verify table
        # =====================================================
        time.sleep(2)

        rows = driver.find_elements(By.XPATH, "//table//tbody/tr")
        assert rows, "❌ No rows found"

        found_chapter = False
        found_module = False

        for row in rows:
            text = row.text.strip()

            if chapter_name in text:
                found_chapter = True

            if module_name in text:
                found_module = True

        assert found_chapter, f"❌ Chapter '{chapter_name}' not found"
        assert found_module, f"❌ Module '{module_name}' not found"

        print("🎉 LESSON CREATED SUCCESSFULLY")
        print("=" * 60)

        return True

    except TimeoutException as e:
        print(f"❌ TIMEOUT: {e}")
        return False

    except Exception as e:
        print(f"❌ FAILED: {e}")
        raise


def perform_edit_chapter(
    driver,
    wait,
    original_name,
    edited_name,
):

    print("\n" + "=" * 60)
    print("🎯 LESSONS - EDIT CHAPTER")
    print("=" * 60)

    try:

        # =====================================================
        # 1. Main tab Lessons
        # =====================================================
        navigate_to_page_button(driver, wait, "Lessons")
        time.sleep(1)

        # =====================================================
        # 2. Others tab
        # =====================================================
        navigate_to_lessons_others(driver, wait)
        time.sleep(1)

        edit_chapter(driver, wait, original_name, edited_name)

        # revert
        edit_chapter(driver, wait, edited_name, original_name)

        print("🎉 EDIT CHAPTER SUCCESS")
        print("=" * 60)

        return True

    except TimeoutException as e:
        print(f"❌ TIMEOUT : {e}")
        return False

    except Exception as e:
        print(f"❌ FAILED : {e}")
        raise


def edit_chapter(driver, wait, old_name, new_name):

    # =====================================================
    # Cari row chapter
    # =====================================================

    rows = wait.until(
        EC.presence_of_all_elements_located(
            (By.XPATH, "//table//tbody/tr")
        )
    )

    target_row = None

    for row in rows:

        text = row.text.strip()
        print("ROW:", text)

        if old_name in text:
            target_row = row
            break

    assert target_row is not None, (
        f"Chapter '{old_name}' tidak ditemukan"
    )

    print(f"✅ Chapter ditemukan : {old_name}")

    # =====================================================
    # Klik Edit
    # =====================================================

    edit_button = target_row.find_element(
        By.XPATH,
        ".//td[1]//button[2]"
    )

    driver.execute_script(
        "arguments[0].click();",
        edit_button
    )

    print("✏️ Edit dialog opened")

    # =====================================================
    # Input nama
    # =====================================================

    name_input = wait.until(
        EC.element_to_be_clickable(
            (
                By.NAME,
                "nama"
            )
        )
    )

    current_value = name_input.get_attribute("value")

    assert current_value == old_name, (
        f"Expected '{old_name}', got '{current_value}'"
    )

    name_input.click()
    name_input.send_keys(Keys.CONTROL, "a")
    name_input.send_keys(Keys.DELETE)
    name_input.send_keys(new_name)

    print(f"✅ Chapter renamed : {old_name} -> {new_name}")

    # =====================================================
    # Save
    # =====================================================

    save_button = wait.until(
        EC.element_to_be_clickable(
            (
                By.XPATH,
                "/html/body/div[1]/div/div[3]/div/div[2]/div/button[2]"
            )
        )
    )

    driver.execute_script(
        "arguments[0].click();",
        save_button
    )

    wait_for_toast(wait)

    print("✅ Save success")

    time.sleep(1)