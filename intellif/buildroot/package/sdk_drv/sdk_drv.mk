SDK_DRV_VERSION = 0.1
SDK_DRV_LICENSE = MIT
SDK_DRV_SITE = $(TOPDIR)/../intellif/source/sdk_drv
SDK_DRV_SITE_METHOD = local
SDK_DRV_INSTALL_STAGING = YES
SDK_DRV_INSTALL_TARGET = YES

# 下面这行指定了这是一个使用 CMake 构建系统的包
SDK_DRV_DEPENDENCIES = host-pkgconf

$(eval $(cmake-package))
