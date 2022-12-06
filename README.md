# cluster-security-risk-analyze-system


目前欠缺的几个问题：
1. 有些是自定义镜像没有进行扫描，[自定义搭建镜像模块](./framework/Builder/)需要整合
2. 有些公开镜像的版本号不一定检索得到，也许可以直接选用latest版本
3. 有些服务的depend_on存在问题，只能默认docker-compose是按照规则写的
4. 暂未整合[漏洞扫描模块](./framework/Scanner/)，也许可以采用保存为tar包的形式进行扫描