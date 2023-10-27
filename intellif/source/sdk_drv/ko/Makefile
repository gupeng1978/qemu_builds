# 如果使用buildroot 的$(eval $(kernel-module))和$(eval $(generic-package))）标准构建，那么仅需要定义obj-m.
obj-m += ko.o


# 下面部分是模块单独编译的Makefile部分
KERNEL_DIR ?= /lib/modules/$(shell uname -r)/build
INSTALL_DIR ?= /lib/modules/$(shell uname -r)/extra
all:
	make -C $(KERNEL_DIR) M=$(PWD) modules

clean:
	make -C $(KERNEL_DIR) M=$(PWD) clean
	
install:
	make -C $(KERNEL_DIR) M=$(PWD) INSTALL_MOD_PATH=$(INSTALL_DIR) modules_install
