import yaml


def AST(service,cluster_services,containers,containers_info,images,networks):
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
    return

# 加载yaml文件的信息，生成AST
def loader(yamlPath):
    metadata = {}
    
    containers=[]
    containers_info={}
    images=[]
    networks={}

    f = open(yamlPath,'r',encoding='utf-8')
    myYaml = yaml.load(f,Loader=yaml.FullLoader)
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
        AST(service,cluster_services,containers,containers_info,images,networks)
    # 理清出父-子容器依赖关系
    for child in cluster_services:
        if containers_info[child]['parents'] is not None:
            for parent in containers_info[child]['parents']:
                containers_info[parent]['children'].append(child)
        

    # 保存至元数据组
    metadata['containers_info'] = containers_info
    metadata['containers'] = containers
    metadata['images'] = images
    metadata['networks'] = networks

    return metadata

if __name__ == "__main__":
    # yamlPath = "/home/zhangquan/code/cluster-security-risk-analysis-system/database/traefik-golang_compose.yaml"
    yamlPath = "/home/zhangquan/code/cluster-security-risk-analyze-system/framework/database/docker-prometheus.dockerapp_docker-compose.yml"
    tmp=loader(yamlPath)
    print(tmp)

