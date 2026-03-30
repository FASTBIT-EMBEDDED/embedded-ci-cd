cmake_minimum_required(VERSION 3.22)

# ── Platform selection ─────────────────────────────────────────────────────────
# PLATFORM is passed by the Makefile via -DPLATFORM=<name>.
# The matching toolchain file (cmake/platform/<PLATFORM>.cmake) is also passed
# via -DCMAKE_TOOLCHAIN_FILE by the Makefile — so the compiler is already
# configured before this file runs.
# To add a new MCU: add cmake/platform/<name>.cmake + cmake/bsp/<name>/.
if(NOT DEFINED PLATFORM)
    set(PLATFORM "stm32f3")
    message(WARNING "PLATFORM not set, defaulting to '${PLATFORM}'. "
                    "Pass -DPLATFORM=<name> or use the Makefile.")
endif()

set(CMAKE_C_STANDARD 11)
set(CMAKE_C_STANDARD_REQUIRED ON)
set(CMAKE_C_EXTENSIONS ON)
set(CMAKE_EXPORT_COMPILE_COMMANDS ON)

if(NOT CMAKE_BUILD_TYPE)
    set(CMAKE_BUILD_TYPE Debug)
endif()

project(020_Bouncy_Ball C ASM)
message(STATUS "Platform : ${PLATFORM}")
message(STATUS "Build    : ${CMAKE_BUILD_TYPE}")

# ── Application executable (must exist before the BSP subdirectory adds sources) ─
add_executable(${PROJECT_NAME}
    Core/drivers/game/app.c
    Core/drivers/game/game.c
    Core/drivers/game/ball_img.c
    Core/drivers/game/player.c
    Core/drivers/game/world.c
    Core/drivers/gfx/gfx.c
    Core/drivers/imu/mpu6050.c
    Core/drivers/display/gc9a01a.c
)

target_include_directories(${PROJECT_NAME} PRIVATE
    Core/drivers/game
    Core/drivers/gfx
    Core/drivers/imu
    Core/drivers/display
)

target_compile_options(${PROJECT_NAME} PRIVATE
    -Wall
    -Wextra
    -Wshadow
    -Wundef
    -Wdouble-promotion
    -Wformat=2
    -Wno-unused-parameter
)

# ── Board Support Package ──────────────────────────────────────────────────────
# Runs after add_executable so the BSP can call target_sources / target_link_libraries
# on the already-defined target. Adds HAL sources, startup, includes, defines.
add_subdirectory(cmake/bsp/${PLATFORM})
