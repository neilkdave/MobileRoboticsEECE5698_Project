#!/usr/bin/env python

import rospy
import random
import math
from move_base_msgs.msg import MoveBaseGoal, MoveBaseAction
from kobuki_msgs.msg import BumperEvent
import actionlib
from actionlib_msgs.msg import *
from geometry_msgs.msg import Twist, Pose, Point, Quaternion
from tf2_msgs.msg import TFMessage
from tf import TransformListener
from kobuki_msgs.msg import Sound

# global variables
bump = False
action_duration = 0.5
movement_speed = 0.2
turn_speed = 0.5
min_turn_duration = 3.5
max_turn_duration = 10.5

# global variables 2
detected = [False, False, False, False, False, False]
stored = [False, False, False, False, False, False]
position = ["0","0","0","0","0","0"]
quaternion = ["0","0","0","0","0","0"]
quaternion_true = {'r1' : 0.000, 'r2' : 0.000, 'r3' : 0.000, 'r4' : 1.000}
curr_pos = {'x': 0, 'y': 0, 'z': 0}



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
        success = self.goto(position[num], quaternion_true)

        if success:
            rospy.loginfo("Hooray, I reached waypoint %s",num)
        else:
            rospy.loginfo("Shucks, I can't reach waypoint %s",num)

        # Sleep to give the last log messages time to be sent
        rospy.sleep(1)
	return success

    def callback(self,data):
	global detected
	global stored
	global position
	global quaternion
	global curr_pos
	# rospy.loginfo(data.transforms[0].child_frame_id)
	if data.transforms[0].child_frame_id == 'base_footprint':
	    curr_pos = {'x': data.transforms[0].transform.translation.x, 'y': data.transforms[0].transform.translation.y, 'z': data.transforms[0].transform.translation.z}
	    # rospy.loginfo(curr_pos)

	if sum(detected) == 6:
	    return

        if self.tf.frameExists("/happy_thoughts") and self.tf.frameExists("/map") and detected[0] == False:
	    #Get Transform
            tempos, temqua = self.tf.lookupTransform("/map", "/happy_thoughts", self.tf.getLatestCommonTime("/map", "/happy_thoughts"))

            rospy.loginfo("#0")
            position[0] = {'x': tempos[0], 'y': tempos[1], 'z': tempos[2]}
            quaternion[0] = {'r1': temqua[0],'r2': temqua[1],'r3': temqua[2],'r4': temqua[3]}
            rospy.loginfo(position[0])
            detected[0] = True

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


    def listener(self):
	rospy.sleep(1);
        rospy.Subscriber('tf',TFMessage,self.callback)
        # rospy.spin()



def yay(sound_pub):
	sound_type = Sound()
	sound_type.value = 5
	sound_pub.publish(sound_type)
	rospy.sleep(0.5)
	sound_type.value = 4
	sound_pub.publish(sound_type)
	rospy.sleep(0.4)
	sound_type.value = 0
	sound_pub.publish(sound_type)
	rospy.sleep(0.6)
	sound_type.value = 6
	sound_pub.publish(sound_type)
	rospy.sleep(0.8)
	sound_type.value = 5
	sound_pub.publish(sound_type)
	rospy.sleep(0.5)
	sound_type.value = 4
	sound_pub.publish(sound_type)
	rospy.sleep(0.4)
	sound_type.value = 0
	sound_pub.publish(sound_type)
	rospy.sleep(0.6)
	sound_type.value = 6
	sound_pub.publish(sound_type)
	rospy.sleep(0.8)

# listen (adapted from line_follower
def processSensing(BumperEvent):
     global bump
     bumper_num = BumperEvent.bumper
     bumper_state = BumperEvent.state

     if (bumper_state==0):
          bump = bumper_num
     else:
          bump = -1
     
