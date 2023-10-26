add_executable(app app.cpp)
target_link_libraries(app PRIVATE sdk_drv_lib)

install(TARGETS app DESTINATION bin)
