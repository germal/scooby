#!/usr/bin/env python

import rospy
from std_msgs.msg import String
from geometry_msgs.msg import Twist
import pyrebase
import time
import os
import re

def firebase_node():
    rospy.loginfo("Setting Up the Node...")
    rospy.init_node('firebase_node', anonymous=True)

    #--- Create the servo array publisher
    fire_cmd        = Twist()
    ros_pub_fire_cmd = rospy.Publisher("/fire_cmd", Twist, queue_size=10)

    rospy.loginfo("> Publisher corrrectly initialized")
    
    config = {
        "apiKey": "AAAA6BYFJnA:APA91bESUm5sRscZLxe2ey74U4dGHHkqkGXz04SC4xHvzRbPBEGBGm92EMbk9SWcgTv9D_NCHKtXRxXKwfXhNClWyi9JxB6IhnrukG0Vv3rOvhCl7gm0L_aKoIqR21TV7fKr1eNOnMQd",
        "authDomain": "scooby-a36d6.firebaseapp.com",
        "databaseURL": "https://scooby-a36d6-default-rtdb.firebaseio.com/",
        "storageBucket": "scooby-a36d6.appspot.com"
    }

    firebase = pyrebase.initialize_app(config)
    db = firebase.database()
    
    rate = rospy.Rate(10) # 10hz

    #--- Get the last time e got a commands
    last_time_cmd_rcv     = time.time()
    timeout_s             = 3

    while not rospy.is_shutdown():
        user = db.child("cmd_vel").get()
        a = str(user.val())
        b = re.findall(r"[-+]?\d*\.\d+|\d+",a)
        rospy.loginfo(b)
        #print("Linear: "+b[0]+" "+ "Angular: "+b[1])
        #print(float(b[0]))
        if float(b[0]) == 1:
            if(abs(float(b[2])) > 0.1):
                fire_cmd.linear.x = float(b[2])
            else:
                fire_cmd.linear.x = 0.00

            if(abs(float(b[1])) > 0.1):   
                fire_cmd.angular.z = float(b[1])
            else:
                fire_cmd.angular.z = 0.00
        else:
            fire_cmd.linear.x = 0.00
            fire_cmd.angular.z = 0.00

        ros_pub_fire_cmd.publish(fire_cmd)
        rate.sleep()


if __name__ == '__main__':
    try:
        firebase_node()
    except rospy.ROSInterruptException:
        pass
