#!/usr/bin/env python

import rospy
from geometry_msgs.msg import Twist
from square_service_pkg.srv import SquareMovement, SquareMovementResponse
import math

def move_in_circle(radius, speed, repetitions):
    pub = rospy.Publisher('/cmd_vel', Twist, queue_size=10)
    move = Twist()
    rate = rospy.Rate(10)

    angular_velocity = speed / radius

    for _ in range(repetitions):
        move.linear.x = speed
        move.angular.z = angular_velocity

        time_for_one_circle = (2 * math.pi * radius) / speed

        t0 = rospy.Time.now().to_sec()
        while rospy.Time.now().to_sec() - t0 < time_for_one_circle:
            pub.publish(move)
            rate.sleep()

        move.linear.x = 0.0
        move.angular.z = 0.0
        pub.publish(move)
        rospy.sleep(1)

    return True

def handle_circle_request(req):
    speed = 0.2
    success = move_in_circle(req.side, speed, req.repetitions)
    return SquareMovementResponse(success)

def circle_service_server():
    rospy.init_node('circle_service_server')
    service = rospy.Service('/circle_move', SquareMovement, handle_circle_request)
    rospy.loginfo("Service ready to receive circle move commands.")
    rospy.spin()

if __name__ == "__main__":
    circle_service_server()
