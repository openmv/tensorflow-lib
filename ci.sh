#!/bin/bash

########################################################################################
# Install ARM GCC.
TOOLCHAIN="gcc-arm-none-eabi-10-2020-q4-major-x86_64-linux.tar.bz2"
TOOLCHAIN_PATH=${HOME}/cache/gcc
TOOLCHAIN_URL="https://armkeil.blob.core.windows.net/developer/Files/downloads/gnu-rm/10-2020q4/${TOOLCHAIN}"

ci_install_arm_gcc_apt() {
    sudo apt-get install gcc-arm-none-eabi libnewlib-arm-none-eabi
    arm-none-eabi-gcc --version
}

ci_install_arm_gcc() {
    mkdir -p ${TOOLCHAIN_PATH}
    wget --no-check-certificate -O - ${TOOLCHAIN_URL} | tar --strip-components=1 -jx -C ${TOOLCHAIN_PATH}
    export PATH=${TOOLCHAIN_PATH}/bin:${PATH}
    arm-none-eabi-gcc --version
}

########################################################################################
# Update Submodules.

ci_update_submodules() {
  git submodule update --init --recursive
}

########################################################################################
# Build Targets.

ci_build_target() {
    export PATH=${TOOLCHAIN_PATH}/bin:${PATH}
    python make.py
}

########################################################################################
# Prepare Firmware Packages.

ci_package_release() {
    (cd libtf && zip -r ../libtf.zip *)
}

ci_package_development() {
    (cd libtf && zip -r ../libtf.zip *)
}
