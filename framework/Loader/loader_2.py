import yaml


def helper(service,cluster_services,containers,containers_info,images,networks):
    # print(service)
    cluster_service = cluster_services[service]
    containers.append(service)
    containers_info[service] = {"name":service,"image":"","link":[],"parents":[],"networks":[],"children":[]}

    if 'image' in cluster_service:
        containers_info[service]['image'] = cluster_service['image']
        images.append(cluster_service['image'])
    if 'link' in cluster_service:
        for link in cluster_service['link']:
            containers_info[service]['link'].append(link)
    if 'networks' in cluster_service:
        for network in cluster_service['networks']:
            containers_info[service]['networks'].append(network)
            networks[network].append(service)
    else:
        containers_info[service]['networks'].append('bridge')
        networks['bridge'].append(service)
    if 'depends_on' in cluster_service:
        for depends_on in cluster_service['depends_on']:
            containers_info[service]['parents'].append(depends_on)
            if depends_on not in containers_info:
                helper(depends_on,cluster_services,containers,containers_info,images,networks)
            containers_info[depends_on]['children'].append(service)
    return

def loader(yamlPath):
    metadata = {}
    
    containers=[]
    containers_info={}
    images=[]
    networks={}

    f = open(yamlPath,'r',encoding='utf-8')
    myYaml = yaml.load(f,Loader=yaml.FullLoader)
    # print()
    cluster_services = []
    cluster_networks = []
    if 'services' in myYaml:
        cluster_services = myYaml['services']
    else:
        return
    if 'networks' in myYaml:
        for network in myYaml['networks']:
            cluster_networks.append(network)
    cluster_networks.append("bridge")
    # print(cluster_networks)
    for cluster_network in cluster_networks:
        networks[cluster_network]=[]

    for service in cluster_services:
        helper(service,cluster_services,containers,containers_info,images,networks)

        # cluster_service = cluster_services[service]
        # # container = {"key":"valu"}
        # # container = {"name":service,"image":"","link":[],"depends_on":[],"networks":[]}
        # # print(container)

        # # container['name'] = service
        # # print(service)
        # # print(type(service))
        # # print(cluster_services[service])
        # # containers.append(service)
        
        # containers.append(service)
        # containers_info[service] = {"name":service,"image":"","link":[],"parents":[],"networks":[],"children":[]}
        # # 有一些容器由dockerfile直接搭建，需要特别注意一下
       
        # if 'image' in cluster_service:
        #     containers_info[service]['image'] = cluster_service['image']
        #     images.append(cluster_service['image'])
        # if 'link' in cluster_service:
        #     for link in cluster_service['link']:
        #         containers_info[service]['link'].append(link)
        # if 'depends_on' in cluster_service:
        #     for depends_on in cluster_service['depends_on']:
        #         containers_info[service]['parents'].append(depends_on)
        # if 'networks' in cluster_service:
        #     for network in cluster_service['networks']:
        #         containers_info[service]['networks'].append(network)
        #         networks[network].append(service)
        # else:
        #     containers_info[service]['networks'].append('bridge')
        #     networks['bridge'].append(service)

        # # print(container)
        # # containers_info[container['name']] = container
        

    # 保存至元数据组
    metadata['containers_info'] = containers_info
    metadata['containers'] = containers
    metadata['images'] = images
    metadata['networks'] = networks

    # print(metadata)

    return metadata

if __name__ == "__main__":
    # yamlPath = "/home/zhangquan/code/cluster-security-risk-analysis-system/database/traefik-golang_compose.yaml"
    yamlPath = "/home/zhangquan/code/cluster-security-risk-analysis-system/database/react-express-mysql_compose.yaml"
    loader(yamlPath)

# metadata:{
#     containers_info:{
#         container1:{
#             name:""
#             image:""
#             link:[]
#             depend_on:[]
#             childs:[](还没有搭建)
#             network:[]
#         }
#     }
#     images:[]
#     containers:[]
#     networks:{
#         network1:[]
#         newwork2:[]
#     }   
# }