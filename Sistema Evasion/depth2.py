#! /usr/bin/env python3


from lib.multi_depth_model_woauxi import RelDepthModel
from lib.net_tools import load_ckpt
import matplotlib.pyplot as plt
import torchvision.transforms as transforms
import cv2
import os
import argparse
import numpy as np
import torch


import matplotlib as mpl
import matplotlib.cm as cm


def scale_torch(img):
	"""
	Escale la imagen y envíela en torch.tensor.
	: param img: input rgb tiene forma [H, W, C], profundidad de entrada / disp tiene forma [H, W]
	: param scale: el factor de escala. flotador
	: return: img. [C, H, W] 
	"""
	if len(img.shape) == 2:
		 img = img[np.newaxis, :, :]
	if img.shape[2] == 3:
		 transform = transforms.Compose([transforms.ToTensor(),
		 transforms.Normalize((0.485, 0.456, 0.406) , (0.229, 0.224, 0.225) )])
		 img = transform(img)
	else:
		 img = img.astype(np.float32)
		 img = torch.from_numpy(img)
	return img		
 
def model():
	'''
	Funcion que carga el modelo
	'''
	parser = argparse.ArgumentParser(description='Configs for LeReS')
	parser.add_argument('--load_ckpt', default='./res50.pth')
	parser.add_argument('--backbone', default='resnet50')
	args = parser.parse_args()
	# create depth model
	depth_model = RelDepthModel(backbone=args.backbone)
	depth_model.eval()
	# load checkpoint
	modelo = load_ckpt(args, depth_model, None, None)
	depth_model.cuda() #Para utilizar la tarjeta grafica

	return depth_model

		
	
def procesamiento(rgb,depth_model):
	'''
	Funcion que realiza la inferencia con imagen rescalada a 448x448
	Devuelve la imagen disparidad de [0 0.1]
	'''
	rgb_c = rgb[:, :, ::-1].copy()
	A_resize = cv2.resize(rgb_c, (448, 448))
	rgb_half = cv2.resize(rgb, (rgb.shape[1]//2, rgb.shape[0]//2), interpolation=cv2.INTER_LINEAR)
	img_torch = scale_torch(A_resize)[None, :, :, :]
	pred_depth = depth_model.inference(img_torch).cpu().numpy().squeeze()
	pred_depth_ori = cv2.resize(pred_depth, (rgb.shape[1], rgb.shape[0]))
	prediccion = (pred_depth_ori/pred_depth_ori.max() * 255).astype(np.uint8)	

	return prediccion