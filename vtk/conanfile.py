import os
from conans import ConanFile, CMake,tools

class VTKConan(ConanFile):
    name = "VTK"
    generators = "cmake"
    settings = "os", "compiler", "build_type", "arch"
    options = {"shared": [True, False], "with_qt":[True,False] }
    default_options = "shared=True","with_qt=False"
    url="http://github.com/av3m/conan-vtk.git"
    license="http://www.vtk.org/licensing/"
    short_paths=True
    

    def configure(self):
        if self.options.with_qt == True:
            self.requires("Qt/[>=5.0.0]@%s/%s" %(self.user,self.channel))
    
    def system_requirements(self):
        installer= tools.SystemPackageTool(self)
        if tools.os_info.is_linux and tools.os_info.linux_distro in [ "ubuntu" , "debian" ]:
                installer.install("freeglut3-dev")
                installer.install("mesa-common-dev")
                installer.install("mesa-utils-extra")
                installer.install("libgl1-mesa-dev")
                installer.install("libglapi-mesa")

    def remove_qt_absolute_paths(self):
        qt_lib_path = os.path.join(self.deps_cpp_info["Qt"].rootpath,"lib")
        qt_lib_path = qt_lib_path.replace("\\","/") + "/"
        tools.replace_in_file("_install/lib/cmake/vtk-7.1/VTKTargets.cmake",qt_lib_path,"")


    def source(self):
        self.run("git clone --branch v%s --single-branch https://gitlab.kitware.com/vtk/vtk.git vtk" %(self.version) )
        tools.replace_in_file("vtk/CMakeLists.txt","""project(VTK)""","""project(VTK)
        include(${CMAKE_BINARY_DIR}/conanbuildinfo.cmake)
        conan_basic_setup()""")

    def build(self):
        cmake = CMake(self,parallel=True)

        cmake.definitions["BUILD_TESTING"] = "OFF"
        cmake.definitions["BUILD_EXAMPLES"] = "OFF"
        cmake.definitions["CMAKE_INSTALL_PREFIX"] = "_install" 

        if self.options.shared == False:
            cmake.definitions["BUILD_SHARED_LIBS"] = "OFF"
        else:
            cmake.definitions["BUILD_SHARED_LIBS"] = "ON"
        if self.options.with_qt == True:
            cmake.definitions["VTK_Group_Qt:BOOL"] = "ON"
            cmake.definitions["VTK_BUILD_QT_DESIGNER_PLUGIN:BOOL"] = "ON"

        if self.settings.build_type == "Debug" and self.settings.compiler == "Visual Studio":
            cmake.definitions["CMAKE_DEBUG_POSTFIX"] = "_d"

        cmake.configure(source_dir="vtk", build_dir=".")
        cmake.build()
        cmake.install()
        #if self.options.with_qt == True:
        #    self.remove_qt_absolute_paths()

    def package(self):
        self.copy("*", dst=".", src="_install")

    def package_info(self):
        self.short_version = ".".join(str(self.version).split(".")[0:2])
        LIB_POSTFIX = ""
        if self.settings.build_type == "Debug" and self.settings.compiler == "Visual Studio":
            LIB_POSTFIX = "_d"
        libs = [
            "vtkalglib-%s" % self.short_version + LIB_POSTFIX,
            "vtkChartsCore-%s" % self.short_version + LIB_POSTFIX,
            "vtkCommonColor-%s" % self.short_version + LIB_POSTFIX,
            "vtkCommonComputationalGeometry-%s" % self.short_version + LIB_POSTFIX,
            "vtkCommonCore-%s" % self.short_version + LIB_POSTFIX,
            "vtkCommonDataModel-%s" % self.short_version + LIB_POSTFIX,
            "vtkCommonExecutionModel-%s" % self.short_version + LIB_POSTFIX,
            "vtkCommonMath-%s" % self.short_version + LIB_POSTFIX,
            "vtkCommonMisc-%s" % self.short_version + LIB_POSTFIX,
            "vtkCommonSystem-%s" % self.short_version + LIB_POSTFIX,
            "vtkCommonTransforms-%s" % self.short_version + LIB_POSTFIX,
            "vtkDICOMParser-%s" % self.short_version + LIB_POSTFIX,
            "vtkDomainsChemistry-%s" % self.short_version + LIB_POSTFIX,
            "vtkDomainsChemistryOpenGL2-%s" % self.short_version + LIB_POSTFIX,
            "vtkexoIIc-%s" % self.short_version + LIB_POSTFIX,
            "vtkexpat-%s" % self.short_version + LIB_POSTFIX,
            "vtkFiltersAMR-%s" % self.short_version + LIB_POSTFIX,
            "vtkFiltersCore-%s" % self.short_version + LIB_POSTFIX,
            "vtkFiltersExtraction-%s" % self.short_version + LIB_POSTFIX,
            "vtkFiltersFlowPaths-%s" % self.short_version + LIB_POSTFIX,
            "vtkFiltersGeneral-%s" % self.short_version + LIB_POSTFIX,
            "vtkFiltersGeneric-%s" % self.short_version + LIB_POSTFIX,
            "vtkFiltersGeometry-%s" % self.short_version + LIB_POSTFIX,
            "vtkFiltersHybrid-%s" % self.short_version + LIB_POSTFIX,
            "vtkFiltersHyperTree-%s" % self.short_version + LIB_POSTFIX,
            "vtkFiltersImaging-%s" % self.short_version + LIB_POSTFIX,
            "vtkFiltersModeling-%s" % self.short_version + LIB_POSTFIX,
            "vtkFiltersParallel-%s" % self.short_version + LIB_POSTFIX,
            "vtkFiltersParallelImaging-%s" % self.short_version + LIB_POSTFIX,
            "vtkFiltersProgrammable-%s" % self.short_version + LIB_POSTFIX,
            "vtkFiltersSelection-%s" % self.short_version + LIB_POSTFIX,
            "vtkFiltersSMP-%s" % self.short_version + LIB_POSTFIX,
            "vtkFiltersSources-%s" % self.short_version + LIB_POSTFIX,
            "vtkFiltersStatistics-%s" % self.short_version + LIB_POSTFIX,
            "vtkFiltersTexture-%s" % self.short_version + LIB_POSTFIX,
            "vtkFiltersVerdict-%s" % self.short_version + LIB_POSTFIX,
            "vtkfreetype-%s" % self.short_version + LIB_POSTFIX,
            "vtkGeovisCore-%s" % self.short_version + LIB_POSTFIX,
            "vtkglew-%s" % self.short_version + LIB_POSTFIX,
            "vtkhdf5_hl-%s" % self.short_version + LIB_POSTFIX,
            "vtkhdf5-%s" % self.short_version + LIB_POSTFIX,
            "vtkImagingColor-%s" % self.short_version + LIB_POSTFIX,
            "vtkImagingCore-%s" % self.short_version + LIB_POSTFIX,
            "vtkImagingFourier-%s" % self.short_version + LIB_POSTFIX,
            "vtkImagingGeneral-%s" % self.short_version + LIB_POSTFIX,
            "vtkImagingHybrid-%s" % self.short_version + LIB_POSTFIX,
            "vtkImagingMath-%s" % self.short_version + LIB_POSTFIX,
            "vtkImagingMorphological-%s" % self.short_version + LIB_POSTFIX,
            "vtkImagingSources-%s" % self.short_version + LIB_POSTFIX,
            "vtkImagingStatistics-%s" % self.short_version + LIB_POSTFIX,
            "vtkImagingStencil-%s" % self.short_version + LIB_POSTFIX,
            "vtkInfovisCore-%s" % self.short_version + LIB_POSTFIX,
            "vtkInfovisLayout-%s" % self.short_version + LIB_POSTFIX,
            "vtkInteractionImage-%s" % self.short_version + LIB_POSTFIX,
            "vtkInteractionStyle-%s" % self.short_version + LIB_POSTFIX,
            "vtkInteractionWidgets-%s" % self.short_version + LIB_POSTFIX,
            "vtkIOAMR-%s" % self.short_version + LIB_POSTFIX,
            "vtkIOCore-%s" % self.short_version + LIB_POSTFIX,
            "vtkIOEnSight-%s" % self.short_version + LIB_POSTFIX,
            "vtkIOExodus-%s" % self.short_version + LIB_POSTFIX,
            "vtkIOExport-%s" % self.short_version + LIB_POSTFIX,
            "vtkIOGeometry-%s" % self.short_version + LIB_POSTFIX,
            "vtkIOImage-%s" % self.short_version + LIB_POSTFIX,
            "vtkIOImport-%s" % self.short_version + LIB_POSTFIX,
            "vtkIOInfovis-%s" % self.short_version + LIB_POSTFIX,
            "vtkIOLegacy-%s" % self.short_version + LIB_POSTFIX,
            "vtkIOLSDyna-%s" % self.short_version + LIB_POSTFIX,
            "vtkIOMINC-%s" % self.short_version + LIB_POSTFIX,
            "vtkIOMovie-%s" % self.short_version + LIB_POSTFIX,
            "vtkIONetCDF-%s" % self.short_version + LIB_POSTFIX,
            "vtkIOParallel-%s" % self.short_version + LIB_POSTFIX,
            "vtkIOParallelXML-%s" % self.short_version + LIB_POSTFIX,
            "vtkIOPLY-%s" % self.short_version + LIB_POSTFIX,
            "vtkIOSQL-%s" % self.short_version + LIB_POSTFIX,
            "vtkIOVideo-%s" % self.short_version + LIB_POSTFIX,
            "vtkIOXML-%s" % self.short_version + LIB_POSTFIX,
            "vtkIOXMLParser-%s" % self.short_version + LIB_POSTFIX,
            "vtkjpeg-%s" % self.short_version + LIB_POSTFIX,
            "vtkjsoncpp-%s" % self.short_version + LIB_POSTFIX,
            "vtklibxml2-%s" % self.short_version + LIB_POSTFIX,
            "vtkmetaio-%s" % self.short_version + LIB_POSTFIX,
            "vtkNetCDF_cxx-%s" % self.short_version + LIB_POSTFIX,
            "vtkNetCDF-%s" % self.short_version + LIB_POSTFIX,
            "vtkoggtheora-%s" % self.short_version + LIB_POSTFIX,
            "vtkParallelCore-%s" % self.short_version + LIB_POSTFIX,
            "vtkpng-%s" % self.short_version + LIB_POSTFIX,
            "vtkproj4-%s" % self.short_version + LIB_POSTFIX,
            "vtkRenderingAnnotation-%s" % self.short_version + LIB_POSTFIX,
            "vtkRenderingContext2D-%s" % self.short_version + LIB_POSTFIX,
            "vtkRenderingContextOpenGL2-%s" % self.short_version + LIB_POSTFIX,
            "vtkRenderingCore-%s" % self.short_version + LIB_POSTFIX,
            "vtkRenderingFreeType-%s" % self.short_version + LIB_POSTFIX,
            "vtkRenderingImage-%s" % self.short_version + LIB_POSTFIX,
            "vtkRenderingLabel-%s" % self.short_version + LIB_POSTFIX,
            "vtkRenderingLOD-%s" % self.short_version + LIB_POSTFIX,
            "vtkRenderingOpenGL2-%s" % self.short_version + LIB_POSTFIX,
            "vtkRenderingVolume-%s" % self.short_version + LIB_POSTFIX,
            "vtkRenderingVolumeOpenGL2-%s" % self.short_version + LIB_POSTFIX,
            "vtksqlite-%s" % self.short_version + LIB_POSTFIX,
            "vtksys-%s" % self.short_version + LIB_POSTFIX,
            "vtktiff-%s" % self.short_version + LIB_POSTFIX,
            "vtkverdict-%s" % self.short_version + LIB_POSTFIX,
            "vtkViewsContext2D-%s" % self.short_version + LIB_POSTFIX,
            "vtkViewsCore-%s" % self.short_version + LIB_POSTFIX,
            "vtkViewsInfovis-%s" % self.short_version + LIB_POSTFIX,
            "vtkzlib-%s" % self.short_version + LIB_POSTFIX
        ]
        if self.options.with_qt:
            libs.append("vtkGUISupportQt-%s" % self.short_version + LIB_POSTFIX)
            libs.append("vtkGUISupportQtSQL-%s" % self.short_version + LIB_POSTFIX)
        self.cpp_info.libs = libs
        self.cpp_info.includedirs = [
            "include/vtk-%s" % self.short_version,
            "include/vtk-%s/vtknetcdf/include" % self.short_version,
        ]
