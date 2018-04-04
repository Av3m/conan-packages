from conans import ConanFile, CMake, tools
import os

class NugetConan(ConanFile):
    name = "nuget"
    version = "4.4.1"
    license = "Apache License 2.0"
    url = "https://github.com/Av3m/conan-nuget.git"
    settings = {
        "os": ["Windows"],
        "arch": ["x86_64", "x86"]
    }
    generators = "txt"

    def source(self):
        tools.download('https://dist.nuget.org/win-x86-commandline/v%s/nuget.exe' % (self.version), "nuget.exe")

    def build(self):
        pass

    def package(self):
        self.copy("*.exe", dst="bin", src=".")

    def package_info(self):
        self.cpp_info.bindirs = ["bin"]
        self.env_info.PATH.append(os.path.join(self.package_folder, "bin"))
