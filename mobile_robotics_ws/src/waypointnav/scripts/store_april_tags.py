#!/usr/bin/env python



# TurtleBot must have minimal.launch & amcl_demo.launch
# running prior to starting this script
# For simulation: launch gazebo world & amcl_demo prior to run this script

import rospy
import sys
from move_base_msgs.msg import MoveBaseAction, MoveBaseGoal
import actionlib
from actionlib_msgs.msg import *
from geometry_msgs.msg import Pose, Point, Quaternion
from nav_msgs.msg import OccupancyGrid
#from apriltags_ros.msg import AprilTagDetection
from tf2_msgs.msg import TFMessage
from tf import TransformListener

detected = [False, False, False, False, False, False]
initialrun = True;
tagframe1    = "0"
position = ["0","0","0","0","0","0"]
quaternion = ["0","0","0","0","0","0"]
quaternion_true = {'r1' : 0.000, 'r2' : 0.000, 'r3' : 0.000, 'r4' : 1.000}

curr_pos = {'x': 0, 'y': 0, 'z': 0}

map_data = OccupancyGrid()
   
class GoToPose():
    
    def __init__(self):
        self.tf = TransformListener()
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
    
    #Go to globally saved position num
    def return_to_sender(self, num):
        rospy.loginfo("Go to (%s, %s) pose", position[num]['x'], position[num]['y'])
        success = navigator.goto(position[num], quaternion_true)

        if success:
            rospy.loginfo("Hooray, I reached waypoint %s",num)
        else:
            rospy.loginfo("Shucks, I can't reach waypoint %s",num)

        # Sleep to give the last log messages time to be sent
        rospy.sleep(1)
	return success

    def callback(self,data):

	# rospy.loginfo(data.transforms[0].child_frame_id)
	if data.transforms[0].child_frame_id == 'base_footprint':
	    curr_pos = {'x': data.transforms[0].transform.translation.x, 'y': data.transforms[0].transform.translation.y, 'z': data.transforms[0].transform.translation.z}
	    # rospy.loginfo(curr_pos)

	if sum(detected) == 6:
	    return

        if self.tf.frameExists("/happy_thoughts") and self.tf.frameExists("/map") and detected[0] == False:
            detected[0] = True

            #Get Transform
            tempos, temqua = self.tf.lookupTransform("/map", "/happy_thoughts", self.tf.getLatestCommonTime("/map", "/happy_thoughts"))

            rospy.loginfo("#0")
            position[0] = {'x': tempos[0], 'y': tempos[1], 'z': tempos[2]}
            quaternion[0] = {'r1': temqua[0],'r2': temqua[1],'r3': temqua[2],'r4': temqua[3]}
            rospy.loginfo(position[0])
	    rospy.loginfo(map_data.data[0])
	    # rospy.loginfo(int((position[0]['x'] * 20) + (position[0]['y'] * 20 * map_data['h'])))
	    # rospy.loginfo(map_grid[int((position[0]['x'] * 20 * map_data['w']) + (position[0]['y'] * 20))])
            # rospy.loginfo(quaternion[0])

        if self.tf.frameExists("/fucking_happy_thoughts") and self.tf.frameExists("/map") and detected[1] == False:

            #Get Transform
            tempos, temqua = self.tf.lookupTransform("/map", "/fucking_happy_thoughts", self.tf.getLatestCommonTime("/map", "/fucking_happy_thoughts"))

            rospy.loginfo("#1")
            position[1] = {'x': tempos[0], 'y': tempos[1], 'z': tempos[2]}
            quaternion[0] = {'r1': temqua[0],'r2': temqua[1],'r3': temqua[2],'r4': temqua[3]}
            rospy.loginfo(position[1])
            detected[1] = True

        if self.tf.frameExists("/more_fucking_happy_thoughts") and self.tf.frameExists("/map") and detected[2] == False:

            #Get Transform
            tempos, temqua = self.tf.lookupTransform("/map", "/more_fucking_happy_thoughts", self.tf.getLatestCommonTime("/map", "/more_fucking_happy_thoughts"))

            rospy.loginfo("#2")
            position[2] = {'x': tempos[0], 'y': tempos[1], 'z': tempos[2]}
            quaternion[0] = {'r1': temqua[0],'r2': temqua[1],'r3': temqua[2],'r4': temqua[3]}
            rospy.loginfo(position[2])
            detected[2] = True

        if self.tf.frameExists("/jesus_more_fucking_happy_thoughts") and self.tf.frameExists("/map") and detected[3] == False:

            #Get Transform
            tempos, temqua = self.tf.lookupTransform("/map", "/jesus_more_fucking_happy_thoughts", self.tf.getLatestCommonTime("/map", "/jesus_more_fucking_happy_thoughts"))

            rospy.loginfo("#3")
            position[3] = {'x': tempos[0], 'y': tempos[1], 'z': tempos[2]}
            quaternion[0] = {'r1': temqua[0],'r2': temqua[1],'r3': temqua[2],'r4': temqua[3]}
            rospy.loginfo(position[3])
            detected[3] = True

        if self.tf.frameExists("/fuuuuuuuuuuckkkkkk") and self.tf.frameExists("/map") and detected[4] == False:

            #Get Transform
            tempos, temqua = self.tf.lookupTransform("/map", "/fuuuuuuuuuuckkkkkk", self.tf.getLatestCommonTime("/map", "/fuuuuuuuuuuckkkkkk"))

            rospy.loginfo("#4")
            position[4] = {'x': tempos[0], 'y': tempos[1], 'z': tempos[2]}
            quaternion[0] = {'r1': temqua[0],'r2': temqua[1],'r3': temqua[2],'r4': temqua[3]}
            rospy.loginfo(position[4])
            detected[4] = True

        if self.tf.frameExists("/five") and self.tf.frameExists("/map") and detected[5] == False:

            #Get Transform
            tempos, temqua = self.tf.lookupTransform("/map", "/five",  self.tf.getLatestCommonTime("/map", "/five"))

            rospy.loginfo("#5")
            position[5] = {'x': tempos[0], 'y': tempos[1], 'z': tempos[2]}
            quaternion[0] = {'r1': temqua[0],'r2': temqua[1],'r3': temqua[2],'r4': temqua[3]}
            rospy.loginfo(position[5])
            detected[5] = True

        if sum(detected) == 6:
          rospy.loginfo("youdidit");
          rospy.sleep(1);
          success = self.return_to_sender(0)
          success = self.return_to_sender(1)
          success = self.return_to_sender(2)
          success = self.return_to_sender(3)
          success = self.return_to_sender(4)
          success = self.return_to_sender(5)
          if success:
            rospy.loginfo("Hooray, reached the desired pose")
          else:
            rospy.loginfo("The base failed to reach the desired pose")


    def update_position(self,data):
	global map_data = data
	rospy.loginfo(sys.getsizeof(map_data.data))
	return

    def listener(self):
        global initialrun
        # position = {'x': .5, 'y' : 1}
        # quaternion = {'r1' : 0.000, 'r2' : 0.000, 'r3' : 0.000, 'r4' : 1.000}
        #rospy.init_node('listener', anonymous = True)
        #rospy.sleep(30); #Game plan for now is to map tags in teleop, store coordinates, when all tags hit, sleep, close out of teleop, then begin navigtion routine to all tags.
	rospy.sleep(1);
        rospy.Subscriber('tf',TFMessage,self.callback)
        rospy.Subscriber('map',OccupancyGrid,self.update_position)
        if initialrun == True:
           # success = self.goto(position, quaternion)
            initialrun = False
        rospy.spin()
  

if __name__ == '__main__':
    try:
        rospy.init_node('nav_test', anonymous=False)
        navigator = GoToPose()
        # Customize the following values so they are appropriate for your location
        # position = {'x': .5, 'y' : 1}
        # quaternion = {'r1' : 0.000, 'r2' : 0.000, 'r3' : 0.000, 'r4' : 1.000}
	# rospy.loginfo(Point());
        # rospy.loginfo("Go to (%s, %s) pose", position['x'], position['y'])
	# detected[3] = True
	# detected[4] = True
	# detected[5] = True
        navigator.listener();
        #success = navigator.goto(position, quaternion)

      #  if success:
       #     rospy.loginfo("Hooray, reached the desired pose")
       # else:
        #    rospy.loginfo("The base failed to reach the desired pose")

        # Sleep to give the last log messages time to be sent
      #  rospy.sleep(1)

    except rospy.ROSInterruptException:
        rospy.loginfo("Ctrl-C caught. Quitting")

