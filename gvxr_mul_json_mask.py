from util import (save_xray_image_front, save_xray_image_front_side_pdf,
                  save_screen_shot, get_binary_image, save_binary_image_pattle)
from gvxrPython3 import gvxr  # Simulate X-ray images
import os  # Locate files
import numpy as np  # Who does not use Numpy?
import cv2

# filename
input_data = "input_data"
output_data = "output_data"
object = "cudaball"

def init(input_data, object, json):
    has_mpl = True
    try:
        import matplotlib.pyplot as plt  # Plotting
        from gvxrPython3 import gvxr  # Simulate X-ray images
        from gvxrPython3 import json2gvxr  # Set gVirtualXRay and the simulation up using a JSON file
        from gvxrPython3.utils import \
            compareWithGroundTruth  # Plot the ground truth, the test image, and the relative error map in %
        from gvxrPython3.utils import plotScreenshot  # Visualise the 3D environment if Matplotlib is supported
    except:
        has_mpl = False
    print(json2gvxr.initGVXR(os.path.join(input_data, object, json), "OPENGL"))
    # Imps, NoImps = get_stl(os.path.join(input_data, object))
    print(json2gvxr.initSourceGeometry())
    print(json2gvxr.initSpectrum(verbose=0))  # 绘制光谱，详细见作者demo
    print(json2gvxr.initDetector())  # np.loadtxt("Gate_data/responseDetector.txt") 可视化检测器相应
    return json2gvxr

def get_xray_img(json2gvxr, input_data, object, json):
    print(json2gvxr.initGVXR(os.path.join(input_data, object, json), "OPENGL"))
    print(json2gvxr.initSamples(verbose=0))
    # 可视化修正
    gvxr.moveToCentre()
    gvxr.displayScene()
    gvxr.useLighing()
    # gvxr.useWireframe()
    gvxr.setZoom(400)
    gvxr.setWindowBackGroundColour(1, 1, 1)
    # gvxr.rotateNode("root", 180, 0, 0, 1)
    # gvxr.rotateNode("root", 180, 0, 1, 0)
    gvxr.computeXRayImage()
    gvxr.displayScene()
    gvxr.displayScene()
    xray_image_front = np.array(gvxr.computeXRayImage()).astype(np.single)
    # gvxr.destroyAllWindows()
    return xray_image_front

def make_one_mask(input_data, object, num, label_pix_value):
    json2gvxr = init(input_data, object, "main.json")
    imp_gray = get_xray_img(json2gvxr, input_data, object, "imp.json")
    imp_binary = get_binary_image(output_data, object, imp_gray, label_pix_value, "imp_grayimg")
    noimp_gray = get_xray_img(json2gvxr, input_data, object, "noimp.json")
    noimp_binary = get_binary_image(output_data, object, noimp_gray,label_pix_value, "noimp_grayimg")

    # 0和255的二值化图像 0是黑色 255是白色 255作为物体
    mask_binary = np.maximum(imp_binary-noimp_binary, 0)
    save_binary_image_pattle(output_data, object, num, mask_binary)


    main_gray = get_xray_img(json2gvxr, input_data, object, "main.json")
    save_xray_image_front(output_data, object, main_gray, "img"+ str(num),flip=True,log_out=False)


make_one_mask(input_data, object, 1, 1)
gvxr.renderLoop()





