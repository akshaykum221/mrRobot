#!/usr/bin/env python

"""
    talkback.py - Say back what is heard by the pocketsphinx recognizer.
"""

import roslib; roslib.load_manifest('pi_speech_tutorial')
import rospy
from std_msgs.msg import String
from geometry_msgs.msg import Twist
import datetime




from sound_play.libsoundplay import SoundClient
import sys 

class TimeInWords2():
    def __init__(self):
        self.words=["one", "two", "three", "four", "five", "six", "seven", "eight","nine", 
       "ten", "eleven", "twelve", "thirteen", "fourteen", "quarter", "sixteen",
       "seventeen", "eighteen", "nineteen", "twenty", "twenty one", 
       "twenty two", "twenty three", "twenty four", "twenty five", 
       "twenty six", "twenty seven", "twenty eight", "twenty nine", "half"]
         
    def caltime(self):
        dd=datetime.datetime.now()
        hrs = dd.hour
        mins = dd.minute
        header="It is "
        msg=""
        if (hrs >12):
            hrs=hrs-12
        if (mins == 0):
            hr = self.words[hrs-1]
            msg=header + hr + " o'clock."
        elif (mins < 31):      
               hr = self.words[hrs-1]
               mn = self.words[mins-1]
               msg = header + mn + " past " + hr + "."
        else:
            hr = self.words[hrs]
            mn =self.words[(60 - mins-1)]
            msg = header + mn + " to " + hr + "."
        return msg
 
class TalkBack:
    def __init__(self):
        rospy.on_shutdown(self.cleanup)
          
        self.voice = rospy.get_param("~voice", "voice_cmu_us_bdl_arctic_clunits")
        self.wavepath = rospy.get_param("~wavepath", "")
        
        # Create the sound client object
        self.soundhandle = SoundClient()
        
        rospy.sleep(1)
        self.soundhandle.stopAll()

        	
        # Subscribe to the recognizer output
        rospy.Subscriber('/recognizer/output', String, self.talkback)

    
	
    def talkback(self, msg):
        # Print the recognized words on the screen
        rospy.loginfo(msg.data)
	twist =Twist()
	
        if msg.data ==  "left":
         #self.soundhandle.say("turning left", self.voice)
	 twist.linear.x = 0; twist.linear.y = 0; twist.linear.z = 0
         twist.angular.x = 0; twist.angular.y = 0; twist.angular.z = 1	
	 pub.publish(twist)
	
        if msg.data == "right" :
         #self.soundhandle.say("turning right", self.voice)
	 twist.linear.x = 0; twist.linear.y = 0; twist.linear.z = 0
         twist.angular.x = 0; twist.angular.y = 0; twist.angular.z = -1	
	 pub.publish(twist)

	if msg.data == "stop" :
         #self.soundhandle.say("brakes applied", self.voice)
	 twist.linear.x = 0; twist.linear.y = 0; twist.linear.z = 0
         twist.angular.x = 0; twist.angular.y = 0; twist.angular.z = 0	
	 pub.publish(twist)

	if msg.data == "back":
         #self.soundhandle.say("going back", self.voice)
	 twist.linear.x = -1; twist.linear.y = 0; twist.linear.z = 0
         twist.angular.x = 0; twist.angular.y = 0; twist.angular.z = 0
	 pub.publish(twist)

	if msg.data == "forward" :
         #self.soundhandle.say("going straight", self.voice)
	 twist.linear.x = 1; twist.linear.y = 0; twist.linear.z = 0
         twist.angular.x = 0; twist.angular.y = 0; twist.angular.z = 0	
	 pub.publish(twist)
	
         	
        
        elif msg.data == "what time is it" :
         self.soundhandle.say("the time is " , self.voice)
	 t = TimeInWords2()
    	 self.soundhandle.say(t.caltime(), self.voice)
           
        
    def cleanup(self):
        rospy.loginfo("Shutting down talkback node...")

if __name__=="__main__":
    rospy.init_node('talkback')
    try:
        pub = rospy.Publisher('/cmd_vel', Twist,queue_size=1)
        twist =Twist()
        TalkBack()
        rospy.spin()
    except:
        pass

