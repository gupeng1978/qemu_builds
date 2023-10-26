cmake_minimum_required(VERSION 3.10)
project(sdk_drv)

# add_subdirectory(ko)
# 为ko文件创建一个自定义目标
set(KO_DIR ${CMAKE_SOURCE_DIR}/ko)
add_custom_target(
  my_ko ALL
  COMMAND $(MAKE) -C ${KO_DIR} install
)

add_subdirectory(lib)
add_subdirectory(app)