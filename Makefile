# ====================================================================
# VTS UI Test Makefile
# ====================================================================

.DEFAULT_GOAL := test-all

REPORT_OPTS := --html=/reports/report.html --self-contained-html --disable-warnings -q
ADMIN_ROOT := tests/roles/admin/pages
INST_ROOT := tests/roles/instructor/pages

# --------------------------------------------------------------------
# 1. Global
# --------------------------------------------------------------------

test-all:
	@echo "🔥 Running ALL tests in 'tests/' folder..."
	pytest $(REPORT_OPTS) || true

test-verbose:
	@echo "🔍 Running ALL tests with verbose output..."
	pytest --verbose $(REPORT_OPTS) || true


# --------------------------------------------------------------------
# 2. Role-based
# --------------------------------------------------------------------

test-admin:
	@echo "▶️ Running all Admin tests..."
	pytest $(ADMIN_ROOT) $(REPORT_OPTS) || true

test-instructor:
	@echo "▶️ Running all Instructor tests..."
	pytest $(INST_ROOT) $(REPORT_OPTS) || true


# --------------------------------------------------------------------
# 3. Admin Modules
# --------------------------------------------------------------------

test-admin-quiz:
	@echo "▶️ Running all Quiz Management tests (Admin)..."
	pytest $(ADMIN_ROOT)/quiz $(REPORT_OPTS) || true

test-admin-user:
	@echo "▶️ Running all User Management tests (Admin)..."
	pytest $(ADMIN_ROOT)/user $(REPORT_OPTS) || true


# --------------------------------------------------------------------
# 4. Quiz List (per file)
# --------------------------------------------------------------------

QUIZ_LIST_DIR := $(ADMIN_ROOT)/quiz/quiz_list

test-quiz-list-all:
	@echo "📄 Running ALL tests in Quiz List folder..."
	pytest $(QUIZ_LIST_DIR) $(REPORT_OPTS) || true

test-quiz-add:
	@echo "📄 Running test_create_new_add.py..."
	pytest $(QUIZ_LIST_DIR)/test_create_new_add.py $(REPORT_OPTS) || true

test-quiz-add-delete:
	@echo "📄 Running test_create_new_delete.py..."
	pytest $(QUIZ_LIST_DIR)/test_create_new_delete.py $(REPORT_OPTS) || true

test-quiz-add-edit:
	@echo "📄 Running test_create_new_edit.py..."
	pytest $(QUIZ_LIST_DIR)/test_create_new_edit.py $(REPORT_OPTS) || true

test-quiz-del:
	@echo "📄 Running test_action_delete.py..."
	pytest $(QUIZ_LIST_DIR)/test_action_delete.py $(REPORT_OPTS) || true

test-quiz-search:
	@echo "📄 Running test_search.py..."
	pytest $(QUIZ_LIST_DIR)/test_search.py $(REPORT_OPTS) || true

test-quiz-preview:
	@echo "📄 Running test_action_preview.py..."
	pytest $(QUIZ_LIST_DIR)/test_action_preview.py $(REPORT_OPTS) || true

test-quiz-submission:
	@echo "📄 Running test_action_quiz_submission.py..."
	pytest $(QUIZ_LIST_DIR)/test_action_quiz_submission.py $(REPORT_OPTS) || true


# --------------------------------------------------------------------
# 5. Group
# --------------------------------------------------------------------

test-group-add:
	@echo "📄 Running test_edit_group_add.py..."
	pytest $(QUIZ_LIST_DIR)/test_edit_group_add.py $(REPORT_OPTS) || true

test-group-del:
	@echo "📄 Running test_edit_group_delete.py..."
	pytest $(QUIZ_LIST_DIR)/test_edit_group_delete.py $(REPORT_OPTS) || true

test-group-edit:
	@echo "📄 Running test_edit_group_edit.py..."
	pytest $(QUIZ_LIST_DIR)/test_edit_group_edit.py $(REPORT_OPTS) || true


# --------------------------------------------------------------------
# 6. Result
# --------------------------------------------------------------------

test-score-edit:
	@echo "📄 Running test_edit_score.py..."
	pytest $(ADMIN_ROOT)/quiz/result/test_edit_score.py $(REPORT_OPTS) || true


# --------------------------------------------------------------------
# 7. Marker
# --------------------------------------------------------------------

test-smoke:
	@echo "💨 Running Smoke Tests..."
	pytest -m smoke $(REPORT_OPTS) || true


# --------------------------------------------------------------------
# 8. Lesson & Assignment
# --------------------------------------------------------------------

LESSON_DIR := $(ADMIN_ROOT)/lessons

test-lesson-delete:
	@echo "📄 Running lesson delete test..."
	pytest $(LESSON_DIR)/test_file_action_delete.py $(REPORT_OPTS) || true

ASSIGNMENTS_DIR := $(ADMIN_ROOT)/assignments

test-add-assignment:
	@echo "📄 Running add course..."
	pytest $(ASSIGNMENTS_DIR)/test_add_course.py $(REPORT_OPTS) || true

test-delete-assignment:
	@echo "📄 Running delete course..."
	pytest $(ASSIGNMENTS_DIR)/test_delete_course.py $(REPORT_OPTS) || true
