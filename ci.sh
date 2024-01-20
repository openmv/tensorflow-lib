#!/bin/bash

########################################################################################
# Install ARM GCC.
TOOLCHAIN_PATH=${HOME}/cache/gcc
TOOLCHAIN_URL="https://developer.arm.com/-/media/Files/downloads/gnu/13.2.rel1/binrel/arm-gnu-toolchain-13.2.rel1-x86_64-arm-none-eabi.tar.xz"

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

ci_build() {
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
