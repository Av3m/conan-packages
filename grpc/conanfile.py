from conans import ConanFile, CMake, tools
import os


class GrpcConan(ConanFile):
    name = "grpc"
    version = "1.10.0"
    license = "Apache License 2.0"
    description = "Remote Procedure Calls (RPCs) provide a useful abstraction for building distributed applications and services. \
           The libraries in this repository provide a concrete implementation of the gRPC protocol, layered over HTTP/2. \
           These libraries enable communication between clients and servers using any combination of the supported languages."
    url = ""
    settings = "os", "compiler", "build_type", "arch"
    options = {"shared": [True, False]}
    default_options = "shared=False"
    generators = "cmake"

    def requirements(self):
        self.requires('zlib/1.2.11@conan/stable')
        self.requires('OpenSSL/1.1.0g@conan/stable')
        self.requires('Protobuf/3.5.1.1@intence/testing')
        self.requires('cares/1.14.0@intence/stable')
    def source(self):
        self.run("git clone --branch v%s --single-branch https://github.com/grpc/grpc.git" % ( self.version) )
        self.run('git submodule update --init',cwd='grpc')

        # This small hack might be useful to guarantee proper /MT /MD linkage in MSVC
        # if the packaged project doesn't have variables to set it properly
        tools.replace_in_file("grpc/CMakeLists.txt", 'project(${PACKAGE_NAME} C CXX)', 
        '''project(${PACKAGE_NAME} C CXX)
        include(${CMAKE_BINARY_DIR}/conanbuildinfo.cmake)
        conan_basic_setup()''')

        tools.replace_in_file("grpc/cmake/ssl.cmake", 'set(_gRPC_SSL_LIBRARIES OpenSSL::SSL OpenSSL::Crypto)',
                                                      'set(_gRPC_SSL_LIBRARIES OpenSSL::SSL OpenSSL::Crypto ${CONAN_LIBS_OPENSSL})' )
        tools.replace_in_file("grpc/cmake/ssl.cmake", 'set(_gRPC_SSL_LIBRARIES ${OPENSSL_LIBRARIES})',
                                                      'set(_gRPC_SSL_LIBRARIES ${OPENSSL_LIBRARIES} ${CONAN_LIBS_OPENSSL})' )
    def build(self):
        cmake = CMake(self)
        cmake.definitions["CMAKE_INSTALL_PREFIX"] = os.path.join(self.build_folder,"install")
        cmake.definitions["gRPC_ZLIB_PROVIDER"] = "package"
        cmake.definitions["gRPC_SSL_PROVIDER"] = "package"
        cmake.definitions["gRPC_PROTOBUF_PROVIDER"] = "package"
        cmake.definitions["gRPC_CARES_PROVIDER"] = "package"
        cmake.definitions["gRPC_BUILD_TESTS"] = "OFF"
        cmake.definitions["gRPC_INSTALL"] = "ON"
        cmake.configure(source_folder="grpc",build_folder=".")
        cmake.build()
        cmake.install()

    def package(self):
        self.copy("*", src=os.path.join(self.build_folder,"install"), dst=".")

    def package_info(self):
        pass
