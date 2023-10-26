#include <iostream>

extern "C" void call_ko() {
    std::cout << "Calling kernel module function" << std::endl;
    // Call kernel module functions here
}