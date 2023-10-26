add_library(sdk_drv_lib SHARED drv.cpp)

install(TARGETS sdk_drv_lib
    LIBRARY DESTINATION lib
    ARCHIVE DESTINATION lib/static)
