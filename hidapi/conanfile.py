from conans import ConanFile, CMake, tools, MSBuild, VisualStudioBuildEnvironment
import shutil
import glob

class HidapiConan(ConanFile):
    name = "hidapi"
    version = "0.8.0-rc1"
    license = "BSD"
    url = "https://github.com/Av3m/conan-hidapi.git"
    settings = "os", "compiler", "build_type", "arch"
    options = {"shared": [True, False]}
    default_options = "shared=False"
    generators = "cmake"
    exports_sources="sln*"
    

    def source(self):
        self.run("git clone https://github.com/signal11/hidapi.git")
        self.run("git checkout tags/hidapi-%s" % (self.version), cwd="hidapi" )
        for file in glob.glob("sln/*"):
            shutil.copy(file,"hidapi/windows")
        

    def build(self):
        if self.settings.compiler == "Visual Studio":
            msbuild = MSBuild(self)
            msbuild.build("hidapi/windows/hidapi.sln")
        else:
            cmake = CMake(self)
            self.run('cmake hello %s' % cmake.command_line)
            self.run("cmake --build . %s" % cmake.build_config)

        
    def package(self):
        self.copy("*.h", dst="include", src="hidapi")
        self.copy("*.lib", dst="lib", keep_path=False)
        self.copy("*.dll", dst="bin", keep_path=False)
        self.copy("*.pdb", dst="bin", keep_path=False)
        self.copy("*.so", dst="lib", keep_path=False)
        self.copy("*.dylib", dst="lib", keep_path=False)
        self.copy("*.a", dst="lib", keep_path=False)

    def package_info(self):
        self.cpp_info.libs = ["hidapi"]
