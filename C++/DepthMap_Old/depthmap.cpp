
// #include <opencv2/opencv.hpp>
// #include <opencv2/core.hpp>
#include <opencv2/highgui.hpp>
#include <iostream>

using namespace cv;
using namespace std;

int main()
{
    cv::Mat image_L; 
    cv::Mat image_R;
    image_L = cv::imread("./tsukuba_l.png",IMREAD_GRAYSCALE);
    image_R = cv::imread("./tsukuba_r.png",IMREAD_GRAYSCALE);
    cv::imshow("Left Image", image_L);
    cv::imshow("Right Image", image_R);
    waitKey(0);

    std::cout << "test run" << std::endl;
    return 0;
}

// int compare_blocks(const int row, const int column, const int width, const int height,
//                 const Mat *left_img, const Mat *right_img)
//                 {
//                 return 0;
//                 }