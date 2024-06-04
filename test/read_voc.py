from PIL import Image
import os
import numpy as np
import matplotlib; matplotlib.use('TkAgg')
import matplotlib.pyplot as plt

font = {'family': 'serif',
        'size': 10
        }
matplotlib.rc('font', **font)

def read_file_list(root, is_train=True):
    txt_fname = root + '/ImageSets/Segmentation/' + ('trainval.txt' if is_train else 'val.txt')
    with open(txt_fname, 'r') as f:
        filenames = f.read().split()
    images = [os.path.join(root, 'JPEGImages', i + '.jpg') for i in filenames]
    labels = [os.path.join(root, 'SegmentationClass', i + '.png') for i in filenames]
    return images, labels  # file list

def label_color_img(label, img):
    palette = label.getpalette()
    label_np = np.array(label)
    new_label = np.array(img)
    width, height = img.size
    grouped_palette = [np.array(palette[i:i+3]).astype(new_label.dtype) for i in range(0, len(palette), 3)]


    for i, line in enumerate(label_np):
        for j, pix in enumerate(line):
            if pix != 0:
                new_label[i, j] = grouped_palette[pix]

    return new_label


def ReadVOC2012(voc_root="../VOC2012"):
    images, labels = read_file_list(voc_root, True)
    for i in range(len(images)):
        img = Image.open(images[i]).convert('RGB')
        img_np = np.array(img)
        label = Image.open(labels[i])
        label_img = label_color_img(label, img)


        label_np = np.array(label)
        nonzero_pixels = label_np[(label_np != 0) & (label_np != 255)]
        unique_values = np.unique(nonzero_pixels)
        print("标签真实值：", unique_values)


        plt.subplot(121), plt.imshow(img)
        plt.subplot(122), plt.imshow(label_img)
        plt.show()

def ReadImg_PattleLabel(img_dir="../output_data/X-Ray-VOC2012/JPEGImages/triangle7.jpg",
                        label_dir="../output_data/X-Ray-VOC2012/SegmentationClass/triangle7.png"):
    img = Image.open(img_dir).convert('RGB')
    label = Image.open(label_dir)
    label_img = label_color_img(label, img)

    label_np = np.array(label)
    nonzero_pixels = label_np[(label_np != 0) & (label_np != 255)]
    unique_values = np.unique(nonzero_pixels)
    print("标签真实值：", unique_values)

    plt.subplot(121)
    plt.title("XRay Gray Image")
    plt.imshow(img)

    plt.subplot(122)
    plt.title("Segmentation Mask")
    plt.imshow(label_img)
    plt.show()

# ReadVOC2012("../output_data/X-Ray-VOC2012")
ReadImg_PattleLabel()
ReadImg_PattleLabel(img_dir="../output_data/X-Ray-VOC2012/JPEGImages/ball7.jpg",
                    label_dir="../output_data/X-Ray-VOC2012/SegmentationClass/ball7.png")
ReadImg_PattleLabel(img_dir="../output_data/X-Ray-VOC2012/JPEGImages/cube7.jpg",
                    label_dir="../output_data/X-Ray-VOC2012/SegmentationClass/cube7.png")