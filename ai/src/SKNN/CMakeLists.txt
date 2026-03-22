cmake_minimum_required(VERSION 3.10)
project(sknn LANGUAGES C)

include(cmake/config.cmake)

add_library(sknn STATIC)

include_directories(${CMAKE_SOURCE_DIR}/include)

add_subdirectory(${CMAKE_SOURCE_DIR}/src)

option(TEST_EXAMPLE "Build exaple" OFF)
if(TEST_EXAMPLE)
  add_subdirectory(${CMAKE_SOURCE_DIR}/example)
  target_link_libraries(example sknn)
  add_executable(example)
endif()

install(TARGETS sknn)
