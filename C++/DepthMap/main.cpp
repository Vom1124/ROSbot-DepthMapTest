#include <stdio.h>
// #include <ppl.h>
#include <opencv4/opencv2/opencv.hpp>
#include <opencv4/opencv2/core.hpp>
#include <opencv4/opencv2/highgui.hpp>
#include <iostream>
#include <thread>
#include <mutex>
#include <vector>

using namespace cv;
using namespace std;

int BLOCK_SIZE=7; //block size for the block matching
int Num_Disparities=16; // number of disparities in the stereo images.

static const int num_threads=8;

mutex mtx; // Mutual Exclusion for locking and unlocking the thread

void my_BM_algo(Mat left_img, Mat right_img, Mat DM, 
                int H, int W, int WS, int scale_adjust, 
                int start_row, int end_row)
{
    for(int i=(start_row); i<(end_row)+BLOCK_SIZE;++i)
    {
        uchar *imDM_i = DM.ptr(i+BLOCK_SIZE);
        for (int j=0+WS; j<W-WS; ++j)
        {
            int prev_SAD=INT_MAX;
            int best_disparity=0;
            for (int k=0; k<Num_Disparities-1; ++k)
            {
                int SAD=0;
                int SAD_tmp=0;
                // Begin Cost Function
                for (int u=0;u<BLOCK_SIZE;++u){
                    for (int v=0; v<BLOCK_SIZE; ++v){
                        SAD_tmp=(left_img.at<uchar>(i+u,j+v)-right_img.at<uchar>(i+u,j+v-k));
                        SAD+=abs(SAD_tmp); 
                    }
                }
                if (SAD<prev_SAD){
                    prev_SAD=SAD;
                    best_disparity=k;
                }
            }
            // mtx.lock();
            imDM_i[j] = best_disparity*scale_adjust;
            // DM->at<uchar>(i,j)=best_disparity*scale_adjust;
            // mtx.unlock();
        }
    }
    // return DM;
}





int main()
{   
    clock_t start_time, end_time;
    Mat left_img = cv::imread("/home/vom/ros2_ws/ROSbot-codes/C++/DepthMap/tsukuba_l.png",IMREAD_GRAYSCALE);
    Mat right_img = cv::imread("/home/vom/ros2_ws/ROSbot-codes/C++/DepthMap/tsukuba_r.png",IMREAD_GRAYSCALE);
    int H = left_img.rows; int W = left_img.cols; // image size
    // imshow("Left Image", left_img);
    // imshow("Right Image",right_img);
    // waitKey();

    Mat DM=Mat(H,W,CV_8UC1);
    Mat resized_DM;
    int WS=BLOCK_SIZE/2;
    int scale_adjust =255/Num_Disparities;
    vector<thread> my_threads;
    int chunk_size = ((H-BLOCK_SIZE)/num_threads);
    start_time=clock();
    thread th1,th2,th3,th4,th5,th6,th7,th8;
     

    for (int i=0; i<num_threads-1; ++i)
    {
        my_threads.push_back(thread(my_BM_algo, left_img, right_img, DM, H, W, WS, scale_adjust, 
                            (i*(chunk_size)), ((i+1)*(chunk_size)) ));    

        // cout<<"thread number: "<<i<<endl;
    }   
    for (auto& th: my_threads)
    {
        th.join();
    }
    
    // thread th1(my_BM_algo, left_img, right_img, DM, H, W, WS, scale_adjust, 
    //                     WS, int(1*H/8)); 
    // thread th2(my_BM_algo, left_img, right_img, DM, H, W, WS, scale_adjust, 
    //                     int(1*H/8), int(2*H/8));              
    // thread th3(my_BM_algo, left_img, right_img, DM, H, W, WS, scale_adjust, 
    //                     int(2*H/8),int(3*H/8)); 
    // thread th4(my_BM_algo, left_img, right_img, DM, H, W, WS, scale_adjust, 
    //                     int(3*H/8),int(4*H/8)); 
    // thread th5(my_BM_algo, left_img, right_img, DM, H, W, WS, scale_adjust, 
    //                     int(4*H/8),int(5*H/8)); 
    // thread th6(my_BM_algo, left_img, right_img, DM, H, W, WS, scale_adjust, 
    //                     int(5*H/8),int(6*H/8)); 
    // thread th7(my_BM_algo, left_img, right_img, DM, H, W, WS, scale_adjust, 
    //                     int(6*H/8),int(7*H/8)); 
    // thread th8(my_BM_algo, left_img, right_img, DM, H, W, WS, scale_adjust, 
    //                     int(7*H/8),int(8*H/8));                                                                                                                                                                                                                                                                        
    // th1.join();
    // th2.join();
    // th3.join();
    // th4.join();
    // th5.join();
    // th6.join();
    // th7.join();
    // th8.join();
    end_time=clock();
    resize(DM, resized_DM, Size(), 2.5, 2.5);
    imshow("Disparity Map", resized_DM);
    
    double time_taken=double(end_time-start_time)/double(CLOCKS_PER_SEC);
    cout<<"The time taken to execute Disparity BM algoithm:"<<fixed<<time_taken<<setprecision(1)<<" seconds"<<endl;
    waitKey();
    return 0;
}
