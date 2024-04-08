Odometry Reset:

ros2 service call /set_pose robot_localization/srv/SetPose "pose:
   header:
     stamp:
       sec: 0
       nanosec: 0
     frame_id: ''
   pose:
     pose:
       position:
         x: 0.0
         y: 0.0

       orientation:
         x: 0.0
         y: 0.0
         z: 0.0
         w: 0.0
     covariance:
     - 0.0
     - 0.0
     - 0.0
     - 0.0
     - 0.0
     - 0.0
     - 0.0
     - 0.0
     - 0.0
     - 0.0
     - 0.0
     - 0.0
     - 0.0
     - 0.0
     - 0.0
     - 0.0
     - 0.0
     - 0.0
     - 0.0
     - 0.0
     - 0.0
     - 0.0
     - 0.0
     - 0.0
     - 0.0
     - 0.0
     - 0.0
     - 0.0
     - 0.0
     - 0.0
     - 0.0
     - 0.0
     - 0.0
     - 0.0
     - 0.0
     - 0.0"
