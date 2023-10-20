cmake_minimum_required(VERSION 3.10)
project(app_opencv_demo_0)
set(CMAKE_CXX_STANDARD 11)


find_package(OpenCV REQUIRED)

add_executable(app_opencv_demo_0 main.cpp)


target_link_libraries(app_opencv_demo_0 ${OpenCV_LIBS})

install(TARGETS app_opencv_demo_0 DESTINATION bin)
