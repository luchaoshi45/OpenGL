#!/usr/bin/env python3

# Import packages
import os, copy
import numpy as np # Who does not use Numpy?
import cv2 # OpenCV

has_mpl = True
try:
    from util import save_xray_image_front, save_xray_image_front_side_pdf, save_screen_shot
    import matplotlib.pyplot as plt  # Plotting
    from gvxrPython3 import gvxr  # Simulate X-ray images
    from gvxrPython3.utils import compareWithGroundTruth  # Plot the ground truth, the test image, and the relative error map in %
    from gvxrPython3.utils import plotScreenshot  # Visualise the 3D environment if Matplotlib is supported
except:
    has_mpl = False


# filename
input_data = "input_data"
output_data = "output_data"
object = "cudaball"
parts_list = ["ball.stl","cube.stl"]
screen_shot_img = [None, None]
# materials = ["Al", "Fe"] # 对应 parts_list
materials = [
    ((22, 13, 23), (0.9, 0.06, 0.04)),
    ((62, 78, 41), (0.4, 0.59, 0.01)),
] # 对应 parts_list
density = [4.43, 6.94]
part_files = [(input_data+"/"+object+"/"+i) for i in parts_list]


gvxr.createOpenGLContext()
gvxr.setWindowSize(512,512)
gvxr.setSourcePosition(0.0, -20.0, 0.0, "cm")
gvxr.usePointSource()
gvxr.setMonoChromatic(0.5, "MeV", 1000)
gvxr.setDetectorNumberOfPixels(1920, 1024)
gvxr.setDetectorPixelSize(0.1, 0.1, "mm")
gvxr.setDetectorPosition(0.0, 10.0, 0.0, "cm")
gvxr.setDetectorUpVector(0, 0, -1)

for part_id, part_fname in zip(parts_list, part_files):
    gvxr.loadMeshFile(part_id, part_fname, "mm")
# transformation_matrix_backbup1 = gvxr.getNodeWorldTransformationMatrix("root")
gvxr.translateNode("root", 0.0, -20.0, 0.0, "cm")
gvxr.moveToCentre()
gvxr.displayScene()
# transformation_matrix_backbup2 = gvxr.getNodeWorldTransformationMatrix("root")

# Set the materials
for part_id, part_material, part_Density in zip(parts_list, materials, density):
     # gvxr.setElement(part_id, part_material)
     # gvxr.setMixture("Dragon", "Ti90Al6V4")
     gvxr.setMixture(part_id, part_material[0], part_material[1])
     gvxr.setDensity(part_id, part_Density, "g/cm3")
xray_image_front = np.array(gvxr.computeXRayImage()).astype(np.single)
gvxr.displayScene()
gvxr.displayScene()
screen_shot_img[0] = save_screen_shot(os.path.join(output_data, object),"after material.png")



# Save the transformation matrix
transformation_matrix_backbup = gvxr.getNodeWorldTransformationMatrix("root")
# Rotate the object and compute the X-ray image
gvxr.rotateNode("root", 90, 1, 0, 0)
xray_image_side = np.array(gvxr.computeXRayImage()).astype(np.single)
gvxr.displayScene()
gvxr.displayScene()
screen_shot_img[1] = save_screen_shot(os.path.join(output_data, object),"Rotate after material.png")
# Restore the transformation matrix
gvxr.setNodeTransformationMatrix("root", transformation_matrix_backbup)



save_xray_image_front(output_data, object, xray_image_front)
save_xray_image_front_side_pdf(output_data, object, screen_shot_img, xray_image_front, xray_image_side)
gvxr.renderLoop()



