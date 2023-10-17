APP_OPENCV_DEMO_0_VERSION = 0.1
APP_OPENCV_DEMO_0_LICENSE = MIT


APP_OPENCV_DEMO_0_SITE = $(TOPDIR)/../intellif/source/app_opencv_demo_0
APP_OPENCV_DEMO_0_SITE_METHOD = local

define APP_OPENCV_DEMO_0_BUILD_CMDS
    $(info Building app opencv demo...)
endef

define APP_OPENCV_DEMO_0_INSTALL_TARGET_CMDS
    $(info Installing app opencv demo...)
endef

$(eval $(generic-package))
