# tensorflow-lib #

TensorFlow package for Cortex-M0-Plus, Cortex-M4, Cortex-M7, and Cortex-M55 CPUs.

Instructions for building
=========================

1. Clone this repo recursively:

    ```
    git clone --recursive https://github.com/openmv/tensorflow-lib.git
    ```

2. If you already have `arm-none-eabi-gcc` installed and available on your path do:

    ```
    python make.py
    ```

3. Otherwise, install GCC (only needs to be done once):

    ```
    source ci.sh && ci_install_arm_gcc
    ```

4. And then do:

    ```
    source ci.sh ci_build
    ```

You will need to use the `source ci.sh ci_build` to compile the library if you installed gcc via `source ci.sh && ci_install_arm_gcc` and did not add GCC to your path.

Prebuilt Files
==============

You can find libtf pre-built under [releases](https://github.com/openmv/tensorflow-lib/releases). Alternatively, you may include this repo as a submodule and use [libtf](libtf) directly from the repo. This will allow you to easily update libtf without having to store the binaries directly in your repo.
