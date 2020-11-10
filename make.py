#!/usr/bin/env python

# by: Kwabena W. Agyeman - kwagyeman@openmv.io

import argparse, multiprocessing, os, re, shutil, sys

INT8 = False

UINT8_MODEL_C_PATH = "tensorflow/lite/micro/tools/make/downloads/person_model_grayscale/person_detect_model_data.cc"
UINT8_MODEL_H_PATH = "tensorflow/lite/micro/examples/person_detection/person_detect_model_data.h"

INT8_MODEL_C_PATH = "tensorflow/lite/micro/tools/make/downloads/person_model_int8/person_detect_model_data.cc"
INT8_MODEL_H_PATH = "tensorflow/lite/micro/examples/person_detection_experimental/person_detect_model_data.h"

MODEL_C_PATH = INT8_MODEL_C_PATH if INT8 else UINT8_MODEL_C_PATH
MODEL_H_PATH = INT8_MODEL_H_PATH if INT8 else UINT8_MODEL_H_PATH

def patch_files(dir_path):
    for dname, dirs, files in os.walk(dir_path):
        for fname in files:
            fpath = os.path.join(dname, fname)
            with open(fpath) as f:
                s = f.read()
            s = s.replace("fprintf", "(void)")
            with open(fpath, "w") as f:
                f.write(s)

