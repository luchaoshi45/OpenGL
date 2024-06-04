import os
import shutil, random
import numpy as np

from core import init, get_xray_img
from core import get_binary_image
from core import (save_xray_image_front, save_binary_image_pattle)

from gvxrPython3 import gvxr  # Simulate X-ray images

class VOC2012:
    # 初始化方法，用于设置对象的初始状态
    def __init__(self,
                 input_data='input_data',
                 output_data='output_data',
                 num_of_iter=100,
                 train_split_k=0.6,
                 objets=None
                 ):
        self.objets = objets
        if self.objets is None:
            self.objets = ["ball", "cube", "triangle"]

        self.num_of_iter = num_of_iter
        self.train_split_k = train_split_k
        self.input_data = input_data
        self.output_data = output_data

        ROOT = "X-Ray-VOC2012"
        self.JPEGImages = os.path.join(self.output_data, ROOT, "JPEGImages")
        self.SegmentationClass = os.path.join(self.output_data, ROOT, "SegmentationClass")
        self.ImageSets_Segmentation = os.path.join(self.output_data, ROOT, "ImageSets/Segmentation")

        self.clear_dir()
        self.mk_voc_dir()

    def clear_dir(self):
        try:
            if os.path.exists(self.output_data):
                shutil.rmtree(self.output_data)
        except Exception as e:
            print(e)
    def mk_voc_dir(self):
        os.makedirs(self.JPEGImages)
        os.makedirs(self.SegmentationClass)
        os.makedirs(self.ImageSets_Segmentation)

    def make_voc2012(self):
        for idx, object in enumerate(self.objets):
            self.make_one_object(object, idx+1, self.num_of_iter)
        self.split_voc()

    def split_voc(self):
        for _, _, imgs in os.walk(self.JPEGImages):
            num_train = int(self.train_split_k * len(imgs))
            train_imgs = random.sample(imgs, num_train)
            val_imgs = [file for file in imgs if file not in train_imgs]

        txts = ["trainval.txt", "train.txt", "val.txt"]
        txt_imgs = [imgs, train_imgs, val_imgs]

        for imgs, txt in zip(txt_imgs, txts):
            with open(os.path.join(self.ImageSets_Segmentation, txt), "w") as file:
                for item in imgs:
                    file.write("%s\n" % item[:-4])


    def make_one_object(self, object, label_pix_value, num_of_iter):
        '''
        :param object: gis工件的名称
        :param label_pix_value: gis工件的像素真值标签
        :return: None
        '''
        # 初始化仿真环境
        json2gvxr = init(self.input_data, object, "main.json")

        for i in range(num_of_iter):
            self.make_one_img(json2gvxr, object, label_pix_value, i)

    def make_one_img(self, json2gvxr, object, label_pix_value, num):

        angle = self.get_rotate_angle()
        # 获得关键部件的灰度图
        imp_gray, transformation_matrix = get_xray_img(json2gvxr, self.input_data, object, "imp.json",
                                                        self.gvxr_rotate, angle)

        main_gray = get_xray_img(json2gvxr, self.input_data, object, "main.json",
                                 self.gvxr_rotate, angle, transformation_matrix)


        # 转换关键部件的灰度图为二值化图像 label_pix_value 是标签真值
        imp_binary = get_binary_image(imp_gray, label_pix_value, True)
        save_binary_image_pattle(self.SegmentationClass, object + str(num), imp_binary)
        # 保存jpg
        save_xray_image_front(self.JPEGImages, object + str(num), main_gray, flip=True, log_out=False)

        # # 差分保存
        # imp_binary = get_binary_image(imp_gray, label_pix_value, True)
        # imp_no_gray = get_xray_img(json2gvxr, self.input_data, object, "imp_no.json",
        #                            self.gvxr_rotate, angle)
        # imp_no_binary = get_binary_image(imp_no_gray, label_pix_value, True)
        # # save_binary_image_pattle(self.SegmentationClass, "imp_binary" + str(num), imp_binary)
        # # save_binary_image_pattle(self.SegmentationClass, "imp_no_binary" + str(num), imp_no_binary)
        # # 保存mask
        # # 0和255的二值化图像 0是黑色 255是白色 255作为物体
        # mask_binary = np.maximum(imp_binary - imp_no_binary, 0)
        # save_binary_image_pattle(self.SegmentationClass, object+str(num), mask_binary)
        # # 保存jpg
        # save_xray_image_front(self.JPEGImages, object+str(num), main_gray, flip=True, log_out=False)

    def get_rotate_angle(self, low=0, high=360):
        random_angle = np.random.uniform(low, high)
        return random_angle
    def gvxr_rotate(self, angle):
        '''
        y轴逆时针随机旋转 回调函数
        :return: None
        '''
        gvxr.rotateNode("root", angle, 0, 1, 0)

if __name__ == "__main__":
    voc = VOC2012("../input_data", "../output_data", 10)
    voc.make_voc2012()
