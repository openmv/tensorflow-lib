#!/usr/bin/env python

# by: Kwabena W. Agyeman - kwagyeman@openmv.io

import argparse, multiprocessing, os, re, shutil, sys

TF_TOP = "edge-impulse-sdk"
TF_TOP_MICRO_PATH = os.path.join(TF_TOP, "tensorflow/lite/micro")
TF_TOP_GEN_PATH = os.path.join(TF_TOP_MICRO_PATH, "tools/make/gen")
TF_TOP_EXPERIMENTAL_PATH = os.path.join(TF_TOP, "tensorflow/lite/experimental")

TF_EXAMPLES_PATH = "tensorflow/lite/micro/examples"
TF_EXAMPLES_MICRO_FEATURES_PATH = os.path.join(TF_EXAMPLES_PATH, "micro_speech/micro_features")

TF_EXPERIMENTAL_PATH = "tensorflow/lite/experimental"
TF_EXPERIMENTAL_MICROFRONTEND_PATH = os.path.join(TF_EXPERIMENTAL_PATH, "microfrontend")

TF_TOOLS_PATH = "tensorflow/lite/micro/tools/make"
TF_TOOLS_DOWNLOADS_PATH = os.path.join(TF_TOOLS_PATH, "downloads")
TF_TOOLS_MAKEFILE_PATH = os.path.join(TF_TOOLS_PATH, "Makefile")

MAKE_PROJECT = "person_detection_int8"
TEST_PROJECT = "person_detection_test_int8"

def patch_files(dir_path):
    for dname, dirs, files in os.walk(dir_path):
        for fname in files:
            fpath = os.path.join(dname, fname)
            with open(fpath) as f:
                s = f.read()
            s = s.replace("fprintf", "(void)")
            with open(fpath, "w") as f:
                f.write(s)

