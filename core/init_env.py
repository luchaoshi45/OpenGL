import os
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
