# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Project Overview

Embedded C firmware for an STM32F303 microcontroller (Cortex-M4 @ 72MHz) that implements a physics-based bouncy ball game. The ball is controlled by tilting the board — an MPU6050 IMU reads tilt angle, and the game renders to a GC9A01A 240×240 circular TFT LCD via SPI.

## Build Commands

```bash
# Debug build (default)
make build

# Release build
make build BUILD=release

# Full quality gate: build + clang-tidy + cppcheck
make all

# Static analysis only (requires a build to exist first)
make analyze

# Format source files
make format

# Check formatting without modifying files
make format-check

# Clean build artifacts and reports
make clean
```

**Makefile variables:**
- `PLATFORM=[stm32f3|...]` (default: `stm32f3`) — the MCU swap point
- `BUILD=[debug|release]` (default: `debug`)

Build artifacts land in `build/<PLATFORM>/<BUILD>/` (e.g., `build/stm32f3/debug/`), so multiple platforms never clobber each other.

## MCU / Platform Swap Point

To target a different MCU, two files are needed:

| File | Purpose |
|---|---|
| `cmake/platform/<name>.cmake` | Toolchain (compiler, CPU flags, linker script) |
| `cmake/bsp/<name>/CMakeLists.txt` | HAL sources, startup file, includes |

Then run `make PLATFORM=<name>`. Nothing else changes.

Current platform: `stm32f3` → `cmake/platform/stm32f3.cmake` + `cmake/bsp/stm32f3/`.

## Architecture (Concentric Layers)

```
Makefile                          Layer 1: user knobs (PLATFORM, BUILD)
  └─ cmake/platform/stm32f3.cmake Layer 2: toolchain (arm-none-eabi, MCU flags)
       └─ CMakeLists.txt          Layer 3: platform-agnostic app definition
            └─ cmake/bsp/stm32f3/ Layer 4: HAL/BSP sources for this MCU
```

### Source layers

```
main.c  →  app.c  →  game.c  →  player.c / world.c
                  ↘  gc9a01a.c (SPI display driver)
                  ↘  mpu6050.c (I2C IMU driver)
```

- **`Core/Src/main.c`** — HAL init, clock config, I2C/SPI setup, calls `app_run()`
- **`Core/drivers/game/`** — game loop, physics, ball rendering, world bounds
- **`Core/drivers/display/gc9a01a.c`** — SPI LCD driver (240×240, pixel/rect/image drawing)
- **`Core/drivers/imu/mpu6050.c`** — I2C IMU driver (accel/gyro sampling, tilt angle)
- **`Core/drivers/gfx/gfx.c`** — thin graphics abstraction over the display driver

### Key types

```c
// error.h — returned by all driver functions
typedef enum { ERR_OK, ERR_INVALID_PARAM, ERR_TIMEOUT, ERR_HW_FAILURE } err_t;

// player.c — ball state
typedef struct { float x, y, vx, vy; uint16_t radius, colour; } player_t;

// world.c — circular arena
typedef struct { uint16_t width, height; float center_x, center_y, radius;
                 uint16_t background_colour; } world_t;
```

## Quality Tools

Tools live in `tools/quality/` and all share `common.py` for config loading and output helpers.

| Script | Called by |
|---|---|
| `format_apply.py` | `make format` |
| `format_check.py` | `make format-check` |
| `run_clang_tidy.py` | `make analyze` |
| `run_cppcheck.py` | `make analyze` |

Analysis scope is controlled by `config/quality_targets.json`:
- **Included:** `Core/drivers/` — application and driver code
- **Excluded:** `Drivers/` (STM32 HAL), `Core/Inc`, `Core/Src`, `build/`, `reports/`

Style config: `.clang-format` (LLVM, Allman braces, 4-space indent, 100-col limit), `.clang-tidy`, `cppcheck/suppressions.txt`.
