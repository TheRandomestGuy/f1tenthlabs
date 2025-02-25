#!/usr/bin/env python

import rospy
from geometry_msgs.msg import Twist
from turtlesim.msg import Pose
from std_srvs.srv import Empty
from math import pow,atan2,sqrt

def pose_func(msg):
    global pose_y
    global pose_x
    pose_y = msg.y
    pose_x = msg.x

class ControlTurtlesim():

    def __init__(self):
        rospy.init_node('ControlTurtlesim', anonymous=False)

        rospy.loginfo(" Press CTRL+c to stop moving the Turtle")

        rospy.on_shutdown(self.shutdown)

	rospy.wait_for_service('/reset')
	res = rospy.ServiceProxy('/reset', Empty)
	res()

    	sub=rospy.Subscriber('/turtle1/pose', Pose, pose_func)

        self.cmd_vel = rospy.Publisher('/turtle1/cmd_vel', Twist, queue_size=60)
        rate = rospy.Rate(60);
        rospy.loginfo("Set rate 60Hz")

        move_cmd = Twist()

	lin_vx = input('Input Linear Velocity in range [2,6]: ')
        move_cmd.linear.x = lin_vx	

	ang_vz = input('Input Angular Velocity in range [1,3]: ')
        move_cmd.angular.z = ang_vz

	temp = 0
	temp2 = 0
	prev = True

	starty = -1
	startx = -1

        while not rospy.is_shutdown():
	    if starty == -1:
		starty = pose_y
	    if startx == -1:
		startx = pose_x	

	    temp = sqrt(pow(pose_x - startx, 2) + pow(pose_y - starty, 2))

	    if temp-temp2 > 0 and temp < 0.5 and prev == False:
		ang_vz = -ang_vz

	    prev = temp-temp2 >= 0

	    temp2 = temp

	    move_cmd.angular.z = ang_vz

            self.cmd_vel.publish(move_cmd)

            rate.sleep()


    def shutdown(self):

        rospy.loginfo("Stopping the turtle")

        self.cmd_vel.publish(Twist())


        rospy.sleep(1)

if __name__ == '__main__':
    try:
        ControlTurtlesim()
    except:
        rospy.loginfo("End of the swim for this Turtle.")
