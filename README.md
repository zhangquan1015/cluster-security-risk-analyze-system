# cluster-security-risk-analyze-system


目前欠缺的几个问题：
1. 有些是自定义镜像没有进行扫描，需要在后续进行升级
2. 有些公开镜像的版本号不一定检索得到，也许可以直接选用latest版本
3. 有些服务的depend_on存在问题，只能默认docker-compose是按照规则写的