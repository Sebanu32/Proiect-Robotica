#!/usr/bin/env python

import rospy
import actionlib
from std_msgs.msg import Empty
from geometry_msgs.msg import Twist
import time

from ardrone_as.msg import ArdroneAction, ArdroneGoal, ArdroneResult, ArdroneFeedback

class ArdoneControlServer:
    def __init__(self):
        rospy.init_node('ardone_control_server_takeoff_only')

        self.takeoff_pub = rospy.Publisher('/ardrone/takeoff', Empty, queue_size=1)
        self.cmd_vel_pub = rospy.Publisher('/cmd_vel', Twist, queue_size=1)

        self._as = actionlib.SimpleActionServer(
            'ardone_control',
            ArdoneControlAction,
            execute_cb=self.execute_callback,
            auto_start=False
        )
        self._as.start()
        rospy.loginfo("Ardrone Control Action Server (TAKEOFF Only) started.")

        self.current_drone_state = "LANDED"
        self.feedback_rate = rospy.Rate(1)

    def execute_callback(self, goal):
        feedback = ArdoneControlFeedback()
        result = ArdoneControlResult()

        if goal.command == "TAKEOFF":
            if self.current_drone_state == "LANDED":
                self.takeoff_pub.publish(Empty())
                rospy.sleep(3)
                self.current_drone_state = "TAKEN_OFF"
                rospy.loginfo("Drone has taken off in Gazebo.")

                while not rospy.is_shutdown() and self.current_drone_state == "TAKEN_OFF":
                    if self._as.is_preempt_requested():
                        self._as.set_preempted()
                        rospy.loginfo("TAKEOFF action preempted.")
                        return

                    self.cmd_vel_pub.publish(Twist())
                    feedback.status = "Drone is in TAKEN_OFF state, hovering."
                    self._as.publish_feedback(feedback)
                    self.feedback_rate.sleep()
                
                if self.current_drone_state == "TAKEN_OFF":
                    self._as.set_succeeded(result)
                    rospy.loginfo("TAKEOFF action succeeded (drone will remain hovering until node shutdown).")

            else:
                feedback.status = f"Cannot TAKEOFF. Drone is already {self.current_drone_state}."
                self._as.publish_feedback(feedback)
                self._as.set_aborted(result, "Drone not in LANDED state for TAKEOFF.")
        else:
            feedback.status = f"Unknown command: {goal.command}. Only TAKEOFF is supported."
            self._as.publish_feedback(feedback)
            self._as.set_aborted(result, "Invalid command received. Only TAKEOFF is supported.")

if __name__ == '__main__':
    try:
        server = ArdoneControlServer()
        rospy.spin()
    except rospy.ROSInterruptException:
        pass
