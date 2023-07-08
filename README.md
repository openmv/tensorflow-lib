# tensorflow-lib #
TensorFlow package for Cortex-M0-Plus, Cortex-M4, Cortex-M7, and Cortex-M55 CPUs.

Instructions for building
=========================

1. Clone this repo recursively:

    ```
    git clone --recursive https://github.com/openmv/tensorflow-lib.git
    ```

2. Install GCC:

    ```
    source ci.sh && ci_install_arm_gcc
    ```

3. In `/`, do:

    ```
    source ci.sh ci_build
    ```

Prebuilt Files
==============

You can find libtf pre-built under [releases](https://github.com/openmv/tensorflow-lib/releases). Alternatively, you may include this repo as a submodule and use [libtf](libtf) directly from the repo. This will allow you to easily update libtf without having to store the binaries directly in your repo.
