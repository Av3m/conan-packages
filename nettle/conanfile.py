from conans import ConanFile
import shutil
import os
from conans.tools import download, unzip
from conans import AutoToolsBuildEnvironment


class NettleConan(ConanFile):
    name = "nettle"
    generators = "txt","pkg_config"
    settings =  "os", "compiler", "arch", "build_type"
    options = {"shared": [True, False]}
    default_options = "shared=True"
    url = "http://github.com/Av3m/conan-repo"
    
    def requirements(self):
        self.requires("gmp/6.1.2@%s/%s" % ( self.user, self.channel))

    def configure(self):
        if self.options.shared:
            self.options['gmp'].shared = True
        else:
            self.options['gmp'].shared = False

        if self.settings.os == "Windows":
            if self.settings.compiler == "gcc":
                self.requires("mingw_installer/1.0@conan/stable")

    def source(self):
        zip_name = "nettle-%s.tar.gz" % self.version
        folder_name = "nettle-%s" % self.version
        download("http://ftp.gnu.org/gnu/nettle/%s" % zip_name, zip_name)
        unzip(zip_name)
        shutil.move(folder_name,"nettle")

    def build(self):
        env_build = AutoToolsBuildEnvironment(self)
        env_build.fpic = True

        if ( self.settings.os == "Windows" and self.settings.compiler == "gcc"):
            env_build.flags.append("-Wl,--out-implib=$@.lib")
        
        
        configure_args = list()
        configure_args.append('--prefix=%s' %(os.path.join(self.build_folder,'__install')) )

        
        if ( self.options.shared):
            configure_args.append('--enable-shared')
            configure_args.append('--disable-static')
        else:
            configure_args.append('--enable-static')
            configure_args.append('--disable-shared')
           
        env_build.configure(args=configure_args, configure_dir="nettle" )
        env_build.make()
        env_build.make(args=["install"])
        

    def package(self):
        self.copy("*", dst="", src="__install", keep_path=True)
        self.copy("*.lib", dst="lib", src=".", keep_path=True)
        self.copy("*.pc", src="__install", dst=".", keep_path=False)

    def package_id(self):
        if ( self.settings.os=="Windows"):
            del self.info.settings.compiler

    def package_info(self):
        if ( self.settings.compiler == "Visual Studio" ):
            self.cpp_info.libs = ['libnettle', 'libhogweed']
        else:
            self.cpp_info.libs = ['nettle', 'hogweed']

        self.env_info.PKG_CONFIG_nettle_PREFIX = self.package_folder



