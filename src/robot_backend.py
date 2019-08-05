#!/usr/bin/python
import rospy
from std_msgs.msg import String
from std_msgs.msg import Int32

pub=rospy.Publisher('robot_go_to',Int32,queue_size=1) #le digo al controlador del robot a donde ir
pub2=rospy.Publisher('vision_process',String,queue_size=1) #le digo al controlador visual que buscar
pub3=rospy.Publisher('flag_interact',String,queue_size=1)
robotStatus="w"
visionStatus="w"
escenario=""
#1=cocina 2=sala 3=recamara 4=go home (comedor)
#breakfast, medicine, eat, snack,

def destinoRobot(lugar):
    global robotStatus

    pub.publish(lugar)
    while robotStatus=="w":
        #pub.publish(lugar)
        pass

    if robotStatus=="f":
        destinoRobot(lugar)
    elif robotStatus=="s":
        if lugar==4:
            pub3.publish("continue")
        robotStatus="w"
        return True

def procesoVision(busco,destino):
    global visionStatus

    if destino==1:
        destiny="cocina"
    if destino==2:
        destiny="sala"
    if destino==3:
        destiny="recamara"
    if destino==4:
        destiny="comedor"

    pub2.publish(busco)
    while visionStatus=="w":
        #esperando a que el robor encuentre Algo
        pass
    if visionStatus=="f":
        #no encontre nada
        visionStatus="w"
        print "NO ENCONTRE NADA EN ",destiny
        return False
    elif visionStatus=="s":
        visionStatus="w"
        print "encontre ",busco, "en ",destiny
        return True

def callback(cadena):
    global robotStatus,escenario
    print cadena.data
    print escenario

    if ((cadena.data=="eat" or cadena.data=="snack") or cadena.data=="breakfast"):
        #el robot va a la cocina
        pub3.publish("wait")
        if destinoRobot(1):
            if procesoVision(cadena.data,1):
                destinoRobot(4)
            else:
                destinoRobot(4)

    #condicional para saber como buscar segun el escenario
    if cadena.data=="medicine" and escenario=="manana":
        pub3.publish("wait")
        if destinoRobot(3):
            if procesoVision(cadena.data,3):
                destinoRobot(4)
            elif destinoRobot(2):
                if procesoVision(cadena.data,2):
                    destinoRobot(4)
                elif destinoRobot(1):
                    if procesoVision(cadena.data,1):
                        destinoRobot(4)
                    else:
                        print "no encontre nada"
                        destinoRobot(4)

    if cadena.data=="medicine" and escenario=="medioDia":
        pub3.publish("wait")
        if destinoRobot(1):
            if procesoVision(cadena.data,1):
                destinoRobot(4)
            elif destinoRobot(2):
                if procesoVision(cadena.data,2):
                    destinoRobot(4)
                elif destinoRobot(3):
                    if procesoVision(cadena.data,3):
                        destinoRobot(4)
                    else:
                        print "no encontre nada"
                        destinoRobot(4)

    if cadena.data=="medicine" and escenario=="tarde":
        pub3.publish("wait")
        if destinoRobot(2):
            if procesoVision(cadena.data,2):
                destinoRobot(4)
            elif destinoRobot(1):
                if procesoVision(cadena.data,1):
                    destinoRobot(4)
                elif destinoRobot(3):
                    if procesoVision(cadena.data,3):
                        destinoRobot(4)
                    else:
                        print "no encontre nada"
                        destinoRobot(4)

def callback2(cadena):
    global robotStatus

    if cadena.data=="succeded":
        robotStatus="s"
    if cadena.data=="failed":
        robotStatus="f"
    if cadena.data=="wait":
        robotStatus="w"
    print "STATUS ",robotStatus

def callback3(cadena):
    global visionStatus

    if cadena.data=="succeded":
        visionStatus="s"
    if cadena.data=="failed":
        visionStatus="f"
    if cadena.data=="wait":
        visionStatus="w"

def callback4(cadena):
    global escenario
    escenario=cadena.data

if __name__=='__main__':
    rospy.init_node('robot_backend',anonymous=True)
    rospy.Subscriber("robot_quest",String,callback) #entrada del interact_backend sobre a donde ir y que buscar
    rospy.Subscriber("robot_goal_status",String,callback2) #estatus que el controlador del robot me da
    rospy.Subscriber("vision_status",String,callback3) #estatus que el controlador de vision me da
    rospy.Subscriber("escenario",String,callback4) #como en interact_backend reviso el turno
    rospy.spin()
