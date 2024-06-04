# import vtk
#
# # 创建一个读取器来读取STL文件
# reader = vtk.vtkSTLReader()
# reader.SetFileName("input_data/breaker/main.stl")
# reader.Update()
#
# # 创建一个mapper将数据映射到图形实体上
# mapper = vtk.vtkPolyDataMapper()
# mapper.SetInputConnection(reader.GetOutputPort())
#
# # 创建一个演员来绘制STL模型
# actor = vtk.vtkActor()
# actor.SetMapper(mapper)
#
# # 创建渲染器和渲染窗口
# renderer = vtk.vtkRenderer()
# renderer.AddActor(actor)
# renderer.SetBackground(1.0, 1.0, 1.0)
#
# renderWindow = vtk.vtkRenderWindow()
# renderWindow.AddRenderer(renderer)
#
# # 创建交互器
# renderWindowInteractor = vtk.vtkRenderWindowInteractor()
# renderWindowInteractor.SetRenderWindow(renderWindow)
#
# # 设置交互器样式
# style = vtk.vtkInteractorStyleTrackballCamera()
# renderWindowInteractor.SetInteractorStyle(style)
#
# # 开始渲染
# renderWindow.Render()
# renderWindowInteractor.Start()


import vtk

# 创建一个渲染器
renderer = vtk.vtkRenderer()

# 创建一个渲染窗口
render_window = vtk.vtkRenderWindow()
render_window.AddRenderer(renderer)

# 创建一个交互器
interactor = vtk.vtkRenderWindowInteractor()
interactor.SetRenderWindow(render_window)

root = './input_data/breaker/'
# 循环加载多个 STL 文件并显示
file_names = ["imp1.stl", "imp2.stl", "imp3.stl", "other.stl"]  # 替换为你的 STL 文件路径
file_names = [root+f for f in file_names]

for file_name in file_names:
    # 读取 STL 文件
    reader = vtk.vtkSTLReader()
    reader.SetFileName(file_name)
    reader.Update()

    # 创建一个 mapper
    mapper = vtk.vtkPolyDataMapper()
    mapper.SetInputConnection(reader.GetOutputPort())

    # 创建一个 actor
    actor = vtk.vtkActor()
    actor.SetMapper(mapper)

    # 添加 actor 到渲染器
    renderer.AddActor(actor)

# 设置渲染器的背景颜色
renderer.SetBackground(0.1, 0.2, 0.4)

# 设置渲染窗口的大小并启动交互器
render_window.SetSize(800, 600)
render_window.Render()
interactor.Start()

