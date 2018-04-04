from conans import ConanFile, CMake, tools
import os

class SuitesparsetestConan(ConanFile):
    name = "suitesparse-test"
    version = "0.1"
    license = "<Put the package license here>"
    url = "<Package recipe repository url here, for issues about the package>"
    description = "<Description of Suitesparsetest here>"
    settings = "os", "compiler", "build_type", "arch"
    generators = "cmake"

    def build(self):
        cmake = CMake(self)
        cmake.configure(source_dir=os.path.join(self.source_folder,"src"), build_dir=".")
        cmake.build()

    def test(self):
        if ( self.settings.os == "Windows"):
            self.run("cholmod-test.exe",cwd="bin")
        else:
            self.run("./cholmod-test",cwd="bin")
