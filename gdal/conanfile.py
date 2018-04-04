
from conans import ConanFile, CMake, tools
from conans.tools import download, unzip, vcvars_command
import shutil
import os

class GdalConan(ConanFile):
    name = "gdal"
    license = "MIT"
    url = "https://github.com/Av3m/conan-gdal.git"
    settings = "os", "compiler", "build_type", "arch"
    options = {}

    def _getargs(self):
        nmake_args = []
        nmake_args = ["WIN64=YES" if self.settings.arch == "x86_64" else "WIN64=NO"]
        if self.settings.compiler == "Visual Studio":
            version = self.settings.compiler.version
            if version == "9":
                nmake_args.append("MSVC_VER=1500")
            elif version == "10":
                nmake_args.append("MSVC_VER=1600")
            elif version == "11":
                nmake_args.append("MSVC_VER=1700")
            elif version == "12":
                nmake_args.append("MSVC_VER=1800")
            else:
                # this is the highest version of msvc that
                # gdal recognises, but if compiles fine at least up
                # to VS 2017
                nmake_args.append("MSVC_VER=1900")
        nmake_args.append("GDAL_HOME={0}".format(self.build_folder ) )
        nmake_args.append("BINDIR={0}".format( os.path.join(self.build_folder,"install","bin") ) )
        nmake_args.append("DATADIR={0}".format(os.path.join(self.build_folder,"install","data") ) )
        nmake_args.append("LIBDIR={0}".format(os.path.join(self.build_folder,"install","lib") ) )
        nmake_args.append("INCDIR={0}".format(os.path.join(self.build_folder,"install","include") ) )
        nmake_args.append("HTMLDIR={0}".format(os.path.join(self.build_folder,"install","doc") ) )
        return nmake_args

    def source(self):
        zip_name = "gdal.zip"
        download("http://download.osgeo.org/gdal/%s/gdal%s.zip" % (str(self.version), str(self.version).replace(".","") ), zip_name)
        unzip(zip_name)
        shutil.move("gdal-%s" % ( self.version), "gdal")
	#copy makefile to source/gdal
	#translate all makefile.vc to linux makefiles
        os.unlink(zip_name)
	

    def build_windows(self):
        nmake_args = self._getargs()
        nmake_args = " ".join(nmake_args)
        cmd = vcvars_command(self.settings)
        self.run("%s && nmake /f makefile.vc %s" %(cmd,nmake_args),cwd="gdal")
        self.run("%s && nmake /f makefile.vc %s devinstall"%(cmd,nmake_args),cwd="gdal")

    def build(self):
        if ( self.settings.compiler == "Visual Studio"):
           self.build_windows()
        else:
           self.run("chmod +x gdal/configure")
           self.run("chmod +x gdal/install-sh")
           self.run("./configure --with-grass=yes --with-geotiff=yes --with-libtiff=yes --with-ogdi=yes --with-pg=yes --with-geos=yes --with-odbc=yes --prefix=%s" % (self.conanfile_directory + "/install"),cwd="gdal")
           #self.run("sudo -i")
           self.run("make",cwd="gdal")
           #self.run("make",cwd="gdal/ogr")
           #self.run("make",cwd="gdal/ogr/ogrsf_frmts")
           self.run("sudo make install",cwd="gdal")
           
    def package(self):
        self.copy("*.h",src="gdal/ogr",dst="include/ogr")
        self.copy("*",src="install",dst=".")
        

    def package_info(self):
        if ( self.settings.compiler == "Visual Studio"):
            self.cpp_info.libs = ['gdal_i']
        else:
            self.cpp_info.libs = ['libgdal']
            
        self.cpp_info.includedirs = ['include', 'include/ogr']  # Ordered list of include paths
        self.cpp_info.libdirs = ['lib']  # Directories where libraries can be found
        self.cpp_info.resdirs = ['doc', 'data']  # Directories where resources, data, etc can be found
        self.cpp_info.bindirs = ['bin']  # Directories where executables and shared libs can be found
        self.cpp_info.defines = []  # preprocessor definitions
        self.cpp_info.cflags = []  # pure C flags
        self.cpp_info.cppflags = []  # C++ compilation flags
        self.cpp_info.sharedlinkflags = []  # linker flags
        self.cpp_info.exelinkflags = []  # linker flags
        
        self.env_info.path.append(os.path.join(self.package_folder,"bin"))
