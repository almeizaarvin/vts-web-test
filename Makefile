# ====================================================================
# VTS UI Test Makefile
# Digunakan untuk menyingkat perintah pytest berdasarkan struktur file
# ====================================================================

# Default command saat menjalankan 'make' tanpa target: Run semua test.
.DEFAULT_GOAL := test-all

# Variabel Global
REPORT_OPTS := --html=report.html --self-contained-html --disable-warnings -q
ADMIN_ROOT := tests/roles/admin/pages
INST_ROOT := tests/roles/instructor/pages

# --------------------------------------------------------------------
# 1. Targets Global (Default)
# --------------------------------------------------------------------

test-all:
	@echo "🔥 Running ALL tests in 'tests/' folder..."
	pytest $(REPORT_OPTS)

test-verbose:
	@echo "🔍 Running ALL tests with verbose output..."
	pytest --verbose $(REPORT_OPTS)


# --------------------------------------------------------------------
# 2. Targets Per Group Role/User
# --------------------------------------------------------------------

test-admin:
	@echo "▶️ Running all Admin tests..."
	pytest $(ADMIN_ROOT) $(REPORT_OPTS)

test-instructor:
	@echo "▶️ Running all Instructor tests..."
	pytest $(INST_ROOT) $(REPORT_OPTS)

# --------------------------------------------------------------------
# 3. Targets Per Modul (Admin Actions)
# --------------------------------------------------------------------

# Semua test di bawah folder quiz (quiz_list dan result)
test-admin-quiz:
	@echo "▶️ Running all Quiz Management tests (Admin)..."
	pytest $(ADMIN_ROOT)/quiz $(REPORT_OPTS)

# Semua test di bawah folder user
test-admin-user:
	@echo "▶️ Running all User Management tests (Admin)..."
	pytest $(ADMIN_ROOT)/user $(REPORT_OPTS)


# --------------------------------------------------------------------
# 4. Targets Per File Spesifik (Paling Sering Dipakai)
# --------------------------------------------------------------------

# --- A. Quiz List Files ---
QUIZ_LIST_DIR := $(ADMIN_ROOT)/quiz/quiz_list

test-quiz-list-all:
	@echo "📄 Running ALL tests in Quiz List folder..."
	pytest $(QUIZ_LIST_DIR) $(REPORT_OPTS)

test-quiz-add:
	@echo "📄 Running test_create_new_add.py..."
	pytest $(QUIZ_LIST_DIR)/test_create_new_add.py $(REPORT_OPTS)

test-quiz-add-delete:
	@echo "📄 Running test_create_new_add.py..."
	pytest $(QUIZ_LIST_DIR)/test_create_new_delete.py $(REPORT_OPTS)

test-quiz-add-edit:
	@echo "📄 Running test_create_new_add.py..."
	pytest $(QUIZ_LIST_DIR)/test_create_new_edit.py $(REPORT_OPTS)


test-quiz-del:
	@echo "📄 Running test_action_delete.py..."
	pytest $(QUIZ_LIST_DIR)/test_action_delete.py $(REPORT_OPTS)

test-quiz-search:
	@echo "📄 Running test_search.py..."
	pytest $(QUIZ_LIST_DIR)/test_search.py $(REPORT_OPTS)
	
test-quiz-preview:
	@echo "📄 Running test_action_preview.py..."
	pytest $(QUIZ_LIST_DIR)/test_action_preview.py $(REPORT_OPTS)

test-quiz-submission:
	@echo "📄 Running test_action_quiz_submission.py..."
	pytest $(QUIZ_LIST_DIR)/test_action_quiz_submission.py $(REPORT_OPTS)


# --- B. Group Files (Berada di dalam Quiz List, berdasarkan struktur) ---
test-group-add:
	@echo "📄 Running test_edit_group_add.py..."
	pytest $(QUIZ_LIST_DIR)/test_edit_group_add.py $(REPORT_OPTS)

test-group-del:
	@echo "📄 Running test_edit_group_delete.py..."
	pytest $(QUIZ_LIST_DIR)/test_edit_group_delete.py $(REPORT_OPTS)

test-group-edit:
	@echo "📄 Running test_edit_group_edit.py..."
	pytest $(QUIZ_LIST_DIR)/test_edit_group_edit.py $(REPORT_OPTS)


# --- C. Result Files ---
test-score-edit:
	@echo "📄 Running test_edit_score.py..."
	pytest $(ADMIN_ROOT)/quiz/result/test_edit_score.py $(REPORT_OPTS)

# --------------------------------------------------------------------
# 5. Targets Run via Marker
# --------------------------------------------------------------------

test-smoke:
	@echo "💨 Running Smoke Tests (using marker -m smoke)..."
	pytest -m smoke $(REPORT_OPTS)

LESSON_DIR := $(ADMIN_ROOT)/lessons

test-lesson-delete:
	@echo "📄 Running lesson delete test..."
	pytest $(LESSON_DIR)/test_file_action_delete.py $(REPORT_OPTS)


ASSIGNMENTS_DIR := $(ADMIN_ROOT)/assignments

test-add-assignment:
	@echo "📄 Running add course..."
	pytest $(ASSIGNMENTS_DIR)/test_add_course.py $(REPORT_OPTS)
	
test-delete-assignment:
	@echo "📄 Running delete course..."
	pytest $(ASSIGNMENTS_DIR)/test_delete_course.py $(REPORT_OPTS)