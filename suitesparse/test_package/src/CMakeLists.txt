project(SuitesparseTest)


include(${CMAKE_BINARY_DIR}/conanbuildinfo.cmake)
conan_basic_setup()
find_package(Cholmod REQUIRED)

add_executable(cholmod-test cholmod-test.cpp)
TARGET_LINK_LIBRARIES(cholmod-test ${Cholmod_LIBRARIES})
