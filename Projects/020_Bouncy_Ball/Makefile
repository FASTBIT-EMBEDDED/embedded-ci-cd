# ============================================================
# User controls
# ============================================================

build  ?= debug
target ?= target
test   ?= all

# ============================================================
# Project settings
# ============================================================

PROJECT_NAME := 020_Bouncy_Ball
CUR_DIR      := $(CURDIR)
BUILD_DIR    := build/$(build)
TOOLCHAIN    := $(CUR_DIR)/cmake/gcc-arm-none-eabi.cmake

PYTHON := python

RUN_CPPCHECK   := $(PYTHON) tools/quality/run_cppcheck.py
RUN_CLANG_TIDY := $(PYTHON) tools/quality/run_clang_tidy.py
FORMAT_APPLY   := $(PYTHON) tools/quality/format_apply.py
FORMAT_CHECK   := $(PYTHON) tools/quality/format_check.py

VALID_TESTS := all gtest qutest none
VALID_TARGETS := host target
VALID_BUILDS := debug release

ifeq ($(filter $(test),$(VALID_TESTS)),)
$(error Invalid test='$(test)'. Use one of: $(VALID_TESTS))
endif

ifeq ($(filter $(target),$(VALID_TARGETS)),)
$(error Invalid target='$(target)'. Use one of: $(VALID_TARGETS))
endif

ifeq ($(filter $(build),$(VALID_BUILDS)),)
$(error Invalid build='$(build)'. Use one of: $(VALID_BUILDS))
endif

ifeq ($(build),debug)
CMAKE_BUILD_TYPE := Debug
else ifeq ($(build),release)
CMAKE_BUILD_TYPE := Release
endif

# ============================================================
# Main targets
# ============================================================

.PHONY: all analyze cppcheck clangtidy tests gtest qutest \
        build_bin configure_target build_target \
        format format_check clean summary reconfigure

all: analyze tests build_bin

# ------------------------------------------------------------
# Static analysis
# Only test=none skips analysis
# ------------------------------------------------------------
analyze:
ifeq ($(test),none)
	@echo == Static analysis skipped \(test=none\) ==
else
	@echo == Static analysis ==
	$(MAKE) cppcheck
	$(MAKE) clangtidy
endif

cppcheck:
	@echo == cppcheck ==
	@$(RUN_CPPCHECK)

clangtidy:
	@echo == clang-tidy ==
	@$(RUN_CLANG_TIDY)

# ------------------------------------------------------------
# Tests
# ------------------------------------------------------------
tests:
ifeq ($(test),all)
	$(MAKE) gtest
	$(MAKE) qutest
else ifeq ($(test),gtest)
	$(MAKE) gtest
else ifeq ($(test),qutest)
	$(MAKE) qutest
else ifeq ($(test),none)
	@echo == Tests skipped \(test=none\) ==
endif

gtest:
ifeq ($(target),target)
	@echo GTest is host-only. Use: make target=host test=gtest
	@exit 1
else
	@echo == GTest ==
	@echo TODO: wire real host gtest build/run here
endif

qutest:
	@echo == QUTEST ==
ifeq ($(target),host)
	@echo TODO: wire host qutest flow here
else
	@echo TODO: wire target qutest flow here
endif

# ------------------------------------------------------------
# Build
# ------------------------------------------------------------
build_bin:
ifeq ($(target),host)
	@echo == Host build \(build=$(build)\) ==
	@echo TODO: wire real host build here
else
	$(MAKE) build_target
endif

configure_target:
	@if not exist "$(BUILD_DIR)\build.ninja" ( \
		echo [driver] Configuring STM32 target build \(type=$(CMAKE_BUILD_TYPE)\) && \
		cube-cmake -DCMAKE_BUILD_TYPE=$(CMAKE_BUILD_TYPE) -DCMAKE_TOOLCHAIN_FILE=$(TOOLCHAIN) -DCMAKE_COMMAND=cube-cmake -S $(CUR_DIR) -B $(BUILD_DIR) -G Ninja \
	)

build_target: configure_target
	@echo [driver] Building STM32 target \(type=$(CMAKE_BUILD_TYPE)\)
	@cube-cmake --build $(BUILD_DIR) --

reconfigure:
	@if exist "$(BUILD_DIR)" rmdir /s /q "$(BUILD_DIR)"
	@$(MAKE) configure_target

# ------------------------------------------------------------
# Formatting
# ------------------------------------------------------------
format:
	@$(FORMAT_APPLY)

format_check:
	@$(FORMAT_CHECK)

# ------------------------------------------------------------
# Utility
# ------------------------------------------------------------
summary:
	@echo =====================================
	@echo Project          : $(PROJECT_NAME)
	@echo Build           : $(build)
	@echo CMake build type: $(CMAKE_BUILD_TYPE)
	@echo Target          : $(target)
	@echo Test            : $(test)
	@echo Build dir       : $(BUILD_DIR)
	@echo =====================================

clean:
	@if exist build rmdir /s /q build
	@if exist reports rmdir /s /q reports