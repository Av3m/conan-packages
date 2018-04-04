from conans import ConanFile, CMake, tools
import os


class PclConan(ConanFile):
    name = "pcl"
    version = "1.8.1"
    license = "3-clause BSD license"
    url = "http://pointclouds.org"
    settings = "os", "compiler", "build_type", "arch"
    options = {"shared": [True, False],"with_qt": [True,False]}
    default_options = "shared=True","with_qt=False"
    generators = "cmake","txt"
    description="""
    The Point Cloud Library (or PCL) is a large scale, open project for 2D/3D image and point cloud processing. 
    The PCL framework contains numerous state-of-the art algorithms including filtering, feature estimation, 
    surface reconstruction, registration, model fitting and segmentation. These algorithms can be used, for example, 
    to filter outliers from noisy data, stitch 3D point clouds together, segment relevant parts of a scene, extract keypoints 
    and compute descriptors to recognize objects in the world based on their geometric appearance, and create surfaces from point clouds and visualize them -- to name a few. 
    """
            
    def requirements(self):
      self.requires("Eigen3/3.3.4@%s/%s"%(self.user, self.channel))
      self.requires("VTK/7.1.1@%s/%s"%(self.user, self.channel))
      self.requires("flann/1.8.4@%s/%s"%(self.user, self.channel))
      self.requires("QHull/2015.2@%s/%s"%(self.user, self.channel))
      self.requires("boost/1.66.0@conan/stable")
      self.requires("flann/1.8.4@%s/%s"%(self.user, self.channel))
      
    def source(self):
        self.run("git clone --branch pcl-%s --single-branch https://github.com/PointCloudLibrary/pcl.git" %(self.version))
        tools.replace_in_file("pcl/CMakeLists.txt","""project(PCL)""",
        """project(PCL)
        include(${CMAKE_BINARY_DIR}/conanbuildinfo.cmake)
        conan_basic_setup()
        set(Boost_DIR ${CONAN_BOOST_ROOT})
        find_package(Boost REQUIRED COMPONENTS system filesystem thread date_time iostreams)""")

    def build(self):
        cmake = CMake(self,parallel=True)
        cmake.definitions["WITH_VTK"] = "ON"
        cmake.definitions["WITH_CUDA"] = "OFF"
        cmake.definitions["CMAKE_INSTALL_PREFIX"] = "__install"
        
        
        if ( self.options.with_qt == True):
            cmake.definitions["WITH_QT"] = "ON"
        else:
            cmake.definitions["WITH_QT"] = "OFF"
            
        if ( self.options.shared == True):
            cmake.definitions["BUILD_SHARED_LIBS"] = "ON"
        else:
            cmake.definitions["BUILD_SHARED_LIBS"] = "OFF"
            
        cmake.configure(source_dir="pcl", build_dir=".")
        cmake.build()
        cmake.install()

    def package(self):
        self.copy("*", dst=".", src="__install")

    def package_info(self):
        pcl_libs = [ 'apps','common', 'features', 'filters', 'io_ply', 'io', 'kdtree', 'keypoints', 
                     'ml', 'octree', 'outofcore', 'people', 'recognition', 'registration', 
                     'sample_consensus', 'search', 'segmentation', 'stereo', 'surface', 'tracking' , 'visualization']

        if self.settings.build_type == "Debug": 
            for lib in pcl_libs:
                self.cpp_info.libs.append("pcl_" + lib + "_debug" )
        elif self.settings.build_type == "Release": 
            for lib in pcl_libs:
                self.cpp_info.libs.append("pcl_" + lib + "_release" )

        self.cpp_info.includedirs = ['include']  # Ordered list of include paths
        self.cpp_info.libdirs = ['lib']  # Directories where libraries can be found
        self.cpp_info.bindirs = ['bin']  # Directories where executables and shared libs can be found
