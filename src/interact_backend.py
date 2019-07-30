#!/usr/bin/python
import rospy
import aiml
import os
import sys
from std_msgs.msg import String
#voy a buscar "medicine,comida"
pub=rospy.Publisher("robot_quest",String,queue_size=1)
response_publisher=rospy.Publisher("response",String,queue_size=1)
houseBot=aiml.Kernel()

def load_aiml(xml_file,turno):
    data_path=rospy.get_param("aiml_path")
    print data_path
    os.chdir(data_path)

    if turno=="manana":
        if os.path.isfile("manana.brn"):
            mybot.bootstrap(brainFile="manana.brn")
        else:
            mybot.bootstrap(learnFiles=xml_file,commands="load aiml manana")
            mybot.saveBrain("manana.brn")
    if turno=="medioDia":
        if os.path.isfile("medioDia.brn"):
            mybot.bootstrap(brainFile="medioDia.brn")
        else:
            mybot.bootstrap(learnFiles=xml_file,commands="load aiml medioDia")
            mybot.saveBrain("medioDia.brn")
    if turno=="tarde":
        if os.path.isfile("tarde.brn"):
            mybot.bootstrap(brainFile="tarde.brn")
        else:
            mybot.bootstrap(learnFiles=xml_file,commands="load aiml tarde")
            mybot.saveBrain("tarde.brn")

def callback(cadena):
    load_aiml('startup.xml',cadena.data)

def userCallback(data):
    response=mybot.respond(data.data)
    rospy.loginfo("I heard:: %s",data.data)
    rospy.loginfo("I spoke:: %s",response)
    response_publisher.publish(response)

def callback2(cadena):
    global flagStatus

    if cadena.data=="continue":
        flagStatus="c"
    if cadena.data=="wait":
        flagStatus="w"


if __name__ == '__main__':
    rospy.init_node('interact_backend',anonymous=True)
    rospy.Subscriber("escenario",String,callback)
    rospy.Subscriber("flag_interact",String,callback2)
    rospy.loginfo("Starting ROS AIML Server")
    rospy.Subscriber("chatter",String,userCallback)
    rospy.spin()
