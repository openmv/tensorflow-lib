#!/usr/bin/env python

# by: Kwabena W. Agyeman - kwagyeman@openmv.io

import argparse, glob, multiprocessing, os, re, shutil, stat, sys, subprocess

def make():

    __folder__ = os.path.dirname(os.path.abspath(__file__))

    parser = argparse.ArgumentParser(description =
    "Make Script")

    args = parser.parse_args()

    ###########################################################################

    cpus = multiprocessing.cpu_count()

    if os.system("cd tensorflow" +
    " && make -f tensorflow/lite/experimental/micro/tools/make/Makefile TAGS=\"openmvcam\" generate_projects"):
        sys.exit("Make Failed...")

if __name__ == "__main__":
    make()

