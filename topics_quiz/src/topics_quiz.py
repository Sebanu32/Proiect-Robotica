#!/usr/bin/env python
from sensor_msgs.msg import LaserScan
from geometry_msgs.msg import Twist

rospy.init_node('Proiect-Robotica')
pub = rospy.Publisher('/robot/cmd_vel', Twist, queue_size=1)
sub = rospy.Subscriber('/robot/front_laser/scan', LaserScan, callback)
def callback(data):
	move = Twist()
	fata = data.ranges[]
	stanga = data.ranges[]
	dreapta = data.ranges[]

if fata > 1.0:
	move.linear.x = 0.7
	move.angular.z = 0.0
else
	move.linear.x = 0.0
	move.angular.z = 0.7

if dreapta > 1.0:
	move.linear.x = 0.0
	move.angular.z = 0.7

if stanga > 1.0:
	move.linear.x = 0.0
	move.angular.z = 0.7

pub.publish(move)

rospy.spin()
