from conans import ConanFile
import shutil
import os
from conans.tools import download, unzip
from conans import AutoToolsBuildEnvironment


class GmpConan(ConanFile):
    name = "gmp"
    generators = "txt"
    settings =  "os", "compiler", "arch", "build_type"
    options = {"shared": [True, False]}
    default_options = "shared=False"
    url = "http://github.com/Av3m/conan-repo"
    
    def configure(self):
        if self.settings.os == "Windows":
            if self.settings.compiler == "gcc":
                self.requires("mingw_installer/1.0@conan/stable")
                self.options.shared = True

    def source(self):
        zip_name = "gmp-%s.tar.bz2" % self.version
        folder_name = "gmp-%s" % self.version
        download("https://gmplib.org/download/gmp/%s" % zip_name, zip_name)
        unzip(zip_name)
        shutil.move(folder_name,"gmp")

    def build(self):
        env_build = AutoToolsBuildEnvironment(self)
        env_build.fpic = True
        
        configure_args = list()
        configure_args.append('--prefix=%s' %(os.path.join(self.build_folder,'__install')) )

        
        if ( self.options.shared):
            configure_args.append('--enable-shared')
            configure_args.append('--disable-static')
        else:
            configure_args.append('--enable-static')
            configure_args.append('--disable-shared')
           
        env_build.configure(args=configure_args, configure_dir="gmp" )
        env_build.make()
        env_build.make(args=["install"])
        


    def package(self):
        self.copy("*", dst="", src="__install", keep_path=True)
        self.copy("*.lib", dst="lib", src=".", keep_path=False)
        self.copy("*.pc", src="__install", dst=".", keep_path=False)

    def package_id(self):
        if ( self.settings.os=="Windows"):
            del self.info.settings.compiler

    def package_info(self):
        if ( self.settings.compiler == "Visual Studio" ):
            self.cpp_info.libs = ['libgmp-6']
        else:
            self.cpp_info.libs = ['gmp']

        self.env_info.PKG_CONFIG_gmp_PREFIX = self.package_folder



