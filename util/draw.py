#!/usr/bin/env python3

# Import packages
import os, copy
import numpy as np # Who does not use Numpy?
import cv2 # OpenCV
import matplotlib # To plot images
import matplotlib.pyplot as plt # Plotting
from matplotlib.colors import LogNorm # Look up table
from matplotlib.colors import PowerNorm # Look up table
from gvxrPython3 import gvxr  # Simulate X-ray images
from PIL import Image
import imgviz

font = {'family': 'serif',
        'size': 15
        }
matplotlib.rc('font', **font)
class Draw:
    # 初始化方法，用于设置对象的初始状态
    def __init__(self, outdir: str, object: str):
        self.name = outdir
        self.age = object
        self.check_and_create_directory(outdir, object)
    def check_and_create_directory(dir1, dir11):
        '''
        检查目录是否存在，不存在创出
        dir1/dir11
        '''
        dir = os.path.join(dir1, dir11)
        if not os.path.exists(dir):
            os.makedirs(dir)
def save_screen_shot(outdir: str, outname: str, title: str = "", show: bool = False):
    screenshot = gvxr.takeScreenshot()
    out = os.path.join(outdir, outname)
    if not os.path.exists(outdir):
        os.makedirs(outdir)
    if title== "":
        title = outname
    plt.imsave(out, np.array(screenshot))
    # or display it using Matplotlib
    if show:
        plt.figure(figsize=(10, 10))
        plt.imshow(screenshot)
        plt.title(title)
        plt.axis('off');
    return np.array(screenshot)

def save_xray_image_front(output_data, object, xray_image_front,
                          name="save_xray_image_front", flip=True,
                          log_out = True):
    if flip:
        xray_image_front = np.flipud(xray_image_front)
    out_dir = os.path.join(output_data, object)
    if not os.path.exists(out_dir):
        os.makedirs(out_dir)
    out = os.path.join(out_dir, name+".jpg")
    xray_image_front = copy.deepcopy(xray_image_front)
    # 保存图像为PNG格式
    # img = 255*xray_image_front/(xray_image_front.max() - xray_image_front.min())
    img = 255*xray_image_front/(xray_image_front.max())
    cv2.imwrite(out, img)

    if log_out:
        log_out = os.path.join(out_dir, name+"_log.jpg")
        img = np.log10(xray_image_front)
        img = 255 * img / (img.max())
        cv2.imwrite(log_out, img)

from matplotlib.backends.backend_pdf import PdfPages
def save_xray_image_front_side_pdf(output_data, object, screen_shot, xray_image_front, xray_image_side, flip=True):
    if flip:
        xray_image_front = np.flipud(xray_image_front)
    with PdfPages(os.path.join(output_data, object, "save_xray_image_front_side.pdf"), 'w') as pdf:
        # Plot the X-ray images
        fig, axarr = plt.subplots(1, 2, figsize=(12.5, 12.5 * 0.618))
        fig.suptitle("X-Ray Imaging Smulation")
        axarr[0].set_title("front view")
        imga = axarr[0].imshow(screen_shot[0])
        fig.suptitle("X-Ray Imaging Smulation")
        axarr[1].set_title("side view")
        imgb = axarr[1].imshow(screen_shot[1])
        pdf.savefig()
        plt.close()

        fig, axarr = plt.subplots(2, 2, figsize=(12.5, 12.5 * 0.618))
        # 设置子图间距
        plt.subplots_adjust(left=0.1, right=0.9, bottom=0.1, top=0.9, wspace=0.4, hspace=0.3)
        fig.suptitle("X-Ray Imaging Smulation")
        axarr[0][0].set_title("front view")
        img1 = axarr[0][0].imshow(xray_image_front, cmap="gray")
        axarr[0][1].set_title("side view")
        img2 = axarr[0][1].imshow(xray_image_side, cmap="gray")
        fig.colorbar(img2)

        axarr[1][0].set_title("front view log")
        img3 = axarr[1][0].imshow(xray_image_front, cmap="gray", norm=LogNorm())
        axarr[1][1].set_title("side view log")
        img4 = axarr[1][1].imshow(xray_image_side, cmap="gray", norm=LogNorm())
        fig.colorbar(img4)
        pdf.savefig()
        plt.close()


def get_binary_image(xray_image_front, label_pix_value, flip=True):
    if flip:
        xray_image_front = np.flipud(xray_image_front)
    xray_image_front = copy.deepcopy(xray_image_front)
    # 保存图像为PNG格式
    img = 255*xray_image_front/(xray_image_front.max())
    binary_image = np.where(img >= 255-1e-3, 0, label_pix_value)
    return binary_image

def save_binary_image_pattle(output_data, object, num, binary_image):
    check_and_create_directory(output_data, object)
    out = os.path.join(output_data, object, "label" + str(num) + ".png")
    # 创建调色板模式的 8 位图像
    palette_img = Image.fromarray(binary_image.astype(np.uint8), mode='P')

    # 转换成VOC格式的P模式图像
    colormap = imgviz.label_colormap()
    palette_img.putpalette(colormap.flatten())
    palette_img.save(out)

    # 保存图像
    # palette_img.save(out)

def check_and_create_directory(dir1, dir11):
    '''
    检查目录是否存在，不存在创出
    dir1/dir11
    '''
    dir = os.path.join(dir1, dir11)
    if not os.path.exists(dir):
        os.makedirs(dir)
