import os

def get_stl(directory):
    '''
    需要标注的stl文件，请名字 务必包含imp关键字
    不需要标注的stl文件，请名字 不要包含imp关键字
    '''
    Imps = []
    NoImps = []
    for root, dirs, files in os.walk(directory):
        for file in files:
            if "imp" in file and file.endswith(".stl"):
                Imps.append(file)
            elif file.endswith(".stl") and not file =="all.stl":
                NoImps.append(file)
    return Imps, NoImps
