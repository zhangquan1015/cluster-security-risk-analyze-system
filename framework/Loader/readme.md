loader_1.py
读取架构信息，在success_list，fail_list分别记录已读取结果
将架构特在保存在clusterInfo内部compose.yml同名+_image.txt的文件中

将所需要的镜像源保存在image内部compose.yml同名+_image.txt文件中

loader_2.py
```
if __name__ == "__main__":
    # yamlPath = "/home/zhangquan/code/cluster-security-risk-analysis-system/database/traefik-golang_compose.yaml"
    yamlPath = "/home/zhangquan/code/cluster-security-risk-analyze-system/framework/database/docker-prometheus.dockerapp_docker-compose.yml"
    loader(yamlPath)

```

./image/1.txt
1集群下需要什么镜像

./clusterInfo/a.txt
a集群内部的架构特征