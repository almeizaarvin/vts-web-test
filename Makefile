# ====================================================================
# VTS UI Test Makefile (Docker Agent Friendly)
# ====================================================================

.DEFAULT_GOAL := test-all

# REPORT: RELATIVE ke workspace Jenkins
REPORT_OPTS := --html=reports/report.html --self-contained-html --disable-warnings -q

ADMIN_ROOT := tests/roles/admin/pages
INST_ROOT := tests/roles/instructor/pages
QUIZ_LIST_DIR := $(ADMIN_ROOT)/quiz/quiz_list

# --------------------------------------------------------------------
# 1. Global
# --------------------------------------------------------------------

test-all:
	@echo "🔥 Running ALL tests..."
	mkdir -p reports
	pytest $(REPORT_OPTS)

test-verbose:
	@echo "🔍 Running ALL tests (verbose)..."
	mkdir -p reports
	pytest --verbose $(REPORT_OPTS)

# --------------------------------------------------------------------
# 2. Role-based
# --------------------------------------------------------------------

test-admin:
	@echo "▶️ Admin tests..."
	mkdir -p reports
	pytest $(ADMIN_ROOT) $(REPORT_OPTS)

test-instructor:
	@echo "▶️ Instructor tests..."
	mkdir -p reports
	pytest $(INST_ROOT) $(REPORT_OPTS)

# --------------------------------------------------------------------
# 3. Admin Modules
# --------------------------------------------------------------------

test-admin-quiz:
	@echo "▶️ Admin Quiz tests..."
	mkdir -p reports
	pytest $(ADMIN_ROOT)/quiz $(REPORT_OPTS)

test-admin-user:
	@echo "▶️ Admin User tests..."
	mkdir -p reports
	pytest $(ADMIN_ROOT)/user $(REPORT_OPTS)

# --------------------------------------------------------------------
# 4. Quiz List
# --------------------------------------------------------------------

test-quiz-list-all:
	mkdir -p reports
	pytest $(QUIZ_LIST_DIR) $(REPORT_OPTS)

test-quiz-add:
	mkdir -p reports
	pytest $(QUIZ_LIST_DIR)/test_create_new_add.py $(REPORT_OPTS)

test-quiz-add-delete:
	mkdir -p reports
	pytest $(QUIZ_LIST_DIR)/test_create_new_delete.py $(REPORT_OPTS)

test-quiz-add-edit:
	mkdir -p reports
	pytest $(QUIZ_LIST_DIR)/test_create_new_edit.py $(REPORT_OPTS)

test-quiz-del:
	mkdir -p reports
	pytest $(QUIZ_LIST_DIR)/test_action_delete.py $(REPORT_OPTS)

test-quiz-search:
	mkdir -p reports
	pytest $(QUIZ_LIST_DIR)/test_search.py $(REPORT_OPTS)

test-quiz-preview:
	mkdir -p reports
	pytest $(QUIZ_LIST_DIR)/test_action_preview.py $(REPORT_OPTS)

test-quiz-submission:
	mkdir -p reports
	pytest $(QUIZ_LIST_DIR)/test_action_quiz_submission.py $(REPORT_OPTS)

# --------------------------------------------------------------------
# 5. Group
# --------------------------------------------------------------------

test-group-add:
	mkdir -p reports
	pytest $(QUIZ_LIST_DIR)/test_edit_group_add.py $(REPORT_OPTS)

test-group-del:
	mkdir -p reports
	pytest $(QUIZ_LIST_DIR)/test_edit_group_delete.py $(REPORT_OPTS)

test-group-edit:
	mkdir -p reports
	pytest $(QUIZ_LIST_DIR)/test_edit_group_edit.py $(REPORT_OPTS)

# --------------------------------------------------------------------
# 6. Result
# --------------------------------------------------------------------

test-score-edit:
	mkdir -p reports
	pytest $(ADMIN_ROOT)/quiz/result/test_edit_score.py $(REPORT_OPTS)

# --------------------------------------------------------------------
# 7. Marker
# --------------------------------------------------------------------

test-smoke:
	mkdir -p reports
	pytest -m smoke $(REPORT_OPTS)
