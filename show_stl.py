import vtk

# 创建一个读取器来读取STL文件
reader = vtk.vtkSTLReader()
reader.SetFileName("input_data/cudaball/cubeball.stl")
reader.Update()

# 创建一个mapper将数据映射到图形实体上
mapper = vtk.vtkPolyDataMapper()
mapper.SetInputConnection(reader.GetOutputPort())

# 创建一个演员来绘制STL模型
actor = vtk.vtkActor()
actor.SetMapper(mapper)

# 创建渲染器和渲染窗口
renderer = vtk.vtkRenderer()
renderer.AddActor(actor)
renderer.SetBackground(1.0, 1.0, 1.0)

renderWindow = vtk.vtkRenderWindow()
renderWindow.AddRenderer(renderer)

# 创建交互器
renderWindowInteractor = vtk.vtkRenderWindowInteractor()
renderWindowInteractor.SetRenderWindow(renderWindow)

# 设置交互器样式
style = vtk.vtkInteractorStyleTrackballCamera()
renderWindowInteractor.SetInteractorStyle(style)

# 开始渲染
renderWindow.Render()
renderWindowInteractor.Start()
