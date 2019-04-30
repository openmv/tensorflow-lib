#!/usr/bin/env python

# by: Kwabena W. Agyeman - kwagyeman@openmv.io

import argparse, multiprocessing, os, shutil, sys

def generate(target, __folder__, cpus, builddir, bindir, compile_flags):

    if os.system("cd tensorflow" +
    " && git clean -fdx" +
    " && make -f tensorflow/lite/experimental/micro/tools/make/Makefile test" +
    " && make -f tensorflow/lite/experimental/micro/tools/make/Makefile TAGS=\"openmvcam\" generate_projects"):
        sys.exit("Make Failed...")

    if os.path.exists(os.path.join(builddir, target)):
        shutil.rmtree(os.path.join(builddir, target), ignore_errors = True)
    shutil.copytree("tensorflow/tensorflow/lite/experimental/micro/tools/make/gen/linux_x86_64/prj/micro_speech/make",
                    os.path.join(builddir, target))

    data = None
    with open(os.path.join(builddir, target, "Makefile"), 'r') as original:
        data = original.read()
        data = data.replace("  tensorflow/lite/experimental/micro/examples/micro_speech/main.cc", " libtf.cc")
        data = data.replace("--std=c++11 -g -DTF_LITE_STATIC_MEMORY", "--std=c++11 -DTF_LITE_STATIC_MEMORY")
        data = data.replace("-DNDEBUG -g -DTF_LITE_STATIC_MEMORY", "-DNDEBUG -DTF_LITE_STATIC_MEMORY")
        data = data.replace("$(CXX) $(CXXFLAGS) -o $@ $(OBJS) $(LDFLAGS)", "arm-none-eabi-ar rcs libtf.a $(OBJS)")

    with open(os.path.join(builddir, target, "Makefile"), 'w') as modified:
        modified.write("CC = arm-none-eabi-gcc\n")
        modified.write("CXX = arm-none-eabi-g++\n")
        modified.write("CCFLAGS += " + compile_flags + "\n")
        modified.write("CXXFLAGS += " + compile_flags + "\n")
        modified.write(data)

    shutil.copy(os.path.join(__folder__, "libtf.cc"), os.path.join(builddir, target))
    shutil.copy(os.path.join(__folder__, "libtf.h"), os.path.join(builddir, target))
    shutil.copy(os.path.join(__folder__, "models/mobilenet_v1_0.25_128_quant/libtf-mobilenet.c"), os.path.join(builddir, target))
    shutil.copy(os.path.join(__folder__, "libtf-mobilenet.h"), os.path.join(builddir, target))

    if os.system("cd " + os.path.join(builddir, target) + " && make -j" + str(cpus) + 
        " && arm-none-eabi-gcc " + compile_flags + " -o libtf-mobilenet.o -c libtf-mobilenet.c" +
        " && arm-none-eabi-ar rcs libtf-mobilenet.a libtf-mobilenet.o"):
        sys.exit("Make Failed...")

    if not os.path.exists((os.path.join(bindir, target))):
        os.mkdir(os.path.join(bindir, target))
    shutil.copy(os.path.join(builddir, target, "libtf.a"), os.path.join(bindir, target))
    shutil.copy(os.path.join(builddir, target, "libtf-mobilenet.a"), os.path.join(bindir, target))
    shutil.copy(os.path.join(__folder__, "libtf.h"), os.path.join(bindir, target))
    shutil.copy(os.path.join(__folder__, "libtf-mobilenet.h"), os.path.join(bindir, target))

    with open(os.path.join(bindir, target, "README.txt"), 'w') as file:
        file.write("Compiled with " + compile_flags + "\n")
        file.write("Make sure to link this library with arm-none-eabi-g++ as it was written in C++.\n")
        file.write("Finally, this library outputs debugging information via printf() (so printf() must be implemented on your system).\n")

def build_target(target, __folder__, cpus, builddir, bindir):

    if (target == "OPENMV1") or (target == "OPENMV2") or (target == "cortex-m4"):
        generate(target, __folder__, cpus, builddir, bindir, "-mthumb -nostartfiles -fdata-sections -ffunction-sections -mcpu=cortex-m4 -mtune=cortex-m4 -mfpu=fpv4-sp-d16 -mfloat-abi=hard")
    elif (target == "OPENMV3") or (target == "OPENMV4") or (target == "cortex-m7"):
        generate(target, __folder__, cpus, builddir, bindir, "-mthumb -nostartfiles -fdata-sections -ffunction-sections -mcpu=cortex-m7 -mtune=cortex-m7 -mfpu=fpv5-sp-d16 -mfloat-abi=hard")
    else:
        sys.exit("Unknown target!")

def make():

    __folder__ = os.path.dirname(os.path.abspath(__file__))

    parser = argparse.ArgumentParser(description =
    "Make Script")

    args = parser.parse_args()

    ###########################################################################

    cpus = multiprocessing.cpu_count()

    builddir = os.path.join(__folder__, "build")

    if not os.path.exists(builddir):
        os.mkdir(builddir)

    bindir = os.path.join(__folder__, "bin")

    if not os.path.exists(bindir):
        os.mkdir(bindir)

    build_target("OPENMV1", __folder__, cpus, builddir, bindir)
    build_target("OPENMV2", __folder__, cpus, builddir, bindir)
    build_target("cortex-m4", __folder__, cpus, builddir, bindir)
    build_target("OPENMV3", __folder__, cpus, builddir, bindir)
    build_target("OPENMV4", __folder__, cpus, builddir, bindir) 
    build_target("cortex-m7", __folder__, cpus, builddir, bindir)

if __name__ == "__main__":
    make()
