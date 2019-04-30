# tensorflow-lib #
TensorFlow package for the Cortex-M4 and Cortex-M7.

Instructions for building
=========================

In `/`, do:

     ```
     $ ./make.py
     ```

If you get errors, install the missing tools. E.g. https://github.com/openmv/openmv/wiki#linux-installation

Prebuilt Files
==============

In `bin` you'll find libtf built for the OpenMV Cam 1/2/cortex-m4 and OpenMV Cam 3/4/cortex-m7. Additionally, the smallest version of mobilenet is included for linking into the OpenMV Cam binary image (only fits on the OpenMV Cam 3/4).

If you'd like to run larger mobilenet models you can download them from [here](https://github.com/tensorflow/models/blob/master/research/slim/nets/mobilenet_v1.md) and then you just need to do `xxd -i model.tflite > model.c` to convert the model to a c file. You will also need to manually fix variable types in the c file afterwards to make the c file compatible with our [header file](https://github.com/openmv/tensorflow-lib/blob/master/libtf-mobilenet.h).
