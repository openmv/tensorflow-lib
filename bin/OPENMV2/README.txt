Compiled with -mthumb -nostartfiles -fdata-sections -ffunction-sections -mcpu=cortex-m4 -mtune=cortex-m4 -mfpu=fpv4-sp-d16 -mfloat-abi=hard
Make sure to link this library with arm-none-eabi-g++ as it was written in C++.
Finally, this library outputs debugging information via printf() (so printf() must be implemented on your system).
