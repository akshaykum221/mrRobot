#!/usr/bin/env python

"""
    talkback.py - Say back what is heard by the pocketsphinx recognizer.
"""

import roslib; roslib.load_manifest('pi_speech_tutorial')
import rospy
from std_msgs.msg import String
from ros_arduino_msgs.srv import DigitalWrite
from ros_arduino_msgs.msg import Analog


#to control the robot base
from geometry_msgs.msg import Twist

from sound_play.libsoundplay import SoundClient
import sys 
class TalkBack:
    def __init__(self):
        rospy.on_shutdown(self.cleanup)
          
        self.voice = rospy.get_param("~voice", "voice_cmu_us_bdl_arctic_clunits")
        self.wavepath = rospy.get_param("~wavepath", "")
        
        # Create the sound client object
        self.soundhandle = SoundClient()
        
        rospy.sleep(1)
        self.soundhandle.stopAll()
        
        # Announce that we are ready for input
        self.soundhandle.playWave(self.wavepath + "/R2D2a.wav")
        rospy.sleep(1)
        self.soundhandle.say("How can I help U Sir", self.voice)
        
        rospy.loginfo("Say one of the navigation commands...")
	
        # Subscribe to the recognizer output
        rospy.Subscriber('/recognizer/output', String, self.talkback)

    
	
    def talkback(self, msg):
        # Print the recognized words on the screen
        rospy.loginfo(msg.data)
	twist =Twist()
	
        if msg.data ==  "move left":
         self.soundhandle.say("turning left", self.voice)
	 twist.linear.x = 0; twist.linear.y = 0; twist.linear.z = 0
         twist.angular.x = 0; twist.angular.y = 0; twist.angular.z = 1	
	 pub.publish(twist)
	
        if msg.data == "move right" :
         self.soundhandle.say("turning right", self.voice)
	 twist.linear.x = 0; twist.linear.y = 0; twist.linear.z = 0
         twist.angular.x = 0; twist.angular.y = 0; twist.angular.z = -1	
	 pub.publish(twist)

	if msg.data == "stop" :
         self.soundhandle.say("brakes applied", self.voice)
	 twist.linear.x = 0; twist.linear.y = 0; twist.linear.z = 0
         twist.angular.x = 0; twist.angular.y = 0; twist.angular.z = 0	
	 pub.publish(twist)

	if msg.data == "move back":
         self.soundhandle.say("going back", self.voice)
	 twist.linear.x = -1; twist.linear.y = 0; twist.linear.z = 0
         twist.angular.x = 0; twist.angular.y = 0; twist.angular.z = 0
	 pub.publish(twist)

	if msg.data == "move straight" :
         self.soundhandle.say("going straight", self.voice)
	 twist.linear.x = 1; twist.linear.y = 0; twist.linear.z = 0
         twist.angular.x = 0; twist.angular.y = 0; twist.angular.z = 0	
	 pub.publish(twist)

        if msg.data == "lights on" :
         self.soundhandle.say("lights are on", self.voice)
	 #pin =13
         #value = True
	 #arduino_digi_write(pin,value)

	if msg.data == "lights off" :
         self.soundhandle.say("lights are off", self.voice)
	 #pin =13
         #value = False
	#arduino_digi_write(pin,value)
         	
        elif msg.data == "bring me the glass" :
         self.soundhandle.say("ther are no glasses here", self.voice)
       
       
        
        # Uncomment to play one of the built-in sounds
        #rospy.sleep(2)
        #self.soundhandle.play(5)
        
        # Uncomment to play a wave file
        #rospy.sleep(2)
        #self.soundhandle.playWave(self.wavepath + "/R2D2a.wav")
    def cleanup(self):
        rospy.loginfo("Shutting down talkback node...")

if __name__=="__main__":
    rospy.init_node('talkback')
    try:
        #rospy.wait_for_service('Arduino/digital_write')
	pub = rospy.Publisher('/cmd_vel', Twist,queue_size=1)
        twist =Twist()
	#arduino_digi_write = rospy.ServiceProxy('Arduino/digital_write', DigitalWrite)
        TalkBack()
        rospy.spin()
    except:
        pass

