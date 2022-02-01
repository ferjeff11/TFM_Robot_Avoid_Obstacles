#! /usr/bin/env python3

#Librerias a utilizar
import numpy as np
from keras.preprocessing import image
import cv2
from keras.models import load_model


 
def modelo_rob():
	'''
	Funcion que devuelve el modelo entrenado
	Clase 0 = adelante
	Clase 1 = derecha
	clase 2 = izquierda
	'''	
	modelo_desicion_1 = load_model('decision_model.h5')
	return modelo_desicion_1

		
	
def prediccion(depth,new_model):
	'''
	Funcion que realiza la inferencia y reduciendo la resolucion
	de la imagen a mitad
	'''		
	img=cv2.resize(depth, dsize=(240,320))
	x = image.img_to_array(img)
	x = np.expand_dims(x, axis=0)
	classes = new_model.predict(x)
	clase = np.argmax(classes[0])
	
	return clase












	
