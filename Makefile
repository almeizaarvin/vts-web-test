# ====================================================================
# VTS UI Test Makefile (Clean Separation: Admin vs Instructor)
# ====================================================================

.DEFAULT_GOAL := test-all

REPORT_OPTS := --html=reports/report.html --self-contained-html --disable-warnings -q

# ROOTS
ADMIN_ROOT := tests/roles/admin/pages
INSTRUCTOR_ROOT := tests/roles/instructor/pages

# MODULES (ADMIN)
ADMIN_ASSIGNMENT := $(ADMIN_ROOT)/assignments
ADMIN_LESSONS := $(ADMIN_ROOT)/lessons
ADMIN_QUIZ := $(ADMIN_ROOT)/quiz
ADMIN_USER := $(ADMIN_ROOT)/user

# MODULES (INSTRUCTOR)
INST_ASSIGNMENT := $(INSTRUCTOR_ROOT)/assignments

# ============================================================
# GLOBAL
# ============================================================

test-all:
	@echo "🔥 Running ALL tests..."
	mkdir -p reports
	pytest $(REPORT_OPTS)

test-verbose:
	@echo "🔍 Running ALL tests (verbose)..."
	mkdir -p reports
	pytest -v $(REPORT_OPTS)

# ============================================================
# ADMIN GROUP
# ============================================================

test-admin:
	@echo "▶️ Running ADMIN tests..."
	mkdir -p reports
	pytest $(ADMIN_ROOT) $(REPORT_OPTS)

test-admin-assignments:
	@echo "▶️ ADMIN - Assignments"
	mkdir -p reports
	pytest $(ADMIN_ASSIGNMENT) $(REPORT_OPTS)

test-admin-lessons:
	@echo "▶️ ADMIN - Lessons"
	mkdir -p reports
	pytest $(ADMIN_LESSONS) $(REPORT_OPTS)

test-admin-quiz:
	@echo "▶️ ADMIN - Quiz"
	mkdir -p reports
	pytest $(ADMIN_QUIZ) $(REPORT_OPTS)

test-admin-user:
	@echo "▶️ ADMIN - User"
	mkdir -p reports
	pytest $(ADMIN_USER) $(REPORT_OPTS)

# ============================================================
# INSTRUCTOR GROUP
# ============================================================

test-instructor:
	@echo "▶️ Running INSTRUCTOR tests..."
	mkdir -p reports
	pytest $(INSTRUCTOR_ROOT) $(REPORT_OPTS)

test-instructor-assignments:
	@echo "▶️ INSTRUCTOR - Assignments"
	mkdir -p reports
	pytest $(INST_ASSIGNMENT) $(REPORT_OPTS)