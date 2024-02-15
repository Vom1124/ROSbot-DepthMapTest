# /usr/bin/env python
import rclpy
from rclpy.node import Node
from nav_msgs.msg import Odometry
from geometry_msgs.msg import Twist
from geometry_msgs.msg import Point
from tf_transformations import euler_from_quaternion
from math import atan2

x = 0.0
y = 0.0
theta = 0.0

class MyController(Node):

        def __init__(self):
                super().__init__("OdometryController")
                self.get_logger().info("Odometry Controller initiated")

                #Create a publisher to publish the velocity commands to reach the destination
                self.odom_pub = self.create_publisher(Twist, '/cmd_vel', 10)

                # Create a  subscriber from the Odometry
                self.odom_sub = self.create_subscription(Odometry, '/odometry/filtered', self.odom_callback, 10)

                # Timer Callback
                self.create_timer(0.25, self.odom_nav)

        def odom_callback(self, msg):

                global x
                global y
                global theta
                x = msg.pose.pose.position.x
                y = msg.pose.pose.position.y

                rot_q =  msg.pose.pose.orientation #rotation quaternion

                (roll, pitch, theta) = euler_from_quaternion([rot_q.x, rot_q.y, rot_q.z, rot_q.w]) #yaw=theta here

        def odom_nav(self):

                nav = Twist()#navigation to orient the goal orientation
                #self.get_logger().info("This loop started  " + "x=  " + str(x) + "  y=  " + str(y) )
                goal = Point()
                goal.x = 1.0
                goal.y = 0.5

                inc_x = goal.x - x
                inc_y = goal.y - y
                angle_to_goal = atan2(inc_y, inc_x)

                        #Checking to see the current pose == goal pose
                if abs(angle_to_goal - theta)>0.1:
                        nav.linear.x = 0.0
                        nav.angular.z = 0.0

                else:
                        nav.linear.x = 0.0
                        nav.angular.z = 0.0

                self.get_logger().info("The current pose  " + str(theta) + " "  + "  The goal pose " + str(angle_to_goal))
                #Publishing the velocity command
                self.odom_pub.publish(nav)

def main(args=None):
    rclpy.init(args=args)
    node = MyController()
    rclpy.spin(node)
    rclpy.shutdown()

if __name__ == '__main__':
    main()

