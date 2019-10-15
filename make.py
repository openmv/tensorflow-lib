#!/usr/bin/env python

# by: Kwabena W. Agyeman - kwagyeman@openmv.io

import argparse, multiprocessing, os, re, shutil, sys

def generate(target, target_arch, __folder__, args, cpus, builddir, libdir, c_compile_flags, cxx_compile_flags):

    print("==============================\n Building Target - " + target + "\n==============================")

    project_folder = "tensorflow/tensorflow/lite/experimental/micro/tools/make/gen/openmvcam_" + target_arch + "/prj/person_detection/make"

    if (not os.path.isdir(project_folder)) or (not args.skip_generation):
        if os.system("cd tensorflow" +
        " && make -f tensorflow/lite/experimental/micro/tools/make/Makefile -j" + str(cpus) + " TARGET=\"openmvcam\" TARGET_ARCH=\"" + target_arch + "\" generate_person_detection_make_project"):
            sys.exit("Make Failed...")
 
    if os.path.exists(os.path.join(builddir, target)):
        shutil.rmtree(os.path.join(builddir, target), ignore_errors = True)

    shutil.copytree(project_folder,
                    os.path.join(builddir, target))

    shutil.copytree("libm",
                    os.path.join(builddir, target, "libm"))

    with open(os.path.join(builddir, target, "Makefile"), 'r') as original:
        data = re.sub(r"tensorflow/lite/experimental/microfrontend/\S+[ \t]*", "", original.read())
        data = re.sub(r"tensorflow/lite/experimental/micro/examples/\S+[ \t]*", "", data)
        data = re.sub(r"tensorflow/lite/experimental/micro/tools/\S+[ \t]*", "", data)
        data = data.replace("SRCS := \\", "SRCS := libtf.cc libm/exp.c libm/floor.c libm/fmaxf.c libm/fminf.c libm/frexp.c libm/round.c libm/scalbn.c \\")
        data = data.replace("-O3 -DNDEBUG -std=c++11 -g -DTF_LITE_STATIC_MEMORY ", "")
        data = data.replace("-DNDEBUG -g -DTF_LITE_STATIC_MEMORY ", "")
        data = data.replace("$(CXX) $(CXXFLAGS) -o $@ $(OBJS) $(LDFLAGS)", "arm-none-eabi-ar rcs libtf.a $(OBJS)")

    with open(os.path.join(builddir, target, "Makefile"), 'w') as modified:
        modified.write("CC = arm-none-eabi-gcc\n")
        modified.write("CXX = arm-none-eabi-g++\n")
        modified.write("CCFLAGS += " + c_compile_flags + "\n")
        modified.write("CXXFLAGS += " + cxx_compile_flags + "\n")
        modified.write(data)

    shutil.copy(os.path.join(__folder__, "libtf.cc"), os.path.join(builddir, target))
    shutil.copy(os.path.join(__folder__, "libtf.h"), os.path.join(builddir, target))
    shutil.copy(os.path.join(project_folder, "tensorflow/lite/experimental/micro/tools/make/downloads/person_model_grayscale/person_detect_model_data.cc"), os.path.join(builddir, target, "libtf_person_detect_model_data.cc"))
    shutil.copy(os.path.join(project_folder, "tensorflow/lite/experimental/micro/examples/person_detection/person_detect_model_data.h"), os.path.join(builddir, target, "libtf_person_detect_model_data.h"))

    if os.system("cd " + os.path.join(builddir, target) + " && make -j" + str(cpus) +
        " && arm-none-eabi-gcc " + cxx_compile_flags + " -o libtf_person_detect_model_data.o -c libtf_person_detect_model_data.cc" +
        " && arm-none-eabi-ar rcs libtf_person_detect_model_data.a libtf_person_detect_model_data.o"):
        sys.exit("Make Failed...")

    if not os.path.exists((os.path.join(libdir, target))):
        os.mkdir(os.path.join(libdir, target))

    shutil.copy(os.path.join(builddir, target, "libtf.a"), os.path.join(libdir, target))
    shutil.copy(os.path.join(builddir, target, "libtf_person_detect_model_data.a"), os.path.join(libdir, target))
    shutil.copy(os.path.join(__folder__, "libtf.h"), os.path.join(libdir, target))
    shutil.copy(os.path.join(builddir, target, "libtf_person_detect_model_data.h"), os.path.join(libdir, target))
    shutil.copy(os.path.join(builddir, target, "LICENSE"), os.path.join(libdir, target))

    with open(os.path.join(libdir, target, "README"), "w") as f:
        f.write("You must link this library to your application with arm-none-eabi-g++ and have implemented puts().\n\n")
        f.write("C Compile Flags: " + c_compile_flags + "\n\n")
        f.write("CXX Compile Flags: " + cxx_compile_flags + "\n")

