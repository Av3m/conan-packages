from conans import ConanFile, CMake, tools
import os
import shutil


class SuiteSparseConan(ConanFile):
    name = "suitesparse"
    license = "<Put the package license here>"
    url = "https://github.com/Av3m/conan-suitesparse.git"
    settings = "os", "compiler", "build_type", "arch"
    generators = "cmake"
    exports_sources = "*.cmake"
    
    def system_requirements(self):
        packages = []
        installer = tools.SystemPackageTool()
        
        if tools.os_info.linux_distro == "ubuntu":
            packages.append("liblapack-dev")
            packages.append("liblas-dev")
        
        if ( len(packages) > 0):
            installer.install(packages)

    def source(self):
        self.run("git clone --branch master http://github.com/jlblancoc/suitesparse-metis-for-windows.git suitesparse")
        self.run("cd suitesparse && git checkout %s" % (self.version))
        # This small hack might be useful to guarantee proper /MT /MD linkage in MSVC
        # if the packaged project doesn't have variables to set it properly
        tools.replace_in_file("suitesparse/CMakeLists.txt", "PROJECT(SuiteSparseProject)", '''PROJECT(SuiteSparseProject)
include(${CMAKE_BINARY_DIR}/conanbuildinfo.cmake)
conan_basic_setup()''')

        #tools.replace_in_file("suitesparse/CMakeLists.txt",
        #       """set(ConfigPackageLocation ${CMAKE_INSTALL_LIBDIR}/cmake/suitesparse-${SuiteSparse_VERSION})""",
        #       """set(ConfigPackageLocation ${CMAKE_INSTALL_PREFIX}/cmake""")

    def build(self):
        cmake = CMake(self)
        cmake.definitions["BUILD_SHARED_LIBS"] = "ON"
		
        cmake.definitions["CMAKE_INSTALL_PREFIX"] = os.path.join(self.build_folder,"install")
        cmake.configure(source_dir='suitesparse',build_dir='.')
        cmake.build()
        cmake.install()
        
        if self.settings.compiler == "Visual Studio":
            shutil.copy("install/lib64/lapack_blas_windows/liblapack.lib","install/lib64/lapack_blas_windows/lapack.lib")
            shutil.copy("install/lib64/lapack_blas_windows/libblas.lib","install/lib64/lapack_blas_windows/blas.lib")

	

    def package(self):
        self.copy("*",src="install", dst=".", keep_path=True)
        self.copy("FindCholmod.cmake",src=".", dst=".", keep_path=True)
        self.copy("FindCSparse.cmake",src=".", dst=".", keep_path=True)
        if ( self.settings.compiler == "Visual Studio" ):
            self.copy("FindBLAS.cmake",src=".", dst=".", keep_path=True)
            self.copy("FindLAPACK.cmake",src=".", dst=".", keep_path=True)



    def package_info(self):
        self.cpp_info.libdirs = ['lib']
        self.cpp_info.includedirs = ['include', 'include/suitesparse']  # Ordered list of include paths
        self.cpp_info.bindirs = ['bin']  # Directories where executables and shared libs can be found

        self.cpp_info.libs = ['libamd',
                             'libbtf',
                             'libcamd',
                             'libccolamd',
                             'libcholmod',
                             'libcolamd',
                             'libcxsparse',
                             'libklu',
                             'libldl',
                             'libspqr',
                             'libumfpack',
                             'metis',
                             'suitesparseconfig']  # The libs to link against
        
        if ( self.settings.os=="Windows"):
                self.cpp_info.libs.append('libblas')
                self.cpp_info.libs.append('liblapack')
                self.cpp_info.bindirs.append('lib64/lapack_blas_windows')
                self.env_info.path.append(os.path.join(self.package_folder, 'lib64/lapack_blas_windows'))
                
                if (  self.settings.arch == "x86_64"):
                        self.cpp_info.libdirs.append('lib64/lapack_blas_windows')
                else:
                        self.cpp_info.libdirs.append('lib/lapack_blas_windows')
                
        if (  self.settings.arch == "x86_64"):
                self.cpp_info.libdirs.append('lib64')
        else:
                self.cpp_info.libdirs.append('lib')
	

        self.cpp_info.resdirs = []  # Directories where resources, data, etc can be found
      
        self.cpp_info.defines = []  # preprocessor definitions
        self.cpp_info.cflags = []  # pure C flags
        self.cpp_info.cppflags = []  # C++ compilation flags
        self.cpp_info.sharedlinkflags = []  # linker flags
        self.cpp_info.exelinkflags = []  # linker flags
        
