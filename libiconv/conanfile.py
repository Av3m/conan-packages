from conans import ConanFile
import os, shutil
from conans.tools import download, unzip, replace_in_file, check_md5
from conans import CMake, AutoToolsBuildEnvironment


class LibiconvConan(ConanFile):
    name = "libiconv"
    generators = "cmake"
    settings =  "os", "compiler", "arch", "build_type"
    options = {"shared": [True, False]}
    default_options = "shared=False"
    url = "http://github.com/Av3m/conan-packages"
    
    def configure(self):
        if self.settings.compiler=="Visual Studio":
            raise Exception("Package can not be compiled with MSVC! Please use package win-iconv!")

    def source(self):
        zip_name = "libiconv-%s.tar.gz" % self.version
        folder_name = "libiconv-%s" % self.version
        download("http://ftp.gnu.org/pub/gnu/libiconv/%s" % zip_name, zip_name)
        unzip(zip_name)
        shutil.move(folder_name,"libiconv")

    def build(self):
        env_build = AutoToolsBuildEnvironment(self)
        env_build.fpic = True
        
        
        configure_args = list()
        configure_args.append('--disable-rpath')
        
        if ( self.options.shared):
            configure_args.append('--enable-shared')
        else:
            configure_args.append('--enable-static')
           
        env_build.configure(args=configure_args, configure_dir="libiconv" )
        env_build.make()
        


    def package(self):
        self.copy("*.h", dst="include", src="libiconv/include", keep_path=True)
        if self.options.shared:
            self.copy(pattern="*.so*", dst="lib", src=".", keep_path=False)
            self.copy(pattern="*.dll*", dst="bin", src=".", keep_path=False)
        else:
            self.copy(pattern="*.a", dst="lib", src=".", keep_path=False)

        self.copy(pattern="*.lib", dst="lib", src=".", keep_path=False)

    def package_info(self):
        self.cpp_info.libs = ['charset', 'iconv']
        if self.settings.os == "Linux" or (self.options.shared and self.settings.os == "Macos"):
            self.cpp_info.defines.append("LIBICONV_PLUG=1")


