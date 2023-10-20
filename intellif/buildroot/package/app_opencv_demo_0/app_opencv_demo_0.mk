APP_OPENCV_DEMO_0_VERSION = 0.1
APP_OPENCV_DEMO_0_LICENSE = MIT


APP_OPENCV_DEMO_0_SITE = $(TOPDIR)/../intellif/source/app_opencv_demo_0
APP_OPENCV_DEMO_0_SITE_METHOD = local
APP_OPENCV_DEMO_0_INSTALL_STAGING = NO
APP_OPENCV_DEMO_0_DEPENDENCIES = opencv4



# define APP_OPENCV_DEMO_0_BUILD_CMDS
#     $(info Building app opencv demo...)
#     $(TARGET_MAKE_ENV) $(CMAKE) -H$(@D) -B$(@D)/build -DCMAKE_BUILD_TYPE=Release
#     $(TARGET_MAKE_ENV) $(MAKE) -C $(@D)/build
# endef

# define APP_OPENCV_DEMO_0_INSTALL_TARGET_CMDS
#     $(info Installing app opencv demo...)
#     $(INSTALL) -D -m 0755 $(@D)/build/app_opencv_demo_0 $(TARGET_DIR)/usr/bin/app_opencv_demo_0
# endef

$(eval $(cmake-package))
