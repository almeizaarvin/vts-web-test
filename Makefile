# ====================================================================
# VTS UI Test Makefile (FINAL)
# HTML report FIXED for Jenkins & Docker
# ====================================================================

.DEFAULT_GOAL := test-all

# --------------------------------------------------------------------
# Global config
# --------------------------------------------------------------------

# PENTING:
# - path RELATIVE
# - pytest nulis ke ./reports/report.html
REPORT_OPTS := --html=reports/report.html --self-contained-html --disable-warnings -q

ADMIN_ROOT := tests/roles/admin/pages
INST_ROOT  := tests/roles/instructor/pages

# Helper
define RUN_PYTEST
	mkdir -p reports
	pytest $(1) $(REPORT_OPTS) || true
endef

# --------------------------------------------------------------------
# 1. Global
# --------------------------------------------------------------------

test-all:
	@echo "🔥 Running ALL tests..."
	$(call RUN_PYTEST,)

test-verbose:
	@echo "🔍 Running ALL tests (verbose)..."
	mkdir -p reports
	pytest --verbose $(REPORT_OPTS) || true

# --------------------------------------------------------------------
# 2. Role-based
# --------------------------------------------------------------------

test-admin:
	@echo "▶️ Running all Admin tests..."
	$(call RUN_PYTEST,$(ADMIN_ROOT))

test-instructor:
	@echo "▶️ Running all Instructor tests..."
	$(call RUN_PYTEST,$(INST_ROOT))

# --------------------------------------------------------------------
# 3. Admin Modules
# --------------------------------------------------------------------

test-admin-quiz:
	@echo "▶️ Running all Quiz Management tests (Admin)..."
	$(call RUN_PYTEST,$(ADMIN_ROOT)/quiz)

test-admin-user:
	@echo "▶️ Running all User Management tests (Admin)..."
	$(call RUN_PYTEST,$(ADMIN_ROOT)/user)

# --------------------------------------------------------------------
# 4. Quiz List (per file)
# --------------------------------------------------------------------

QUIZ_LIST_DIR := $(ADMIN_ROOT)/quiz/quiz_list

test-quiz-list-all:
	@echo "📄 Running ALL Quiz List tests..."
	$(call RUN_PYTEST,$(QUIZ_LIST_DIR))

test-quiz-add:
	@echo "📄 Running test_create_new_add.py..."
	$(call RUN_PYTEST,$(QUIZ_LIST_DIR)/test_create_new_add.py)

test-quiz-add-delete:
	@echo "📄 Running test_create_new_delete.py..."
	$(call RUN_PYTEST,$(QUIZ_LIST_DIR)/test_create_new_delete.py)

test-quiz-add-edit:
	@echo "📄 Running test_create_new_edit.py..."
	$(call RUN_PYTEST,$(QUIZ_LIST_DIR)/test_create_new_edit.py)

test-quiz-del:
	@echo "📄 Running test_action_delete.py..."
	$(call RUN_PYTEST,$(QUIZ_LIST_DIR)/test_action_delete.py)

test-quiz-search:
	@echo "📄 Running test_search.py..."
	$(call RUN_PYTEST,$(QUIZ_LIST_DIR)/test_search.py)

test-quiz-preview:
	@echo "📄 Running test_action_preview.py..."
	$(call RUN_PYTEST,$(QUIZ_LIST_DIR)/test_action_preview.py)

test-quiz-submission:
	@echo "📄 Running test_action_quiz_submission.py..."
	$(call RUN_PYTEST,$(QUIZ_LIST_DIR)/test_action_quiz_submission.py)

# --------------------------------------------------------------------
# 5. Group
# --------------------------------------------------------------------

test-group-add:
	@echo "📄 Running test_edit_group_add.py..."
	$(call RUN_PYTEST,$(QUIZ_LIST_DIR)/test_edit_group_add.py)

test-group-del:
	@echo "📄 Running test_edit_group_delete.py..."
	$(call RUN_PYTEST,$(QUIZ_LIST_DIR)/test_edit_group_delete.py)

test-group-edit:
	@echo "📄 Running test_edit_group_edit.py..."
	$(call RUN_PYTEST,$(QUIZ_LIST_DIR)/test_edit_group_edit.py)

# --------------------------------------------------------------------
# 6. Result
# --------------------------------------------------------------------

test-score-edit:
	@echo "📄 Running test_edit_score.py..."
	$(call RUN_PYTEST,$(ADMIN_ROOT)/quiz/result/test_edit_score.py)

# --------------------------------------------------------------------
# 7. Marker
# --------------------------------------------------------------------

test-smoke:
	@echo "💨 Running Smoke Tests..."
	mkdir -p reports
	pytest -m smoke $(REPORT_OPTS) || true

# --------------------------------------------------------------------
# 8. Lesson & Assignment
# --------------------------------------------------------------------

LESSON_DIR := $(ADMIN_ROOT)/lessons
ASSIGNMENTS_DIR := $(ADMIN_ROOT)/assignments

test-lesson-delete:
	@echo "📄 Running lesson delete test..."
	$(call RUN_PYTEST,$(LESSON_DIR)/test_file_action_delete.py)

test-add-assignment:
	@echo "📄 Running add course..."
	$(call RUN_PYTEST,$(ASSIGNMENTS_DIR)/test_add_course.py)

test-delete-assignment:
	@echo "📄 Running delete course..."
	$(call RUN_PYTEST,$(ASSIGNMENTS_DIR)/test_delete_course.py)
