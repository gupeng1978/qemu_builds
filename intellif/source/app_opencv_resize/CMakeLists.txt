cmake_minimum_required(VERSION 3.10)
project(app_opencv_resize)
set(CMAKE_CXX_STANDARD 11)
find_package(OpenCV REQUIRED)

set(LOG_LEVEL "LOG_LEVEL_DEBUG" CACHE STRING "Set the log level")
set_property(CACHE LOG_LEVEL PROPERTY STRINGS LOG_LEVEL_DEBUG LOG_LEVEL_INFO LOG_LEVEL_ERROR)

add_executable(app_opencv_resize main.cpp)
target_link_libraries(app_opencv_resize ${OpenCV_LIBS})
target_compile_definitions(app_opencv_resize PRIVATE LOG_LEVEL=${LOG_LEVEL})

message(STATUS "LOG_LEVEL=${LOG_LEVEL}")
message(STATUS "CMAKE_BUILD_TYPE=${CMAKE_BUILD_TYPE}")

install(TARGETS app_opencv_resize DESTINATION bin)
install(FILES data/cat.jpg DESTINATION /usr/share/app_opencv_resize)
