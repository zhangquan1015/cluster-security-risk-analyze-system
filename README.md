# cluster-security-risk-analyze-system


目前欠缺的几个问题：
1. 有些是自定义镜像没有进行扫描，[自定义搭建镜像模块](./framework/Builder/)需要整合
2. 有些公开镜像的版本号不一定检索得到，也许可以直接选用latest版本
3. 有些服务的depend_on存在问题，只能默认docker-compose是按照规则写
4. 暂未整合[漏洞扫描模块](./framework/Scanner/)，也许可以采用保存为tar包的形式进行扫描


# 模块设计
Loader
加载集群环境的配置文件，获取集群所需要的环境信息
Downloader
拉取集群容器所需要的基础镜像
Scanner
扫描镜像的漏洞信息
Extractor
提取漏洞的其他信息保存在本地数据库


Estimator
输入信息： k1 k2 
对集群内部的漏洞进行风险分析
Outer
输入信息   可利用修复成本  可利用攻击成本
输出信息   可修复漏洞信息及修复前后集群风险分数
