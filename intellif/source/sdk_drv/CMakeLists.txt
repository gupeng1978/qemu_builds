cmake_minimum_required(VERSION 3.10)

# ---------
# 设置project信息
# ---------
function(get_sdk_drv_version)
  file(STRINGS "include/Version.h" _temp REGEX "SDK_DRV_VERSION_STRING")
  string(REGEX MATCH "\"([^\"]+)\"" _temp "${_temp}")
  set(SDK_DRV_VERSION "${CMAKE_MATCH_1}" PARENT_SCOPE)
endfunction()

get_sdk_drv_version()
project(sdk_drv VERSION "${SDK_DRV_VERSION}")


# ---------
# lib 编译
# ---------
file(GLOB SDK_DRV_HEADERS
  include/*.h
)

add_library(sdk_drv_lib SHARED lib/drv.cpp)
# 任何其他目标如果链接到sdk_drv_lib库，它们也会自动获得interface目录，这样就可以正确地找到所有必要的头文件。
target_include_directories(sdk_drv_lib INTERFACE
    $<BUILD_INTERFACE:${CMAKE_CURRENT_SOURCE_DIR}/include>
    $<INSTALL_INTERFACE:include>  # <prefix>/include
)


# ---------
# app 编译
# ---------
add_executable(sdk_drv_app app/app.cpp)
target_link_libraries(sdk_drv_app PRIVATE sdk_drv_lib)


# ---------
# install
# ---------
# include(GNUInstallDirs) 是 CMake 中的一个命令，它提供了一种标准的方式来定义安装目录的位置。
# 这个命令定义的变量是基于GNU编程标准，它们包括但不限于：
# CMAKE_INSTALL_BINDIR: 二进制文件的安装目录，通常是 bin。
# CMAKE_INSTALL_SBINDIR: 系统二进制文件的安装目录，通常是 sbin。
# CMAKE_INSTALL_LIBDIR: 库文件的安装目录，通常是 lib。
# CMAKE_INSTALL_INCLUDEDIR: 头文件的安装目录，通常是 include。
# CMAKE_INSTALL_DATAROOTDIR: 共享数据的根目录，通常是 share。
include(GNUInstallDirs)
set(config_install_dir "${CMAKE_INSTALL_LIBDIR}/cmake/${PROJECT_NAME}")
set(generated_dir "${CMAKE_CURRENT_BINARY_DIR}/generated")
set(version_config "${generated_dir}/${PROJECT_NAME}ConfigVersion.cmake")
set(project_config "${generated_dir}/${PROJECT_NAME}Config.cmake")
set(TARGETS_EXPORT_NAME "${PROJECT_NAME}Targets")
set(namespace "${PROJECT_NAME}::")


# CMakePackageConfigHelpers 是 CMake 中的一个模块，它提供了一种简单的方式来创建和使用 CMake 配置文件。
# 可以创建和安装适用于find_package()命令的配置文件，以便其他项目可以轻松找到和使用你的项目, CMakePackageConfigHelpers中的函数:
# 1. write_basic_package_version_file：这个函数会创建一个版本配置文件，它包含了用于检查包版本兼容性的代码。
# 2. configure_package_config_file：这个函数会创建一个配置文件，它包含了项目的导出配置。
include(CMakePackageConfigHelpers)
write_basic_package_version_file(
    "${version_config}" COMPATIBILITY SameMajorVersion
)

configure_package_config_file(
    "cmake/Config.cmake.in"
    "${project_config}"
    INSTALL_DESTINATION "${config_install_dir}"
)
# 安装库和头文件
install(TARGETS sdk_drv_lib
    EXPORT "${TARGETS_EXPORT_NAME}"
    LIBRARY DESTINATION "${CMAKE_INSTALL_LIBDIR}"
    ARCHIVE DESTINATION "${CMAKE_INSTALL_LIBDIR}"
    RUNTIME DESTINATION "${CMAKE_INSTALL_BINDIR}"
    INCLUDES DESTINATION "${CMAKE_INSTALL_INCLUDEDIR}"
)

install(DIRECTORY include/ DESTINATION "${CMAKE_INSTALL_INCLUDEDIR}")

# 安装导出目标文件，其他项目中可以使用find_package()和target_link_libraries()命令来找到和链接
install(EXPORT "${TARGETS_EXPORT_NAME}"
    NAMESPACE "${namespace}"
    DESTINATION "${config_install_dir}"
)

# 安装配置文件
install(FILES "${project_config}" "${version_config}"
    DESTINATION "${config_install_dir}"
)

# 安装app
install(TARGETS sdk_drv_app DESTINATION bin)

