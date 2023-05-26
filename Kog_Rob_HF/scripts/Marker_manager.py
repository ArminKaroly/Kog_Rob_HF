#!/usr/bin/env python

import sys
import time
import math
import rospy
import numpy as np
import cv2, PIL, os
from cv2 import aruco
from os import system, name
from cv_bridge import CvBridge
from sensor_msgs.msg import Image
from geometry_msgs.msg import Twist
from matplotlib import pyplot as plt
from scipy.spatial.transform import Rotation as R
from sensor_msgs.msg import CameraInfo


def clear():
    # for windows
    if name == 'nt':
        _ = system('cls')
    # for mac and linux(here, os.name is 'posix')
    else:
        _ = system('clear') 

class Markers:
    def __init__(self):
        self.markers=[]

    def markers_build(self):
        for y in range(9):
            for x in range(9):
                self.markers.append([-4+x,-2+y,2.5,-math.sqrt(2)/2,math.sqrt(2)/2,0,0])
        
        self.markers.append([-5,5,2.5,-math.sqrt(2)/2,math.sqrt(2)/2,0,0])
        self.markers.append([-6,5,2.5,-math.sqrt(2)/2,math.sqrt(2)/2,0,0])
        self.markers.append([-5,6,2.5,-math.sqrt(2)/2,math.sqrt(2)/2,0,0])
        self.markers.append([-6,6,2.5,-math.sqrt(2)/2,math.sqrt(2)/2,0,0])
    
    def markers_array(self):
        self.markers_build()
        return self.markers
      
class Locate_robot:
    def __init__(self,ar_dict,ar_param):
        self.ids = None
        self.rvecs = None
        self.tvecs = None
        self.image = None
        self.mtx = None
        # Define dictionary and aruco parameters
        self.aruco_dict = ar_dict
        self.arucoParams = ar_param 
        # Define marker size
        self.markerLength = 0.5
        rospy.Subscriber('/camera/camera_info', CameraInfo, self.caminfo_sub)
    # rodriguaez értékek mátrixba konvertálása    
    def rodrigues_vec_to_rotation_mat(self,rodrigues_vec):
        theta = np.linalg.norm(rodrigues_vec)
        if theta < sys.float_info.epsilon:              
            rotation_mat = np.eye(3, dtype=float)
        else:
            r = rodrigues_vec / theta
            I = np.eye(3, dtype=float)
            r_rT = np.array([
                [r[0]*r[0], r[0]*r[1], r[0]*r[2]],
                [r[1]*r[0], r[1]*r[1], r[1]*r[2]],
                [r[2]*r[0], r[2]*r[1], r[2]*r[2]]
            ])
            r_cross = np.array([
                [0, -r[2], r[1]],
                [r[2], 0, -r[0]],
                [-r[1], r[0], 0]
            ])
            rotation_mat = math.cos(theta) * I + (1 - math.cos(theta)) * r_rT + math.sin(theta) * r_cross
        return rotation_mat
    
    # kép feldologozás értékek kimentése a self.rvecs, és self.tvecs-be robot koord rendszerben hol a qrcode
    def image_callback(self,msg):
      if self.mtx is not None:
        self.image = bridge.imgmsg_to_cv2(msg, "bgr8")
        gray = cv2.cvtColor(self.image, cv2.COLOR_BGR2GRAY)
        if True:
            corners, self.ids, rejectedImgPoints = aruco.detectMarkers(gray, self.aruco_dict, parameters=self.arucoParams)
            datas = aruco.estimatePoseSingleMarkers(corners, self.markerLength , self.mtx, np.zeros((12)))
            self.rvecs=datas[0] # rodiguez formula alapján szögek
            self.tvecs=datas[1] # távok mm-ben megadva (akkor pontos ez a kettő ha a markerLength pontos)
            self.Calculate_robot_pos()
        #except:
        #    print("Cannot detect charuco")
    
    def caminfo_sub(self,msg):
        if self.mtx is None:
            self.mtx =  np.reshape(msg.K,(3,3))
        
    # a képből megkapott értékek alapján hol vagyunk a robottal (x,y) szerinti elforgatást semminek vesszük mert a robot nem fog eldőlni, a kamerája pedig tökéletesen felfele fog nézni        
    def Calculate_robot_pos(self): # QR code-ok alapján számol pozíciót a robotra azt publish-eli
         if self.rvecs is not None and self.tvecs is not None and self.ids is not None: # ha nincs érték nin értelme számolni
             clear()
             Rob_tvecs = np.array([0,0,0])  # ez lesz majd a robot helyzete
             Rob_rvecs = np.array([0,0,0])
                         
             for i in range(len(self.tvecs)):  # végigmegyünk a képből kiszedett pontokon, ezt használva létrehozunk hom koord-okat
                 T = np.append(self.rodrigues_vec_to_rotation_mat(self.rvecs[i,0,:]),np.reshape(self.tvecs[i,0,:],(3,1)),axis = 1)
                 T = np.append(T,np.array([[0,0,0,1]]),axis = 0)                 
                                                  
                 T_point = np.append(R.from_quat(markers[self.ids[i].item()][3:7]).as_matrix(),np.reshape(markers[self.ids[i].item()][0:3],(3,1)),axis = 1)
                 
                 T_point = np.append(T_point,np.array([[0,0,0,1]]),axis = 0)
                 
                 # számolunk egy inverzet
                 T_rob = np.matmul(T_point,np.linalg.inv(T)) # origó->qrcode->robot   innen a robot helyzete megvan, ezt mentjük, és majd publisheljük
                 
                 Eul_rob = R.from_matrix(T_rob[0:3,0:3]).as_euler('xyz',degrees = False)
                 
                 Rob_tvecs = Rob_tvecs + np.array([T_rob[0,3],T_rob[1,3],0]) # xy síkban mozgunk a Zben nem tehát 0
                 Rob_rvecs = Rob_rvecs + np.array([0,0,Eul_rob[2]]) # xy síkban mozgunk ezért csak z-ben tud forogni
             
             Rob_tvecs = Rob_tvecs/len(self.tvecs)
             Rob_rvecs = Rob_rvecs/len(self.rvecs)
             
             # átlagolt értékek publish-olása topicba
           
             pub = rospy.Publisher('/Robot_act_pos', Twist, queue_size=10)
             rate = rospy.Rate(120)
             my_msg = Twist()
             my_msg.linear.x = Rob_tvecs[0]
             my_msg.linear.y = Rob_tvecs[1]
             my_msg.linear.z = Rob_tvecs[2]
             my_msg.angular.x = Rob_rvecs[0]
             my_msg.angular.y = Rob_rvecs[1]
             my_msg.angular.z = Rob_rvecs[2]
             print("Cafebot aktuális pozíciója:")
             print(my_msg)
             pub.publish(my_msg) 
             


bridge = CvBridge()
 
if __name__ == '__main__':
    ar_dict = aruco.Dictionary_get(aruco.DICT_4X4_100)
    ar_param = aruco.DetectorParameters_create()
    marker=Markers()
    markers = marker.markers_array()  
    rospy.init_node('QR')
    Robot = Locate_robot(ar_dict,ar_param)
    rospy.Subscriber('/camera/image', Image, Robot.image_callback)
    
    rospy.spin()
