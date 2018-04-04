import os
from conans import ConanFile, CMake 
from conans.tools import download, unzip, patch, vcvars_command

class ProjConan(ConanFile):
    name = "proj"
    generators = "cmake"
    settings = "os", "compiler", "build_type", "arch"
    exports = ["CMakeLists.txt", "FindPROJ4.cmake"]
    options = {"shared": [True, False]}
    default_options = "shared=True"
    url="http://github.com/av3m/conan-proj4"
    license="https://github.com/OSGeo/proj.4"

    
    

    def source(self):
        self.run("git clone --branch %s --single-branch https://github.com/OSGeo/proj.4.git proj" %(self.version))

    def build_msvc(self):
        cmd = vcvars_command(self.settings)
        self.run("%s &&  nmake /f makefile.vc INSTDIR=%s " % (cmd,os.path.join(self.build_folder,"install")),cwd="proj")
        self.run("%s && nmake /f makefile.vc install-all INSTDIR=%s" % (cmd,os.path.join(self.build_folder,"install")),cwd="proj")
    
    def build_gcc(self):
        self.run("./configure --prefix=%s" % (os.path.join(self.build_folder,"install")),cwd="proj")
        self.run("make",cwd="proj")
        self.run("make install",cwd="proj")
        
    def build(self):
        if self.settings.compiler=="Visual Studio":
            self.build_msvc()
        else:
            self.build_gcc()
            
            
    def build_id(self):
        self.info_build.options.shared = "Both"
        
    def package_id(self):
        self.info.options.shared = "Both"

    def package(self):
        self.copy("FindPROJ4.cmake", ".", ".")
        self.copy("*", dst=".", src="install")

    def package_info(self):
        if ( self.options.shared == True and self.settings.compiler=="Visual Studio"):
            self.cpp_info.libs = ["proj_i"]
        else:
            self.cpp_info.libs = ["proj"]
            
        self.cpp_info.bindirs = ["bin"]