def build_target(target, __folder__, args, cpus, builddir, libdir):

    compile_flags = "-D __FPU_PRESENT=1 " \
                    "-DGEMMLOWP_ALLOW_SLOW_SCALAR_FALLBACK " \
                    "-DNDEBUG " \
                    "-DTF_LITE_DISABLE_X86_NEON " \
                    "-DTF_LITE_MCU_DEBUG_LOG " \
                    "-DTF_LITE_STATIC_MEMORY " \
                    "-MMD " \
                    "-O3 " \
                    "-Wall " \
                    "-Wextra " \
                    "-Wvla " \
                    "-Wno-missing-field-initializers " \
                    "-Wno-parentheses " \
                    "-Wno-sign-compare " \
                    "-Wno-strict-aliasing " \
                    "-Wno-type-limits " \
                    "-Wno-unused-but-set-variable " \
                    "-Wno-unused-parameter " \
                    "-Wno-unused-variable " \
                    "-Wno-write-strings " \
                    "-fdata-sections " \
                    "-ffunction-sections " \
                    "-fmessage-length=0 " \
                    "-fomit-frame-pointer " \
                    "-funsigned-char " \
                    "-fno-builtin " \
                    "-fno-delete-null-pointer-checks " \
                    "-fno-exceptions " \
                    "-fno-unwind-tables " \
                    "-mfloat-abi=hard " \
                    "-mlittle-endian " \
                    "-mthumb " \
                    "-mno-unaligned-access " \
                    "-nostdlib "

    c_compile_flags = compile_flags + \
                      "-Wno-pointer-sign "

    cxx_compile_flags = compile_flags + \
                        "-std=c++11 " \
                        "-std=gnu++11 " \
                        "-fno-rtti " \
                        "-fpermissive "

    if target == "cortex-m4":

        cortex_m4_compile_flags = "-DARM_CMSIS_NN_M4 " \
                                  "-DARM_MATH_CM4 " \
                                  "-mcpu=cortex-m4 " \
                                  "-mfpu=fpv4-sp-d16 " \
                                  "-mtune=cortex-m4"

        cortex_m4_c_compile_flags = c_compile_flags + cortex_m4_compile_flags

        cortex_m4_cxx_compile_flags = cxx_compile_flags + cortex_m4_compile_flags

        generate(target, "cortex-m4", __folder__, args, cpus, builddir, libdir,
                 cortex_m4_c_compile_flags, cortex_m4_cxx_compile_flags)

    elif target == "cortex-m7":

        cortex_m7_compile_flags = "-DARM_CMSIS_NN_M7 " \
                                  "-DARM_MATH_CM7 " \
                                  "-mcpu=cortex-m7 " \
                                  "-mfpu=fpv5-sp-d16 " \
                                  "-mtune=cortex-m7"

        cortex_m7_c_compile_flags = c_compile_flags + cortex_m7_compile_flags

        cortex_m7_cxx_compile_flags = cxx_compile_flags + cortex_m7_compile_flags

        generate(target, "cortex-m7", __folder__, args, cpus, builddir, libdir,
                 cortex_m7_c_compile_flags, cortex_m7_cxx_compile_flags)

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

    libdir = os.path.join(__folder__, "libtf")

    if not os.path.exists(libdir):
        os.mkdir(libdir)

    ###########################################################################

    if (not os.path.isfile("tensorflow/tensorflow/lite/experimental/micro/tools/make/gen/linux_x86_64/bin/person_detection_test")) or (not args.skip_generation):
        if os.system("cd tensorflow" +
        " && make -f tensorflow/lite/experimental/micro/tools/make/Makefile -j" + str(cpus) + " test_person_detection_test"):
            sys.exit("Make Failed...")

    build_target("cortex-m4", __folder__, args, cpus, builddir, libdir)
    build_target("cortex-m7", __folder__, args, cpus, builddir, libdir)

    print("==============================\n Done\n==============================")

if __name__ == "__main__":
    make()
