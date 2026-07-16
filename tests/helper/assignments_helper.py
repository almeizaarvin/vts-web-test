"""
Helper functions for VTS UI Test - Assignment Management.
Contains functions for course CRUD operations on the Assignment page.
"""

import time
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException

from tests.helper.general_helper import safe_click, wait_for_toast


def add_course_to_assignment(driver, wait, course_name):
    """
    Add a new course to the Assignment page.

    Args:
        driver: WebDriver instance
        wait: WebDriverWait instance
        course_name: Name of the course to add

    Returns:
        bool: True if course was added successfully

    Raises:
        AssertionError: If toast verification fails
    """
    print(f"\n{'='*60}")
    print(f"🎯 Memulai: Menambahkan Course '{course_name}'")
    print(f"{'='*60}")

    # 1. Click 'Add Course' button
    print("➕ Mengklik tombol 'Add Course'...")
    add_course_btn = wait.until(
        EC.element_to_be_clickable((By.XPATH, "//button[contains(text(), 'Add Course')]"))
    )
    safe_click(driver, add_course_btn)
    print("✅ Tombol Add Course diklik.")

    # 2. Fill course name
    print(f"✍️ Mengisi nama course: '{course_name}'...")
    course_name_input = wait.until(
        EC.presence_of_element_located((By.XPATH, "//input[@name='courseName']"))
    )
    course_name_input.clear()
    course_name_input.send_keys(course_name)

    # 3. Click 'Save' button
    print("💾 Mengklik tombol 'Save'...")
    save_btn = wait.until(
        EC.element_to_be_clickable((By.XPATH, "//button[normalize-space()='Save']"))
    )
    safe_click(driver, save_btn)

    # 4. Verify success toast
    wait_for_toast(wait)
    print(f"✅ Course '{course_name}' berhasil ditambahkan.")
    print(f"{'='*60}\n")

    return True


def perform_delete_course(driver, wait, course_name):
    """
    Delete a course from the Assignment page.

    Args:
        driver: WebDriver instance
        wait: WebDriverWait instance
        course_name: Name of the course to delete

    Returns:
        bool: True if course was deleted successfully

    Raises:
        AssertionError: If toast verification fails
    """
    print(f"\n{'='*60}")
    print(f"🎯 Memulai: Menghapus Course '{course_name}'")
    print(f"{'='*60}")

    # 1. Find the course row and click delete
    print(f"🔍 Mencari course '{course_name}'...")
    course_row = wait.until(
        EC.presence_of_element_located((By.XPATH, f"//td[contains(text(), '{course_name}')]/.."))
    )
    print(f"✅ Course '{course_name}' ditemukan.")

    delete_btn = course_row.find_element(By.XPATH, ".//button[@aria-label='Delete']")
    safe_click(driver, delete_btn)
    print("🗑️ Tombol Delete diklik.")

    # 2. Confirm delete
    print("❓ Mengkonfirmasi penghapusan...")
    confirm_btn = wait.until(
        EC.element_to_be_clickable((By.XPATH, "//button[normalize-space()='Delete']"))
    )
    safe_click(driver, confirm_btn)

    # 3. Verify success toast
    wait_for_toast(wait)
    print(f"✅ Course '{course_name}' berhasil dihapus.")
    print(f"{'='*60}\n")

    return True


def perform_edit_course(driver, wait, old_course_name, new_course_name):
    """
    Edit a course name on the Assignment page.

    Args:
        driver: WebDriver instance
        wait: WebDriverWait instance
        old_course_name: Current course name
        new_course_name: New course name

    Returns:
        bool: True if course was edited successfully

    Raises:
        AssertionError: If toast verification fails
    """
    print(f"\n{'='*60}")
    print(f"🎯 Memulai: Mengedit Course '{old_course_name}' → '{new_course_name}'")
    print(f"{'='*60}")

    # 1. Find the course row and click edit
    print(f"🔍 Mencari course '{old_course_name}'...")
    course_row = wait.until(
        EC.presence_of_element_located((By.XPATH, f"//td[contains(text(), '{old_course_name}')]/.."))
    )
    print(f"✅ Course '{old_course_name}' ditemukan.")

    edit_btn = course_row.find_element(By.XPATH, ".//button[@aria-label='Edit']")
    safe_click(driver, edit_btn)
    print("✏️ Tombol Edit diklik.")

    # 2. Clear and fill new course name
    print(f"✍️ Mengubah nama menjadi: '{new_course_name}'...")
    course_name_input = wait.until(
        EC.presence_of_element_located((By.XPATH, "//input[@name='courseName']"))
    )
    course_name_input.clear()
    course_name_input.send_keys(new_course_name)

    # 3. Click 'Save' button
    print("💾 Mengklik tombol 'Save'...")
    save_btn = wait.until(
        EC.element_to_be_clickable((By.XPATH, "//button[normalize-space()='Save']"))
    )
    safe_click(driver, save_btn)

    # 4. Verify success toast
    wait_for_toast(wait)
    print(f"✅ Course berhasil diubah dari '{old_course_name}' menjadi '{new_course_name}'.")
    print(f"{'='*60}\n")

    return True
