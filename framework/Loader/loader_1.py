import json
import os
import loader_2

# curPath = os.path.dirname(os.path.realpath(__file__))
# curPath = os.path.dirname(curPath)
# curPath = os.path.dirname(curPath)
# dataPath = os.path.join(curPath,"database")
# print(dataPath)
# os.
# print(os.path.realpath(__file__))
curPath = os.path.dirname(os.path.realpath(__file__))
frameworkPath = os.path.dirname(curPath)
dataPath = os.path.join(frameworkPath,"database")
dataName = os.listdir(dataPath)

# 删除非空路径
def remove_dir(dir):
    dir = dir.replace('\\', '/')
    if(os.path.isdir(dir)):
        for p in os.listdir(dir):
            remove_dir(os.path.join(dir,p))
        if(os.path.exists(dir)):
            os.rmdir(dir)
    else:
        if(os.path.exists(dir)):
            os.remove(dir)
# 初始化文件夹
def existsHelper(path):
    if os.path.exists(path):
        remove_dir(path)
    os.mkdir(path)

clusterPath = os.path.join(curPath,'clusterInfo')
existsHelper(clusterPath)
# if os.path.isdir(clusterPath):
#     remove_dir(clusterPath)
# os.mkdir(clusterPath)

imagePath = os.path.join(curPath,'image')
existsHelper(imagePath)
# if os.path.isdir(imagePath):
#     remove_dir(imagePath)
# os.mkdir(imagePath)


file_success=open("./success_list",'a')
file_fail=open("./fail_list",'a')
for i in dataName:
    print(i)
    yamlPath = os.path.join(dataPath,i)
    try:
        clusterInfo = loader_2.loader(yamlPath)

        file = i[0:-5]+"_image"
        # print(file)
        # print(clusterInfo)
        # file = open(clusterInfo['containers_info'])
        # print(imagePath+"/"+file)
        f_cluster = open(os.path.join(clusterPath,file)+".txt",'w')

        # write() argument must be str, not dict
        # f_cluster.write(clusterInfo)
        f_cluster.write(json.dumps(clusterInfo))

        f_image = open(os.path.join(imagePath,file)+".txt",'w')
        images = [line+"\n" for line in clusterInfo['images']]
        f_image.writelines(images)
        
        f_image.close()
        f_cluster.close()
        file_success.write(i+"\n")
        print("正常："+i)
    except:
        print("ERROR：" + i)
        file_fail.write(i+"\n")       
