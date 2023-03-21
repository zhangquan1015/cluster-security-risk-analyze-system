import json
import os
import terminal as shell
import function as func

# 定义路径信息   数据源路径
curPath = os.path.dirname(os.path.realpath(__file__))
frameworkPath = os.path.dirname(curPath)
dataPath = os.path.join(frameworkPath,"DB")
dataName = os.listdir(dataPath)


clusterPath = os.path.join(curPath,'clusterInfo')
shell.existsHelper(clusterPath)

imagePath = os.path.join(curPath,'image')
shell.existsHelper(imagePath)

file_success=open("./success_list",'a')
file_fail=open("./fail_list",'a')

# 对所有集群进行分析
for i in dataName:
    print(i)
    yamlPath = os.path.join(dataPath,i)
    try:
        clusterInfo = func.loader(yamlPath)

        file = i[0:-5]+"_image"
        # 保存架构信息
        f_cluster = open(os.path.join(clusterPath,file)+".json",'w')
        f_cluster.write(json.dumps(clusterInfo))
        # 保存集群中的镜像名称 
        f_image = open(os.path.join(imagePath,file)+".txt",'w')
        images = [line+"\n" for line in clusterInfo['images']]
        f_image.writelines(images)
        file_success.write(i+"\n")    

        f_image.close()
        f_cluster.close()
        print("正常：" + i)
    except:
        file_fail.write(i+"\n")
        print("异常：" + i)       
        
file_success.close()
file_fail.close()