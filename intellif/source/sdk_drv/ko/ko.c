#include <linux/init.h>
#include <linux/module.h>
#include <linux/device.h>
#include <linux/kernel.h>
#include <linux/fs.h>
#include <linux/uaccess.h>

#define  DEVICE_NAME "hello"
#define  CLASS_NAME  "hello"

MODULE_LICENSE("GPL");

static int    majorNumber;
static char   message[256] = {0};
static short  size_of_message;
static struct class*  helloClass  = NULL;
static struct device* helloDevice = NULL;

static int     dev_open(struct inode *, struct file *);
static int     dev_release(struct inode *, struct file *);
static ssize_t dev_read(struct file *, char *, size_t, loff_t *);

static struct file_operations fops =
{
   .open = dev_open,
   .read = dev_read,
   .release = dev_release,
};

static int __init hello_init(void){
   strcpy(message, "Hello World!\n");
   size_of_message = strlen(message);
   majorNumber = register_chrdev(0, DEVICE_NAME, &fops);
   if (majorNumber<0){
      printk(KERN_ALERT "Hello failed to register a major number\n");
      return majorNumber;
   }
   helloClass = class_create(THIS_MODULE, CLASS_NAME);
   if (IS_ERR(helloClass)){
      unregister_chrdev(majorNumber, DEVICE_NAME);
      printk(KERN_ALERT "Failed to register device class\n");
      return PTR_ERR(helloClass);
   }
   helloDevice = device_create(helloClass, NULL, MKDEV(majorNumber, 0), NULL, DEVICE_NAME);
   if (IS_ERR(helloDevice)){
      class_destroy(helloClass);
      unregister_chrdev(majorNumber, DEVICE_NAME);
      printk(KERN_ALERT "Failed to create the device\n");
      return PTR_ERR(helloDevice);
   }
   return 0;
}

static void __exit hello_exit(void){
   device_destroy(helloClass, MKDEV(majorNumber, 0));
   class_unregister(helloClass);
   class_destroy(helloClass);
   unregister_chrdev(majorNumber, DEVICE_NAME);
   printk(KERN_INFO "Hello: Goodbye from the LKM!\n");
}

static int dev_open(struct inode *inodep, struct file *filep){
   printk(KERN_INFO "Hello: Device has been opened\n");
   return 0;
}

static ssize_t dev_read(struct file *filep, char *buffer, size_t len, loff_t *offset){
   int error_count = 0;
   error_count = copy_to_user(buffer, message, size_of_message);

   if (error_count==0){
      printk(KERN_INFO "Hello: Sent %d characters to the user\n", size_of_message);
      return size_of_message;
   }
   else {
      printk(KERN_INFO "Hello: Failed to send %d characters to the user\n", error_count);
      return -EFAULT;
   }
}

static int dev_release(struct inode *inodep, struct file *filep){
   printk(KERN_INFO "Hello: Device successfully closed\n");
   return 0;
}

module_init(hello_init);
module_exit(hello_exit);
