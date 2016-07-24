#!/usr/bin/env python

import rospy
from geometry_msgs.msg import Twist
from sensor_msgs.msg import Range
from ros_arduino_msgs.msg import Analog
from sound_play.libsoundplay import SoundClient
from std_msgs.msg import String
from sensor_msgs.msg import LaserScan
import sys
 

def scan_callback(msg):
 range_ahead = msg.ranges[len(msg.ranges)/2]
 print "range ahead: %0.1f" % range_ahead

def callback_fc(data):
 global fc
 fcc = data.range
 fc = float(fcc)
 if fc >7.0 :
  twist = Twist()
  twist.linear.x = 0; twist.linear.y = 0; twist.linear.z = 0
  twist.angular.x = 0; twist.angular.y = 0; twist.angular.z = 3
  twist_pub.publish(twist)
  print "front center"

def callback_fl(data):
 global fl
 fll = data.range
 fl = float(fll)
 if fl >7.0 :
  twist = Twist()
  twist.linear.x = 0; twist.linear.y = 0; twist.linear.z = 0
  twist.angular.x = 0; twist.angular.y = 0; twist.angular.z = -1
  twist_pub.publish(twist)
  print "front left"

def callback_fr(data):
 global fr
 frr = data.range
 fr = float(frr)
 if fr >7.0 :
  twist = Twist()
  twist.linear.x = 0; twist.linear.y = 0; twist.linear.z = 0
  twist.angular.x = 0; twist.angular.y = 0; twist.angular.z = 1
  twist_pub.publish(twist)
  print "front right"


def callback_bl(data):
 global bl
 bll = data.range
 bl = float(bll)
 if bl >7.0 :
  twist = Twist()
  twist.linear.x = 0; twist.linear.y = 0; twist.linear.z = 0
  twist.angular.x = 0; twist.angular.y = 0; twist.angular.z = -1
  twist_pub.publish(twist)
  print "back left" 

def callback_br(data):
 global br
 brr = data.range
 br = float(brr)
 if br >7.0 :
  twist = Twist()
  twist.linear.x = 0; twist.linear.y = 0; twist.linear.z = 0
  twist.angular.x = 0; twist.angular.y = 0; twist.angular.z = 1
  twist_pub.publish(twist) 
  print "back right"

rospy.init_node('sensor_nav')
scan_sub = rospy.Subscriber('scan', LaserScan, scan_callback)
rospy.Subscriber('/Arduino/sensor/ir_front_center', Range, callback_fc)
rospy.Subscriber('/Arduino/sensor/ir_front_left', Range, callback_fl)
rospy.Subscriber('/Arduino/sensor/ir_front_right', Range, callback_fr)
rospy.Subscriber('/Arduino/sensor/ir_back_left', Range, callback_bl)
rospy.Subscriber('/Arduino/sensor/ir_back_right', Range, callback_br)
twist_pub = rospy.Publisher('cmd_vel', Twist, queue_size=1)
rospy.spin()
