SDK_DRV_KO_VERSION = 0.1
SDK_DRV_KO_LICENSE = MIT
SDK_DRV_KO_SITE = $(TOPDIR)/../intellif/source/sdk_drv
SDK_DRV_KO_SITE_METHOD = local
SDK_DRV_KO_MODULE_SUBDIRS := ko

# $(info "-----------------------------$(LINUX_MAKE_ENV)")
# $(info "-----------------------------$(LINUX_DIR)")
# $(info "-----------------------------$(LINUX_MAKE_FLAGS)")


$(eval $(kernel-module))
$(eval $(generic-package))


