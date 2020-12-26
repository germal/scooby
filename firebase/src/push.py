#!/usr/bin/env python

import rospy
from std_msgs.msg import String
from geometry_msgs.msg import Twist
import pyrebase
import time

class firebase_push():
    def __init__(self):
        rospy.loginfo("Setting Up the Node...")
        
        rospy.init_node('fire_push')

        #--- Create the Subscriber to Twist commands
        self.ros_sub_twist          = rospy.Subscriber("/joy_teleop/cmd_vel", Twist, self.set_actuators_from_cmdvel)

        config = {
		  "apiKey": "AAAA6BYFJnA:APA91bESUm5sRscZLxe2ey74U4dGHHkqkGXz04SC4xHvzRbPBEGBGm92EMbk9SWcgTv9D_NCHKtXRxXKwfXhNClWyi9JxB6IhnrukG0Vv3rOvhCl7gm0L_aKoIqR21TV7fKr1eNOnMQd",
		  "authDomain": "scooby-a36d6.firebaseapp.com",
		  "databaseURL": "https://scooby-a36d6-default-rtdb.firebaseio.com/",
		  "storageBucket": "scooby-a36d6.appspot.com"
		}

	firebase = pyrebase.initialize_app(config)
	self.db = firebase.database()

        rospy.loginfo("Initialization complete")


    def set_actuators_from_cmdvel(self, message):

        #-- Convert vel into servo values
        #rospy.loginfo("Got a command v = %2.1f  s = %2.1f"%(message.linear.x, message.angular.z))
        data = {"linear": message.linear.x,
				"angular": message.angular.z,
				"status":1.00}
	self.db.child("cmd_vel").update(data)

    @property

    def run(self):

        #--- Set the control rate
        rate = rospy.Rate(2)

        while not rospy.is_shutdown():

            rate.sleep()

if __name__ == "__main__":
    fire_push     = firebase_push()
    fire_push.run()
