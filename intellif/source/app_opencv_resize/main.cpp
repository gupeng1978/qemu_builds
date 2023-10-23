#include <opencv2/opencv.hpp>
#include <iostream>
#include <fstream>

// Define log levels
#define LOG_LEVEL_ERROR 0
#define LOG_LEVEL_INFO 1
#define LOG_LEVEL_DEBUG 2


// Macro for error logging
#define LOG_ERROR(msg) if (LOG_LEVEL >= LOG_LEVEL_ERROR) { std::cerr << "ERROR: " << msg << std::endl; }

// Macro for info logging
#define LOG_INFO(msg) if (LOG_LEVEL >= LOG_LEVEL_INFO) { std::cout << "INFO: " << msg << std::endl; }

// Macro for debug logging
#define LOG_DEBUG(msg) if (LOG_LEVEL >= LOG_LEVEL_DEBUG) { std::cout << "DEBUG: " << msg << std::endl; }

int main() {
    std::string imagePath = "/usr/share/app_opencv_resize/cat.jpg";  // 图像文件路径

    // Check if the image file exists
    std::ifstream file(imagePath);
    if (!file.good()) {
        LOG_ERROR("Failed to open image file at path: " << imagePath);
        return -1;
    }

    cv::Mat image = cv::imread(imagePath, cv::IMREAD_COLOR);

    if (image.empty()) {
        LOG_ERROR("Failed to load image at path: " << imagePath);
        return -1;
    }

    // 将图像缩放到400x400
    cv::Mat resized_image;
    cv::resize(image, resized_image, cv::Size(400, 400));

    LOG_DEBUG("opencv resize: original image size =  " << image.size() << ", resized image size = " << resized_image.size());
    LOG_INFO("opencv resize: original image size =  " << image.size() << ", resized image size = " << resized_image.size());

    return 0;
}
