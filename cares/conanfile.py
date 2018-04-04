from conans import ConanFile, CMake, tools


class CaresConan(ConanFile):
    name = "cares"
    version = "1.14.0"
    license = "<Put the package license here>"
    url = "<Package recipe repository url here, for issues about the package>"
    description = "<Description of Cares here>"
    settings = "os", "compiler", "build_type", "arch"
    options = {"shared": [True, False]}
    default_options = "shared=False"
    generators = "cmake"

    def source(self):
        version_str = 'cares-' + str(self.version).replace(".","_")
        self.run("git clone --branch %s --single-branch https://github.com/c-ares/c-ares.git cares" %(version_str) )
        # This small hack might be useful to guarantee proper /MT /MD linkage
        # in MSVC if the packaged project doesn't have variables to set it
        # properly
        tools.replace_in_file("cares/CMakeLists.txt", "PROJECT (c-ares C)",
                              '''PROJECT (c-ares C)
include(${CMAKE_BINARY_DIR}/conanbuildinfo.cmake)
conan_basic_setup()''')

    def build(self):
        cmake = CMake(self)
        cmake.definitions['CMAKE_INSTALL_PREFIX'] = "install"
        if ( self.options.shared ) :
            cmake.definitions['CARES_STATIC'] = 'OFF'
            cmake.definitions['CARES_SHARED'] = 'ON'
        else:
            cmake.definitions['CARES_STATIC'] = 'ON'
            cmake.definitions['CARES_SHARED'] = 'OFF'
        cmake.configure(source_folder="cares")
        cmake.build()
        cmake.install()

    def package(self):
        self.copy("*", dst=".", src="install")

    def package_info(self):
        pass

