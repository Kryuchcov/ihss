#!/usr/bin/python
import rospy
import aiml
import os
import sys
from std_msgs.msg import String
#voy a buscar "medicine,comida"
rospy.init_node('interact_backend',anonymous=True)
pub=rospy.Publisher("robot_quest",String,queue_size=1)
response_publisher=rospy.Publisher("response",String,queue_size=1)
houseBot=aiml.Kernel()

def load_aiml(xml_file):
    data_path=rospy.get_param("aiml_path")
    turno=rospy.get_param("escenario")
    os.chdir(data_path)

    if turno=="manana":
        if os.path.isfile("manana.brn"):
            houseBot.bootstrap(brainFile="manana.brn")
        else:
            houseBot.bootstrap(learnFiles=xml_file,commands="load aiml manana")
            houseBot.saveBrain("manana.brn")
    if turno=="medioDia":
        if os.path.isfile("medioDia.brn"):
            houseBot.bootstrap(brainFile="medioDia.brn")
        else:
            houseBot.bootstrap(learnFiles=xml_file,commands="load aiml medioDia")
            houseBot.saveBrain("medioDia.brn")
    if turno=="tarde":
        if os.path.isfile("tarde.brn"):
            houseBot.bootstrap(brainFile="tarde.brn")
        else:
            houseBot.bootstrap(learnFiles=xml_file,commands="load aiml tarde")
            houseBot.saveBrain("tarde.brn")

def userCallback(data):
    response=houseBot.respond(data.data)
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
    load_aiml('startup.xml')
    rospy.Subscriber("flag_interact",String,callback2)
    rospy.loginfo("Starting House AIML Server")
    rospy.Subscriber("chatter",String,userCallback)
    rospy.spin()
