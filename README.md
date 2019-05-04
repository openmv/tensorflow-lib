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

You can find libtf pre-built in the [lib](lib) folder for the OpenMV Cam 1/2/cortex-m4 and OpenMV Cam 3/4/cortex-m7. Additionally, the smallest version of MobileNet V1 is included too.

If you'd like to run larger MobileNet V1 models you can download them from [here](https://github.com/tensorflow/models/blob/master/research/slim/nets/mobilenet_v1.md) and then you just need to do `xxd -i model.tflite > model.c` to convert the model to a c file. Finally, you will then need to manually fix variable types in the c file afterwards to make the c file compatible with our [header file](https://github.com/openmv/tensorflow-lib/blob/master/libtf-mobilenet.h).
