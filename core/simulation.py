import os
import numpy as np
from gvxrPython3 import gvxr  # Simulate X-ray images

def get_xray_img(json2gvxr, input_data, object, json, gvxr_callback=None, angle=None, transformation_matrix=None):
    print(json2gvxr.initGVXR(os.path.join(input_data, object, json), "OPENGL"))
    print(json2gvxr.initSamples(verbose=0))

    # print(json2gvxr.initSourceGeometry())
    # print(json2gvxr.initSpectrum(verbose=0))  # 绘制光谱，详细见作者demo
    # print(json2gvxr.initDetector())  # np.loadtxt("Gate_data/responseDetector.txt") 可视化检测器相应

    if transformation_matrix is None:
        # 可视化修正
        gvxr.moveToCentre()
        transformation_matrix = gvxr.getNodeWorldTransformationMatrix("root")

        gvxr.useLighing()
        # gvxr.useWireframe()
        gvxr.setZoom(400)
        gvxr.setWindowBackGroundColour(1, 1, 1)
        if gvxr_callback and angle is not None:
            gvxr_callback(angle)
        # gvxr.rotateNode("root", 180, 0, 0, 1)
        # gvxr.rotateNode("root", 180, 0, 1, 0)
        gvxr.computeXRayImage()
        gvxr.displayScene()
        gvxr.displayScene()
        xray_image_front = np.array(gvxr.computeXRayImage()).astype(np.single)
        # gvxr.renderLoop()

        # gvxr.destroyAllWindows()
        return xray_image_front, transformation_matrix
    else:
        gvxr.setNodeTransformationMatrix("root", transformation_matrix)
        gvxr.useLighing()
        # gvxr.useWireframe()
        gvxr.setZoom(400)
        gvxr.setWindowBackGroundColour(1, 1, 1)
        if gvxr_callback and angle is not None:
            gvxr_callback(angle)
        # gvxr.rotateNode("root", 180, 0, 0, 1)
        # gvxr.rotateNode("root", 180, 0, 1, 0)
        gvxr.computeXRayImage()
        gvxr.displayScene()
        gvxr.displayScene()
        xray_image_front = np.array(gvxr.computeXRayImage()).astype(np.single)
        gvxr.renderLoop()

        # gvxr.destroyAllWindows()
        return xray_image_front