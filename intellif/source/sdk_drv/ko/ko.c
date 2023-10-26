#include <linux/init.h>
#include <linux/module.h>
#include <linux/kernel.h>

MODULE_LICENSE("GPL");
MODULE_AUTHOR("PengGu");
MODULE_DESCRIPTION("A simple Linux driver for the kernel module");
MODULE_VERSION("0.2");

static int __init ko_init(void) {
    pr_info("Hello, ko!\n");
    return 0;
}

static void __exit  ko_exit(void) {
    pr_info("Goodbye, ko!\n");
}

module_init(ko_init);
module_exit(ko_exit);
