add_library(miniOS-boot STATIC)

target_include_directories(miniOS-boot PRIVATE ${CMAKE_SOURCE_DIR}/../drivers)

target_sources(miniOS-boot PRIVATE
  entry.S
)
