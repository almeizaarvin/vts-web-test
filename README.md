# 🧪 VTS UI Test (Selenium + Pytest + Docker)

Automated UI test untuk aplikasi **VTS Web**, menggunakan:

- 🐍 **Python 3.11**
- 🌐 **Selenium WebDriver**
- 🧱 **Pytest + Pytest-HTML**
- 🐳 **Dockerized Environment (Chrome headless)**

---

## 📁 Struktur Folder

```
vts-web-test/
├── Dockerfile
├── pytest.ini
├── requirements.txt
├── .env
├── .env.sample
├── .gitignore
├── README.md
└── tests/
    ├── __init__.py
    ├── conftest.py
    ├── utils/
    │   ├── __init__.py
    │   ├── edit_group_helper.py
    │   └── driver_factory.py
    └── roles/
        ├── __init__.py
        └── admin/
            ├── __init__.py
            ├── test_edit_group_add.py
            └── test_edit_group_delete.py
```

> **⚠️ Penting:** Pastikan di setiap folder (`tests/`, `roles/`, `utils/`, dll.) ada file kosong `__init__.py` agar import relatif seperti `from tests.utils.edit_group_helper import *` bisa berfungsi.

---

## ⚙️ Environment Variables

Buat file bernama `.env` di root project, misalnya:

```env
LOGIN_URL=http://192.168.000.00:9999/
ADMIN_USER=user
ADMIN_PASS=user
```

> **📝 Catatan:** Ganti IP address, username, dan password sesuai dengan environment Anda.

---

## 🚀 Cara Menjalankan Test

### Metode 1: Menggunakan Docker (Recommended)

#### 1️⃣ Build Image

```bash
docker build -t vts-ui-test .
```

#### 2️⃣ Jalankan Test

```bash
docker run --rm -v "${PWD}:/app" vts-ui-test
```

Semua test akan otomatis dijalankan, hasil HTML report tersimpan di: `report.html`

---

### Metode 2: Tanpa Docker (Local Setup)

#### 1️⃣ Prerequisites

Pastikan sudah terinstall:

- **Python 3.11** atau lebih tinggi
- **Google Chrome** browser (latest version)
- **pip** (Python package manager)

#### 2️⃣ Install Python Dependencies

```bash
pip install -r requirements.txt
```

Atau install secara manual:

```bash
pip install selenium==4.23.1 pytest==8.3.3 pytest-html==4.1.1 python-dotenv webdriver-manager
```

#### 3️⃣ Setup Environment Variables

Copy file `.env.sample` menjadi `.env`:

```bash
cp .env.sample .env
```

Kemudian edit file `.env` sesuai konfigurasi Anda:

```env
LOGIN_URL=http://192.168.000.00:9999/
ADMIN_USER=user
ADMIN_PASS=user
```

#### 4️⃣ Jalankan Test

**Jalankan semua test:**

```bash
pytest
```

**Jalankan test dengan output verbose:**

```bash
pytest -v
```

**Jalankan test dan generate HTML report:**

```bash
pytest --html=report.html --self-contained-html
```

**Jalankan test spesifik:**

```bash
# Jalankan satu file test
pytest tests/roles/admin/test_edit_group_add.py

# Jalankan satu test function
pytest tests/roles/admin/test_edit_group_add.py::TestAddGroup::test_add_new_group_success

# Jalankan test dengan marker tertentu
pytest -m admin
```

**Jalankan test dengan output minimal (quiet mode):**

```bash
pytest -q
```

---

## 🧰 Konfigurasi Pytest

File `pytest.ini`:

```ini
[pytest]
addopts = -v --html=report.html --self-contained-html
testpaths = tests
python_files = test_*.py
python_classes = Test*
python_functions = test_*
```

✅ Output report otomatis tersimpan sebagai `report.html`  
✅ Test hanya dieksekusi untuk file yang diawali dengan `test_`

---

## 📦 Dependencies

File `requirements.txt`:

```txt
selenium==4.23.1
pytest==8.3.3
pytest-html==4.1.1
python-dotenv
webdriver-manager
```

**Deskripsi:**

- `selenium`: WebDriver untuk automasi browser
- `pytest`: Testing framework
- `pytest-html`: Generate HTML report
- `python-dotenv`: Load environment variables dari file `.env`
- `webdriver-manager`: Otomatis download & manage ChromeDriver

Semua sudah otomatis di-install lewat Dockerfile atau manual install via `pip`.

---

## 🧩 Struktur Modular Test

Untuk memudahkan maintenance, setiap skenario dibuat modular:

| File                        | Deskripsi                                                                         |
| --------------------------- | --------------------------------------------------------------------------------- |
| `edit_group_helper.py`      | Kumpulan fungsi utilitas umum (open dialog, close dialog, delete, get list, dll.) |
| `driver_factory.py`         | Factory untuk setup WebDriver dengan konfigurasi optimal                          |
| `conftest.py`               | Pytest fixtures global (driver, authenticated_driver, dll.)                       |
| `test_edit_group_add.py`    | Skenario tambah Group baru (misal: Group D)                                       |
| `test_edit_group_delete.py` | Skenario hapus Group tertentu (misal: Group D)                                    |

