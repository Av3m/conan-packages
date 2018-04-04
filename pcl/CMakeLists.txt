include(${CMAKE_BINARY_DIR}/conanbuildinfo.cmake)
conan_basic_setup()

add_definitions(-D_GLIBCXX_USE_CXX11_ABI=0)

set(VTK_DIR ${CONAN_VTK_ROOT} CACHE PATH "")
set(VTK_ROOT ${CONAN_VTK_ROOT} CACHE PATH "")
set(VTK_INCLUDE_DIRS ${CONAN_VTK_ROOT}/include CACHE PATH "")
set(VTK_FOUND TRUE)
add_subdirectory(pcl)

set (CMAKE_CXX_FLAGS "-shared -fPIC")
