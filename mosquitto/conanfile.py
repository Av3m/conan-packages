from conans import ConanFile, CMake, tools
import os
import shutil
import re
class MosquittoConan(ConanFile):
    name = "mosquitto"
    version = "1.4.14"
    license = "Creative Commons Attribution 4.0"
    url = "https://github.com/Av3m/conan-mosquitto.git"
    settings = "os", "compiler", "build_type", "arch"
    options = {"shared": [True, False]}
    default_options = "shared=False"
    generators = "cmake"
    requires = "OpenSSL/[>=1.0.2]@conan/stable"
    exports="patches/*"

    
    def requirements(self):
        if ( self.settings.compiler == "Visual Studio"):
            self.requires("pthread-win32/[*]@{}/{}".format(self.user,self.channel))
            
            
    def source(self):
        self.run("git clone https://github.com/eclipse/mosquitto.git mosquitto")
        self.run("cd mosquitto && git checkout tags/v%s" %(self.version))
        
        #add CONAN to CMake project
        tools.replace_in_file("mosquitto/CMakeLists.txt",
        """project(mosquitto)""",
        """project(mosquitto)
        include(${CMAKE_BINARY_DIR}/conanbuildinfo.cmake)
        conan_basic_setup()""")
        
        
        #Fix C89 incompatibility with MSVC100
        if ( self.settings.compiler == "Visual Studio" and self.settings.compiler.version.value < "12" ):
            tools.patch(patch_file="patches/fix_c89_util_mosq.patch",base_path="mosquitto")
            
        
    def build(self):
        #remove man builds for windows
        tools.replace_in_file("mosquitto/CMakeLists.txt",
        """add_subdirectory(man)""",
        "")
        
        
        if ( self.settings.compiler == "Visual Studio" and self.settings.compiler.version.value > "10"): 
            tools.replace_in_file("mosquitto/CMakeLists.txt",
            """project(mosquitto)""",
            """project(mosquitto)
            add_definitions(-DHAVE_HAVE_STRUCT_TIMESPEC)
            add_definitions(-D_TIMESPEC_DEFINED)""")
            
        if ( self.settings.compiler == "gcc"): 
            tools.replace_in_file("mosquitto/CMakeLists.txt",
            """project(mosquitto)""",
            """project(mosquitto)
            link_libraries(-ldl)""")
            
            
            
        if ( self.settings.compiler == "gcc"): 
            tools.replace_in_file("mosquitto/src/CMakeLists.txt",
            """target_link_libraries(mosquitto_passwd "${OPENSSL_LIBRARIES}")""",
            """target_link_libraries(mosquitto_passwd "${OPENSSL_LIBRARIES}" dl)""")   
        
        
        #remove absolute path for pthread-win32
        with open("mosquitto/lib/CMakeLists.txt", 'r+' ) as f:
            content = f.read()
            content_new = re.sub(r'set\s+\(PTHREAD_LIBRARIES .+\)','set (PTHREAD_LIBRARIES ${CONAN_LIBS_PTHREAD-WIN32})' ,content) 
            f.seek(0)
            f.write(content_new)
            
        with open("mosquitto/lib/CMakeLists.txt", 'r+' ) as f:
            content = f.read()
            content_new = re.sub(r'set\s+\(PTHREAD_INCLUDE_DIR .+\)','set (PTHREAD_INCLUDE_DIR ${CONAN_INCLUDE_DIRS_PTHREAD-WIN32})' ,content) 
            f.seek(0)
            f.write(content_new)
            
            
        #Fix failed header includes
        tools.replace_in_file("mosquitto/lib/mosquitto_internal.h",'''#include <config.h>''','''#include "../config.h"''')
        
        
        cmake = CMake(self,parallel=False)
        cmake.definitions["CMAKE_INSTALL_PREFIX"] = os.path.join(self.conanfile_directory,"install")
        
        
        cmake.configure(source_folder=os.path.join(self.source_folder,"mosquitto"),build_folder=self.conanfile_directory)
        cmake.build()
        cmake.install()

    def package(self):
        self.copy("*", dst="include", src="install/include")
        self.copy("*", dst="bin", src="install")
        self.copy("*.lib", dst="lib", src=".", keep_path=False)
        self.copy("*.pdb", dst="bin", src=".", keep_path=False)

    def package_info(self):
        self.cpp_info.libs = ["mosquitto", "mosquittopp"]
