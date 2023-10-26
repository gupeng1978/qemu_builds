#include <linux/init.h>
#include <linux/module.h>
#include <linux/kernel.h>

MODULE_LICENSE("GPL");
MODULE_AUTHOR("PengGu");
MODULE_DESCRIPTION("A simple Linux driver for the kernel module");
MODULE_VERSION("0.2");

static int __init hello_init(void) {
    pr_info("Hello, World, my name is k2!\n");
    return 0;
}

static void __exit hello_exit(void) {
    pr_info("Goodbye, World!\n");
}


module_init(hello_init);
module_exit(hello_exit);
