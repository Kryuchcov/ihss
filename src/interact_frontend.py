#!/usr/bin/env python
import rospy,os,sys
from sound_play.msg import SoundRequest
from sound_play.libsoundplay import SoundClient
from std_msgs.msg import String

rospy.init_node("interact_frontend",anonymous=True)
soundhandle=SoundClient()
rospy.sleep(1)
soundhandle.stopAll()

def get_response(data):
    soundhandle.say(data.data)

if __name__ == '__main__':
    rospy.loginfo("Starting Anya voice")
    rospy.Subscriber("response",String,get_response,queue_size=10)
    rospy.spin()
