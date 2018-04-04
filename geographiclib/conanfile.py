from conans import ConanFile, CMake
from conans import tools
from conans.util import files
import os
import shutil


class GeographicLibConan(ConanFile):
    name = "GeographicLib"
    version = "1.46"
    url = "https://github.com/Av3m/conan-geographiclib.git"
    settings = "os", "compiler", "build_type", "arch"
    license = "MIT"
    options = {"static": [False, False], "shared": [True, False], "precision": [1, 2, 3, 4, 5]}
    default_options = "static=False", "shared=True", "precision=2"

    def source(self):
        distrib_url = 'https://sourceforge.net/projects/geographiclib/files/distrib/'
        tarball = '%s-%s.tar.gz' % (self.name, self.version)
        self.output.info('Downloading %s' % tarball)
        tools.download(distrib_url + tarball, tarball)
        tools.untargz(tarball)
        shutil.move('%s-%s' % (self.name, self.version), 'geographiclib_src')
        os.unlink(tarball)

    def build(self):
        options = []
        options.append('-DCMAKE_INSTALL_PREFIX=__install')
        options.append('-DGEOGRAPHICLIB_LIB_TYPE=%s' % self.lib_type())
        options.append('-DGEOGRAPHICLIB_PRECISION=%s' % self.options.precision)
        cmake = CMake(self)
        self.run('cmake %s %s geographiclib_src' % (' '.join(options), cmake.command_line))
        self.run('cmake --build . --config %s --target install' % str(self.settings.build_type) )

    def package(self):
        self.copy(pattern="*", dst=".", src="__install")

    def package_info(self):
        if self.settings.build_type == "Release":
            self.cpp_info.libs = ["Geographic_-i"]
        elif self.settings.build_type=="Debug":
            self.cpp_info.libs = ["Geographic_d-i"]
        self.cpp_info.includedirs = ['include']  # Ordered list of include paths
        self.cpp_info.libs = []  # The libs to link against
        self.cpp_info.libdirs = ['lib']  # Directories where libraries can be found
        self.cpp_info.resdirs = ['res']  # Directories where resources, data, etc can be found
        self.cpp_info.bindirs = ['bin']  # Directories where executables and shared libs can be found
        self.cpp_info.defines = []  # preprocessor definitions
        self.cpp_info.cflags = []  # pure C flags
        self.cpp_info.cppflags = []  # C++ compilation flags
        self.cpp_info.sharedlinkflags = []  # linker flags
        self.cpp_info.exelinkflags = []  # linker flags
    def lib_type(self):
        lib_type = None
        if self.options.static and self.options.shared:
            lib_type = 'BOTH'
        elif self.options.shared:
            lib_type = 'SHARED'
        elif self.options.static:
            lib_type = 'STATIC'
        else:
            self.output.error("Enable at least one of options 'shared' and 'static'")
        return lib_type
