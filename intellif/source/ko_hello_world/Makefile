# 对于buildroot构建，/lib/modules/$(shell uname -r)/build
# 在构建内核模块时通常是指向 Linux 内核源代码树的符号链接。
# $(shell uname -r) 会被替换为当前运行的内核版本号。
KERNEL_DIR ?= /lib/modules/$(shell uname -r)/build
INSTALL_DIR ?= /lib/modules/$(shell uname -r)/extra

obj-m += hello.o

all:
	make -C $(KERNEL_DIR) M=$(PWD) modules

clean:
	make -C $(KERNEL_DIR) M=$(PWD) clean
	
install:
	make -C $(KERNEL_DIR) M=$(PWD) INSTALL_MOD_PATH=$(INSTALL_DIR) modules_install
