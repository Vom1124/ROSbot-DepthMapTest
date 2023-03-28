# /usr/bin/env python
import rclpy
from rclpy.node import Node
from nav_msgs.msg import Odometry
from geometry_msgs.msg import Twist
from geometry_msgs.msg import Point
from tf_transformations import euler_from_quaternion
from math import atan2
global x
x = 0.0
global y
y = 0.0
global theta
theta = 0.0
class Nav_Test(Node):

        def __init__(self):
                super().__init__("odometery_nav")
                self.get_logger().info("navigation initiated")
                self.nav_pub = self.create_publisher(Twist, '/cmd_vel', 10)
                self.odom_sub = self.create_subscription(Odometry,'/odometry/filtered', self.odom_callback,10)

                self.create_timer(0.75,self.nav_callback)

        def odom_callback(self,msg):
                x = msg.pose.pose.position.x
                y = msg.pose.pose.position.y
                rot_q =  msg.pose.pose.orientation #rotation quaternio
                (roll, pitch, theta) = euler_from_quaternion([rot_q.x, rot_q.y, rot_q.z, rot_q.w]) #yaw=theta here
                self.get_logger().info(  'x= '+str(x) +'  y=  '+str(y)+ '  theta=  ' + str(theta)  )

        def nav_callback(self):
                nav = Twist()

                if x<=0.5:
                        nav.linear.x = 0.1
                else:
                        nav.linear.x = 0.0

                #self.get_logger().info(  'x= '+str(x) +'  y=  '+str(y)+ '  theta=  ' + str(theta)  )
                self.nav_pub.publish(nav)


def main(args=None):
    rclpy.init(args=args)
    node = Nav_Test()
    rclpy.spin(node)
    rclpy.shutdown()

if __name__ == '__main__':
    main()
