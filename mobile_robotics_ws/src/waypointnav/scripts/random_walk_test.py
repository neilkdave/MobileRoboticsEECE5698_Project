#!/usr/bin/env python

import rospy
import random
from move_base_msgs.msg import MoveBaseGoal, MoveBaseAction
from kobuki_msgs.msg import BumperEvent

# global variables
bump = False
action_duration = 0.25
movement_speed = 0.2
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
     
def hello_create():
##     pub = rospy.Publisher('cmd_vel_mux/input/navi', Twist)
     rospy.Subscriber('/mobile_base/events/bumper', BumperEvent, processSensing)
     rospy.init_node('hello_create')
     #listen
     global bump
##     twist = Twist()
     while not rospy.is_shutdown():
         if bump==2:
             str = "right bumper, turning left %s"%rospy.get_time()
             rospy.loginfo(str)
##             turn(pub, random_duration(), turn_speed)
         elif bump==0:
             str = "left bumper, turning right %s"%rospy.get_time()
             rospy.loginfo(str)
##             turn(pub, random_duration(), -turn_speed)
         elif bump==1:
             str = "both bumpers, turning left %s"%rospy.get_time()
             rospy.loginfo(str)
##             turn(pub, random_duration(), turn_speed)
         else:
             str = "moving straight ahead %s"%rospy.get_time()
             rospy.loginfo(str)
##             twist.linear.x = movement_speed; twist.linear.y = 0; twist.linear.z = 0
##             twist.angular.x = 0; twist.angular.y = 0; twist.angular.z = 0
             bump = False
##         pub.publish(twist)
         bump = -1
         rospy.sleep(action_duration)
         
def random_duration():
    # Calculates a random amount of time for the Roomba to turn for
    duration = min_turn_duration + random.random() * (max_turn_duration - min_turn_duration)
    str = "Random duration: %s"%duration
    rospy.loginfo(str)
    return duration

def turn(pub, duration, weight):
##    twist = Twist()
##    # First, back up slightly from the wall
##    twist.linear.x = -movement_speed; twist.linear.y = 0; twist.linear.z = 0
##    twist.angular.x = 0; twist.angular.y = 0; twist.angular.z = 0
##    pub.publish(twist)
    rospy.sleep(action_duration)
    # Now, keep turning until the end of the specified duration
    currentTime = rospy.get_time();
    stopTime = rospy.get_time() + duration;
    while (rospy.get_time() < stopTime):
         str = "turning %s"%rospy.get_time()
         rospy.loginfo(str)
##         twist.linear.x = 0.0; twist.linear.y = 0; twist.linear.z = 0
##         twist.angular.x = 0; twist.angular.y = 0; twist.angular.z = weight
##         pub.publish(twist)
         rospy.sleep(action_duration)
         
if __name__ == '__main__':
     try:
         hello_create()
     except rospy.ROSInterruptException: pass
