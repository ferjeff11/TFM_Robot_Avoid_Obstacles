#!/usr/bin/env python
import rospy
import sys
from geometry_msgs.msg import Twist
from motor_driver import MotorDriver
from std_msgs.msg import String

class RobotMover(object):

    def __init__(self, value_BASE_PWM, value_MULTIPLIER_STANDARD, value_MULTIPLIER_PIVOT, value_simple_mode):
        rospy.Subscriber("cmd_vel", Twist, self.cmd_vel_callback)
        self.pub = rospy.Publisher('cmd_vel_chat', String, queue_size=10)
        self.motor_driver = MotorDriver( i_BASE_PWM=value_BASE_PWM,
                                         i_MULTIPLIER_STANDARD=value_MULTIPLIER_STANDARD,
                                         i_MULTIPLIER_PIVOT=value_MULTIPLIER_PIVOT,
                                         simple_mode=value_simple_mode)


        rospy.loginfo("RobotMover Started...")


    def cmd_vel_callback(self, msg):
        linear_speed = msg.linear.x
        angular_speed = msg.angular.z
        print(linear_speed)
        print(angular_speed)
        # Decide Speed
        self.motor_driver.set_cmd_vel(linear_speed, angular_speed)
        self.pub.publish("w")

    def listener(self):
        rospy.spin()

if __name__ == '__main__':
    rospy.init_node('cmd_vel_listener', anonymous=True)


    value_BASE_PWM = 50
    value_MULTIPLIER_STANDARD = 0.1
    value_MULTIPLIER_PIVOT = 0.1
    value_simple_mode = True

    robot_mover = RobotMover(value_BASE_PWM,
                                 value_MULTIPLIER_STANDARD,
                                 value_MULTIPLIER_PIVOT,
                                 value_simple_mode)
    robot_mover.listener()

