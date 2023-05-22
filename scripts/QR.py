#!/usr/bin/env python

import sys
import time
import math
import rospy
import numpy as np
import cv2, PIL, os
from cv2 import aruco
from cv_bridge import CvBridge
from sensor_msgs.msg import Image
from std_msgs.msg import Float64MultiArray
from scipy.spatial.transform import Rotation as R
from sensor_msgs.msg import CameraInfo

class Locate_robot:
    def __init__(self):
        self.ids = None
        self.rvecs = None
        self.tvecs = None
        self.image = None
        self.mtx = None
        # Define dictionary and aruco parameters
        self.aruco_dict = aruco.Dictionary_get(aruco.DICT_4X4_1000)
        self.arucoParams = aruco.DetectorParameters_create()
        # Define marker size
        self.markerLength = 200
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
        self.image = bridge.imgmsg_to_cv2(msg, "bgr8")
        gray = cv2.cvtColor(self.image, cv2.COLOR_BGR2GRAY)
        try:
            corners, self.ids, rejectedImgPoints = aruco.detectMarkers(gray, aruco_dict, parameters=arucoParams)
            datas = aruco.estimatePoseSingleMarkers(corners, markerLength , self.mtx, dist)
            self.rvecs=datas[0] # rodiguez formula alapján szögek
            self.tvecs=datas[1] # távok mm-ben megadva (akkor pontos ez a kettő ha a markerLength pontos)
            self.Calculate_robot_pos()
            time.sleep(0.2)
        except:
            print("Cannot detect charuco")
    
    def caminfo_sub(self,msg):
        self.mtx =  msg.K
        
    # a képből megkapott értékek alapján hol vagyunk a robottal (x,y) szerinti elforgatást semminek vesszük mert a robot nem fog eldőlni, a kamerája pedig tökéletesen felfele fog nézni        
    def Calculate_robot_pos(self): # QR code-ok alapján számol pozíciót a robotra azt publish-eli
         if self.rvecs is not None and self.tvecs is not None and self.ids is not None: # ha nincs érték nin értelme számolni
             
             Rob_tvecs = np.array([0,0,0])  # ez lesz majd a robot helyzete
             Rob_rvecs = np.array([0,0,0])
             points = np.genfromtxt('points.csv', delimiter=',') # pontok értékei euler mm-ben kiszedjük
             
             for i in range(len(self.tvecs)):  # végigmegyünk a képből kiszedett pontokon, ezt használva létrehozunk hom koord-okat
                 T = np.append(self.rodrigues_vec_to_rotation_mat(self.rvecs[i,0,:]),np.reshape(self.tvecs[i,0,:],(3,1)),axis = 1)
                 T = np.append(T,np.array([[0,0,0,1]]),axis = 0)
                 
                 T_point = np.append(R.from_euler('xyz',points[self.ids[i],0:3],degrees = True).as_matrix(),np.reshape(points[self.ids[i],3:6],(3,1)),axis = 1)
                 T_points = np.append(T,np.array([[0,0,0,1]]),axis = 0)
                 
                 # számolunk egy inverzet
                 
                 T_rob = np.matmul(T_point,np.linalg.inv(T)) # origó->qrcode->robot   innen a robot helyzete megvan, ezt mentjük, és majd publisheljük
                 
                 Eul_rob = R.from_matrix(T_rob[0:3,0:3]).as_euler('xyz',degrees = True)
                 if Eul_rob[2]<0:
                     Eul_rob[2] = 360+Eul_rob[2]# ne legyen negatív szög
                 Rob_tvecs = Rob_tvecs + np.array([T_rob[0,3],T_rob[1,3],0]) # xy síkban mozgunk a Zben nem tehát 0
                 Rob_rvecs = Rob_rvecs + np.array([0,0,Eul_rob[2]]) # xy síkban mozgunk ezért csak z-ben tud forogni
             
             Rob_tvecs = Rob_tvecs/len(self.tvecs)
             Rob_rvecs = Rob_rvecs/len(self.rvecs)
             # átlagolt értékek publish-olása topicba
             
             pub = rospy.Publisher('/Robot_act_pos_pub', Float64MultiArray, queue_size=10)
             rate = rospy.Rate(120)
             my_msg = Float64MultiArray()
             my_msg.data = np.append(Rob_rvecs,Rob_tvecs).flatten()
             my_msg.layout.data_offset =  0
             pub.publish(my_msg)
             rate.sleep()    
         
# Create CV2 bridge to read images from gazebo
bridge = CvBridge()
# Calibrated parameters in .csv files in /devel
dist = np.zeros(((14,1))) 

# Capture Video (Can be change to video capture from Gazebo) 
if __name__ == '__main__':
    rospy.init_node('QR')
    Robot = Locate_robot()
    rospy.Subscriber('/camera/image', Image, Robot.image_callback)
    rospy.spin()