def generate(target, target_arch, __folder__, args, cpus, builddir, libdir, c_flags, cxx_flags):

    print("==============================\n Building Target - " + target + "\n==============================")

    project_folder = os.path.join(TF_TOP_GEN_PATH, "cortex_m_generic_" + target_arch + "_default")

    if (not os.path.isdir(project_folder)) or (not args.skip_generation):
        if os.system("cd " + TF_TOP +
        " && make -f " + TF_TOOLS_MAKEFILE_PATH + " -j" + str(cpus) +
                " TARGET=cortex_m_generic TARGET_ARCH=" + target_arch +
                " OPTIMIZED_KERNEL_DIR=cmsis_nn generate_" + MAKE_PROJECT + "_make_project"):
            sys.exit("Make Failed...")

    if os.path.exists(os.path.join(builddir, target)):
        shutil.rmtree(os.path.join(builddir, target), ignore_errors = True)

    shutil.copytree(project_folder, os.path.join(builddir, target))

    tflite_micro_project_folder = os.path.join("prj", MAKE_PROJECT, "make")
    tflite_micro_gen_folder = "genfiles/tensorflow/lite/micro/models"

    shutil.copytree("libc", os.path.join(builddir, target, tflite_micro_project_folder, "libc"))
    shutil.copytree("libm", os.path.join(builddir, target, tflite_micro_project_folder, "libm"))

    shutil.copytree(os.path.join(TF_TOP_MICRO_PATH, "tools/make/downloads/kissfft"),
                    os.path.join(builddir, target, tflite_micro_project_folder, TF_TOOLS_DOWNLOADS_PATH, "kissfft"))

    shutil.copytree(os.path.join(TF_TOP_EXPERIMENTAL_PATH, "microfrontend"),
                    os.path.join(builddir, target, tflite_micro_project_folder, TF_EXPERIMENTAL_MICROFRONTEND_PATH))

    shutil.copytree(os.path.join(TF_TOP_MICRO_PATH, "examples/micro_speech/micro_features"),
                    os.path.join(builddir, target, tflite_micro_project_folder, TF_EXAMPLES_MICRO_FEATURES_PATH))

    patch_files(os.path.join(builddir, target, tflite_micro_project_folder, TF_TOOLS_DOWNLOADS_PATH, "kissfft"))
    patch_files(os.path.join(builddir, target, tflite_micro_project_folder, TF_EXPERIMENTAL_MICROFRONTEND_PATH))
    patch_files(os.path.join(builddir, target, tflite_micro_project_folder, TF_EXAMPLES_MICRO_FEATURES_PATH))

    SRCS = [
        "SRCS :=",
        "libtf.cc",
        "libc/bsearch.c",
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
        os.path.join(TF_TOOLS_DOWNLOADS_PATH, "kissfft/kiss_fft.c"),
        os.path.join(TF_TOOLS_DOWNLOADS_PATH, "kissfft/tools/kiss_fftr.c"),
        os.path.join(TF_EXPERIMENTAL_MICROFRONTEND_PATH, "lib/noise_reduction_io.c"),
        os.path.join(TF_EXPERIMENTAL_MICROFRONTEND_PATH, "lib/filterbank_io.c"),
        os.path.join(TF_EXPERIMENTAL_MICROFRONTEND_PATH, "lib/log_scale_util.c"),
        os.path.join(TF_EXPERIMENTAL_MICROFRONTEND_PATH, "lib/fft_util.cc"),
        os.path.join(TF_EXPERIMENTAL_MICROFRONTEND_PATH, "lib/log_lut.c"),
        os.path.join(TF_EXPERIMENTAL_MICROFRONTEND_PATH, "lib/filterbank_util.c"),
        os.path.join(TF_EXPERIMENTAL_MICROFRONTEND_PATH, "lib/frontend_memmap_generator.c"),
        os.path.join(TF_EXPERIMENTAL_MICROFRONTEND_PATH, "lib/window.c"),
        os.path.join(TF_EXPERIMENTAL_MICROFRONTEND_PATH, "lib/pcan_gain_control_util.c"),
        os.path.join(TF_EXPERIMENTAL_MICROFRONTEND_PATH, "lib/frontend_io.c"),
        os.path.join(TF_EXPERIMENTAL_MICROFRONTEND_PATH, "lib/frontend.c"),
        os.path.join(TF_EXPERIMENTAL_MICROFRONTEND_PATH, "lib/window_util.c"),
        os.path.join(TF_EXPERIMENTAL_MICROFRONTEND_PATH, "lib/fft.cc"),
        os.path.join(TF_EXPERIMENTAL_MICROFRONTEND_PATH, "lib/log_scale_io.c"),
        os.path.join(TF_EXPERIMENTAL_MICROFRONTEND_PATH, "lib/filterbank.c"),
        os.path.join(TF_EXPERIMENTAL_MICROFRONTEND_PATH, "lib/fft_io.c"),
        os.path.join(TF_EXPERIMENTAL_MICROFRONTEND_PATH, "lib/noise_reduction_util.c"),
        os.path.join(TF_EXPERIMENTAL_MICROFRONTEND_PATH, "lib/noise_reduction.c"),
        os.path.join(TF_EXPERIMENTAL_MICROFRONTEND_PATH, "lib/log_scale.c"),
        os.path.join(TF_EXPERIMENTAL_MICROFRONTEND_PATH, "lib/frontend_util.c"),
        os.path.join(TF_EXPERIMENTAL_MICROFRONTEND_PATH, "lib/pcan_gain_control.c"),
        os.path.join(TF_EXAMPLES_MICRO_FEATURES_PATH, "micro_features_generator.cc"),
        "\\"
    ]

    gcc_embedded_folder = os.path.join(__folder__, os.path.join(TF_TOP_MICRO_PATH, "tools/make/downloads/gcc_embedded/bin"))

    arm_none_eabi_gcc = os.path.join(gcc_embedded_folder, "arm-none-eabi-gcc")
    arm_none_eabi_ar = os.path.join(gcc_embedded_folder, "arm-none-eabi-ar")

    with open(os.path.join(builddir, target, tflite_micro_project_folder, "Makefile"), 'r') as original:
        data = original.read()
        data = re.sub(r"TARGET_TOOLCHAIN_ROOT := \S*", "TARGET_TOOLCHAIN_ROOT := " + gcc_embedded_folder + "/", data)
        data = data.replace("LIBRARY_OBJS := $(filter-out tensorflow/lite/micro/examples/%, $(OBJS))", "LIBRARY_OBJS := $(OBJS)")
        data = re.sub(r" tensorflow/lite/micro/examples/\S*", "", data)
        data = data.replace("SRCS := \\", " ".join(SRCS))
        data = data.replace("-Wdouble-promotion ", " ")
        data = data.replace("-Wsign-compare ", " ")

    with open(os.path.join(builddir, target, tflite_micro_project_folder, "Makefile"), 'w') as modified:
        modified.write("CCFLAGS = " + c_flags + "\n")
        modified.write("CXXFLAGS = " + cxx_flags + "\n")
        modified.write(data)

    shutil.copy(os.path.join(__folder__, "libtf.cc"), os.path.join(builddir, target, tflite_micro_project_folder))
    shutil.copy(os.path.join(__folder__, "libtf.h"), os.path.join(builddir, target, tflite_micro_project_folder))

    if os.system("cd " + os.path.join(builddir, target, tflite_micro_project_folder) +
        " && make -j " + str(cpus) + " lib"):
        sys.exit("Make Failed...")

    if os.system("cd " + os.path.join(builddir, target, tflite_micro_gen_folder) +
        " && sed -i '1,2d' person_detect_model_data.cc" +
        " && sed -i '1s/^............//' person_detect_model_data.cc" +
        " && mv person_detect_model_data.cc person_detect_model_data.c" +
        " && " + arm_none_eabi_gcc + " " + c_flags + " -o libtf_person_detect_model_data.o -c person_detect_model_data.c" +
        " && " + arm_none_eabi_ar + " rcs libtf_person_detect_model_data.a libtf_person_detect_model_data.o" +
        " && sed -i -e '$a\\' person_detect_model_data.h" +
        " && cp person_detect_model_data.h libtf_person_detect_model_data.h"):
        sys.exit("Make Failed...")

    if not os.path.exists((os.path.join(libdir, target))):
        os.mkdir(os.path.join(libdir, target))

    shutil.copy(os.path.join(builddir, target, tflite_micro_project_folder, "libtensorflow-microlite.a"), os.path.join(libdir, target, "libtf.a"))
    shutil.copy(os.path.join(builddir, target, tflite_micro_gen_folder, "libtf_person_detect_model_data.a"), os.path.join(libdir, target))
    shutil.copy(os.path.join(__folder__, "libtf.h"), os.path.join(libdir, target))
    shutil.copy(os.path.join(builddir, target, tflite_micro_gen_folder, "libtf_person_detect_model_data.h"), os.path.join(libdir, target))
    shutil.copy(os.path.join(builddir, target, tflite_micro_project_folder, "LICENSE"), os.path.join(libdir, target))

    with open(os.path.join(libdir, target, "README"), "w") as f:
        f.write("You must link this library to your application with arm-none-eabi-gcc and have implemented putchar().\n")

