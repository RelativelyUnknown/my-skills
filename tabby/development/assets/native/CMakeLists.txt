# Template for a C++ extension built with nanobind and scikit-build-core.
# NOT BUILT HERE: nanobind was not installed in the session that wrote this. Check it against
# the nanobind docs for the version you pin (docs/api_cmake.rst, docs/packaging.rst) before use.
cmake_minimum_required(VERSION 3.18)
project(${SKBUILD_PROJECT_NAME} LANGUAGES CXX)

set(CMAKE_CXX_STANDARD 17)
set(CMAKE_CXX_STANDARD_REQUIRED ON)

find_package(Python 3.12 COMPONENTS Interpreter Development.Module REQUIRED)
find_package(nanobind CONFIG REQUIRED)

# STABLE_ABI: one wheel per platform for Python 3.12+ (ignored below 3.12 and in free-threaded builds;
# measure before choosing it). FREE_THREADED: only after the module's shared state is synchronised.
nanobind_add_module(_core STABLE_ABI NB_STATIC src/_core.cpp)

install(TARGETS _core LIBRARY DESTINATION <pkg>)
