SDK_DRV_VERSION = 0.1
SDK_DRV_LICENSE = MIT
SDK_DRV_SITE = $(TOPDIR)/../intellif/source/sdk_drv
SDK_DRV_SITE_METHOD = local
SDK_DRV_INSTALL_STAGING = NO
SDK_DRV_DEPENDENCIES = linux
$(eval $(cmake-package))
