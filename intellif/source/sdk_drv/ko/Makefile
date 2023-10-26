KERNEL_DIR ?= /lib/modules/$(shell uname -r)/build
INSTALL_DIR ?= /lib/modules/$(shell uname -r)/extra
$(info INSTALL_DIR is $(INSTALL_DIR))

obj-m += ko.o

all:
	make -C $(KERNEL_DIR) M=$(PWD) modules

clean:
	make -C $(KERNEL_DIR) M=$(PWD) clean
	
install:
	make -C $(KERNEL_DIR) M=$(PWD) INSTALL_MOD_PATH=$(INSTALL_DIR) modules_install
