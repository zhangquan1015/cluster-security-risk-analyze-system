import estimator as box
import dic_reader as reader
import os
import csv


cluster_path = os.path.join(os.path.dirname(os.path.dirname(__file__)),"Loader/clusterInfo")
for name in os.listdir(cluster_path):
    cluster_name = name[:-5]
    print("cluster_name:    "+cluster_name)
    cluster_dic = reader.cluster(cluster_name)


    results_path = os.path.join(os.path.dirname(__file__),"results")
    result_path = os.path.join(results_path,cluster_name +".csv")

    # if not os.path.exists(result_path):
    #     header = ('Container','Image','CVE-ID','NetDep','FunDep','Cost_Defender','Cost_Attacker','Risk')
    #     with open(result_path, 'a', newline='') as f:
    #         writer = csv.writer(f)
    #         writer.writerow(header)
    if os.path.exists(result_path):
        continue
    header = ('Container','Image','CVE-ID','NetDep','FunDep','Cost_Defender','Cost_Attacker','Risk')
    with open(result_path, 'a', newline='') as f:
        writer = csv.writer(f)
        writer.writerow(header)
    file = open(result_path, mode='a',encoding='utf-8',newline='') #xixi为文件名称
    csv_writer = csv.DictWriter(file,fieldnames=['Container','Image','CVE-ID','NetDep','FunDep','Cost_Defender','Cost_Attacker','Risk'])

    for container_name in cluster_dic['containers_info']:
        container_dic = cluster_dic['containers_info'][container_name]
        image_name = container_dic['image']
        cve_list = reader.getCVEList(image_name.replace(":","_"))
        if cve_list is None:
            continue
        for cve_id in cve_list:
            print(cve_id)
            result = {}
            cve_dic = reader.cve(cve_id)
            if cve_dic is None:
                print("This cve_dic is None: " + cve_id)
                continue
            result['Container'] = container_name
            result['Image'] = image_name
            result['CVE-ID'] = cve_id
            result['NetDep'] = box.net_helper(container_name,cluster_dic)
            result['FunDep'] = box.fun_helper(container_name,cluster_dic)
            result['Cost_Defender'] = box.Cost_attack(cve_dic)
            result['Cost_Attacker'] = box.Cost_fix(cve_dic)
            result['Risk'] = box.Risk(cve_dic,container_name,cluster_dic)
            csv_writer.writerow(result)

    
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

