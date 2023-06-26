# tensorflow-lib #
TensorFlow package for Cortex-M0-Plus, Cortex-M4, Cortex-M7, and Cortex-M55 CPUs.

Instructions for building
=========================

1. Clone this repo recursively:

    ```
    git clone --recursive https://github.com/openmv/tensorflow-lib.git
    ```

2. Run these commands:

    ```
    sudo apt-get remove gcc-arm-none-eabi
    sudo apt-get autoremove
    sudo add-apt-repository ppa:team-gcc-arm-embedded/ppa
    sudo apt-get update
    sudo apt-get install gcc-arm-embedded
    sudo apt-get install libc6-i386
    ```

3. In `/`, do:

    ```
    ./make.py
    ```

Prebuilt Files
==============

You can find libtf pre-built under [releases](https://github.com/openmv/tensorflow-lib/releases).
