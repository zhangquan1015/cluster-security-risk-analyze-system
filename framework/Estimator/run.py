import estimator as box
import dic_reader as reader
import os
import csv


cluster_path = os.path.join(os.path.dirname(os.path.dirname(__file__)),"Loader/clusterInfo")
# print(os.listdir(cluster_path))
for name in os.listdir(cluster_path):
    cluster_name = name[:-5]
    print(cluster_name)
    # 
    # cve_dic = reader.cve(cve_id)
    cluster_dic = reader.cluster(cluster_name)
    # image_list = reader.image(cluster_name)


    # box.Cost_attack()
    # box.Cost_fix()
    # box.Risk()



    results_path = os.path.join(os.path.dirname(__file__),"results")
    # cve_list = reader.getCVE(image)

    header = ('Container','Image','CVE-ID','NetDep','FunDep','Cost_Defender','Cost_Attacker','Risk')
    with open(os.path.join(results_path,cluster_name +".csv"), 'a', newline='') as f:
        writer = csv.writer(f)
        writer.writerow(header)

    file = open(os.path.join(results_path,cluster_name +".csv"), mode='a',encoding='utf-8',newline='') #xixi为文件名称
    csv_writer = csv.DictWriter(file,fieldnames=['Container','Image','CVE-ID','NetDep','FunDep','Cost_Defender','Cost_Attacker','Risk'])

    for container_name in cluster_dic['containers_info']:
        # print(type(cluster_dic['containers_info']))
        # print(type(container_dic))
        container_dic = cluster_dic['containers_info'][container_name]
        image_name = container_dic['image']
        # print(container_dic)
        # print(image_name)
        cve_list = reader.getCVEList(image_name.replace(":","_"))
        if cve_list is None:
            continue
        for cve_id in cve_list:
            result = {}
            cve_dic = reader.cve(cve_id)
            result['Container'] = container_name
            result['Image'] = image_name
            result['CVE-ID'] = cve_id
            result['NetDep'] = box.net_helper(container_name,cluster_dic)
            result['FunDep'] = box.fun_helper(container_name,cluster_dic)
            result['Cost_Defender'] = box.Cost_attack(cve_dic)
            result['Cost_Attacker'] = box.Cost_fix(cve_dic)
            result['Risk'] = box.Risk(cve_dic,container_name,cluster_dic)
            csv_writer.writerow(result)

    # cve_dic = reader.cve(cve_id)
    # NetDep = box.net_helper("container",cluster_dic)
    # FunDep = box.fun_helper("container",cluster_dic)
    # Cost_Defender = box.Cost_attack(cve_dic)
    # Cost_Attacker = box.Cost_fix(cve_dic)
    # Risk = box.Risk(cve_dic,cluster_dic)
    
    # result['Container'] = "container"
    # result['Image'] = "image"
    # result['CVE-ID'] = cve_id
    # result['NetDep'] = NetDep
    # result['FunDep'] = FunDep
    # result['Cost_Defender'] = Cost_Defender
    # result['Cost_Attacker'] = Cost_Attacker
    # result['Risk'] = Risk

# 输出的结果格式
# Container,Image,CVE-ID,NetDep,FunDep,Cost_Defender,Cost_Attacker,Risk


if __name__ == "__main__":
    print(os.getcwd())
    print(os.path.dirname(__file__))
    # print(image_list)
    print(cve_dic)
    print(cluster_dic)