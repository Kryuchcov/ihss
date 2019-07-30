#!/usr/bin/python
import rospy
from std_msgs.msg import String
import sys
import cv2
import numpy as np
from sensor_msgs.msg import Image
from cv_bridge import CvBridge, CvBridgeError

pub=rospy.Publisher('vision_status',String,queue_size=1)
busco=""
contador=0
limconteo=15

class image_converter:

  def __init__(self):
    self.image_pub = rospy.Publisher("image_topic_2",Image,queue_size=1)

    self.bridge = CvBridge()
    self.image_sub = rospy.Subscriber("/camera/rgb/image_raw",Image,self.callback)
    self.data_sub=rospy.Subscriber("vision_process",String,self.callback2)

  def callback(self,data):
    global contador,busco,limconteo
    try:
      cv_image = self.bridge.imgmsg_to_cv2(data, "bgr8")
    except CvBridgeError as e:
      print(e)

    #RGB to hsv
    hsv=cv2.cvtColor(cv_image,cv2.COLOR_BGR2HSV)

    if busco=="medicine":
        if contador<limconteo:
            contador=contador+1
            print "contador ",contador
            pub.publish("wait")
            #color rojo
            lower=np.array([150,230,10])
            upper=np.array([255,255,255])

            mask=cv2.inRange(hsv,lower,upper)
            res=cv2.bitwise_and(cv_image,cv_image,mask=mask)
            try:
                radius=0
                contours,hierarchy=cv2.findContours(mask,1,2)
                if len(contours)>0:
                    cnt=max(contours,key=cv2.contourArea)
                    (x,y),radius = cv2.minEnclosingCircle(cnt)
                    center = (int(x),int(y))
                    radius = int(radius)
                    cv2.circle(res,center,radius,(0,255,0),2)
            except CvBridgeError as e:
                print (e)
            cv2.imshow('res',res)
            #print "radio ",radius
            if radius>=100:
                pub.publish("succeded")
                contador=0
                busco=""
        else:
            pub.publish("failed")
            contador=0
            busco=""

    if busco=="snack":
        if contador<limconteo:
            contador=contador+1
            #print "contador ",contador
            pub.publish("wait")
            #color azul
            lower=np.array([100,230,10])
            upper=np.array([150,255,255])

            mask=cv2.inRange(hsv,lower,upper)
            res=cv2.bitwise_and(cv_image,cv_image,mask=mask)
            try:
                radius=0
                contours,hierarchy=cv2.findContours(mask,1,2)
                if len(contours)>0:
                    cnt=max(contours,key=cv2.contourArea)
                    (x,y),radius = cv2.minEnclosingCircle(cnt)
                    center = (int(x),int(y))
                    radius = int(radius)
                    cv2.circle(res,center,radius,(0,255,0),2)
            except CvBridgeError as e:
                print (e)
            #print "radio ",radius
            cv2.imshow('res',res)
            if radius>=100:
                pub.publish("succeded")
                contador=0
                busco=""
        else:
            pub.publish("failed")
            contador=0
            busco=""

    if busco=="breakfast":
        if contador<limconteo:
            contador=contador+1
            #print "contador ",contador
            pub.publish("wait")
            #color verde
            lower=np.array([40,230,10])
            upper=np.array([100,255,255])

            mask=cv2.inRange(hsv,lower,upper)
            res=cv2.bitwise_and(cv_image,cv_image,mask=mask)
            try:
                radius=0
                contours,hierarchy=cv2.findContours(mask,1,2)
                if len(contours)>0:
                    cnt=max(contours,key=cv2.contourArea)
                    (x,y),radius = cv2.minEnclosingCircle(cnt)
                    center = (int(x),int(y))
                    radius = int(radius)
                    cv2.circle(res,center,radius,(0,255,0),2)
            except CvBridgeError as e:
                print (e)
            #print "radio ",radius
            cv2.imshow('res',res)
            if radius>=100:
                pub.publish("succeded")
                contador=0
                busco=""
        else:
            pub.publish("failed")
            contador=0
            busco=""

    if busco=="eat":
        if contador<limconteo:
            contador=contador+1
            #print "contador ",contador
            pub.publish("wait")
            #color amarillo
            lower=np.array([10,230,10])
            upper=np.array([30,255,255])

            mask=cv2.inRange(hsv,lower,upper)
            res=cv2.bitwise_and(cv_image,cv_image,mask=mask)
            try:
                radius=0
                contours,hierarchy=cv2.findContours(mask,1,2)
                if len(contours)>0:
                    cnt=max(contours,key=cv2.contourArea)
                    (x,y),radius = cv2.minEnclosingCircle(cnt)
                    center = (int(x),int(y))
                    radius = int(radius)
                    cv2.circle(res,center,radius,(0,255,0),2)
            except CvBridgeError as e:
                print (e)
            #print "radio ",radius
            cv2.imshow('res',res)
            if radius>=100:
                pub.publish("succeded")
                contador=0
                busco=""
        else:
            pub.publish("failed")
            contador=0
            busco=""
    cv2.waitKey(3)

    try:
      self.image_pub.publish(self.bridge.cv2_to_imgmsg(cv_image, "bgr8"))
    except CvBridgeError as e:
      print(e)

  def callback2(self,cadena):
      global busco
      busco=cadena.data

def main(args):
  ic = image_converter()
  rospy.init_node('image_converter', anonymous=True)
  try:
    rospy.spin()
  except KeyboardInterrupt:
    print("Shutting down")
  cv2.destroyAllWindows()

if __name__ == '__main__':
    main(sys.argv)
