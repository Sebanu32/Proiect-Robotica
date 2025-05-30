#!/usr/bin/env python

import rospy

from turtlebot_move.srv import MoveDirection, MoveDirectionRequest

rospy.init_node('service_mode_direction_client')

rospy.wait_for_service('/move_direction')

move_direction_service_client=rospy.ServiceProxy('/move_direction',MoveDirection)

move_direction_request_object =MoveDirectionRequest()

move_direction_request_object.direction = 'right'

result =move_direction_service_client(move_direction_request_object)

print(result)
