#! /usr/bin/env python3


import roslib
import sys
import rospy
import cv2
import depth2 as dp
import modelo_decision as md
from std_msgs.msg import String
from sensor_msgs.msg import Image
from cv_bridge import CvBridge, CvBridgeError

from geometry_msgs.msg import Twist


print("----------Cargando los modelos---------")
modelo = dp.model()
modelo_robot= md.modelo_rob()


contador = 0
decision = 0
inicio = 0
class tesis_evasion:
	
	
	def __init__(self):
		self.contador = contador
		self.inicio = inicio
		self.decision = decision
		self.bridge = CvBridge()
		self.image_sub = rospy.Subscriber("/usb_cam/image_raw",Image,self.callback)
		self.control_pub = rospy.Publisher("cmd_vel",Twist,queue_size = 1) 

	def control_robot(self,x1,y1,z1,th1):
		
		twist = Twist()
		speed = 0.3
		turn = 0.55
		twist.linear.x = x1*speed
		twist.linear.y = y1*speed
		twist.linear.z = z1*speed
		twist.angular.x = 0
		twist.angular.y = 0
		twist.angular.z = th1*turn

		self.control_pub.publish(twist)
	
	def callback(self,data):
		try:
			cv_image = self.bridge.imgmsg_to_cv2(data, "bgr8")
		except CvBridgeError as e:
			print(e)

		
		if self.inicio == 1:   
			if self.contador ==1:
				cv_image = dp.procesamiento(cv_image,modelo)

				self.decision = md.prediccion(cv_image,modelo_robot)
				if self.decision == 0:
					self.control_robot(1,0,0,0)
					print('adelante')
				if self.decision == 1:
					self.control_robot(0,0,0,-1)
					print('derecha')
				if self.decision == 2:
					self.control_robot(0,0,0,1)
					print('izquierda')
				self.contador = 0
			self.contador = self.contador +1
				
				

		
		cv2.imshow("Imagen", cv_image) 
		key = cv2.waitKey(3)
		if key == ord('i'):
			self.inicio = 1
			print("Iniciar")
		if key == ord('d'):
			self.inicio = 0
			self.control_robot(0,0,0,0)
			print('Enviar orden detener')
						 
 




def main(args):
	ic = tesis_evasion()
	rospy.init_node('Principal', anonymous=True)
	try:
		rospy.spin()
	except KeyboardInterrupt:
		print("Terminado...")
	cv2.destroyAllWindows()

if __name__ == '__main__':
		main(sys.argv)
