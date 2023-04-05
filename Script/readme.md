F:\Study\project\cluster-security-risk-analyze-system\Script\load_net.py
例如，如果您运行以下命令：
~~~shell
python script.py docker-compose.yaml networks.json
~~~
它将读取名为 docker-compose.yaml 的文件，将网络和服务信息保存为名为 networks.json 的文件。

保存格式

~~~json
{
  "my_network": [
    "web",
    "db"
  ],
  "bridge": [
    "another_service"
  ]
}
~~~



F:\Study\project\cluster-security-risk-analyze-system\Script\load_dep.py

在终端中，您可以使用以下命令来运行这个代码：

```shell
python example.py docker-compose.yaml depends_on.json
```

其中，`docker-compose.yaml`是您的Docker Compose文件的名称，`depends_on.json`是您希望保存结果的文件的名称。您可以根据实际情况修改这些参数。

```json
{
  "db": ["web", "worker", "scheduler"],
  "cache": ["web", "worker", "scheduler"]
}
```

[nvdparser.py](nvdparser.py)
提供API爬取NVD页面的数据


1. 解析docker-compose.yaml文件，获取每个service的image和build
   保存为compose.csv 格式 service,image,build
2. 对于service的build，查找路径下的Dockerfile
3. 解析Dockerfile，获取baseimage(From),保存为image
4. 更新service的image项
   service,image
5. 多线程下拉取image
6. 多线程下扫描image漏洞
7. 多线程下爬取NVD