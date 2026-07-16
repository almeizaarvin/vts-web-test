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
ADMIN_QUIZ_LIST := $(ADMIN_QUIZ)/quiz_list
ADMIN_QUIZ_RESULT := $(ADMIN_ROOT)/quiz/result

ADMIN_USER := $(ADMIN_ROOT)/user
ADMIN_USER_INSTRUCTOR := $(ADMIN_ROOT)/user/instructor
ADMIN_USER_TRAINEE := $(ADMIN_ROOT)/user/trainee

# MODULES (INSTRUCTOR)
INST_ASSIGNMENT := $(INSTRUCTOR_ROOT)/assignments
INST_LESSONS := $(INSTRUCTOR_ROOT)/lessons

INST_QUIZ := $(INSTRUCTOR_ROOT)/quiz
INST_QUIZ_LIST := $(INST_QUIZ)/quiz_list
INST_QUIZ_RESULT := $(INSTRUCTOR_ROOT)/quiz/result

INST_TRAINEE := $(INSTRUCTOR_ROOT)/trainee
INST_TRAINEE_QUIZ_LIST := $(INST_TRAINEE)/quiz/quiz list

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

test-admin-quiz-list:
	@echo "▶️ ADMIN - Quiz List"
	mkdir -p reports
	pytest $(ADMIN_QUIZ_LIST) $(REPORT_OPTS)

test-admin-quiz-result:
	@echo "▶️ ADMIN - Quiz Result"
	mkdir -p reports
	pytest $(ADMIN_QUIZ_RESULT) $(REPORT_OPTS)

test-admin-user:
	@echo "▶️ ADMIN - User"
	mkdir -p reports
	pytest $(ADMIN_USER) $(REPORT_OPTS)

test-admin-user-instructor:
	@echo "▶️ ADMIN - User Instructor"
	mkdir -p reports
	pytest $(ADMIN_USER_INSTRUCTOR) $(REPORT_OPTS)

test-admin-user-trainee:
	@echo "▶️ ADMIN - User Trainee"
	mkdir -p reports
	pytest $(ADMIN_USER_TRAINEE) $(REPORT_OPTS)

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

test-instructor-lessons:
	@echo "▶️ INSTRUCTOR - Lessons"
	mkdir -p reports
	pytest $(INST_LESSONS) $(REPORT_OPTS)

test-instructor-quiz:
	@echo "▶️ INSTRUCTOR - Quiz"
	mkdir -p reports
	pytest $(INST_QUIZ) $(REPORT_OPTS)

test-instructor-quiz-list:
	@echo "▶️ INSTRUCTOR - Quiz List"
	mkdir -p reports
	pytest $(INST_QUIZ_LIST) $(REPORT_OPTS)

test-instructor-quiz-result:
	@echo "▶️ INSTRUCTOR - Quiz Result"
	mkdir -p reports
	pytest $(INST_QUIZ_RESULT) $(REPORT_OPTS)

test-instructor-trainee:
	@echo "▶️ INSTRUCTOR - Trainee"
	mkdir -p reports
	pytest $(INST_TRAINEE) $(REPORT_OPTS)

test-instructor-trainee-quiz-list:
	@echo "▶️ INSTRUCTOR - Trainee Quiz List"
	mkdir -p reports
	pytest "$(INST_TRAINEE_QUIZ_LIST)" $(REPORT_OPTS)
