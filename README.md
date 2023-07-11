[![Firmware Build 🔥](https://github.com/openmv/tensorflow-lib/actions/workflows/firmware.yml/badge.svg)](https://github.com/openmv/tensorflow-lib/actions/workflows/firmware.yml)
[![GitHub license](https://img.shields.io/github/license/openmv/tensorflow-lib?label=license%20%E2%9A%96)](https://github.com/openmv/tensorflow-lib/blob/master/LICENSE)
![GitHub release (latest SemVer)](https://img.shields.io/github/v/release/openmv/tensorflow-lib?sort=semver)
[![GitHub forks](https://img.shields.io/github/forks/openmv/tensorflow-lib?color=green)](https://github.com/openmv/tensorflow-lib/network)
[![GitHub stars](https://img.shields.io/github/stars/openmv/tensorflow-lib?color=yellow)](https://github.com/openmv/tensorflow-lib/stargazers)
[![GitHub issues](https://img.shields.io/github/issues/openmv/tensorflow-lib?color=orange)](https://github.com/openmv/tensorflow-lib/issues)

<img  width="480" src="https://raw.githubusercontent.com/openmv/openmv-media/master/logos/openmv-logo/logo.png">

# tensorflow-lib #

TensorFlow package for Cortex-M0-Plus, Cortex-M4, Cortex-M7, and Cortex-M55 CPUs.

Instructions for building
=========================

1. Clone this repo recursively:

       git clone --recursive https://github.com/openmv/tensorflow-lib.git

2. If you already have `arm-none-eabi-gcc` installed and available on your path do:

       python make.py

3. Otherwise, install GCC (only needs to be done once):

       source ci.sh && ci_install_arm_gcc

4. And then do:

       source ci.sh ci_build

You will need to use the `source ci.sh ci_build` to compile the library if you installed gcc via `source ci.sh && ci_install_arm_gcc` and did not add GCC to your path.

Prebuilt Files
==============

You can find libtf pre-built under [releases](https://github.com/openmv/tensorflow-lib/releases). Alternatively, you may include this repo as a submodule and use [libtf](libtf) directly from the repo. This will allow you to easily update libtf without having to store the binaries directly in your repo.
