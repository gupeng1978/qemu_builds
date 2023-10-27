// File: hello_lib.c
#include "../include/sdk_drv.h"
#include <stdio.h>
#include <stdlib.h>
#include <fcntl.h>
#include <unistd.h>

char* get_message(void) {
    static char message[256];
    int fd = open("/dev/hello", O_RDONLY);
    if (fd < 0) {
        perror("open");
        return NULL;
    }
    ssize_t len = read(fd, message, sizeof(message)-1);
    if (len < 0) {
        perror("read");
        close(fd);
        return NULL;
    }
    message[len] = '\0';
    close(fd);
    return message;
}
