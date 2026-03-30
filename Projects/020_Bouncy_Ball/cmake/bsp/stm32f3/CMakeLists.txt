# cmake/bsp/stm32f3/CMakeLists.txt
# Board Support Package: STM32F303 HAL + startup sources
#
# Exposes one public target:  bsp  (INTERFACE library)
# App and driver code links against bsp to get includes + defines.
# The HAL itself is compiled as a separate OBJECT library so it is only
# rebuilt when STM32 drivers change, not when application code changes.

cmake_minimum_required(VERSION 3.22)
enable_language(C ASM)

# ── Public interface: includes + defines ──────────────────────────────────────
add_library(bsp INTERFACE)

target_include_directories(bsp INTERFACE
    ${CMAKE_SOURCE_DIR}/Core/Inc
    ${CMAKE_SOURCE_DIR}/Drivers/STM32F3xx_HAL_Driver/Inc
    ${CMAKE_SOURCE_DIR}/Drivers/STM32F3xx_HAL_Driver/Inc/Legacy
    ${CMAKE_SOURCE_DIR}/Drivers/CMSIS/Device/ST/STM32F3xx/Include
    ${CMAKE_SOURCE_DIR}/Drivers/CMSIS/Include
)

target_compile_definitions(bsp INTERFACE
    USE_HAL_DRIVER
    STM32F303xC
    $<$<CONFIG:Debug>:DEBUG>
)

# ── HAL static library ────────────────────────────────────────────────────────
add_library(stm32_hal OBJECT
    ${CMAKE_SOURCE_DIR}/Core/Src/system_stm32f3xx.c
    ${CMAKE_SOURCE_DIR}/Drivers/STM32F3xx_HAL_Driver/Src/stm32f3xx_hal_i2c.c
    ${CMAKE_SOURCE_DIR}/Drivers/STM32F3xx_HAL_Driver/Src/stm32f3xx_hal_i2c_ex.c
    ${CMAKE_SOURCE_DIR}/Drivers/STM32F3xx_HAL_Driver/Src/stm32f3xx_hal.c
    ${CMAKE_SOURCE_DIR}/Drivers/STM32F3xx_HAL_Driver/Src/stm32f3xx_hal_rcc.c
    ${CMAKE_SOURCE_DIR}/Drivers/STM32F3xx_HAL_Driver/Src/stm32f3xx_hal_rcc_ex.c
    ${CMAKE_SOURCE_DIR}/Drivers/STM32F3xx_HAL_Driver/Src/stm32f3xx_hal_gpio.c
    ${CMAKE_SOURCE_DIR}/Drivers/STM32F3xx_HAL_Driver/Src/stm32f3xx_hal_dma.c
    ${CMAKE_SOURCE_DIR}/Drivers/STM32F3xx_HAL_Driver/Src/stm32f3xx_hal_cortex.c
    ${CMAKE_SOURCE_DIR}/Drivers/STM32F3xx_HAL_Driver/Src/stm32f3xx_hal_pwr.c
    ${CMAKE_SOURCE_DIR}/Drivers/STM32F3xx_HAL_Driver/Src/stm32f3xx_hal_pwr_ex.c
    ${CMAKE_SOURCE_DIR}/Drivers/STM32F3xx_HAL_Driver/Src/stm32f3xx_hal_flash.c
    ${CMAKE_SOURCE_DIR}/Drivers/STM32F3xx_HAL_Driver/Src/stm32f3xx_hal_flash_ex.c
    ${CMAKE_SOURCE_DIR}/Drivers/STM32F3xx_HAL_Driver/Src/stm32f3xx_hal_exti.c
    ${CMAKE_SOURCE_DIR}/Drivers/STM32F3xx_HAL_Driver/Src/stm32f3xx_hal_spi.c
    ${CMAKE_SOURCE_DIR}/Drivers/STM32F3xx_HAL_Driver/Src/stm32f3xx_hal_spi_ex.c
)
target_link_libraries(stm32_hal PUBLIC bsp)

# ── Application/startup sources added to the main executable ─────────────────
target_sources(${CMAKE_PROJECT_NAME} PRIVATE
    ${CMAKE_SOURCE_DIR}/Core/Src/main.c
    ${CMAKE_SOURCE_DIR}/Core/Src/stm32f3xx_it.c
    ${CMAKE_SOURCE_DIR}/Core/Src/stm32f3xx_hal_msp.c
    ${CMAKE_SOURCE_DIR}/Core/Src/sysmem.c
    ${CMAKE_SOURCE_DIR}/Core/Src/syscalls.c
    ${CMAKE_SOURCE_DIR}/Core/Startup/startup_stm32f303cctx.s
)

target_link_libraries(${CMAKE_PROJECT_NAME} PRIVATE
    stm32_hal
    bsp
    ${TOOLCHAIN_LINK_LIBRARIES}
)

# Map file is generated at link time; register it for `cmake --build --target clean`
target_link_options(${CMAKE_PROJECT_NAME} PRIVATE
    -Wl,-Map=${CMAKE_PROJECT_NAME}.map
)
set_target_properties(${CMAKE_PROJECT_NAME} PROPERTIES
    ADDITIONAL_CLEAN_FILES ${CMAKE_PROJECT_NAME}.map
)
