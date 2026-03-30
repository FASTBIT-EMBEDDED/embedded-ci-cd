# ── Connection points ──────────────────────────────────────────────────────────
# To switch MCU, change PLATFORM. Each platform needs:
#   cmake/platform/<PLATFORM>.cmake  (toolchain + MCU flags)
#   cmake/bsp/<PLATFORM>/            (HAL sources, startup, linker script)
PLATFORM ?= stm32f3
BUILD    ?= debug

# ── Validation ─────────────────────────────────────────────────────────────────
VALID_BUILDS := debug release
ifeq ($(filter $(BUILD),$(VALID_BUILDS)),)
  $(error BUILD='$(BUILD)' is invalid. Choose: $(VALID_BUILDS))
endif

# ── Derived ────────────────────────────────────────────────────────────────────
BUILD_DIR  := build/$(PLATFORM)/$(BUILD)
CMAKE_TYPE := $(if $(filter release,$(BUILD)),Release,Debug)
TOOLCHAIN  := $(CURDIR)/cmake/platform/$(PLATFORM).cmake

CMAKE  := cmake
PYTHON := python3

# Ensure Ninja is on PATH (STM32CubeCLT bundles it separately from CMake)
export PATH := /c/ST/STM32CubeCLT_1.21.0/Ninja/bin:$(PATH)

.PHONY: all build analyze format format-check clean

# Full quality gate: build then analyze
all: build analyze

# ── Configure (generates compile_commands.json) ────────────────────────────────
$(BUILD_DIR)/build.ninja:
	@echo "[ci] Configuring $(PLATFORM) / $(CMAKE_TYPE) ..."
	@$(CMAKE) \
		-S "$(CURDIR)" -B "$(BUILD_DIR)" -G Ninja \
		-DCMAKE_BUILD_TYPE=$(CMAKE_TYPE) \
		-DCMAKE_TOOLCHAIN_FILE="$(TOOLCHAIN)" \
		-DPLATFORM=$(PLATFORM) \
		-DCMAKE_EXPORT_COMPILE_COMMANDS=ON

# ── Build ──────────────────────────────────────────────────────────────────────
build: $(BUILD_DIR)/build.ninja
	@echo "[ci] Building ..."
	@$(CMAKE) --build "$(BUILD_DIR)"

# ── Analyze (requires a build dir with compile_commands.json) ─────────────────
analyze: build
	@echo "[ci] Running clang-tidy ..."
	@cd tools/quality && $(PYTHON) run_clang_tidy.py --build-dir "$(CURDIR)/$(BUILD_DIR)"
	@echo "[ci] Running cppcheck ..."
	@cd tools/quality && $(PYTHON) run_cppcheck.py

# ── Format ────────────────────────────────────────────────────────────────────
format:
	@cd tools/quality && $(PYTHON) format_apply.py

format-check:
	@cd tools/quality && $(PYTHON) format_check.py

# ── Clean ─────────────────────────────────────────────────────────────────────
clean:
	@rm -rf build reports
