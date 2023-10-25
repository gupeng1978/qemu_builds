cmake_minimum_required(VERSION 3.10)
project(app_hello_world)
set(CMAKE_CXX_STANDARD 11)
add_executable(app_hello_world main.cpp)

set(COMPANY_NAME "ZTE" CACHE STRING "Set the company")
if(DEFINED ENV{COMPANY_NAME})
    set(COMPANY_NAME $ENV{COMPANY_NAME})
endif()
message(STATUS "COMPANY_NAME=${COMPANY_NAME}")
# 用双引号将 ${COMPANY_NAME} 包围，以便它被正确地解析为一个字符串
target_compile_definitions(app_hello_world PRIVATE COMPANY_NAME="${COMPANY_NAME}")

if(DEFINED ENV{VERSION})
    message(STATUS "VERSION=$ENV{VERSION}")
endif()

install(TARGETS app_hello_world DESTINATION bin)
