import os
import json
import pandas as pd

# 当前文件所在文件夹的绝对路径
my_path = os.path.dirname(__file__)
# 当前文件所在文件夹的上一级的绝对路径
father_path = os.path.dirname(my_path)

cluster_path = os.path.join(father_path,'Loader/clusterInfo')
image_path = os.path.join(father_path,'Loader/image')
DB_path = os.path.join(father_path,'Extractor')
CVE_path = os.path.join(father_path,"Scanner/vulns_list")

def getCVEList(image_name):
    # print(len(image_name))
    if len(image_name) == 0:
        return
    df = pd.read_csv(os.path.join(CVE_path,image_name + '.csv'))
    cvelist = df.VulnerabilityID.to_list()
    return cvelist

def csv_to_dict(filename):
    try:
        with open(filename, 'r') as file:
            header, *lines = file.readlines()  # 读取文件数据（包含第一行列名）
            header = header.split(",")  # 第一行列名
            header = [i.strip() for i in header]  # 格式化
            lines = [i.strip() for i in lines]
            result = {}
            for counter, line in enumerate(lines):
                line_dict = {}
                for idx, item in enumerate(line.split(",")):
                    # print(item)
                    # print(header[idx])
                    line_dict[header[idx]] = item
                # print(line.split(",")[0])
                result[line.split(",")[0]] = line_dict
            return result
    except IOError as err:
        print("I/O error({0})".format(err))

def cve(cve_id):
    try:
        cve_dic_lists = csv_to_dict(os.path.join(DB_path,'newDB.csv'))
    # print(type(cve_dic_lists))
        return cve_dic_lists[cve_id]
    except KeyError as key:
        print("The key " + str(key) + " is not in the newDB")

# 读取cluster架构
def cluster(cluster_name):
    with open(cluster_path + "/" + cluster_name +".json",'r', encoding='UTF-8') as f:
        cluster_dic = json.load(f)
    return cluster_dic

def image(cluster_name):
    image_list = []
    with open(image_path + "/" + cluster_name +".txt",'r', encoding='UTF-8') as f:
        f = [i.strip() for i in f]
        for image in f:
            image_list.append(image)
    return image_list

if __name__ == "__main__":
    # print(my_path)
    # print(cluster_path)
    # print(image_path)
    # print(DB_path)
    # # print(cluster("example-voting-app_docker-compos_image"))
    # # print(csv_to_dict(DB_path+"/newDB.csv"))
    # # csv_to_dict(os.path.join(os.getcwd(), 'newDB.csv'))
    # # print(csv_to_dict(os.path.join(os.getcwd(), 'newDB.csv')))
    # cve(213)

    print(getCVEList("postgres_9.4"))