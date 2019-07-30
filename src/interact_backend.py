#!/usr/bin/python
import rospy
from sound_play.libsoundplay import SoundClient
from itertools import permutations
from random import randint
from std_msgs.msg import String

pub=rospy.Publisher("robot_quest",String,queue_size=1)
sound_client=SoundClient()
rospy.sleep(1)
flagStatus=""
preg_man={}
preg_man[1]="The weather for today has a probability to rain in the evening"
preg_man[2]="Do you want to see the news?"
preg_man[3]="Did you take your medicine?"
preg_man[4]="Would you like to take a breakfast?"
preg_man[5]="As a recordatory, today is Irving's birthday"

preg_med={}
preg_med[1]="I have recived a new coupone for the mall, you can check it in your smart phone"
preg_med[2]="Do you want something to eat?"
preg_med[3]="Did you take your medicine?"
preg_med[4]="Do you want to see a TV serie?"
preg_med[5]="I see your a little bit thirsty, you should drink a glass of water"

preg_tar={}
preg_tar[1]="You should check your e-mail"
preg_tar[2]="Irving's birthday is almost over, would you like to call him?"
preg_tar[3]="Did you take your medicine today?"
preg_tar[4]="It's almost night, would you like some food, maybe a snack?"
preg_tar[5]="It's late, we must sleep"

def robot_say(message,printText,sayText):
    if printText==True:
        print message
    if sayText==True:
        sound=sound_client.voiceSound(message)
        sound.play()
        rospy.sleep(2.7)

def numeros():
	res=[1,2,3,4,5]
	perms=permutations(res,3)
	permutaciones=list(perms)
	pos=randint(0,len(permutaciones)-1)
	preguntas=list(permutaciones[pos])
	if 3 in preguntas:
		return preguntas
	else:
		preguntas.append(3)
		return preguntas

def respuestasBasicas(pregunta,respuestaUsuario):
    global flagStatus

    if pregunta.find("medicine")>0 and respuestaUsuario=="no":
        robot_say("Do you have it with you?",True,True)
        answer=raw_input()
        if answer=="no":
            robot_say("I'll send the robot to find it",True,True)
            pub.publish("medicine")
        else:
            robot_say("Take it please",True,True)
            flagStatus="c"
    elif pregunta.find("medicine")>0 and respuestaUsuario=="yes":
        robot_say("ok perfect",True,True)
        flagStatus="c"

    if pregunta.find("eat")>0 and respuestaUsuario=="yes":
        robot_say("I'm sending the robot for something",True,True)
        pub.publish("eat")
    elif pregunta.find("eat")>0 and respuestaUsuario=="no":
        robot_say("ok, no problem",True,True)
        flagStatus="c"

    if pregunta.find("breakfast")>0 and respuestaUsuario=="yes":
        robot_say("All right, the robot will get something",True,True)
        pub.publish("breakfast")
        print pregunta.find("breakfast")
        print pregunta.find("eat")
    elif pregunta.find("breakfast")>0 and respuestaUsuario=="no":
        robot_say("No problem",True,True)
        flagStatus="c"

    if pregunta.find("snack")>0 and respuestaUsuario=="yes":
        robot_say("Sure, robot is on way",True,True)
        pub.publish("snack")
    elif pregunta.find("snack")>0 and respuestaUsuario=="no":
        robot_say("No problem",True,True)
        flagStatus="c"

    if pregunta.find("news")>0 and respuestaUsuario=="yes":
        robot_say("Well, these are from today",True,True)
        flagStatus="c"
    elif pregunta.find("news")>0 and respuestaUsuario=="no":
        robot_say("No problem",True,True)
        flagStatus="c"

    if pregunta.find("TV")>0 and respuestaUsuario=="yes":
        robot_say("Good choise",True,True)
        flagStatus="c"
    elif pregunta.find("TV")>0 and respuestaUsuario=="no":
        robot_say("Ok",True,True)
        flagStatus="c"

    if pregunta.find("call")>0 and respuestaUsuario=="yes":
        robot_say("I'm calling",True,True)
        flagStatus="c"
    elif pregunta.find("call")>0 and respuestaUsuario=="no":
        robot_say("well",True,True)
        flagStatus="c"

def callback(cadena):
    global flagStatus
    flagStatus="w"
    preguntas=numeros()

    if cadena.data=="manana":
        while len(preguntas)>0:
            caso=preguntas.pop()
            frase=preg_man[caso]
            answer=""
            if frase.find("?")>0:
                robot_say(frase,True,True)
                answer=raw_input()
                respuestasBasicas(frase,answer)
                while flagStatus!="c":
                    pass
            else:
                robot_say(frase,True,True)
                rospy.sleep(1.5)

    if cadena.data=="medioDia":
        while len(preguntas)>0:
            caso=preguntas.pop()
            frase=preg_med[caso]
            answer=""
            if frase.find("?")>0:
                robot_say(frase,True,True)
                answer=raw_input()
                respuestasBasicas(frase,answer)
                while flagStatus!="c":
                    pass
            else:
                robot_say(frase,True,True)
                rospy.sleep(1.5)

    if cadena.data=="tarde":
        while len(preguntas)>0:
            caso=preguntas.pop()
            frase=preg_tar[caso]
            answer=""
            if frase.find("?")>0:
                robot_say(frase,True,True)
                answer=raw_input()
                respuestasBasicas(frase,answer)
                while flagStatus!="c":
                    pass
            else:
                robot_say(frase,True,True)
                rospy.sleep(1.5)

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
    rospy.spin()
