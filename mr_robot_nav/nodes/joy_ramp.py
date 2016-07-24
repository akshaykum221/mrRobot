#!/usr/bin/env python

import rospy
from geometry_msgs.msg import Twist
from sensor_msgs.msg import Joy
from ros_arduino_msgs.msg import Analog
import math
from std_msgs.msg import String



def callback(data, twist_pub):
 global g_target_twist, g_last_twist, g_vel_scales
 g_target_twist.angular.z = data.axes[4]
 g_target_twist.linear.x = data.axes[5] * g_vel_scales[1]
 if(data.buttons[2]==1):
  g_vel_scales[0]+=.1
  print "angular range : %.3f" % (g_vel_scales[0])
 if(data.buttons[0]==1):
  g_vel_scales[0]-=.1 
  print "angular range : %.3f" % (g_vel_scales[0])
 if(data.buttons[3]==1):
  g_vel_scales[1]+=.1
  print "linear range : %.3f" % (g_vel_scales[1])
 if(data.buttons[1]==1):
  g_vel_scales[1]-=.1 
  print "linear range : %.3f" % (g_vel_scales[1]) 
 
 if(data.buttons[5]==1):
  g_vel_ramps[0]+=.1
  print "angular accl : %.3f" % (g_vel_ramps[0])
 if(data.buttons[4]==1):
  g_vel_ramps[0]-=.1 
  print "angular accl : %.3f" % (g_vel_ramps[0])
 if(data.buttons[7]==1):
  g_vel_ramps[1]+=.1
  print "linear accl : %.3f" % (g_vel_ramps[1])
 if(data.buttons[6]==1):
  g_vel_ramps[1]-=.1 
  print "linear accl : %.3f" % (g_vel_ramps[1]) 
 
 send_twist(twist_pub)



g_target_twist = None
g_last_twist = None
g_last_send_time = None
g_vel_scales = [1, 0.1] # default to very slow
g_vel_ramps = [0, 1] # units: meters per second^2

def ramped_vel(v_prev, v_target, t_prev, t_now, ramp_rate):
 # compute maximum velocity step
 step = ramp_rate * (t_now - t_prev).to_sec()
 sign = 1 if (v_target > v_prev) else -1
 error = math.fabs(v_target - v_prev)
 if error < step: # we can get there within this timestep. we're done.
  return v_target
 else:
  return v_prev + sign * step # take a step towards the target

def ramped_twist(prev, target, t_prev, t_now, ramps):
 tw = Twist()
 tw.angular.z = g_target_twist.angular.z
 tw.linear.x = ramped_vel(prev.linear.x, target.linear.x, t_prev, t_now, ramps[1])
 return tw

def send_twist(twist_pub):
 global g_last_twist_send_time, g_target_twist, g_last_twist, g_vel_scales, g_vel_ramps
 t_now = rospy.Time.now()
 g_last_twist = ramped_twist(g_last_twist, g_target_twist, g_last_twist_send_time, t_now, g_vel_ramps)
 g_last_twist_send_time = t_now
 twist_pub.publish(g_last_twist)


def fetch_param(name, default):
 if rospy.has_param(name):
  return rospy.get_param(name)
 else:
  print "parameter [%s] not defined. Defaulting to %.3f" % (name, default)
  return default

if __name__ == '__main__':
 rospy.init_node('joystick')
 g_last_twist_send_time = rospy.Time.now()
 twist_pub = rospy.Publisher('cmd_vel', Twist, queue_size=1)
 rospy.Subscriber('joy', Joy, callback, twist_pub)
 g_target_twist = Twist() # initializes to zero
 g_last_twist = Twist() 
 
 rate = rospy.Rate(20)
 while not rospy.is_shutdown():
  send_twist(twist_pub)
  rate.sleep()
