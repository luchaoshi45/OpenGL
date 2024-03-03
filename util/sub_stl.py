import numpy as np
from stl import mesh

# 加载STL文件
def load_stl(file_path):
    mesh_data = mesh.Mesh.from_file(file_path)
    return mesh_data

# 保存STL文件
def save_stl(mesh_data, file_path):
    mesh_data.save(file_path)

# 对两个STL模型进行减法运算
def subtract_mesh(mesh1, mesh2):
    # 获取mesh2的顶点
    vertices2 = np.copy(mesh2.vectors.reshape(-1, 3))
    # 获取mesh1的顶点
    vertices1 = np.copy(mesh1.vectors.reshape(-1, 3))

    # 计算mesh1中不在mesh2中的点
    difference = []
    for vertex in vertices1:
        is_inside = False
        for vertex2 in vertices2:
            if np.all(vertex == vertex2):
                is_inside = True
                break
        if not is_inside:
            difference.append(vertex)

    # 创建新的Mesh对象
    mesh_difference = mesh.Mesh(np.array(difference, dtype=mesh.Mesh.dtype))
    return mesh_difference

if __name__ == "__main__":
    root = "../input_data/cudaball/"
    # 加载两个STL文件
    mesh_all = load_stl(root+"all.stl")
    mesh_part1 = load_stl(root+"imp.stl")

    # 进行减法运算
    mesh_part2 = subtract_mesh(mesh_all, mesh_part1)

    # 保存结果到新的STL文件
    save_stl(mesh_part2, root+"noimp.stl")
