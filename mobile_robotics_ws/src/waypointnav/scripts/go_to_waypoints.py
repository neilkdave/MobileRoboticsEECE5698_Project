#!/usr/bin/env python

# TurtleBot must have minimal.launch & amcl_demo.launch
# running prior to starting this script
# For simulation: launch gazebo world & amcl_demo prior to run this script

import rospy
from move_base_msgs.msg import MoveBaseAction, MoveBaseGoal
import actionlib
from actionlib_msgs.msg import *
from geometry_msgs.msg import Pose, Point, Quaternion

class GoToPose():
    def __init__(self):

        self.goal_sent = False

	# What to do if shut down (e.g. Ctrl-C or failure)
	rospy.on_shutdown(self.shutdown)
	
	# Tell the action client that we want to spin a thread by default
	self.move_base = actionlib.SimpleActionClient("move_base", MoveBaseAction)
	rospy.loginfo("Wait for the action server to come up")

	# Allow up to 5 seconds for the action server to come up
	self.move_base.wait_for_server(rospy.Duration(5))

    def goto(self, pos, quat):

        # Send a goal
        self.goal_sent = True
	goal = MoveBaseGoal()
	goal.target_pose.header.frame_id = 'map'
	goal.target_pose.header.stamp = rospy.Time.now()
        goal.target_pose.pose = Pose(Point(pos['x'], pos['y'], 0.000),
                                     Quaternion(quat['r1'], quat['r2'], quat['r3'], quat['r4']))

	# Start moving
        self.move_base.send_goal(goal)

	# Allow TurtleBot up to 60 seconds to complete task
	success = self.move_base.wait_for_result(rospy.Duration(60)) 

        state = self.move_base.get_state()
        result = False

        if success and state == GoalStatus.SUCCEEDED:
            # We made it!
            result = True
        else:
            self.move_base.cancel_goal()

        self.goal_sent = False
        return result

    def shutdown(self):
        if self.goal_sent:
            self.move_base.cancel_goal()
        rospy.loginfo("Stop")
        rospy.sleep(1)

if __name__ == '__main__':
    try:
        rospy.init_node('waypointnav_simple', anonymous=False)

        # Customize the following values so they are appropriate for your location
	# x_wp1 = float(raw_input("Please enter x value: "))
	# y_wp1 = float(raw_input("Please enter y value: "))
        # position = {'x': x_wp1, 'y' : y_wp1}
########################################################### 1
        navigator = GoToPose()
	position = {'x': 1, 'y' : 0}
        quaternion = {'r1' : 0.000, 'r2' : 0.000, 'r3' : 0.000, 'r4' : 1.000}

        rospy.loginfo("Go to (%s, %s) pose", position['x'], position['y'])
        success = navigator.goto(position, quaternion)

        if success:
            rospy.loginfo("Hooray, I reached the 1st waypoint")
        else:
            rospy.loginfo("Shucks, I can't reach the 1st waypoint")

        # Sleep to give the last log messages time to be sent
        rospy.sleep(1)

########################################################### 2
        position = {'x': 1, 'y' : -1}
        quaternion = {'r1' : 0.000, 'r2' : 0.000, 'r3' : 0.000, 'r4' : 1.000}

        rospy.loginfo("Go to (%s, %s) pose", position['x'], position['y'])
        success = navigator.goto(position, quaternion)

        if success:
            rospy.loginfo("Hooray, I reached the 2nd waypoint")
        else:
            rospy.loginfo("Shucks, I can't reach the 2nd waypoint")

        # Sleep to give the last log messages time to be sent
        rospy.sleep(1)

########################################################### 3
        position = {'x': 2, 'y' : -1}
        quaternion = {'r1' : 0.000, 'r2' : 0.000, 'r3' : 0.000, 'r4' : 1.000}

        rospy.loginfo("Go to (%s, %s) pose", position['x'], position['y'])
        success = navigator.goto(position, quaternion)

        if success:
            rospy.loginfo("Hooray, I reached the 3rd waypoint")
        else:
            rospy.loginfo("Shucks, I can't reach the 3rd waypoint")

        # Sleep to give the last log messages time to be sent
        rospy.sleep(1)

########################################################### 4
        position = {'x': 2, 'y' : -2}
        quaternion = {'r1' : 0.000, 'r2' : 0.000, 'r3' : 0.000, 'r4' : 1.000}

        rospy.loginfo("Go to (%s, %s) pose", position['x'], position['y'])
        success = navigator.goto(position, quaternion)

        if success:
            rospy.loginfo("Hooray, I reached the 4th waypoint")
        else:
		position = {'x': 1, 'y' : -2}
		navigator.goto(position, quaternion)
        	rospy.loginfo("Shucks, I can't reach the 4th waypoint")

        # Sleep to give the last log messages time to be sent
        rospy.sleep(1)

########################################################### 5
	position = {'x': 3, 'y' : -2}
        quaternion = {'r1' : 0.000, 'r2' : 0.000, 'r3' : 0.000, 'r4' : 1.000}

        rospy.loginfo("Go to (%s, %s) pose", position['x'], position['y'])
        success = navigator.goto(position, quaternion)

        if success:
            rospy.loginfo("Hooray, I reached the 5th waypoint")
        else:
		rospy.loginfo("Shucks, I can't reach the 5th waypoint")

        # Sleep to give the last log messages time to be sent
        rospy.sleep(1)


########################################################### Home
	position = {'x': 0, 'y' : 0}
        quaternion = {'r1' : 0.000, 'r2' : 0.000, 'r3' : 0.000, 'r4' : 1.000}

        rospy.loginfo("Go to (%s, %s) pose", position['x'], position['y'])
        success = navigator.goto(position, quaternion)

        if success:
            rospy.loginfo("Hooray, I went home")
        else:
            rospy.loginfo("Shucks, I can't go home")

        # Sleep to give the last log messages time to be sent
        rospy.sleep(1)

    except rospy.ROSInterruptException:
        rospy.loginfo("Ctrl-C caught. Quitting")

