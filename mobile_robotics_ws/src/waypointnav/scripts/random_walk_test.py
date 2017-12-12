#!/usr/bin/env python

import rospy
import random
from move_base_msgs.msg import MoveBaseGoal, MoveBaseAction
from kobuki_msgs.msg import BumperEvent
import actionlib
from actionlib_msgs.msg import *
from geometry_msgs.msg import Twist

# global variables
bump = False
action_duration = 0.5
movement_speed = 0.15
turn_speed = 0.5
min_turn_duration = 3.5
max_turn_duration = 10.5

# listen (adapted from line_follower
def processSensing(BumperEvent):
     global bump
     bumper_num = BumperEvent.bumper
     bumper_state = BumperEvent.state

     if (bumper_state==0):
          bump = bumper_num
     else:
          bump = -1
     #newInfo = True
     
def random_walk():
     pub = rospy.Publisher('cmd_vel_mux/input/navi', Twist, queue_size=10)
     rospy.Subscriber('/mobile_base/events/bumper', BumperEvent, processSensing)
     rospy.init_node('random_walk')
     # move_base = actionlib.SimpleActionClient("move_base", MoveBaseAction)
     # rospy.loginfo("wait for the action server to come up")
     # #allow up to 5 seconds for the action server to come up
     # self.move_base.wait_for_server(rospy.Duration(5))

     # goal = MoveBaseGoal()

     #listen
     global bump
     twist = Twist()
     turn_direction = True

     while not rospy.is_shutdown():
         if (bump!=-1):
             str = "bumper hit, turning around %s"%rospy.get_time()
             rospy.loginfo(str)

             if turn_direction:
                turn(pub, random_duration(), turn_speed)
                move_straight(pub, 0.25)
                turn(pub, random_duration(), turn_speed)
             else:
                turn(pub, random_duration(), -turn_speed)
                move_straight(pub, 0.25)
                turn(pub, random_duration(), -turn_speed)

         # if bump==2:
         #     str = "right bumper, turning left %s"%rospy.get_time()
         #     rospy.loginfo(str)
         #     turn(pub, random_duration(), turn_speed)
         #     move_straight(0.25)
         #     turn(pub, random_duration(), turn_speed)
         # elif bump==0:
         #     str = "left bumper, turning right %s"%rospy.get_time()
         #     rospy.loginfo(str)
         #     turn(pub, random_duration(), -turn_speed)
         # elif bump==1:
         #     str = "front bumper, turning left %s"%rospy.get_time()
         #     rospy.loginfo(str)
         #     turn(pub, random_duration(), turn_speed)
         else:
             str = "moving straight ahead %s"%rospy.get_time()
             rospy.loginfo(str)
             move_straight(pub, 0.5)
             # twist.linear.x = movement_speed
             # twist.angular.z = 0
             # pub.publish(twist)
         bump = -1
         rospy.sleep(action_duration)
         
def move_straight(pub, duration):
    twist = Twist()
    twist.linear.x = movement_speed
    twist.angular.z = 0
    pub.publish(twist)
    rospy.sleep(duration)

def random_duration():
    # Calculates a random amount of time for the Roomba to turn for
    duration = min_turn_duration + random.random() * (max_turn_duration - min_turn_duration)
    str = "Random duration: %s"%duration
    rospy.loginfo(str)
    return duration

def turn(pub, duration, weight):
    twist = Twist()
    # First, back up slightly from the wall
    twist.linear.x = -movement_speed; twist.linear.y = 0; twist.linear.z = 0
    twist.angular.x = 0; twist.angular.y = 0; twist.angular.z = 0
    pub.publish(twist)
    rospy.sleep(action_duration)

    # Now, keep turning until the end of the specified duration
    currentTime = rospy.get_time();
    stopTime = rospy.get_time() + 6;
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