def build_target(target, __folder__, args, cpus, builddir, libdir):

    FLAGS = [
        "-Wno-double-promotion",
        "-Wno-nonnull",
        "-Wno-psabi",
        "-Wno-sign-compare",
        "-Wno-unused-but-set-variable",
        "-Wno-unused-value",
        "-DGEMMLOWP_ALLOW_SLOW_SCALAR_FALLBACK",
        "-DNDEBUG",
        "-MMD",
        "-O3",
        "-fshort-enums",
        "-fno-delete-null-pointer-checks",
        "-fno-exceptions",
        "-mabi=aapcs-linux",
        "-nostartfiles",
        "-nostdlib",
        "-I./" + os.path.join(TF_TOOLS_DOWNLOADS_PATH, "cmsis"),
        "-I./" + os.path.join(TF_TOOLS_DOWNLOADS_PATH, "cmsis/CMSIS/Core/Include"),
        "-I./" + os.path.join(TF_TOOLS_DOWNLOADS_PATH, "cmsis/CMSIS/DSP/Include"),
        "-I./" + os.path.join(TF_TOOLS_DOWNLOADS_PATH, "cmsis/CMSIS/NN/Include"),
        "-I./" + os.path.join(TF_TOOLS_DOWNLOADS_PATH, "kissfft")
    ]

    compile_flags = " ".join(FLAGS)
    c_compile_flags = compile_flags
    cxx_compile_flags = compile_flags + " -fno-use-cxa-atexit"

    if target == "cortex-m0plus":

        cortex_m0_plus_compile_flags = " -DARM_MATH_CM0PLUS" \
                                       " -mcpu=cortex-m0plus" \
                                       " -mfloat-abi=soft" \
                                       " -mtune=cortex-m0plus"

        cortex_m0_plus_c_compile_flags = c_compile_flags + cortex_m0_plus_compile_flags
        cortex_m0_plus_cxx_compile_flags = cxx_compile_flags + cortex_m0_plus_compile_flags
        generate(target, "cortex-m0plus", __folder__, args, cpus, builddir, libdir,
                 cortex_m0_plus_c_compile_flags, cortex_m0_plus_cxx_compile_flags)

    elif target == "cortex-m4":

        cortex_m4_compile_flags = " -DARM_MATH_CM4" \
                                  " -mfpu=fpv4-sp-d16" \
                                  " -mcpu=cortex-m4" \
                                  " -mfloat-abi=hard" \
                                  " -mtune=cortex-m4"

        cortex_m4_c_compile_flags = c_compile_flags + cortex_m4_compile_flags
        cortex_m4_cxx_compile_flags = cxx_compile_flags + cortex_m4_compile_flags
        generate(target, "cortex-m4+fp", __folder__, args, cpus, builddir, libdir,
                 cortex_m4_c_compile_flags, cortex_m4_cxx_compile_flags)

    elif target == "cortex-m7":

        cortex_m7_compile_flags = " -DARM_MATH_CM7" \
                                  " -mfpu=fpv5-sp-d16" \
                                  " -mcpu=cortex-m7" \
                                  " -mfloat-abi=hard" \
                                  " -mtune=cortex-m7"

        cortex_m7_c_compile_flags = c_compile_flags + cortex_m7_compile_flags
        cortex_m7_cxx_compile_flags = cxx_compile_flags + cortex_m7_compile_flags
        generate(target, "cortex-m7+fp", __folder__, args, cpus, builddir, libdir,
                 cortex_m7_c_compile_flags, cortex_m7_cxx_compile_flags)

    elif target == "cortex-m55":

        cortex_m55_compile_flags = " -DARM_MATH_CM55" \
                                   " -mcpu=cortex-m55" \
                                   " -mfloat-abi=hard" \
                                   " -mtune=cortex-m55"

        cortex_m55_c_compile_flags = c_compile_flags + cortex_m55_compile_flags
        cortex_m55_cxx_compile_flags = cxx_compile_flags + cortex_m55_compile_flags
        generate(target, "cortex-m55", __folder__, args, cpus, builddir, libdir,
                 cortex_m55_c_compile_flags, cortex_m55_cxx_compile_flags)

    else:
        sys.exit("Unknown target!")

