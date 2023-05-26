#!/usr/bin/env python

import sys
import time
import math
import rospy
import numpy as np
import cv2, PIL, os
from os import system, name
from geometry_msgs.msg import Twist
    
def clear():
    # for windows
    if name == 'nt':
        _ = system('cls')
    # for mac and linux(here, os.name is 'posix')
    else:
        _ = system('clear')     
    
  
class Service_manager():
    def __init__(self,lin_err,ang_err,Act_tab_draw):
        self.current = None
        self.orders = None
        self.path_index = 1
        self.path_index_memory = 0
        self.forward = True
        self.arrive_back = True
        self.lin_error = lin_err
        self.ang_error = ang_err
        self.Actual_table_drawing = Act_tab_draw 
        print("Az asztalok számozása!")
        print("______________________")
        print("  [5]  [1]  \n  [6]  [2]  \n  [7]  [3]  \n  [8]  [4]\n              *\n") 
        print("*: Cafebot készenléti pozíciója.")
        print("________________________________")
        print("Aktuálisan az asztalok állapota:")
        print(self.Actual_table_drawing)
        print("________________________________")
                
    def Table_drawer(self,table_number):
            if table_number == 1 and self.Actual_table_drawing[8]==" ": 
                self.Actual_table_drawing = self.Actual_table_drawing[:8]+"o"+self.Actual_table_drawing[9:]
            elif table_number == 1 and self.Actual_table_drawing[8]=="o":
                self.Actual_table_drawing = self.Actual_table_drawing[:8]+" "+self.Actual_table_drawing[9:]
            if table_number == 2 and self.Actual_table_drawing[21]==" ": 
                self.Actual_table_drawing = self.Actual_table_drawing[:21]+"o"+self.Actual_table_drawing[22:]
            elif table_number == 2 and self.Actual_table_drawing[21]=="o":
                self.Actual_table_drawing = self.Actual_table_drawing[:21]+" "+self.Actual_table_drawing[22:]
            if table_number == 3 and self.Actual_table_drawing[34]==" ": 
                self.Actual_table_drawing = self.Actual_table_drawing[:34]+"o"+self.Actual_table_drawing[35:]
            elif table_number == 3 and self.Actual_table_drawing[34]=="o":
                self.Actual_table_drawing = self.Actual_table_drawing[:34]+" "+self.Actual_table_drawing[35:]
            if table_number == 4 and self.Actual_table_drawing[47]==" ": 
                self.Actual_table_drawing = self.Actual_table_drawing[:47]+"o"+self.Actual_table_drawing[48:]
            elif table_number == 4 and self.Actual_table_drawing[47]=="o":
                self.Actual_table_drawing = self.Actual_table_drawing[:47]+" "+self.Actual_table_drawing[48:]
            if table_number == 5 and self.Actual_table_drawing[3]==" ": 
                self.Actual_table_drawing = self.Actual_table_drawing[:3]+"o"+self.Actual_table_drawing[4:]
            elif table_number == 5 and self.Actual_table_drawing[3]=="o":
                self.Actual_table_drawing = self.Actual_table_drawing[:3]+" "+self.Actual_table_drawing[4:]
            if table_number == 6 and self.Actual_table_drawing[16]==" ": 
                self.Actual_table_drawing = self.Actual_table_drawing[:16]+"o"+self.Actual_table_drawing[17:]
            elif table_number == 6 and self.Actual_table_drawing[16]=="o":
                self.Actual_table_drawing = self.Actual_table_drawing[:16]+" "+self.Actual_table_drawing[17:]
            if table_number == 7 and self.Actual_table_drawing[29]==" ": 
                self.Actual_table_drawing = self.Actual_table_drawing[:29]+"o"+self.Actual_table_drawing[30:]
            elif table_number == 7 and self.Actual_table_drawing[29]=="o":
                self.Actual_table_drawing = self.Actual_table_drawing[:29]+" "+self.Actual_table_drawing[30:]
            if table_number == 8 and self.Actual_table_drawing[42]==" ": 
                self.Actual_table_drawing = self.Actual_table_drawing[:42]+"o"+self.Actual_table_drawing[43:]
            elif table_number == 8 and self.Actual_table_drawing[42]=="o":
                self.Actual_table_drawing = self.Actual_table_drawing[:42]+" "+self.Actual_table_drawing[43:]
           
            print(self.Actual_table_drawing)
                
    def User_Interface(self):
        input("Nyomj Enter-t a következő kiszolgálás megadásához!")
        clear()
        print("Az asztalok számozása!")
        print("______________________")
        print("  [5]  [1]  \n  [6]  [2]  \n  [7]  [3]  \n  [8]  [4]\n              *\n") 
        print("*: Cafebot készenléti pozíciója.")
        print("________________________________")
        print("Aktuálisan az asztalok állapota:")
        print(self.Actual_table_drawing)
        print("________________________________")
        try:
            table_num = int(input("Kiszolgálandó asztal száma: ")) 
            print("____________________________") 
            if table_num <= 8 and table_num >=1:    
                print("Új asztalok állapota:")
                self.Table_drawer(table_num)
                print("____________________________") 
                self.orders = table_num-1
                self.arrive_back = False
            else:
                print("Érvénytelen értéket adott meg!")                       
        except:
           print("Számértéket adjon meg (int 1-8)!")
    
    def Current_pos(self,msg):
        self.current = msg
        if self.arrive_back:
            print("Cafebot használható!")
            self.orders = None
            self.User_Interface()
        else:
            clear() 
            print("Cafebot használatban van!")
            self.Pub_desired_pos() 
             
            
    def Check_table(self):
        lin_dist = math.sqrt((Routes[5,0,self.orders]-self.current.linear.x)**2+(Routes[5,1,self.orders]-self.current.linear.y)**2)
        ang_dist = math.sqrt((Routes[5,2,self.orders]-self.current.angular.z)**2)
        if lin_dist <= self.lin_error and ang_dist <= self.ang_error and self.path_index == 5:
            print("Cafebot megérkezett az asztalhoz!")
            time.sleep(7.5)
            
    def Check_home(self):
        lin_dist = math.sqrt((Routes[0,0,0]-self.current.linear.x)**2+(Routes[0,1,0]-self.current.linear.y)**2)
        ang_dist = math.sqrt((Routes[0,2,0]-self.current.angular.z)**2)
        if lin_dist <= self.lin_error and ang_dist <= self.ang_error and self.path_index == 0:
            self.arrive_back = True
            clear()
        
    def Check_forward(self):
        lin_dist = math.sqrt((Routes[self.path_index,0,self.orders]-self.current.linear.x)**2+(Routes[self.path_index,1,self.orders]-self.current.linear.y)**2)
        ang_dist = math.sqrt((Routes[self.path_index,2,self.orders]-self.current.angular.z)**2)
        if lin_dist <= self.lin_error and ang_dist <= self.ang_error:
            self.path_index = self.path_index +  1
    
    def Check_backward(self):
        lin_dist = math.sqrt((Routes[self.path_index,0,self.orders]-self.current.linear.x)**2+(Routes[self.path_index,1,self.orders]-self.current.linear.y)**2)
        ang_dist = math.sqrt((Routes[self.path_index,2,self.orders]-self.current.angular.z)**2)
        if lin_dist <= self.lin_error and ang_dist <= self.ang_error:
            self.path_index = self.path_index - 1
        
        
    def Pub_desired_pos(self):            
         if self.Current_pos is not None and self.orders is not None:
             self.Check_home()
             self.Check_table()
             
             if self.path_index == 0:
                 self.forward = True
             if self.path_index == 5:
                 self.forward = False

             if self.forward:
                 self.Check_forward()
             else:
                 self.Check_backward()          

             pub = rospy.Publisher('/Robot_desired', Twist, queue_size=10)
             rate = rospy.Rate(120)
             my_msg0 = Twist()
             my_msg0.linear.x = Routes[self.path_index,0,self.orders]
             my_msg0.linear.y = Routes[self.path_index,1,self.orders]
             my_msg0.linear.z = 0
             my_msg0.angular.x = 0
             my_msg0.angular.y = 0
             my_msg0.angular.z = Routes[self.path_index,2,self.orders]             
             pub.publish(my_msg0)
             print("Cafebot következő útvonalbeli pontja:")
             print(my_msg0)
             
      

if __name__ == '__main__':
    Routes = np.zeros((6,3,8))
    for i in range(0,4):
       Route =  np.array([[-5.5,5.5,-np.pi/2],[-3.5,5.5,-np.pi/2],[-3.5,5.5,-np.pi],[-3.5,-1.5+2*i,-np.pi],[-3.5,-1.5+2*i,-np.pi/2],[-2.5,-1.5+2*i,-np.pi/2]])
       Routes[:,:,i] = Route 
    for i in range(0,4):  
        Route = np.array([[-5.5,5.5,-np.pi/2],[3.5,5.5,-np.pi/2],[3.5,5.5,-np.pi],[3.5,-1.5+2*i,-np.pi],[3.5,-1.5+2*i,np.pi/2],[2.5,-1.5+2*i,np.pi/2]])  
        Routes[:,:,i+4] = Route
    Actual_table_drawing = "  [ ]  [ ]  \n  [ ]  [ ]  \n  [ ]  [ ]  \n  [ ]  [ ]\n              *\n"     
    
    rospy.init_node('Service')
    Ser = Service_manager(0.5,0.5,Actual_table_drawing)    
    rospy.Subscriber('/Robot_act_pos', Twist, Ser.Current_pos)
    rospy.spin()
    
