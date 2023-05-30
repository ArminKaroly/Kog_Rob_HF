#!/usr/bin/env python

import sys
import time
import math
import rospy
import numpy as np
import cv2, PIL, os
from geometry_msgs.msg import Twist


class Velocity_manager():
    def __init__(self):
        self. current = None
        self.desired = None
        
    def Current_pos_sub(self,msg):
        self.current = msg.data
        print("current_pos")

    def Desired_pos_sub(self,msg):
        self.desired.linear = np.array([-5,5,0])
        self.desired.angular = np.array([0,0,-1.57134755]) 
        print("desired_pos")
        
        
    def Publish_velocities(self):
        if self.current is not None and self.desired is not None:
            pub = rospy.Publisher('/cmd_vel', Twist, queue_size=10)
            rate = rospy.Rate(120)
            vel = Twist()
            
            lin_tav = math.sqrt((self.desired.linear[0]-self.current.linear[0])**2 + (self.desired.linear[0]-self.current.linear[0])**2)  #m value
            
            ang_tav = self.desired.angular[2]-self.current.angular[2]      #rad value
            
            # fütykös sebességek megadása
            
            #vel.linear = np.array([0.1,0,0])
            #vel.angular = Rob_rvecs([0,0,0])
            #print(vel)
            #pub.publish(vel)
            
          
if __name__ == '__main__':  
    rospy.init_node('Vel')
    Vel = Velocity_manager()
    rospy.Subscriber('/Robot_act_pos',Twist, Vel.Current_pos_sub)
    rospy.Subscriber('/Desired_pos',Twist, Vel.Desired_pos_sub)
    rospy.spin()
