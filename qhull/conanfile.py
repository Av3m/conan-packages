from conans import ConanFile, CMake, tools
import os


class QhullConan(ConanFile):
    name = "QHull"
    license = "https://github.com/Av3m/conan-qhull.git"
    url = "http://www.qhull.org"
    settings = "os", "compiler", "build_type", "arch"
    generators = "cmake"
    description="""Qhull computes the convex hull, Delaunay triangulation, Voronoi diagram, halfspace intersection about a point, furthest-site Delaunay triangulation, and furthest-site Voronoi diagram. The source code runs in 2-d, 3-d, 4-d, and higher dimensions. Qhull implements the Quickhull algorithm for computing the convex hull. It handles roundoff errors from floating point arithmetic. It computes volumes, surface areas, and approximations to the convex hull."""
    exports_sources="cmake/*"
    
    def source(self):
        self.run("git clone https://github.com/qhull/qhull.git")
        self.run("cd qhull && git checkout %s" %(self.version) )
        # This small hack might be useful to guarantee proper /MT /MD linkage in MSVC
        # if the packaged project doesn't have variables to set it properly
        
        tools.replace_in_file("qhull/CMakeLists.txt","""project(qhull)""","""project(qhull)
        include(${CMAKE_BINARY_DIR}/conanbuildinfo.cmake)
        conan_basic_setup()""")

    def build(self):
        cmake = CMake(self)
        cmake.definitions["CMAKE_INSTALL_PREFIX"] = "__install"
        cmake.configure(source_dir="qhull",build_dir=".")
        cmake.build()
        cmake.install()

    def package(self):
        self.copy("*", dst=".", src="__install")
        self.copy("*.exe", dst="bin", keep_path=False)
        self.copy("*.so", dst="bin", keep_path=False)
        self.copy("*.dll", dst="bin", keep_path=False)
        self.copy("*.lib", dst="lib", keep_path=False)
        self.copy("*.a", dst="lib", keep_path=False)
        self.copy("*.cmake", src="cmake", dst=".", keep_path=False)


    def package_info(self):
        self.cpp_info.includedirs = ['include']  # Ordered list of include paths
        if self.settings.compiler == "Visual Studio":
            self.cpp_info.libs = ['qhullstatic']  # The libs to link against
        else:
            self.cpp_info.libs = ['libqhullstatic']  # The libs to link against

        self.cpp_info.libdirs = ['lib']  # Directories where libraries can be found
        self.cpp_info.bindirs = ['bin']  # Directories where executables and shared libs can be found

