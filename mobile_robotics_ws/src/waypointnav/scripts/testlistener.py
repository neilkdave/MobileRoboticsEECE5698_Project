#!/usr/bin/env python


import rospy
from std_msgs.msg import String
from move_base_msgs.msg import MoveBaseAction, MoveBaseGoal
import actionlib
from actionlib_msgs.msg import *
from geometry_msgs.msg import Pose, Point, Quaternion
from apriltags_ros.msg import AprilTagDetection
from tf2_msgs.msg import TFMessage
from operator import attrgetter
from pprint import pprint


translation_list = [""]
rotation_list = [""]

def callback(data):
   # rospy.loginfo("DICKS IN MY")
   # rospy.loginfo(data.transforms[0])
    if data.transforms[0].child_frame_id == "happy_thoughts":
      translation_list[0] = data.transforms[0].transform
     # rospy.loginfo(data.transforms[0].transform)
      rospy.loginfo(data.transforms[0].transform.translation.x)
  #  pprint(dir(data))
    # map(attrgetter('my_attr'), my_list)
   #  rospy.loginfo(my_list);

def listener():

    # In ROS, nodes are uniquely named. If two nodes with the same
    # name are launched, the previous one is kicked off. The
    # anonymous=True flag means that rospy will choose a unique
    # name for our 'listener' node so that multiple listeners can
    # run simultaneously.
    rospy.init_node('listener', anonymous=True)

    rospy.Subscriber('tf', TFMessage, callback)

    # spin() simply keeps python from exiting until this node is stopped
    rospy.spin()

if __name__ == '__main__':
    listener()


