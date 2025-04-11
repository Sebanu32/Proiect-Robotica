#!/usr/bin/env python

import rospy
from sensor_msgs.msg import LaserScan
from geometry_msgs.msg import Twist
from std_msgs.msg import Int32

def callback(data)
	print(data.ranges)

rospy.init_node('Proiect-Robotica')
sub = rospy.Subscriber ('/robot/front_laser/scan', LaserScan, callback)


rospy.spin()
