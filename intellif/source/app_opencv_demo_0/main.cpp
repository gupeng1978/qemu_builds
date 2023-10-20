#include <opencv2/opencv.hpp>
#include <iostream>

int main() {
    // 创建一个随机的RGB图像（大小为800x800）
    cv::Mat random_image(800, 800, CV_8UC3);
    cv::randu(random_image, cv::Scalar(0,0,0), cv::Scalar(255,255,255));

    // 将图像缩放到400x400
    cv::Mat resized_image;
    // cv::resize(random_image, resized_image, cv::Size(400, 400));

    std::cout << "opencv resize: random_image =  " << random_image.size() << std::endl;

    return 0;
}
