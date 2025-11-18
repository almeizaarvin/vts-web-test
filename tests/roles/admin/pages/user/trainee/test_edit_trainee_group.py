# import pytest
# import time
# from datetime import datetime
# from selenium.webdriver.support.ui import WebDriverWait
# from selenium.webdriver.common.by import By
# from selenium.webdriver.support import expected_conditions as EC
# from selenium.common.exceptions import TimeoutException


# def open_mui_dropdown(driver, popup):
#     wait = WebDriverWait(driver, 10)

#     # Cari elemen select MUI
#     select_el = wait.until(
#         EC.presence_of_element_located((
#             By.CSS_SELECTOR,
#             "form#edit-group-form .MuiInputBase-root .MuiSelect-select"
#         ))
#     )
#     print("🟩 Found MUI Select element")

#     # Scroll dan klik pakai JS
#     driver.execute_script("arguments[0].scrollIntoView({block:'center'});", select_el)
#     driver.execute_script("arguments[0].click();", select_el)
#     print("🟩 CLICK Select (JS click)")

#     # Tunggu panel popup muncul
#     wait.until(
#         EC.presence_of_element_located((By.CSS_SELECTOR, "div[role='presentation']"))
#     )
#     print("🟩 Dropdown terbuka!")


# @pytest.mark.usefixtures("login_as_admin_fixture")
# def test_open_edit_group_popup(login_as_admin_fixture):
#     driver = login_as_admin_fixture
#     wait = WebDriverWait(driver, 15)

#     # Pastikan halaman userlist
#     wait.until(lambda d: "userlist?pageId=0" in d.current_url)

#     print("📄 Analisis tabel untuk mencari row 'Peserta'...")

#     table = wait.until(EC.presence_of_element_located((By.TAG_NAME, "table")))
#     rows = table.find_elements(By.CSS_SELECTOR, "tbody tr")
#     assert rows

#     target_row = None

#     for row in rows:
#         cells = row.find_elements(By.TAG_NAME, "td")
#         if cells and "Peserta" in cells[0].text.strip():
#             target_row = row
#             break

#     assert target_row, "❌ Tidak menemukan user Peserta"

#     # klik tombol edit
#     buttons = target_row.find_elements(By.CSS_SELECTOR, "td:nth-child(3) button")
#     edit_button = None
#     for btn in buttons:
#         try:
#             btn.find_element(By.CSS_SELECTOR, "svg[aria-label='Ubah Kelompok']")
#             edit_button = btn
#             break
#         except:
#             pass

#     driver.execute_script("arguments[0].click();", edit_button)
#     print("🟩 Klik 'Ubah Kelompok'")

#     # popup
#     popup = wait.until(
#         EC.presence_of_element_located((By.CSS_SELECTOR, "form#edit-group-form"))
#     )
#     print("🟩 Popup muncul!")

#     # =====================================
#     #   🚀 BUKA DROPDOWN MUI (langsung)
#     # =====================================
#     open_mui_dropdown(driver, popup)

#     # Ambil panel
#     panel = wait.until(
#         EC.presence_of_element_located((By.CSS_SELECTOR, "div[role='presentation']"))
#     )

#     # cari ul dan klik item '-'
#     ul = panel.find_element(By.TAG_NAME, "ul")
#     li_items = ul.find_elements(By.TAG_NAME, "li")

#     target_li = None
#     for li in li_items:
#         if li.text.strip() == "-":
#             target_li = li
#             break

#     driver.execute_script("arguments[0].click();", target_li)
#     print("🟩 Berhasil pilih '-'")
