from conans import ConanFile, CMake, tools
from conans.tools import download, unzip, check_md5, check_sha1, check_sha256
import os
import shutil


class FlannConan(ConanFile):
    name = "flann"
    license = "BSD-2-Clause"
    url = "http://www.cs.ubc.ca/research/flann/"
    settings = "os", "compiler", "build_type", "arch"
    options = {"shared": [True, False]}
    default_options = "shared=False"
    generators = "cmake"
    exports="patches*"
    description="""FLANN is a library for performing fast approximate nearest neighbor searches in high dimensional spaces. It contains a collection of algorithms we found to work best for nearest neighbor search and a system for automatically choosing the best algorithm and optimum parameters depending on the dataset.
\nFLANN is written in C++ and contains bindings for the following languages: C, MATLAB and Python.
"""

    def source(self):
        zipfile="flann-%s-src.zip" % ( self.version )
        download("http://www.cs.ubc.ca/research/flann/uploads/FLANN/flann-%s-src.zip" % (self.version) ,zipfile )
        unzip(zipfile)
        shutil.move("flann-%s-src" %(self.version) ,"flann_src")

        # This small hack might be useful to guarantee proper /MT /MD linkage in MSVC
        # if the packaged project doesn't have variables to set it properly
        
        tools.replace_in_file("flann_src/CMakeLists.txt", "project(flann)", '''PROJECT(flann)
include(${CMAKE_BINARY_DIR}/conanbuildinfo.cmake)
conan_basic_setup()''')

        if ( self.settings.compiler == "Visual Studio" ):
            tools.patch(patch_file="patches/msvc_fix.patch")
            

    def build(self):
        cmake = CMake(self)
        cmake.definitions["CMAKE_INSTALL_PREFIX"]="install"
        if self.options.shared:
                cmake.definitions["BUILD_SHARED_LIBS"]="ON"
        else:
                cmake.definitions["BUILD_SHARED_LIBS"]="OFF"
        cmake.configure(source_dir="flann_src",build_dir=".")
        cmake.build()
        cmake.install()

    def package(self):
        self.copy("*", dst=".", src="install",keep_path=True)
        self.copy("FindFlann.cmake", dst=".", src="flann_src/cmake",keep_path=False)
        

    def package_info(self):
        self.cpp_info.includedirs = ['include']  # Ordered list of include paths
        self.cpp_info.libs = ['flann']  # The libs to link against
        self.cpp_info.libdirs = ['lib']  # Directories where libraries can be found
        self.cpp_info.resdirs = ['res']  # Directories where resources, data, etc can be found
        self.cpp_info.bindirs = []  # Directories where executables and shared libs can be found
        self.cpp_info.defines = []  # preprocessor definitions
        self.cpp_info.cflags = []  # pure C flags
        self.cpp_info.cppflags = []  # C++ compilation flags
        self.cpp_info.sharedlinkflags = []  # linker flags
        self.cpp_info.exelinkflags = []  # linker flags
        self.env_info.FLANN_ROOT= self.package_folder
        self.env_info.PKG_CONFIG_PATH.append(os.path.join(self.package_folder,"lib","pkgconfig"))
        tools.replace_prefix_in_pc_file(os.path.join(self.package_folder,"lib","pkgconfig","flann.pc"), self.package_folder)
