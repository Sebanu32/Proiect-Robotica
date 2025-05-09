#!/usr/bin/env python

import rospy

from std_srvs.srv import Empty,EmptyResponse
from geometry_msgs.msg import Twist

def my_callback(request):
	rospy.loginfo("The service move_tb3_in_circle has been called")
	move_circle.linear.x=0.2
	move_circle.angular.z=0.2
	my_pub.publish(move_circle)
	rospy.loginfo("Finished service move_tb3_in_circle")
	
	
	return EmptyResponse()
	
rospy.init.node('circle')

my_service=rospy.Service('move_tb3_in_circle', Empty, my_callback)
my_pub=rospy.Publisher('robot/cmd_vel',Twist,queue_size=1)
move_circle=Twist()
rospy.loginfo("Service /move_tb3_in_circle_ready")

rospy.spin()
