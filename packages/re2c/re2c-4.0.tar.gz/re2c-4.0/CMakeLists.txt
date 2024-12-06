cmake_minimum_required(VERSION 3.15)

project(Re2cPythonDistributions NONE)

set(default_build_type "Release")
if(NOT CMAKE_BUILD_TYPE AND NOT CMAKE_CONFIGURATION_TYPES)
  message(STATUS "Setting build type to '${default_build_type}' as none was specified.")
  set(CMAKE_BUILD_TYPE "${default_build_type}" CACHE
      STRING "Choose the type of build." FORCE)
  set_property(CACHE CMAKE_BUILD_TYPE PROPERTY STRINGS
    "Debug" "Release" "MinSizeRel" "RelWithDebInfo")
endif()

enable_language(CXX)
enable_language(C)
include(ExternalProject)

include(re2c_version.cmake)

set(_re2c_cache_args)
set(_re2c_build_flags)

# if(WIN32)
#   set(_re2c_build_flags "${_re2c_build_flags} -static -static-libgcc -static-libstdc++")
# endif()

# re2c
set(RE2C_SOURCE_DIR ${CMAKE_BINARY_DIR}/re2c-src)
set(RE2C_BINARY_DIR ${CMAKE_BINARY_DIR}/re2c-build)

ExternalProject_add(re2c
    SOURCE_DIR ${RE2C_SOURCE_DIR}
    BINARY_DIR ${RE2C_BINARY_DIR}
    URL "https://github.com/skvadrik/re2c/releases/download/${RE2C_VERSION}/re2c-${RE2C_VERSION}.tar.xz"
    CMAKE_CACHE_ARGS
    -DRE2C_BUILD_RE2D:BOOL=OFF
    -DRE2C_BUILD_RE2GO:BOOL=OFF
    -DRE2C_BUILD_RE2HS:BOOL=OFF
    -DRE2C_BUILD_RE2JAVA:BOOL=OFF
    -DRE2C_BUILD_RE2JS:BOOL=OFF
    -DRE2C_BUILD_RE2OCAML:BOOL=OFF
    -DRE2C_BUILD_RE2PY:BOOL=OFF
    -DRE2C_BUILD_RE2RUST:BOOL=OFF
    -DRE2C_BUILD_RE2V:BOOL=OFF
    -DRE2C_BUILD_RE2ZIG:BOOL=OFF
    -DBUILD_TESTING:BOOL=OFF
    -DCMAKE_CXX_STANDARD_REQUIRED:BOOL=ON
    -DCMAKE_CXX_STANDARD:STRING=11
    -DCMAKE_INSTALL_PREFIX:PATH=${CMAKE_INSTALL_PREFIX}
    "-DCMAKE_CXX_COMPILER:FILEPATH=${CMAKE_CXX_COMPILER}"
    "-DCMAKE_C_COMPILER:FILEPATH=${CMAKE_C_COMPILER}"
    "-DCMAKE_BUILD_TYPE:STRING=${CMAKE_BUILD_TYPE}"
    "-DCMAKE_C_FLAGS:STRING=${_re2c_build_flags}"
    "-DCMAKE_CXX_FLAGS:STRING=${_re2c_build_flags}"
    "-DCMAKE_OSX_ARCHITECTURES:STRING=${CMAKE_OSX_ARCHITECTURES}"
    ${_re2c_cache_args}
    INSTALL_COMMAND ""
    DEPENDS
    )
install(SCRIPT ${RE2C_BINARY_DIR}/cmake_install.cmake)
