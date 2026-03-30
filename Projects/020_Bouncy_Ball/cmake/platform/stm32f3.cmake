# cmake/platform/stm32f3.cmake
# Platform: STM32F303 (Cortex-M4 + FPU, arm-none-eabi toolchain)
#
# ── MCU SWAP POINT ────────────────────────────────────────────────────────────
# To target a different MCU, copy this file to cmake/platform/<name>.cmake,
# add cmake/bsp/<name>/CMakeLists.txt, then run: make PLATFORM=<name>
#
# Lines to change for a different ARM part:
#   MCU_FLAGS  — CPU/FPU flags
#   Linker script path in CMAKE_EXE_LINKER_FLAGS
# ─────────────────────────────────────────────────────────────────────────────

set(CMAKE_SYSTEM_NAME      Generic)
set(CMAKE_SYSTEM_PROCESSOR arm)

# Static library probe: no linker invocation during try_compile
set(CMAKE_TRY_COMPILE_TARGET_TYPE STATIC_LIBRARY)

# ── Toolchain binaries ────────────────────────────────────────────────────────
set(TOOLCHAIN_PREFIX    arm-none-eabi-)
set(CMAKE_C_COMPILER    ${TOOLCHAIN_PREFIX}gcc)
set(CMAKE_ASM_COMPILER  ${TOOLCHAIN_PREFIX}gcc)
set(CMAKE_CXX_COMPILER  ${TOOLCHAIN_PREFIX}g++)
set(CMAKE_OBJCOPY       ${TOOLCHAIN_PREFIX}objcopy)
set(CMAKE_SIZE          ${TOOLCHAIN_PREFIX}size)

set(CMAKE_EXECUTABLE_SUFFIX_C   .elf)
set(CMAKE_EXECUTABLE_SUFFIX_ASM .elf)

# ── MCU-specific flags (← change these for a different part) ─────────────────
set(MCU_FLAGS "-mcpu=cortex-m4 -mfpu=fpv4-sp-d16 -mfloat-abi=hard")

set(CMAKE_C_FLAGS   "${MCU_FLAGS} -fdata-sections -ffunction-sections -fstack-usage"
    CACHE STRING "" FORCE)
set(CMAKE_ASM_FLAGS "${MCU_FLAGS} -x assembler-with-cpp -MMD -MP"
    CACHE STRING "" FORCE)

set(CMAKE_C_FLAGS_DEBUG   "-O0 -g3" CACHE STRING "" FORCE)
set(CMAKE_C_FLAGS_RELEASE "-Os -g0" CACHE STRING "" FORCE)

# Note: CMAKE_SOURCE_DIR is valid at link time (try_compile uses STATIC_LIBRARY
# so the linker is never invoked during toolchain probing).
set(CMAKE_EXE_LINKER_FLAGS
    "${MCU_FLAGS} -T \"${CMAKE_SOURCE_DIR}/STM32F303XX_FLASH.ld\" \
     --specs=nano.specs -Wl,--gc-sections -Wl,--print-memory-usage"
    CACHE STRING "" FORCE)

# Extra libs required by the C runtime on bare-metal (consumed by BSP)
set(TOOLCHAIN_LINK_LIBRARIES m)
