#!/usr/bin/env python



# TurtleBot must have minimal.launch & amcl_demo.launch
# running prior to starting this script
# For simulation: launch gazebo world & amcl_demo prior to run this script

import rospy
from move_base_msgs.msg import MoveBaseAction, MoveBaseGoal
import actionlib
from actionlib_msgs.msg import *
from geometry_msgs.msg import Pose, Point, Quaternion
from apriltags_ros.msg import AprilTagDetection
from tf2_msgs.msg import TFMessage

detected = [False, False, False, False, False, False]
basex = "0"
basey = "0"
basez = "0"
tagframe1 = "0"
translationx = ["0","1","0","0","0", "0"]
translationy = ["0","0","0","0","0", "0"]
translationz = ["0","0","0","0","0", "0"]
rotationx = ["0","0","0","0","0", "0"]
rotationy = ["0","0","0","0","0", "0"]
rotationz = ["0","0","0","0","0", "0"]
rotationw = ["0","0","0","0","0", "0"]

def callback(data):
    # rospy.loginfo("DICKS IN MY")
    rospy.loginfo(data.transforms[0])
   
    
    if data.transforms[0].child_frame_id == "happy_thoughts" and detected [0] == False: 
   #   if canTransform(data)
       translationx[0] = data.transforms[0].transform.translation.x
       translationy[0] = data.transforms[0].transform.translation.y
       translationz[0] = data.transforms[0].transform.translation.z
       rospy.loginfo("#1")
       detected[0] = True

    if data.transforms[0].child_frame_id == "fucking_happy_thoughts" and detected[1] == False:
       translationx[1] = data.transforms[0].transform.translation.x
       translationy[1] = data.transforms[0].transform.translation.y
       translationz[1] = data.transforms[0].transform.translation.z
       
       rospy.loginfo("#2")
       detected[1] = True
    
    if data.transforms[0].child_frame_id == "more_fucking_happy_thoughts" and detected[2] == False:
       translationx[2] = data.transforms[0].transform.translation.x
       translationy[2] = data.transforms[0].transform.translation.y
       translationz[2] = data.transforms[0].transform.translation.z
       rospy.loginfo(data.transforms[0].transform.translation)
       rospy.loginfo("#3")
       detected[2] = True   
    
    if data.transforms[0].child_frame_id == "jesus_more_fucking_happy_thoughts" and detected[3] == False:
       translationx[3] = data.transforms[0].transform.translation.x
       translationy[3] = data.transforms[0].transform.translation.y
       translationz[3] = data.transforms[0].transform.translation.z
       rospy.loginfo("#4")
       detected[3] = True
    
    if data.transforms[0].child_frame_id == "fuuuuuuuuuuckkkkkk" and detected[4] == False:
       translationx[4] = data.transforms[0].transform.translation.x
       translationy[4] = data.transforms[0].transform.translation.y
       translationz[4] = data.transforms[0].transform.translation.z
       rospy.loginfo("#5")
       detected[4] = True

    if data.transforms[0].child_frame_id == "five" and detected[5] == False:
       translationx[5] = data.transforms[0].transform.translation.x
       translationy[5] = data.transforms[0].transform.translation.y
       translationz[5] = data.transforms[0].transform.translation.z
       rospy.loginfo("#5")
       detected[5] = True

    if sum(detected) == 6:
      rospy.loginfo("youdidit");
      rospy.loginfo(translationx)
   
def listener():
    #rospy.init_node('listener', anonymous=True)
    rospy.Subscriber('tf',TFMessage,callback)
    rospy.spin()

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
        rospy.init_node('nav_test', anonymous=False)
        navigator = GoToPose()

        # Customize the following values so they are appropriate for your location
        position = {'x': 1.22, 'y' : 2.56}
        quaternion = {'r1' : 0.000, 'r2' : 0.000, 'r3' : 0.000, 'r4' : 1.000}
	rospy.loginfo(Point());
        rospy.loginfo("Go to (%s, %s) pose", position['x'], position['y'])
        listener();
      #  success = navigator.goto(position, quaternion)

      #  if success:
       #     rospy.loginfo("Hooray, reached the desired pose")
       # else:
        #    rospy.loginfo("The base failed to reach the desired pose")

        # Sleep to give the last log messages time to be sent
      #  rospy.sleep(1)

    except rospy.ROSInterruptException:
        rospy.loginfo("Ctrl-C caught. Quitting")

