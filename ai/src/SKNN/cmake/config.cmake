function(add_sknn_sources TARGET_NAME)
  if(NOT TARGET ${TARGET_NAME})
    message(FATAL_ERROR "Target '${TARGET_NAME}' does not exist. ")
  endif()

  set(sknn_sources ${ARGN})
  if(sknn_sources STREQUAL "")
    message(WARNING " No source files provided for target '${TARGET_NAME}'. ")
    return()
  endif()
  list(TRANSFORM sknn_sources PREPEND "${CMAKE_CURRENT_SOURCE_DIR}/")

  target_sources(${TARGET_NAME} PRIVATE ${sknn_sources})
endfunction()