def make():

    __folder__ = os.path.dirname(os.path.abspath(__file__))

    parser = argparse.ArgumentParser(description =
    "Make Script")

    parser.add_argument("--clean", "-c", action="store_true", default=False,
    help="Clean TensorFlow library.")

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

    if args.clean:
        if os.system("cd " + TF_TOP +
        " && make -f " + TF_TOOLS_MAKEFILE_PATH + " clean" +
        " && make -f " + TF_TOOLS_MAKEFILE_PATH + " clean_downloads"):
            sys.exit("Make Failed...")
        return

    if not os.path.isfile(os.path.join(TF_TOP_GEN_PATH, "linux_x86_64_default/bin", TEST_PROJECT)) or (not args.skip_generation):
        if os.system("cd " + TF_TOP +
        " && make -f " + TF_TOOLS_MAKEFILE_PATH + " third_party_downloads"
        " && make -f " + TF_TOOLS_MAKEFILE_PATH + " -j" + str(cpus) + " test_" + TEST_PROJECT):
            sys.exit("Make Failed...")

    build_target("cortex-m0plus", __folder__, args, cpus, builddir, libdir)
    build_target("cortex-m4", __folder__, args, cpus, builddir, libdir)
    build_target("cortex-m7", __folder__, args, cpus, builddir, libdir)
    build_target("cortex-m55", __folder__, args, cpus, builddir, libdir)

    print("==============================\n Done\n==============================")

if __name__ == "__main__":
    make()
