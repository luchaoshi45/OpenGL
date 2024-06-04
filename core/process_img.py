import numpy as np
import copy

def get_binary_image(xray_image_front, label_pix_value, flip=True):
    xray_image_front = copy.deepcopy(xray_image_front)
    if flip:
        xray_image_front = np.flipud(xray_image_front)
    # 保存图像为PNG格式
    img = 255*xray_image_front/(xray_image_front.max())
    binary_image = np.where(img >= 245-1e-3, 0, label_pix_value)
    return binary_image