def generate(target, target_arch, __folder__, args, cpus, builddir, libdir, c_compile_flags, cxx_compile_flags):

    print("==============================\n Building Target - " + target + "\n==============================")

    project_folder = "tensorflow/tensorflow/lite/micro/tools/make/gen/openmvcam_" + target_arch + "/prj/person_detection" + ("_int8" if INT8 else "") + "/make"

    if (not os.path.isdir(project_folder)) or (not args.skip_generation):
        if os.system("cd tensorflow" +
        " && make -f tensorflow/lite/micro/tools/make/Makefile -j" + str(cpus) + " TAGS=\"cmsis-nn\" TARGET=\"openmvcam\" TARGET_ARCH=\"" + target_arch + "\" generate_person_detection" + ("_int8" if INT8 else "") + "_make_project"):
            sys.exit("Make Failed...")

    if os.path.exists(os.path.join(builddir, target)):
        shutil.rmtree(os.path.join(builddir, target), ignore_errors = True)

    shutil.copytree(project_folder,
                    os.path.join(builddir, target))

    shutil.copytree("libm",
                    os.path.join(builddir, target, "libm"))

    shutil.copytree("tensorflow/tensorflow/lite/micro/tools/make/downloads/kissfft/",
                    os.path.join(builddir, target, "kissfft"))

    shutil.copytree("tensorflow/tensorflow/lite/experimental/microfrontend",
                    os.path.join(builddir, target, "microfrontend"))

    shutil.copytree("tensorflow/tensorflow/lite/micro/examples/micro_speech/micro_features/",
                    os.path.join(builddir, target, "micro_features"))

    patch_files(os.path.join(builddir, target, "kissfft"))
    patch_files(os.path.join(builddir, target, "microfrontend"))
    patch_files(os.path.join(builddir, target, "micro_features"))

    SRCS = [
        "SRCS :=",
        "libtf.cc",
        "libm/exp.c",
        "libm/floor.c",
        "libm/fmaxf.c",
        "libm/fminf.c",
        "libm/frexp.c",
        "libm/round.c",
        "libm/sqrt.c",
        "libm/scalbn.c",
        "libm/cos.c",
        "libm/__cos.c",
        "libm/sin.c",
        "libm/__sin.c",
        "libm/log1p.c",
        "libm/__rem_pio2.c",
        "libm/__rem_pio2_large.c",
        "kissfft/kiss_fft.c",
        "kissfft/tools/kiss_fftr.c",
        "microfrontend/lib/noise_reduction_io.c",
        "microfrontend/lib/filterbank_io.c",
        "microfrontend/lib/log_scale_util.c",
        "microfrontend/lib/fft_util.cc",
        "microfrontend/lib/log_lut.c",
        "microfrontend/lib/filterbank_util.c",
        "microfrontend/lib/frontend_memmap_generator.c",
        "microfrontend/lib/window.c",
        "microfrontend/lib/pcan_gain_control_util.c",
        "microfrontend/lib/frontend_io.c",
        "microfrontend/lib/frontend.c",
        "microfrontend/lib/window_util.c",
        "microfrontend/lib/fft.cc",
        "microfrontend/lib/log_scale_io.c",
        "microfrontend/lib/filterbank.c",
        "microfrontend/lib/fft_io.c",
        "microfrontend/lib/noise_reduction_util.c",
        "microfrontend/lib/noise_reduction.c",
        "microfrontend/lib/log_scale.c",
        "microfrontend/lib/frontend_util.c",
        "microfrontend/lib/pcan_gain_control.c",
        "micro_features/micro_features_generator.cc",
        "\\"
    ]

    with open(os.path.join(builddir, target, "Makefile"), 'r') as original:
        data = original.read().replace("SRCS := \\", " ".join(SRCS))
        data = data.replace("-std=c++11 -DTF_LITE_STATIC_MEMORY -DNDEBUG -O3 ", "")
        data = data.replace("-std=c11   -DTF_LITE_STATIC_MEMORY -DNDEBUG -O3 ", "")
        data = data.replace("LIBRARY_OBJS := $(filter-out tensorflow/lite/micro/examples/%, $(OBJS))", "LIBRARY_OBJS := $(OBJS)")
        data = re.sub(r"tensorflow/lite/micro/benchmarks/\S*", "", data)
        data = re.sub(r"tensorflow/lite/micro/testing/\S*", "", data)
        data = re.sub(r"tensorflow/lite/micro/examples/\S*", "", data)
        data = re.sub(r"tensorflow/lite/micro/tools/make/downloads/person_model_grayscale/\S*", "", data)
        data = re.sub(r"tensorflow/lite/micro/tools/make/downloads/person_model_int8/\S*", "", data)

    extra_includes = " -I./../../tensorflow/" \
                     " -I./tensorflow/lite/micro/tools/make/downloads" \
                     " -I./../../tensorflow/tensorflow/lite/micro/tools/make/downloads/cmsis/CMSIS/Core/Include"

    with open(os.path.join(builddir, target, "Makefile"), 'w') as modified:
        modified.write("CCFLAGS = " + c_compile_flags + extra_includes + "\n")
        modified.write("CXXFLAGS = " + cxx_compile_flags + extra_includes + "\n")
        modified.write(data)

    shutil.copy(os.path.join(__folder__, "libtf.cc"), os.path.join(builddir, target))
    shutil.copy(os.path.join(__folder__, "libtf.h"), os.path.join(builddir, target))
    shutil.copy(os.path.join(project_folder, MODEL_C_PATH), os.path.join(builddir, target, "libtf_person_detect_model_data.cc"))
    shutil.copy(os.path.join(project_folder, MODEL_H_PATH), os.path.join(builddir, target, "libtf_person_detect_model_data.h"))

    if os.system("cd " + os.path.join(builddir, target) + " && make -j " + str(cpus) + " lib TARGET_TOOLCHAIN_PREFIX=arm-none-eabi-"
        " && arm-none-eabi-gcc " + cxx_compile_flags + " -o libtf_person_detect_model_data.o -c libtf_person_detect_model_data.cc" +
        " && arm-none-eabi-ar rcs libtf_person_detect_model_data.a libtf_person_detect_model_data.o"):
        sys.exit("Make Failed...")

    if not os.path.exists((os.path.join(libdir, target))):
        os.mkdir(os.path.join(libdir, target))

    shutil.copy(os.path.join(builddir, target, "libtensorflow-microlite.a"), os.path.join(libdir, target, "libtf.a"))
    shutil.copy(os.path.join(builddir, target, "libtf_person_detect_model_data.a"), os.path.join(libdir, target))
    shutil.copy(os.path.join(__folder__, "libtf.h"), os.path.join(libdir, target))
    shutil.copy(os.path.join(builddir, target, "libtf_person_detect_model_data.h"), os.path.join(libdir, target))
    shutil.copy(os.path.join(builddir, target, "LICENSE"), os.path.join(libdir, target))

    with open(os.path.join(libdir, target, "README"), "w") as f:
        f.write("You must link this library to your application with arm-none-eabi-gcc and have implemented putchar().\n\n")
        f.write("C Compile Flags: " + c_compile_flags + "\n\n")
        f.write("CXX Compile Flags: " + cxx_compile_flags + "\n")

