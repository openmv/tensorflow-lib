#!/usr/bin/env python

# by: Kwabena W. Agyeman - kwagyeman@openmv.io

import argparse, multiprocessing, os, shutil, sys

def generate(target, target_arch, __folder__, args, cpus, builddir, libdir, compile_flags):

    print("==============================\n Building Target - " + target + "\n==============================")

    project_folder = "tensorflow/tensorflow/lite/experimental/micro/tools/make/gen/linux_" + target_arch + "/prj/softmax_test/make"

    if (not os.path.isdir("tensorflow/tensorflow/lite/experimental/micro/tools/make/gen/linux_x86_64/prj/softmax_test/make")) or (not args.skip_generation):
        if os.system("cd tensorflow" +
        " && make -f tensorflow/lite/experimental/micro/tools/make/Makefile -j" + str(cpus) + " TAGS=\"openmvcam\" TARGET_ARCH=\"" + target_arch + "\" generate_projects"):
            sys.exit("Make Failed...")

    if os.path.exists(os.path.join(builddir, target)):
        shutil.rmtree(os.path.join(builddir, target), ignore_errors = True)

    shutil.copytree(project_folder,
                    os.path.join(builddir, target))

    shutil.copytree("libm",
                    os.path.join(builddir, target, "libm"))

    with open(os.path.join(builddir, target, "Makefile"), 'r') as original:
        data = original.read()
        data = data.replace("tensorflow/lite/experimental/micro/kernels/softmax_test.cc", "libtf.cc libm/exp.c libm/floor.c libm/frexp.c libm/round.c libm/scalbn.c")
        data = data.replace("-O3 -DNDEBUG --std=c++11 -g -DTF_LITE_STATIC_MEMORY", "")
        data = data.replace("-DNDEBUG -g -DTF_LITE_STATIC_MEMORY", "")
        data = data.replace("$(CXX) $(CXXFLAGS) -o $@ $(OBJS) $(LDFLAGS)", "arm-none-eabi-ar rcs libtf.a $(OBJS)")

    with open(os.path.join(builddir, target, "Makefile"), 'w') as modified:
        modified.write("CC = arm-none-eabi-gcc\n")
        modified.write("CXX = arm-none-eabi-g++\n")
        modified.write("CCFLAGS += " + compile_flags.replace("-fno-rtti ", "").replace("-std=c++11 ", "").replace("-std=gnu++11 ", "").replace("-fpermissive ", "") + "\n")
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

    if not os.path.exists((os.path.join(libdir, target))):
        os.mkdir(os.path.join(libdir, target))

    shutil.copy(os.path.join(builddir, target, "libtf.a"), os.path.join(libdir, target))
    shutil.copy(os.path.join(builddir, target, "libtf-mobilenet.a"), os.path.join(libdir, target))
    shutil.copy(os.path.join(__folder__, "libtf.h"), os.path.join(libdir, target))
    shutil.copy(os.path.join(__folder__, "libtf-mobilenet.h"), os.path.join(libdir, target))

    with open(os.path.join(libdir, target, "README.txt"), 'w') as file:
        file.write("Compiled with " + compile_flags + "\n")
        file.write("Make sure to link this library with arm-none-eabi-g++ as it was written in C++.\n")
        file.write("Finally, this library outputs debugging information via puts() (so puts() must be implemented on your system).\n")

def build_target(target, __folder__, args, cpus, builddir, libdir):

    compile_flags = "-DNDEBUG " \
                    "-DTF_LITE_DISABLE_X86_NEON " \
                    "-DGEMMLOWP_ALLOW_SLOW_SCALAR_FALLBACK " \
                    "-DTF_LITE_STATIC_MEMORY " \
                    "-DTF_LITE_MCU_DEBUG_LOG " \
                    "-D __FPU_PRESENT=1 " \
                    "-fno-rtti " \
                    "-fmessage-length=0 " \
                    "-fno-exceptions " \
                    "-fno-unwind-tables " \
                    "-fno-builtin " \
                    "-ffunction-sections " \
                    "-fdata-sections " \
                    "-funsigned-char " \
                    "-MMD " \
                    "-mthumb " \
                    "-mlittle-endian " \
                    "-mno-unaligned-access " \
                    "-mfloat-abi=hard " \
                    "-std=c++11 " \
                    "-std=gnu++11 " \
                    "-Wvla " \
                    "-Wall " \
                    "-Wextra " \
                    "-Wno-unused-parameter " \
                    "-Wno-missing-field-initializers " \
                    "-Wno-write-strings " \
                    "-Wno-sign-compare " \
                    "-fno-delete-null-pointer-checks " \
                    "-fomit-frame-pointer " \
                    "-fpermissive " \
                    "-nostdlib " \
                    "-O3 "

    if (target == "OPENMV1") or (target == "OPENMV2") or (target == "cortex-m4"):
        generate(target, "cortex-m4", __folder__, args, cpus, builddir, libdir, compile_flags +
                                                                                "-DARM_MATH_CM4 " +
                                                                                "-DARM_CMSIS_NN_M4 " +
                                                                                "-mcpu=cortex-m4 " +
                                                                                "-mtune=cortex-m4 " +
                                                                                "-mfpu=fpv4-sp-d16")
    elif (target == "OPENMV3") or (target == "OPENMV4") or (target == "cortex-m7"):
        generate(target, "cortex-m7", __folder__, args, cpus, builddir, libdir, compile_flags +
                                                                                "-DARM_MATH_CM7 " +
                                                                                "-DARM_CMSIS_NN_M7 " +
                                                                                "-mcpu=cortex-m7 " +
                                                                                "-mtune=cortex-m7 " +
                                                                                "-mfpu=fpv5-sp-d16")
    else:
        sys.exit("Unknown target!")

def make():

    __folder__ = os.path.dirname(os.path.abspath(__file__))

    parser = argparse.ArgumentParser(description =
    "Make Script")

    parser.add_argument("--skip_generation", "-s", action="store_true", default=False,
    help="Skip TensorFlow library generation.")

    args = parser.parse_args()

    ###########################################################################

    cpus = multiprocessing.cpu_count()

    builddir = os.path.join(__folder__, "build")

    if not os.path.exists(builddir):
        os.mkdir(builddir)

    libdir = os.path.join(__folder__, "lib")

    if not os.path.exists(libdir):
        os.mkdir(libdir)

    ###########################################################################

    if (not os.path.isdir("tensorflow/tensorflow/lite/experimental/micro/tools/make/gen/linux_x86_64/prj/softmax_test/make")) or (not args.skip_generation):
        if os.system("cd tensorflow" +
        " && make -f tensorflow/lite/experimental/micro/tools/make/Makefile -j" + str(cpus) + " test"):
            sys.exit("Make Failed...")

    build_target("OPENMV1",   __folder__, args, cpus, builddir, libdir)
    build_target("OPENMV2",   __folder__, args, cpus, builddir, libdir)
    build_target("cortex-m4", __folder__, args, cpus, builddir, libdir)

    build_target("OPENMV3",   __folder__, args, cpus, builddir, libdir)
    build_target("OPENMV4",   __folder__, args, cpus, builddir, libdir) 
    build_target("cortex-m7", __folder__, args, cpus, builddir, libdir)

    print("==============================\n Done\n==============================")

if __name__ == "__main__":
    make()
