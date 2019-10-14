# tensorflow-lib #
TensorFlow package for Cortex-M4 and Cortex-M7 CPUs with hardware floating point.

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

You can find libtf pre-built in the [lib](lib) folder for the OpenMV Cam 1/2/cortex-m4 and OpenMV Cam 3/4/cortex-m7.
