#!/usr/bin/env python

import rospy
from kobuki_msgs.msg import Sound
from kobuki_msgs.msg import Led

rospy.init_node('sound_test')

sound_pub = rospy.Publisher('/mobile_base/commands/sound', Sound, queue_size = 10)
led_pub1 = rospy.Publisher('/mobile_base/commands/led1', Led, queue_size = 10)
led_pub2 = rospy.Publisher('/mobile_base/commands/led2', Led, queue_size = 10)

led_1 = Led()
led_2 = Led()
sound_type = Sound()
sound_type.value = 5
# sound_type.value = 0
while not rospy.is_shutdown():
	sound_type.value = 5
	led_1 = Led.GREEN
	led_2 = Led.RED
	sound_pub.publish(sound_type)
	led_pub1.publish(led_1)
	led_pub2.publish(led_2)
	rospy.sleep(0.5)
	sound_type.value = 4
	led_1 = Led.ORANGE
	led_2 = Led.GREEN
	sound_pub.publish(sound_type)
	led_pub1.publish(led_1)
	led_pub2.publish(led_2)
	rospy.sleep(0.4)
	sound_type.value = 0
	led_1 = Led.RED
	led_2 = Led.ORANGE
	led_pub1.publish(led_1)
	led_pub2.publish(led_2)
	sound_pub.publish(sound_type)
	rospy.sleep(0.6)
	sound_type.value = 6
	led_1 = Led.ORANGE
	led_2 = Led.GREEN
	led_pub1.publish(led_1)
	led_pub2.publish(led_2)
	sound_pub.publish(sound_type)
	rospy.sleep(0.8)