Contoh import di test:

```python
from tests.utils.edit_group_helper import *
```

---

## 📊 Hasil Test Report

Setelah test selesai, buka file:

```
report.html
```

Di situ ada hasil lengkap test + screenshot (jika diimplementasikan).

**Contoh output console:**

```
============================= test session starts ==============================
collected 5 items

tests/roles/admin/test_edit_group_add.py::TestAddGroup::test_add_new_group_success PASSED [ 20%]
tests/roles/admin/test_edit_group_add.py::TestAddGroup::test_add_duplicate_group PASSED [ 40%]
tests/roles/admin/test_edit_group_delete.py::TestDeleteGroup::test_delete_existing_group PASSED [ 60%]

============================== 5 passed in 45.23s ===============================
```

---

## 🧩 Tips & Best Practices

### Jika test tidak mendeteksi helper:

- Pastikan sudah ada `__init__.py` di setiap folder test
- Gunakan import absolut: `from tests.utils.edit_group_helper import *`

### Menjalankan test di background (headless mode):

Edit file `.env`:

```env
HEADLESS=true
```

Atau jalankan dengan environment variable:

```bash
HEADLESS=true pytest
```

### Men-debug test yang gagal:

```bash
# Tampilkan output print statement
pytest -s

# Stop di test pertama yang gagal
pytest -x

# Tampilkan full traceback
pytest --tb=long
```

### Virtual Environment (Recommended):

```bash
# Buat virtual environment
python -m venv venv

# Aktivasi virtual environment
# Windows
venv\Scripts\activate

# Linux/Mac
source venv/bin/activate

# Install dependencies
pip install -r requirements.txt

# Jalankan test
pytest
```

---

## ✅ Contoh Perintah Lengkap

### Quick Run (Docker):

```bash
# 1. Build image
docker build -t vts-ui-test .

# 2. Jalankan test dan simpan report
docker run --rm -v "${PWD}:/app" vts-ui-test
```

### Quick Run (Local):

```bash
# 1. Setup (one time only)
python -m venv venv
source venv/bin/activate  # Linux/Mac
pip install -r requirements.txt
cp .env.sample .env

# 2. Edit .env sesuai konfigurasi Anda

# 3. Jalankan test
pytest

# 4. Lihat report
open report.html  # Mac
xdg-open report.html  # Linux
start report.html  # Windows
```

---

## 🔧 Troubleshooting

### Error: `ModuleNotFoundError: No module named 'tests'`

**Solusi:** Pastikan ada file `__init__.py` di folder `tests/` dan sub-foldernya.

```bash
touch tests/__init__.py
touch tests/utils/__init__.py
touch tests/roles/__init__.py
touch tests/roles/admin/__init__.py
```

---

### Error: Chrome driver not found

**Solusi:** `webdriver-manager` akan otomatis download ChromeDriver. Pastikan:

1. Koneksi internet stabil
2. Google Chrome sudah terinstall
3. Jalankan ulang test

Manual download (jika perlu):

```bash
# Cek versi Chrome
google-chrome --version  # Linux
chrome --version  # Mac

# Download ChromeDriver yang sesuai dari:
# https://chromedriver.chromium.org/downloads
```

---

### Error: `selenium.common.exceptions.WebDriverException: Message: unknown error: cannot find Chrome binary`

**Solusi:** Install Google Chrome browser terlebih dahulu.

**Linux:**

```bash
wget https://dl.google.com/linux/direct/google-chrome-stable_current_amd64.deb
sudo dpkg -i google-chrome-stable_current_amd64.deb
```

**Mac:**

```bash
brew install --cask google-chrome
```

**Windows:** Download dari [https://www.google.com/chrome/](https://www.google.com/chrome/)

---

### Test timeout

**Solusi:** Sesuaikan timeout di `.env`:

```env
IMPLICIT_WAIT=20
EXPLICIT_WAIT=30
```

Atau edit langsung di `conftest.py` atau `driver_factory.py`.

---

### Docker volume permission error (Linux)

**Solusi:**

```bash
sudo chown -R $USER:$USER .
docker run --rm -v "${PWD}:/app" -u $(id -u):$(id -g) vts-ui-test
```

---

### Browser window terbuka saat test (local mode)

**Solusi:** Gunakan headless mode dengan menambahkan di `.env`:

```env
HEADLESS=true
```

---

### Error: `ImportError: attempted relative import with no known parent package`

**Solusi:** Jalankan pytest dari root folder project, bukan dari dalam folder `tests/`.

```bash
# Salah ❌
cd tests
pytest

# Benar ✅
pytest tests/
```

---

## 📚 Dokumentasi Tambahan

- [Selenium Documentation](https://www.selenium.dev/documentation/)
- [Pytest Documentation](https://docs.pytest.org/)
- [WebDriver Manager](https://github.com/SergeyPirogov/webdriver_manager)

---

**Happy Testing! 🚀**
