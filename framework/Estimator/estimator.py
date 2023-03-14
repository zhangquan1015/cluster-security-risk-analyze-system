# 注意需要对具体返回值进行更新  对应exploit的标签
def exploit_helper(exploit):
    if exploit == "Not Defined":
        return 0
    elif exploit == "Unproven":
        return 0.5
    else:
        return 1

def patch_helper(patch):
    if patch == "Third Party Fix":
        return 0.8
    elif patch == "Official Fix":
        return 0.5
    else:
        return 1


def net_helper(container,cluster_dic):
    networks=cluster_dic['networks']
    num = 0
    for net in cluster_dic['containers_info'][container]['networks']:
        num += len(networks[net])
    return num

def fun_helper(container,cluster_dic):
    num = 1
    if len(cluster_dic['containers_info'][container]['children']) == 0:
        return num

    for child in cluster_dic['containers_info'][container]['children']:
        num += fun_helper(child,cluster_dic)
    return num

def Cost_attack(cve_dic):
    ESC = float(cve_dic['ESC'])
    return round(10-ESC,1)

def Cost_fix(cve_dic,k1 = 1,k2 = 1):
    ESC = float(cve_dic['ESC'])
    Patch = patch_helper(cve_dic['Patch'])
    Vul = exploit_helper(cve_dic['Exploit'])
    return round(Patch*(k1*ESC + k2*Vul),1)

def Risk(cve_dic,container,cluster_dic,w1 = 1,w2 = 1):
    ISC = float(cve_dic['ISC'])
    NetDep = net_helper(container,cluster_dic)
    FunDep = fun_helper(container,cluster_dic)
    return round(ISC*(w1*NetDep+w2*FunDep),1)




if __name__ == "__main__":
    cve_dic = {'CVE': 'CVE-2016-7942', 'ESC': 3.9, 'ISC': 5.9, 'BSC': 9.8, 'BaseSeverity': 'CRITICAL', 'CVSS': 'CVSS:3.0/AV:N/AC:L/PR:N/UI:N/S:U/C:H/I:H/A:H', 'CWE': ['CWE-264', 'CWE-787'], 'Exploit': 'Not Defined', 'Patch': 'Third Party Fix'}
    cluster_dic={"containers_info": {"vote": {"name": "vote", "image": "", "link": [], "parents": ["redis"], "networks": ["front-tier", "back-tier"], "children": []}, "result": {"name": "result", "image": "", "link": [], "parents": ["db"], "networks": ["front-tier", "back-tier"], "children": []}, "worker": {"name": "worker", "image": "", "link": [], "parents": ["redis", "db"], "networks": ["back-tier"], "children": []}, "redis": {"name": "redis", "image": "redis:5.0-alpine3.10", "link": [], "parents": [], "networks": ["back-tier"], "children": ["vote", "worker"]}, "db": {"name": "db", "image": "postgres:9.4", "link": [], "parents": [], "networks": ["back-tier"], "children": ["result", "worker"]}}, "containers": ["vote", "result", "worker", "redis", "db"], "images": ["redis:5.0-alpine3.10", "postgres:9.4"], "networks": {"front-tier": ["vote", "result"], "back-tier": ["vote", "result", "worker", "redis", "db"], "bridge": []}}
    # cve_dic['ESC'] = "2"
    # print(Cost_attack(cve_dic))
    print(cve_dic)
    print(Cost_attack(cve_dic))
    print(Cost_fix(cve_dic,1,1))
    print(net_helper('redis',cluster_dic))
    print(fun_helper('redis',cluster_dic))


# def Cost_attack(ESC):
#     return 10-ESC

# def Cost_fix(ESC,Vul,Patch,k1,k2):
#     return Patch*(k1*ESC + k2*Vul)

# def Risk(ISC,NetDep,FunDep,w1,w2):
#     return ISC*(w1*NetDep+w2*FunDep)