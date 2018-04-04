from conans import ConanFile
import os
from conans.tools import download
from conans.tools import unzip
from conans import CMake


class WinIConvConan(ConanFile):
    name = "win-iconv"
    version = "0.0.8"
    license = "MIT"
    generators = "cmake"
    settings = "os", "arch", "compiler", "build_type"
    options = {"shared": [True, False]}
    default_options = "shared=False"
    url="http://github.com/Av3m/conan-packages"
    license="https://github.com/win-iconv/win-iconv"

    def source(self):
        self.run("git clone --branch v%s --single-branch https://github.com/win-iconv/win-iconv.git" %(self.version))

    def build(self):
        cmake = CMake(self)
        
        cmake.definitions["CMAKE_INSTALL_PREFIX"] = "__install"
        if ( self.options.shared):
            cmake.definitions["BUILD_SHARED_LIBS"] = "ON"
        else:
            cmake.definitions["BUILD_SHARED_LIBS"] = "OFF"
        
        cmake.configure(source_dir="win-iconv", build_dir=".")
        cmake.build()
        cmake.install()

    def package(self):
        # Copying headers
        self.copy(pattern="*", dst=".", src="__install", keep_path=True)



    def package_info(self):
        self.cpp_info.libs = ['iconv']