def random_walk():
     rospy.init_node('random_walk')
     navigator = GoToPose()
     navigator.listener();

     pub = rospy.Publisher('cmd_vel_mux/input/navi', Twist, queue_size=10)
     sound_pub = rospy.Publisher('/mobile_base/commands/sound', Sound, queue_size = 10)
     rospy.Subscriber('/mobile_base/events/bumper', BumperEvent, processSensing)
     

     #listen
     global bump
     global stored
     global detected
     global position
     global quaternion
     global curr_pos
     bump = -1
     twist = Twist()
     turn_direction = True
     bumper_threshold = 5
     stopTime = 0

     while not rospy.is_shutdown():
         if (bump!=-1):
             str = "bumper hit, turning around %s"%rospy.get_time()
             rospy.loginfo(str)
	     current_time = rospy.get_time()

	     if (current_time < stopTime):
                turn_direction = ~turn_direction

             if turn_direction:
                move_straight(pub, 1.5, -movement_speed)
                turn(pub, 5, turn_speed)
                move_straight(pub, 1, movement_speed)
                turn(pub, 5, turn_speed)
                turn_direction = False
             else:
                move_straight(pub, 1.5, -movement_speed)
                turn(pub, 4.5, -turn_speed)
                move_straight(pub, 1, movement_speed)
                turn(pub, 4, -turn_speed)
                turn_direction = True
             bump = -1
             stopTime = rospy.get_time() + bumper_threshold;

	 elif stored != detected:
	      if stored[0] != detected[0]:
	           num = 0
	      elif stored[1] != detected[1]:
	           num = 1
	      elif stored[2] != detected[2]:
	           num = 2
	      elif stored[3] != detected[3]:
	           num = 3
	      elif stored[4] != detected[4]:
	           num = 4
	      elif stored[5] != detected[5]:
	           num = 5
	      oldx=(position[num]['x']-curr_pos['x'])
              oldy=(position[num]['y']-curr_pos['y'])
              length= math.hypot(oldx,oldy)
              angle=math.atan2(oldy,oldx)
              newx=(length-0.5)*math.cos(angle)
	      newy=(length-0.5)*math.sin(angle)
	      rospy.loginfo(newx)
              rospy.loginfo(newy)
              position[num] = {'x': curr_pos['x']+newx, 'y': curr_pos['y']+newy, 'z': 0}
              #position[num] = {'x': position[num]['x']-0.5, 'y': position[num]['y'], 'z': 0}

	      stored[num] = True

	      # navigator.return_to_sender(num)
	      yay(sound_pub)
	      # turn(pub, 36, turn_speed)

	 elif sum(detected) == 6:
              rospy.loginfo("youdidit");
              rospy.sleep(1);
              success = navigator.return_to_sender(0)
	      yay(sound_pub)
              success = navigator.return_to_sender(1)
	      yay(sound_pub)
              success = navigator.return_to_sender(2)
	      yay(sound_pub)
              success = navigator.return_to_sender(3)
	      yay(sound_pub)
              success = navigator.return_to_sender(4)
	      yay(sound_pub)
              success = navigator.return_to_sender(5)
	      yay(sound_pub)
              if success:
                   rospy.loginfo("Hooray, reached the desired pose")
              else:
                   rospy.loginfo("The base failed to reach the desired pose")
	      rospy.shutdown()

         else:
             str = "moving straight ahead %s"%rospy.get_time()
             rospy.loginfo(str)
             move_straight(pub, 0.5, movement_speed)
         
def move_straight(pub, duration, speed):
    currentTime = rospy.get_time();
    stopTime = rospy.get_time() + duration;
    while (rospy.get_time() < stopTime):
	 twist = Twist()
         twist.linear.x = speed
         twist.angular.z = 0
         pub.publish(twist)
         rospy.sleep(action_duration)

def random_duration():
    # Calculates a random amount of time for the Roomba to turn for
    duration = min_turn_duration + random.random() * (max_turn_duration - min_turn_duration)
    str = "Random duration: %s"%duration
    rospy.loginfo(str)
    return duration

def turn(pub, duration, weight):
    twist = Twist()

    # Now, keep turning until the end of the specified duration
    currentTime = rospy.get_time();
    stopTime = rospy.get_time() + duration;
    while (rospy.get_time() < stopTime):
         str = "turning %s"%rospy.get_time()
         rospy.loginfo(str)
         twist.linear.x = 0.0; twist.linear.y = 0; twist.linear.z = 0
         twist.angular.x = 0; twist.angular.y = 0; twist.angular.z = weight
         pub.publish(twist)
         rospy.sleep(action_duration)
         
if __name__ == '__main__':
     try:
         random_walk()
     except rospy.ROSInterruptException: pass
