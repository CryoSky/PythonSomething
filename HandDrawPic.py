# -*- coding:utf-8 -*-
# Code by cryosky, 2017-12-27, main part copied from https://www.icourse163.org/learn/BIT-1001870002?tid=1001963001#/learn/content?type=detail&id=1002794378&cid=1003153722 Python数据展示

from PIL import Image
import numpy as np


filename = input("Enter your image filename with suffix (should be in the same folder): ")

a = np.asarray(Image.open('./'+filename).convert('L')).astype('float')   #convert'L'将图像转为灰度图像

depth = 10. 						# (0-100)
grad = np.gradient(a)				#取图像灰度的梯度值，会有两个数组
grad_x, grad_y = grad 				#分别取横纵图像梯度值, a,b=c理解为返回一个元组，然后c里面的值分别放入a和b中
grad_x = grad_x*depth/100.
grad_y = grad_y*depth/100.
A = np.sqrt(grad_x**2 + grad_y**2 + 1.)
uni_x = grad_x/A
uni_y = grad_y/A
uni_z = 1./A

vec_el = np.pi/2.2 					# 光源的俯视角度，弧度值
vec_az = np.pi/4. 					# 光源的方位角度，弧度值
dx = np.cos(vec_el)*np.cos(vec_az) 	#光源对x 轴的影响
dy = np.cos(vec_el)*np.sin(vec_az) 	#光源对y 轴的影响
dz = np.sin(vec_el) 				#光源对z 轴的影响

b = 255*(dx*uni_x + dy*uni_y + dz*uni_z) 	#光源归一化
b = b.clip(0,255)                   #去除少数溢出值

im = Image.fromarray(b.astype('uint8')) 	#重构图像

realname = filename.split(".")[0]
suffix = filename.split(".")[1]
im.save('./'+realname+'_handsketch.'+suffix)

