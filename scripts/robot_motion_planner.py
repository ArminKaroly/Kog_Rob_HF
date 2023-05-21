#!/usr/bin/env python3
# 
import os
import sys
import time
import math
import rospy
import numpy as np
from std_msgs.msg import Float64MultiArray
from geometry_msgs.msg import Twist
from geometry_msgs.msg import Pose2D

import rospy
try:
    from queue import Queue
except ImportError:
    from Queue import Queue
import threading
import numpy as np

max_speed = 2 #m/s
dest = Pose2D()
curr_pos = Pose2D()
vel = Twist()

class BufferQueue(Queue):
    """Slight modification of the standard Queue that discards the oldest item
    when adding an item and the queue is full.
    """
    def put(self, item, *args, **kwargs):
        # The base implementation, for reference:
        # https://github.com/python/cpython/blob/2.7/Lib/Queue.py#L107
        # https://github.com/python/cpython/blob/3.8/Lib/queue.py#L121
        with self.mutex:
            if self.maxsize > 0 and self._qsize() == self.maxsize:
                self._get()
            self._put(item)
            self.unfinished_tasks += 1
            self.not_empty.notify()
def SetDestination(dest_msg):
    print('new destination set:')
    print(dest_msg.x, dest_msg.y , dest_msg.theta)
    dest=dest_msg

    

def CalcCommanVelocity(odom_msg):
    print (odom_msg.data[0], odom_msg.data[1],odom_msg.data[5])
    curr_pos.x = odom_msg.data[0]
    curr_pos.y = odom_msg.data[1]
    curr_pos.theta = odom_msg.data[5]
    # if current position is not desired position -> move
    dist=math.sqrt((dest.x-curr_pos.x)^2 + (dest.x-curr_pos.x)^2)
    if ( dist > 0.01 or math.abs(curr_pos.theta-dest.theta>0.01)):
        if (curr_pos.theta > dest.theta):
            vel.angular += (curr_pos.theta-dest.theta)*0.1
        if (dist>0.01):
            vel.linear=max_speed*dist*0.5
            if vel.linear>max_speed: vel.linear=max_speed
    #TODO: atgondolni joe ez, obstacle avoidance, forgas speedre is egy maximum lehet kell
        pub.publish(vel)

rospy.init_node('motion_planner')
odom_topic= "/Robot_act_pos_pub"
destination_topic= "/destination"
# Set up your subscriber and define its callback
rospy.Subscriber(odom_topic, Float64MultiArray, CalcCommanVelocity)
rospy.Subscriber(destination_topic, Pose2D, SetDestination)

pub = rospy.Publisher('/cmd_vel', Twist, queue_size=1)

# Start image processing thread


# Spin until Ctrl+C
rospy.spin()