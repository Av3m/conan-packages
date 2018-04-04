#!/usr/bin/python3
from conan.packager import ConanMultiPackager
import os


os.environ['CONAN_USERNAME'] = 'av3m'
os.environ['CONAN_CHANNEL'] = 'testing'

if __name__ == "__main__":
    #windows builds
    os.environ['CONAN_USE_DOCKER'] = "0"
    builder = ConanMultiPackager(
        gcc_versions=[],
        apple_clang_versions=[],
        visual_versions=["10","17"], 
        visual_runtimes=["MD"],
        archs=["x86_64"],
        build_types=["Debug", "Release"])
    builder.add_common_builds()
    builder.run()


    #linux build
    os.environ['CONAN_USE_DOCKER'] = '1'
    builder = ConanMultiPackager(
        gcc_versions=["4.9","5","6","7"],
        apple_clang_versions=[],
        archs=["x86_64"],
        visual_versions=[], 
        visual_runtimes=[],
        build_types=["Debug", "Release"])
    builder.add_common_builds()
    builder.run()
