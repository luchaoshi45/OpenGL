from core import VOC2012

objets = ["ball", "cube", "triangle"] # 第一个label对于像素值为 1
# objets = ["breaker", "ball", "cube", "triangle"] # 第一个label对于像素值为 1
objets = ["breaker"] # 第一个label对于像素值为 1
num_of_iter = 5

voc = VOC2012("./input_data", "./output_data",
              num_of_iter=num_of_iter,
              train_split_k=0.6,
              objets=objets)

voc.make_voc2012()
