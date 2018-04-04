from conans import ConanFile, CMake, tools
import os

class Eigen3Conan(ConanFile):
    name = "Eigen3"
    license = "<Put the package license here>"
    url = "https://github.com/Av3m/conan-eigen.git"
    options = {"shared": [True, False]}
    default_options = "shared=False"
    settings = "os", "arch", "build_type", "compiler"
    generators = "cmake"

    def source(self):
        self.run("hg clone https://bitbucket.org/eigen/eigen")
        self.run("hg checkout %s" %( self.version ),cwd="eigen")

    def build(self):
        cmake = CMake(self)
        cmake.definitions["CMAKE_INSTALL_PREFIX"] = "install"
        cmake.configure(source_dir="eigen", build_dir=".")
        cmake.build()
        cmake.install()
        
    def package(self):
        self.copy("*", dst=".", src="install")
        self.copy("*", dst="cmake", src="install/share/eigen3/cmake")
        tools.replace_in_file(os.path.join(self.package_folder,"cmake","Eigen3Config.cmake") ,"""get_filename_component(PACKAGE_PREFIX_DIR "${CMAKE_CURRENT_LIST_DIR}/../../../" ABSOLUTE)""","""get_filename_component(PACKAGE_PREFIX_DIR "${CMAKE_CURRENT_LIST_DIR}/../" ABSOLUTE)""")

    def package_info(self):
        self.cpp_info.includedirs = [ os.path.join("include","eigen3") ]
