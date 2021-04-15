#!/usr/bin/env python

from __future__ import print_function
import sys, tty, termios
from std_srvs.srv import Trigger, TriggerRequest
from sensor_msgs.msg import JointState
from control_msgs.msg import FollowJointTrajectoryGoal
from trajectory_msgs.msg import JointTrajectoryPoint
from std_msgs.msg import String
import rospy
# This allows Ctrl-C and related keyboard commands to still function.
# It detects escape codes in order to recognize arrow keys. It also
# has buffer flushing to avoid repeated commands.  This is
# blocking code.

def getch():
  stdin_fd = 0
  # "Return a list containing the tty attributes for file descriptor
  # fd, as follows: [iflag, oflag, cflag, lflag, ispeed, ospeed, cc]"
  # from https://docs.python.org/2/library/termios.html
  original_tty_attributes = termios.tcgetattr(stdin_fd)
  new_tty_attributes = original_tty_attributes[:]
  # Change the lflag (local modes) to turn off canonical mode
  new_tty_attributes[3] &= ~termios.ICANON
  try:
    termios.tcsetattr(stdin_fd, termios.TCSAFLUSH, new_tty_attributes)
    ch1 = sys.stdin.read(1)
    if ch1 == '\x1b':
      # special key pressed
      ch2 = sys.stdin.read(1)
      ch3 = sys.stdin.read(1)
      ch = ch1 + ch2 + ch3
    else:
      # not a special key
      ch = ch1
  finally:
    termios.tcsetattr(stdin_fd, termios.TCSAFLUSH, original_tty_attributes)
  return ch

def talker():
  stretch_keyboard_pub = rospy.Publisher('/stretch/keyboard_pub',String, queue_size=10)
  rospy.init_node('stretch_talker')
  rate = rospy.Rate(10)
  rospy.loginfo('successfully init node:{}'.format("stretch_talker"))
  while not rospy.is_shutdown():
    c = getch()
    stretch_keyboard_pub.publish(c)
    rate.sleep()

if __name__ == '__main__':
  try:
    talker()
  except rospy.ROSInterruptException:
    pass

