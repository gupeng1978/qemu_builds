KO_HELLO_WORLD_VERSION = 0.2
KO_HELLO_WORLD_LICENSE = MIT
KO_HELLO_WORLD_SITE = $(TOPDIR)/../intellif/source/ko_hello_world
KO_HELLO_WORLD_SITE_METHOD = local


$(eval $(kernel-module))
$(eval $(generic-package))
