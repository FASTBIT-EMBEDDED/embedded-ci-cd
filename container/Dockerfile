FROM ubuntu:24.04

ENV DEBIAN_FRONTEND=noninteractive

# ── Base tools (same for every MCU) ───────────────────────
RUN apt-get update && apt-get install -y \
    cmake ninja-build make python3 python3-pip \
    git curl wget unzip \
    clang-format clang-tidy cppcheck ccache \
    && rm -rf /var/lib/apt/lists/*

# ── MCU toolchain (← swap this block per MCU) ─────────────
# STM32 / ARM:
RUN apt-get update && apt-get install -y \
    gcc-arm-none-eabi binutils-arm-none-eabi \
    && rm -rf /var/lib/apt/lists/*

# ESP32 would be:
# RUN pip3 install espidf ...

WORKDIR /workspace
RUN ln -sf /usr/bin/python3 /usr/bin/python