def build_target(target, __folder__, args, cpus, builddir, libdir):

    compile_flags = "-DGEMMLOWP_ALLOW_SLOW_SCALAR_FALLBACK " \
                    "-DNDEBUG " \
                    "-DTF_LITE_MCU_DEBUG_LOG " \
                    "-DTF_LITE_STATIC_MEMORY " \
                    "-MMD " \
                    "-O3 " \
                    "-Wall " \
                    "-Werror " \
                    "-Warray-bounds " \
                    "-Wextra " \
                    "-Wvla " \
                    "-Wno-missing-field-initializers " \
                    "-Wno-strict-aliasing " \
                    "-Wno-type-limits " \
                    "-Wno-unused-but-set-variable " \
                    "-Wno-unused-parameter " \
                    "-Wno-unused-variable " \
                    "-Wno-unused-value " \
                    "-Wno-error=sign-compare " \
                    "-Wno-error=nonnull " \
                    "-Wno-error=unused-value " \
                    "-fdata-sections " \
                    "-ffunction-sections " \
                    "-fmessage-length=0 " \
                    "-fomit-frame-pointer " \
                    "-funsigned-char " \
                    "-fshort-enums " \
                    "-fno-delete-null-pointer-checks " \
                    "-fno-exceptions " \
                    "-fno-unwind-tables " \
                    "-mabi=aapcs-linux " \
                    "-mfloat-abi=hard " \
                    "-mthumb " \
                    "-nostartfiles " \
                    "-nostdlib "

    c_compile_flags = compile_flags + \
                      "-std=c11 "

    cxx_compile_flags = compile_flags + \
                        "-std=c++11 " \
                        "-fno-rtti " \
                        "-fno-threadsafe-statics " \
                        "-fno-use-cxa-atexit "

    if target == "cortex-m4":

        cortex_m4_compile_flags = "-DARM_MATH_CM4 " \
                                  "-mcpu=cortex-m4 " \
                                  "-mfpu=fpv4-sp-d16 " \
                                  "-mtune=cortex-m4"

        cortex_m4_c_compile_flags = c_compile_flags + cortex_m4_compile_flags

        cortex_m4_cxx_compile_flags = cxx_compile_flags + cortex_m4_compile_flags

        generate(target, "cortex-m4", __folder__, args, cpus, builddir, libdir,
                 cortex_m4_c_compile_flags, cortex_m4_cxx_compile_flags)

    elif target == "cortex-m7":

        cortex_m7_compile_flags = "-DARM_MATH_CM7 " \
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

    if (not os.path.isfile("tensorflow/tensorflow/lite/micro/tools/make/gen/linux_x86_64/bin/person_detection_test" + ("_int8" if INT8 else ""))) or (not args.skip_generation):
        if os.system("cd tensorflow" +
        " && make -f tensorflow/lite/micro/tools/make/Makefile -j" + str(cpus) + " clean" +
        " && make -f tensorflow/lite/micro/tools/make/Makefile -j" + str(cpus) + " test_person_detection_test" + ("_int8" if INT8 else "")):
            sys.exit("Make Failed...")

    build_target("cortex-m4", __folder__, args, cpus, builddir, libdir)
    build_target("cortex-m7", __folder__, args, cpus, builddir, libdir)

    print("==============================\n Done\n==============================")

if __name__ == "__main__":
    make()
