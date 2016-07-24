#!/usr/bin/env python

import rospy
from geometry_msgs.msg import Twist
from sensor_msgs.msg import Joy
from ros_arduino_msgs.msg import Analog

def callback(data):
 t = Twist()
 t.linear.x = data.axes[5]; t.linear.y = 0; t.linear.z = 0
 t.angular.x = 0; t.angular.y = 0; t.angular.z = data.axes[4]
 twist_pub.publish(t)  


  
def cleanup(self):
        rospy.loginfo("Shutting down joystick node...")



if __name__ == '__main__':
 rospy.init_node('joystick')
 twist_pub = rospy.Publisher('cmd_vel', Twist, queue_size=1)
 rospy.Subscriber('joy', Joy, callback)
 rospy.spin()
