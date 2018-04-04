from conans import ConanFile, CMake, tools
from conans.util.files import load, save
import os
import re
import shutil

class ProtobufConan(ConanFile):
    name = "Protobuf"
    url = "https://github.com/Av3m/conan-protobuf.git"
    license = "https://github.com/google/protobuf/blob/v{}/LICENSE".format(version)
    requires = "zlib/1.2.11@conan/stable"
    settings = "os", "compiler", "build_type", "arch"
   # exports = "CMakeLists.txt", "lib*.cmake", "extract_includes.bat.in", "protoc.cmake", "tests.cmake", "change_dylib_names.sh"
    options = {"shared": [True, False]}
    default_options = "shared=False"
    generators = "cmake"

    def replace_in_file_regex(self, file_path, regex, replace):
        content = load(file_path)
        content = re.sub(regex, replace, content)
        with open(file_path, "w") as handle:
            handle.write(content)

    def config(self):
        self.options["zlib"].shared = self.options.shared

    def source(self):
        self.run("git clone --branch v%s --single-branch https://github.com/google/protobuf.git" % (self.version) )
        tools.replace_in_file("protobuf/cmake/CMakeLists.txt", "project(protobuf C CXX)", '''project(protobuf C CXX)
include(${CMAKE_BINARY_DIR}/conanbuildinfo.cmake)
conan_basic_setup()''')
        tools.replace_in_file("protobuf/cmake/install.cmake",
                              'set(CMAKE_INSTALL_CMAKEDIR "${CMAKE_INSTALL_LIBDIR}/cmake/protobuf" CACHE STRING "${_cmakedir_desc}")',
                              'set(CMAKE_INSTALL_CMAKEDIR "cmake" CACHE STRING "${_cmakedir_desc}")') # Install to the same folder for all compilers.

    def build(self):
        cmake = CMake(self)
        cmake.definitions['CMAKE_INSTALL_PREFIX'] = os.path.join(self.build_folder,"install")
        cmake.definitions['protobuf_BUILD_EXAMPLES'] = 'OFF'
        cmake.definitions['protobuf_BUILD_TESTS'] = 'OFF'
        cmake.definitions['Dprotobuf_WITH_ZLIB'] = 'ON'
        
        
        if ( self.options.shared == True ):
            cmake.definitions['BUILD_SHARED_LIBS'] = 'ON'
        else:
            cmake.definitions['BUILD_SHARED_LIBS'] = 'OFF'
            
        if self.settings.compiler == "Visual Studio":
            if self.settings.compiler.runtime == "MT" or self.settings.compiler.runtime == "MTd":
                args += ["-Dprotobuf_MSVC_STATIC_RUNTIME=ON"]
                cmake.definitions['protobuf_MSVC_STATIC_RUNTIME'] = 'ON'
            else:
                cmake.definitions['protobuf_MSVC_STATIC_RUNTIME'] = 'OFF'
        
        cmake.configure(source_dir="protobuf/cmake",build_dir=".")
        cmake.build()
        cmake.install()

    def package(self):
        # Install FindProtobuf files:
        # Fix some hard paths first:
        self.replace_in_file_regex("install/cmake/protobuf-targets.cmake", r"INTERFACE_LINK_LIBRARIES \".+zlib.+\"", 'INTERFACE_LINK_LIBRARIES "${ZLIB_LIBRARY}"')
        tools.replace_in_file("install/cmake/protobuf-targets.cmake", '''set_target_properties(protobuf::libprotobuf PROPERTIES''', '''find_package(ZLIB)
set_target_properties(protobuf::libprotobuf PROPERTIES''') # hard path to zlib.

        tools.replace_in_file("install/cmake/protobuf-targets.cmake", 'get_filename_component(_IMPORT_PREFIX "${_IMPORT_PREFIX}" PATH)', '''get_filename_component(_IMPORT_PREFIX "${_IMPORT_PREFIX}" PATH)
  set(_IMPORT_PREFIX "${CONAN_PROTOBUF_ROOT}")''') # search everything in the conan folder, not the install folder.
        tools.replace_in_file("install/cmake/protobuf-options.cmake", 'option(protobuf_MODULE_COMPATIBLE "CMake build-in FindProtobuf.cmake module compatible" OFF)',
        'option(protobuf_MODULE_COMPATIBLE "CMake build-in FindProtobuf.cmake module compatible" ON)') # We want to override the FindProtobuf.cmake shipped within CMake
        
        # Copy FindProtobuf.cmakes to package
        cmake_files = ["protobuf-config.cmake", "protobuf-config-version.cmake", "protobuf-options.cmake", "protobuf-module.cmake", "protobuf-targets.cmake"]
        for file in cmake_files:
            self.copy(file, dst=".", src="install/cmake/")
          # Copy the build_type specific file only for the right one:
        self.copy("protobuf-targets-{}.cmake".format("debug" if self.settings.build_type == "Debug" else "release"), dst=".", src="install/cmake/")

        # Copy Headers to package include folder
        self.copy("*.h", dst="include", src="install/include")

        # Copy all proto files:
        self.copy("*.proto", dst="bin", src="protobuf/src")

        # TODO: we should just use the stuff from the install folder directly.
        if self.settings.os == "Windows":
            self.copy("*.lib", dst="lib", src="lib", keep_path=False)
            self.copy("protoc.exe", dst="bin", src="bin", keep_path=False)

            if self.options.shared:
                self.copy("*.dll", dst="bin", src="", keep_path=False)
        else:
            # Copy the libs to lib
            if not self.options.shared:
                self.copy("*.a", "lib", "", keep_path=False)
            else:
                self.copy("*.so*", "lib", "", keep_path=False)
                self.copy("*.9.dylib", "lib", "", keep_path=False)

            # Copy the exe to bin
            # we need some sort of dynlib converter for macosx here, see memshardeds protobuf
            self.copy("protoc", "bin", "bin", keep_path=False)

    def package_info(self):
        basename = "libprotobuf"
        if self.settings.build_type == "Debug":
            basename = "libprotobufd"

        if self.settings.os == "Windows":
            self.cpp_info.libs = [basename]
            if self.options.shared:
                self.cpp_info.defines = ["PROTOBUF_USE_DLLS"]
        elif self.settings.os == "Macos":
            self.cpp_info.libs = [basename + ".a"] if not self.options.shared else [basename + ".9.dylib"]
        else:
            self.cpp_info.libs = [basename + ".a"] if not self.options.shared else [basename + ".so.9"]

        self.env_info.path.append(os.path.join(self.package_folder,"bin"))
