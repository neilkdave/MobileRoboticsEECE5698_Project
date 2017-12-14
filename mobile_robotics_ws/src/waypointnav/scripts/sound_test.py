#!/usr/bin/env python

import rospy
from kobuki_msgs.msg import Sound

rospy.init_node('sound_test')

sound_pub = rospy.Publisher('/mobile_base/commands/sound', Sound, queue_size = 10)

sound_type = Sound()
sound_type.value = 5
# sound_type.value = 0
while not rospy.is_shutdown():
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
