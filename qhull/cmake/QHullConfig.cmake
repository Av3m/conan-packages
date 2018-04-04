include(LibFindMacros)

get_filename_component(this_dir ${CMAKE_CURRENT_LIST_FILE} PATH)
# Include dir

find_path(QHull_INCLUDE_DIR
  NAMES libqhull.h
  PATHS ${this_dir}/include/libqhull
)

get_filename_component(QHull_INCLUDE_DIR_PARENT ${QHull_INCLUDE_DIR} PATH)


# Finally the library itself
find_library(QHull_LIBRARY
  NAMES qhullstatic libqhullstatic
  PATHS ${this_dir}/lib
)

# Set the include dir variables and the libraries and let libfind_process do the rest.
# NOTE: Singular variables for this library, plural for libraries this this lib depends on.
set(QHull_PROCESS_INCLUDES QHull_INCLUDE_DIR QHull_INCLUDE_DIR_PARENT QHull_INCLUDE_DIRS)
set(QHull_PROCESS_LIBS QHull_LIBRARY QHull_LIBRARIES)
libfind_process(QHull)

