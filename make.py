#!/usr/bin/env python

# by: Kwabena W. Agyeman - kwagyeman@openmv.io

import argparse, multiprocessing, os, shutil, sys

def make():

    __folder__ = os.path.dirname(os.path.abspath(__file__))

    parser = argparse.ArgumentParser(description =
    "Make Script")

    parser.add_argument("-s", "--skip_generate_projects", action='store_true', default=False,
    help = "Skip generate_projects")

    args = parser.parse_args()

    ###########################################################################

    cpus = multiprocessing.cpu_count()

    builddir = os.path.join(__folder__, "build")

    if not os.path.exists(builddir):
        os.mkdir(builddir)

    if not args.skip_generate_projects:
        if os.system("cd tensorflow" +
        " && make -f tensorflow/lite/experimental/micro/tools/make/Makefile TAGS=\"openmvcam\" generate_projects"):
            sys.exit("Make Failed...")

    # OPENMV1 #################################################################

    if os.path.exists(os.path.join(builddir, "OPENMV1")):
        shutil.rmtree(os.path.join(builddir, "OPENMV1"), ignore_errors = True)
    shutil.copytree("tensorflow/tensorflow/lite/experimental/micro/tools/make/gen/linux_x86_64/prj/micro_speech/make",
                    os.path.join(builddir, "OPENMV1"))

    data = None
    with open(os.path.join(builddir, "OPENMV1/Makefile"), 'r') as original:
        data = original.read()
        data = data.replace("  tensorflow/lite/experimental/micro/examples/micro_speech/main.cc", " libtf.cc")
        data = data.replace("$(CXX) $(CXXFLAGS) -o $@ $(OBJS) $(LDFLAGS)", "arm-none-eabi-ar rcs libtf.a $<")

    with open(os.path.join(builddir, "OPENMV1/Makefile"), 'w') as modified:
        modified.write("CC = arm-none-eabi-gcc\n")
        modified.write("CXX = arm-none-eabi-g++\n")
        modified.write("CCFLAGS += -mthumb -nostartfiles -fdata-sections -ffunction-sections\n")
        modified.write("CXXFLAGS += -mthumb -nostartfiles -fdata-sections -ffunction-sections\n")
        modified.write("CCFLAGS += -mcpu=cortex-m4 -mtune=cortex-m4 -mfpu=fpv4-sp-d16 -mfloat-abi=hard\n")
        modified.write("CXXFLAGS += -mcpu=cortex-m4 -mtune=cortex-m4 -mfpu=fpv4-sp-d16 -mfloat-abi=hard\n")
        modified.write(data)

    shutil.copy(os.path.join(__folder__, "libtf.cc"), os.path.join(builddir, "OPENMV1"))
    shutil.copy(os.path.join(__folder__, "libtf.h"), os.path.join(builddir, "OPENMV1"))

    if os.system("cd " + os.path.join(builddir, "OPENMV1") + " && make -j" + str(cpus)):
        sys.exit("Make Failed...")

    # OPENMV2 #################################################################

    if os.path.exists(os.path.join(builddir, "OPENMV2")):
        shutil.rmtree(os.path.join(builddir, "OPENMV2"), ignore_errors = True)
    shutil.copytree("tensorflow/tensorflow/lite/experimental/micro/tools/make/gen/linux_x86_64/prj/micro_speech/make",
                    os.path.join(builddir, "OPENMV2"))

    data = None
    with open(os.path.join(builddir, "OPENMV2/Makefile"), 'r') as original:
        data = original.read()
        data = data.replace("  tensorflow/lite/experimental/micro/examples/micro_speech/main.cc", " libtf.cc")
        data = data.replace("$(CXX) $(CXXFLAGS) -o $@ $(OBJS) $(LDFLAGS)", "arm-none-eabi-ar rcs libtf.a $<")

    with open(os.path.join(builddir, "OPENMV2/Makefile"), 'w') as modified:
        modified.write("CC = arm-none-eabi-gcc\n")
        modified.write("CXX = arm-none-eabi-g++\n")
        modified.write("CCFLAGS += -mthumb -nostartfiles -fdata-sections -ffunction-sections\n")
        modified.write("CXXFLAGS += -mthumb -nostartfiles -fdata-sections -ffunction-sections\n")
        modified.write("CCFLAGS += -mcpu=cortex-m4 -mtune=cortex-m4 -mfpu=fpv4-sp-d16 -mfloat-abi=hard\n")
        modified.write("CXXFLAGS += -mcpu=cortex-m4 -mtune=cortex-m4 -mfpu=fpv4-sp-d16 -mfloat-abi=hard\n")
        modified.write(data)

    shutil.copy(os.path.join(__folder__, "libtf.cc"), os.path.join(builddir, "OPENMV2"))
    shutil.copy(os.path.join(__folder__, "libtf.h"), os.path.join(builddir, "OPENMV2"))

    if os.system("cd " + os.path.join(builddir, "OPENMV2") + " && make -j" + str(cpus)):
        sys.exit("Make Failed...")

    # OPENMV3 #################################################################

    if os.path.exists(os.path.join(builddir, "OPENMV3")):
        shutil.rmtree(os.path.join(builddir, "OPENMV3"), ignore_errors = True)
    shutil.copytree("tensorflow/tensorflow/lite/experimental/micro/tools/make/gen/linux_x86_64/prj/micro_speech/make",
                    os.path.join(builddir, "OPENMV3"))

    data = None
    with open(os.path.join(builddir, "OPENMV3/Makefile"), 'r') as original:
        data = original.read()
        data = data.replace("  tensorflow/lite/experimental/micro/examples/micro_speech/main.cc", " libtf.cc")
        data = data.replace("$(CXX) $(CXXFLAGS) -o $@ $(OBJS) $(LDFLAGS)", "arm-none-eabi-ar rcs libtf.a $<")

    with open(os.path.join(builddir, "OPENMV3/Makefile"), 'w') as modified:
        modified.write("CC = arm-none-eabi-gcc\n")
        modified.write("CXX = arm-none-eabi-g++\n")
        modified.write("CCFLAGS += -mthumb -nostartfiles -fdata-sections -ffunction-sections\n")
        modified.write("CXXFLAGS += -mthumb -nostartfiles -fdata-sections -ffunction-sections\n")
        modified.write("CCFLAGS += -mcpu=cortex-m7 -mtune=cortex-m7 -mfpu=fpv5-sp-d16 -mfloat-abi=hard\n")
        modified.write("CXXFLAGS += -mcpu=cortex-m7 -mtune=cortex-m7 -mfpu=fpv5-sp-d16 -mfloat-abi=hard\n")
        modified.write(data)

    shutil.copy(os.path.join(__folder__, "libtf.cc"), os.path.join(builddir, "OPENMV3"))
    shutil.copy(os.path.join(__folder__, "libtf.h"), os.path.join(builddir, "OPENMV3"))

    if os.system("cd " + os.path.join(builddir, "OPENMV3") + " && make -j" + str(cpus)):
        sys.exit("Make Failed...")

    # OPENMV4 #################################################################

    if os.path.exists(os.path.join(builddir, "OPENMV4")):
        shutil.rmtree(os.path.join(builddir, "OPENMV4"), ignore_errors = True)
    shutil.copytree("tensorflow/tensorflow/lite/experimental/micro/tools/make/gen/linux_x86_64/prj/micro_speech/make",
                    os.path.join(builddir, "OPENMV4"))

    data = None
    with open(os.path.join(builddir, "OPENMV4/Makefile"), 'r') as original:
        data = original.read()
        data = data.replace("  tensorflow/lite/experimental/micro/examples/micro_speech/main.cc", " libtf.cc")
        data = data.replace("$(CXX) $(CXXFLAGS) -o $@ $(OBJS) $(LDFLAGS)", "arm-none-eabi-ar rcs libtf.a $<")

    with open(os.path.join(builddir, "OPENMV4/Makefile"), 'w') as modified:
        modified.write("CC = arm-none-eabi-gcc\n")
        modified.write("CXX = arm-none-eabi-g++\n")
        modified.write("CCFLAGS += -mthumb -nostartfiles -fdata-sections -ffunction-sections\n")
        modified.write("CXXFLAGS += -mthumb -nostartfiles -fdata-sections -ffunction-sections\n")
        modified.write("CCFLAGS += -mcpu=cortex-m7 -mtune=cortex-m7 -mfpu=fpv5-sp-d16 -mfloat-abi=hard\n")
        modified.write("CXXFLAGS += -mcpu=cortex-m7 -mtune=cortex-m7 -mfpu=fpv5-sp-d16 -mfloat-abi=hard\n")
        modified.write(data)

    shutil.copy(os.path.join(__folder__, "libtf.cc"), os.path.join(builddir, "OPENMV4"))
    shutil.copy(os.path.join(__folder__, "libtf.h"), os.path.join(builddir, "OPENMV4"))

    if os.system("cd " + os.path.join(builddir, "OPENMV4") + " && make -j" + str(cpus)):
        sys.exit("Make Failed...")

    ###########################################################################

if __name__ == "__main__":
    make()

