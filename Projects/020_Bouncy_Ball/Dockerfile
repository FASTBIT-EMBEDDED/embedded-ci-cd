FROM ubuntu:24.04

ENV DEBIAN_FRONTEND=noninteractive
ENV TZ=UTC

RUN apt-get update && apt-get install -y \
    build-essential \
    cmake \
    ninja-build \
    python3 \
    python3-pip \
    python3-venv \
    git \
    curl \
    wget \
    unzip \
    clang-format \
    clang-tidy \
    cppcheck \
    ccache \
    gcc-arm-none-eabi \
    binutils-arm-none-eabi \
    gdb-multiarch \
    && rm -rf /var/lib/apt/lists/*

WORKDIR /workspace

# optional: make python available as "python"
RUN ln -sf /usr/bin/python3 /usr/bin/python

# ccache defaults
ENV CCACHE_DIR=/ccache
ENV CC="ccache gcc"
ENV CXX="ccache g++"

CMD ["/bin/bash"]