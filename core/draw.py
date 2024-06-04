#!/usr/bin/env python3

# Import packages
import os, copy
import numpy as np # Who does not use Numpy?
import cv2 # OpenCV
import matplotlib # To plot images
from PIL import Image
import imgviz

font = {'family': 'serif',
        'size': 15
        }
matplotlib.rc('font', **font)

def save_xray_image_front(output_dir, name, xray_image_front, flip=True, log_out=True):
    if flip:
        xray_image_front = np.flipud(xray_image_front)
    out = os.path.join(output_dir, name + ".jpg")
    # 保存图像为jpg格式
    img = 255*xray_image_front/(xray_image_front.max())
    # img = xray_image_front
    cv2.imwrite(out, img)
    if log_out:
        log_out = os.path.join(output_dir, name + "_log.jpg")
        img = np.log10(xray_image_front)
        img = 255 * img / (img.max())
        cv2.imwrite(log_out, img)

def save_binary_image_pattle(output_data, name, binary_image):
    out = os.path.join(output_data, name + ".png")
    # 创建调色板模式的 8 位图像
    palette_img = Image.fromarray(binary_image.astype(np.uint8), mode='P')

    # 转换成VOC格式的P模式图像
    colormap = imgviz.label_colormap()
    palette_img.putpalette(colormap.flatten())
    palette_img.save(out)

    # 保存图像
    # palette_img.save(out)

