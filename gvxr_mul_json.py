has_mpl = True
try:
    import os  # Locate files
    import numpy as np  # Who does not use Numpy?
    from util import save_xray_image_front, save_xray_image_front_side_pdf, save_screen_shot
    import matplotlib.pyplot as plt  # Plotting
    from gvxrPython3 import gvxr  # Simulate X-ray images
    from gvxrPython3 import json2gvxr  # Set gVirtualXRay and the simulation up using a JSON file
    from gvxrPython3.utils import compareWithGroundTruth  # Plot the ground truth, the test image, and the relative error map in %
    from gvxrPython3.utils import plotScreenshot  # Visualise the 3D environment if Matplotlib is supported
except:
    has_mpl = False


# filename
input_data = "input_data"
output_data = "output_data"
object = "cudaball"
screen_shot_img = [None, None]

print(json2gvxr.initGVXR(os.path.join(input_data, object, "main.json"), "OPENGL"))
# Imps, NoImps = get_stl(os.path.join(input_data, object))
print(json2gvxr.initSourceGeometry())
print(json2gvxr.initSpectrum(verbose=0)) # l可以绘制光谱，详细见作者demo
print(json2gvxr.initDetector()) # np.loadtxt("Gate_data/responseDetector.txt") 可视化检测器相应
print(json2gvxr.initSamples(verbose=0))


# 可视化修正
gvxr.moveToCentre()
gvxr.displayScene()
gvxr.useLighing()
# gvxr.useWireframe()
gvxr.setZoom(400)
gvxr.setWindowBackGroundColour(1, 1, 1)
# import math
# angle = math.pi
# rotation_matrix_x = np.array([ 1, 0, 0, 0,
#                                0, math.cos(angle), -math.sin(angle), 0,
#                                0, math.sin(angle),  math.cos(angle), 0,
#                                0, 0, 0, 1])
# rotation_matrix_z = np.array([ math.cos(angle), -math.sin(angle), 0, 0,
#                                math.sin(angle),  math.cos(angle), 0, 0,
#                                0, 0, 1, 0,
#                                0, 0, 0, 1])
# rotation_matrix_x.shape = [4,4]
# rotation_matrix_z.shape = [4,4]
# transformation_matrix = np.identity(4)
# transformation_matrix = np.matmul(rotation_matrix_x, transformation_matrix)
# transformation_matrix = np.matmul(rotation_matrix_z, transformation_matrix)
# gvxr.setSceneRotationMatrix(transformation_matrix.flatten())
# gvxr.rotateNode("root", 180, 0, 0, 1)
gvxr.computeXRayImage()
gvxr.displayScene()
gvxr.displayScene()



# 出来二维图像
xray_image_front = np.array(gvxr.computeXRayImage()).astype(np.single)
save_xray_image_front(output_data, object, xray_image_front)
screen_shot_img[0] = save_screen_shot(os.path.join(output_data, object),"after material.png")
# Save the transformation matrix
transformation_matrix_backbup = gvxr.getNodeWorldTransformationMatrix("root")
# Rotate the object and compute the X-ray image
gvxr.rotateNode("root", 90, 1, 0, 0)
gvxr.computeXRayImage()
gvxr.displayScene()
gvxr.displayScene()
xray_image_side = np.array(gvxr.computeXRayImage()).astype(np.single)
screen_shot_img[1] = save_screen_shot(os.path.join(output_data, object),"Rotate after material.png")
save_xray_image_front_side_pdf(output_data, object, screen_shot_img, xray_image_front, xray_image_side)


# Restore the transformation matrix
gvxr.setNodeTransformationMatrix("root", transformation_matrix_backbup)
gvxr.computeXRayImage()
gvxr.displayScene()
gvxr.displayScene()
gvxr.renderLoop()



