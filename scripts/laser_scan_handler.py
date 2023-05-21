#/urs/bin/env python
# puts temporary obstacles on map in order to avoit them
import rospy
from sensor_msgs.msg import LaserScan

def laser_callback(msg):
    print('s1 [0]')
    print(msg.ranges[0])

rospy.init_node('laser_scanner')
sub = rospy.Subscriber('scan',LaserScan,laser_callback)

rospy.spin()
