#!/usr/bin/python

import rospy
import cv2
import numpy as np

from sensor_msgs.msg import Image
from geometry_msgs.msg import Twist

from cv_bridge import CvBridge


def detect_line(image):
    h, w = image.shape
    left = np.argmax(image[-1] > 100)
    right = w - np.argmax(image[-1, ::-1] > 100)
    center = (left + right) / 2
    return center


class FollowerNode:

    def __init__(self):
        rospy.init_node('follower')

        self.sub = rospy.Subscriber('/camera/rgb/image_raw', Image, self.on_image, queue_size=10)
        self.pub = rospy.Publisher('/cmd_vel', Twist, queue_size=10)

        self.cv_bridge = CvBridge()

        rospy.on_shutdown(self.stop)
    
    def run(self):
        rospy.spin()

    def on_image(self, msg):
        image = self.cv_bridge.imgmsg_to_cv2(msg, "mono8")
        h, w = image.shape
        target = w / 2 - 450
        center = detect_line(image)

        vel_msg = Twist()
        vel_msg.linear.x = 0.2
        vel_msg.angular.z = 0.002 * (target - center)

        self.pub.publish(vel_msg)
    
    def stop(self):
        vel_msg = Twist()
        self.pub.publish(vel_msg)

def main():
    follower_node = FollowerNode()
    follower_node.run()


if __name__ == '__main__':
    main()
