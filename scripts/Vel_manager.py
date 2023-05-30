#!/usr/bin/env python

import sys
import math
import rospy
import numpy as np
import cv2, PIL, os
from os import system, name
from std_msgs.msg import Bool
from geometry_msgs.msg import Twist


def clear():
    # for windows
    if name == 'nt':
        _ = system('cls')
    # for mac and linux(here, os.name is 'posix')
    else:
        _ = system('clear') 


class Velocity_manager():
    def __init__(self,lin_gain,ang_gain,lin_error_gain,maxi_lin_vel,maxi_ang_vel):
        self.desired = None        
        self. current = None
        self.linear_gain = lin_gain
        self.angular_gain = ang_gain
        self.max_lin_vel = maxi_lin_vel
        self.max_ang_vel = maxi_ang_vel
        self.lin_err_gain = lin_error_gain
        self.movement = None
        self.forward = True
        self.wait = False
        self.last_desired = Twist()
        self.last_desired.linear.x = -5.5
        self.last_desired.linear.y = 5.5
        self.last_desired.linear.z = 0
        self.last_desired.angular.x = 0
        self.last_desired.angular.y = 0
        self.last_desired.angular.z = 0
         
    def Wait(self,msg):
        self.wait = msg.data
        pub = rospy.Publisher('/cmd_vel', Twist, queue_size=10)
        rate = rospy.Rate(120)
        vel = Twist()
        if self.wait:
            vel.linear.x = 0
            vel.linear.y = 0
            vel.linear.z = 0
            vel.angular.x = 0
            vel.angular.y = 0
            vel.angular.z = 0                
            pub.publish(vel) 
            clear()
            print(vel)
            
    def Current_pos_sub(self,msg):
        self.current = msg
        #print("CURRENT")
        #print(self.current)
        

    def Desired_pos_sub(self,msg):
        self.desired = msg
        #print("DESIRED")
        #print(self.desired)
        #print("*************************************")
        self.Publish_velocities()
        
    def Publish_velocities(self):
        clear()
        if self.current is not None and self.desired is not None:
            pub = rospy.Publisher('/cmd_vel', Twist, queue_size=10)
            rate = rospy.Rate(120)
            vel = Twist()
                        
            if self.desired.linear.x != self.last_desired.linear.x:
                self.movement = 'x'
                if self.desired.linear.x-self.last_desired.linear.x >= 0:
                    self.forward = True
                else:
                    self.forward = False 
                
            elif self.desired.linear.y != self.last_desired.linear.y:
                self.movement = 'y'
                if self.desired.linear.y-self.last_desired.linear.y <= 0:
                    self.forward = True
                else:
                    self.forward = False 
                
            elif self.desired.angular.z != self.last_desired.angular.z:
                self.movement = 'z'
           
            #print(self.forward)    
            #print(self.movement)
            # Mozgásviszonyhoz sebességek hozzárendelése
            if self.movement == 'x':
                vel.linear.x = (self.desired.linear.x-self.current.linear.x)*self.linear_gain
                sideways_error = self.desired.linear.y-self.current.linear.y
                #print(sideways_error)
                #print(sideways_error * self.lin_err_gain)
                if (np.absolute(sideways_error) > 0.15):
                    vel.angular.z = sideways_error * self.lin_err_gain
                    if self.forward == False:
                        vel.angular.z = -vel.angular.z
                else:
                    vel.angular.z = (self.desired.angular.z-self.current.angular.z)*self.angular_gain*0.5
                
                        
            elif self.movement == 'y':
                vel.linear.x = -(self.desired.linear.y-self.current.linear.y)*self.linear_gain
                sideways_error = self.desired.linear.x-self.current.linear.x
                #print(sideways_error)
                #print(sideways_error * self.lin_err_gain)
                if (np.absolute(sideways_error) > 0.15):
                    vel.angular.z = sideways_error * self.lin_err_gain
                    if self.forward == False:
                        vel.angular.z = -vel.angular.z
                else:
                    vel.angular.z = (self.desired.angular.z-self.current.angular.z)*self.angular_gain*0.5
                
                    
            elif self.movement == 'z':
                vel.linear.x = 0
                vel.angular.z = (self.desired.angular.z-self.current.angular.z) * self.angular_gain 

            if np.absolute(vel.angular.z) > self.max_ang_vel:
                vel.angular.z = np.sign(vel.angular.z) * self.max_ang_vel
        
            if np.absolute(vel.linear.x) > self.max_lin_vel:
                vel.linear.x = np.sign(vel.linear.x) * self.max_lin_vel
            
            vel.linear.y = 0
            vel.linear.z = 0
            vel.angular.x = 0
            vel.angular.y = 0             
                                       
            pub.publish(vel)
            print(vel)
            
            self.last_desired = self.desired
           
            
if __name__ == '__main__':  
    rospy.init_node('Velocities')
    # LIN_GAIN, ANG_GAIN LIN_ERR_GAIN MAX_LIN_VEL MAX_ANG_VEL
    Vel = Velocity_manager(0.75,1,0.5,0.5,0.5)
    rospy.Subscriber('/Wait',Bool, Vel.Wait)
    rospy.Subscriber('/Robot_act_pos',Twist, Vel.Current_pos_sub)
    rospy.Subscriber('/Robot_desired',Twist, Vel.Desired_pos_sub)
    rospy.spin()
