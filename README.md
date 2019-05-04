# tensorflow-lib #
TensorFlow package for Cortex-M4 and Cortex-M7 CPUs with hardware floating point.

Instructions for building
=========================

1. Clone the repo recursively.
2. Run all the commands [here](https://github.com/openmv/openmv/wiki#linux-installation).
3. In `/`, do:

    ```
    $ ./make.py
    ```

Prebuilt Files
==============

You can find libtf pre-built in the [lib](lib) folder for the OpenMV Cam 1/2/cortex-m4 and OpenMV Cam 3/4/cortex-m7. Additionally, the smallest version of MobileNet V1 is included for linking into your binary image.

If you'd like to run larger MobileNet V1 models you can download them from [here](https://github.com/tensorflow/models/blob/master/research/slim/nets/mobilenet_v1.md) and then you just need to do `xxd -i model.tflite > model.c` to convert the model to a c file. Finally, you will then need to manually fix variable types in the c file afterwards to make the c file compatible with our [header file](https://github.com/openmv/tensorflow-lib/blob/master/libtf-mobilenet.h).
