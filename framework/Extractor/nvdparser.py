from time import sleep
import requests

def parse(cve):
    req_jason = request_data(cve)
    return parse_data(req_jason)
    # return CVE

def request_data(cve):
    sleep(6) # 防止API访问受限
    url="https://services.nvd.nist.gov/rest/json/cves/2.0?cveId=" + cve
    req = requests.get(url, timeout=30) # 请求连接
    req_jason = None
    try:
        req_jason = req.json() # 获取数据    
    except Exception as ex:
        print("execption")
        print(ex)
    return req_jason

CVE={}
# 若NVD中存在CVSS信息则提取关键信息，若不存在则返回null
def parse_data(req_jason):
    if req_jason is None:
        print('req_jason is None')
        return
    CVEID=""
    # CVSSV2={}
    # CVSSV3={}
    CWEINFO=[]
    Patch=[]
    Exploit=[]
    # 提取 cve的相关信息
    # 1. 获取包含所需信息的dict
    # 2. 选择合适的键值 
        #   "id" -> cve-id
        #   "metrics" -> CVSS Metrics
        #   "weaknesses" -> CWE-ID 
        #   "references" -> Patch Exploit
    # 3. 需要保存的键值信息 
    #   "metrics": cvssMetricV31,cvssMetricV2
    #   "references": 遍历所有refs
        # 检查tags是否包含Patch 或者 Exploit 等字样
        # Patch 记录 url Patch类型（Third Party Advisory，Vendor Advisory）
        # Exploit
    vuln_trunk = req_jason['vulnerabilities'][0]['cve']# 获取vulnerabilities键值下的cve的dict
    # time_now = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S") #获取当前时刻
    CVEInfo = vuln_trunk['id']
    CVSSInfo = vuln_trunk['metrics']
    if 'weaknesses' in vuln_trunk:
        CWEInfo = vuln_trunk['weaknesses']
    if 'references' in vuln_trunk:
        References = vuln_trunk['references']

    CVEID = CVEInfo

    # CVSSV2 = CVSSInfo['cvssMetricV2'][0]
    # CVSSV3 = CVSSInfo['cvssMetricV31'][0]

    # if CVSSInfo.has_key('cvssMetricV31'):
    if 'cvssMetricV31' in CVSSInfo:
        # 如果V3不为空保存V3
        # print("V31")
        CVSS = CVSSInfo['cvssMetricV31'][0]
    elif 'cvssMetricV30' in CVSSInfo:
        # 如果V3不为空保存V3
        # print("V30")
        CVSS = CVSSInfo['cvssMetricV30'][0]
    elif 'cvssMetricV2' in CVSSInfo:
        # 反之保存V2
        # print("保存V2")
        CVSS = CVSSInfo['cvssMetricV2'][0]
    else:
        # 不存在CVSS的话返回null 不存在CVSS的话没有识别的意义
        print("NVD中不存在该漏洞信息")
        return
    # if CVSSV3:
    #     # 如果V3不为空保存V3
    #     CVSS = CVSSV3
    #     print("保存V3")
    # elif CVSSV2:
    #     CVSS = CVSSV2
    #     # 反之保存V2
    #     print("保存V2")
    # else:
    #     # 不存在CVSS的话返回null 不存在CVSS的话没有识别的意义
    #     return

    # 遍历所有weaknesses ，记录CVE对应的所有CWE
    for i in CWEInfo:
        for j in i['description']:
            CWEINFO.append(j['value'])

    # 记录发现到的所有Exploit以及Patch格式为 list(advisory+url) 
    for i in References:
        if 'tags' not in i:
            continue
        tags = i['tags']
        url = i['url']
        advisory = "Unknown"
        hasExploit = False
        hasPatch = False
        for j in tags:
            if j == "Exploit":
                hasExploit = True
            elif j == "Patch":
                hasPatch = True
            elif "Advisory" in j:
                advisory = j

        if hasExploit:
            Exploit.append([advisory,url])
        if hasPatch:
            Patch.append([advisory,url])
    # CVE ID,CVSS Metrics,Attack Vector ,Attack Complexity,Privileges Required,User Interaction,Scope ,Confidentiality,Integrity,Availability,CWE ID,Threat,Exploit Code Maturity,Remediation Level,Prioritization Score,Prioritization Level
    CVE['CVE-ID'] = CVEID
    # 'version': '2.0'
    CVE['CVSS'] = [CVSS['cvssData']['version'],CVSS['cvssData']['vectorString']]
    # 'accessVector': 'NETWORK', 'accessComplexity': 'LOW', 'authentication': 'NONE', 'confidentialityImpact': 'PARTIAL', 'integrityImpact': 'NONE', 'availabilityImpact': 'NONE'
    # 'baseScore': 5.0, 'baseSeverity': 'MEDIUM'
    CVE['CWE-ID'] = CWEINFO
    CVE['Exploits'] = Exploit
    CVE['Patchs'] = Patch
    CVE['CVSS  Metrics'] = CVSS['cvssData']
    # CVEList.append([CVEID,CVE])
    return CVE




# class CVSSMetrics:
#     # version = ""
#     # attack_vector = ""
#     # attack_complexity = ""
#     # privileges_required = ""
#     # user_interaction = ""
#     # scope = ""
#     # confidentiality = ""
#     # integrity = ""
#     # availability = ""
#     def __init__(self, attack_vector, attack_complexity,privileges_required,user_interaction):
#         self.attack_vector = attack_vector
#         self.attack_complexity = attack_complexity
#         self.privileges_required = privileges_required
#         self.user_interaction = user_interaction

# CVE-ID,Threat,Exploitation,Remediation,CWE-ID,Prioritization Score,Prioritization Level,CVSS Metrics
# Attack Vector ,Attack Complexity,Privileges Required,User  Interaction,Scope ,Confidentiality,Integrity,Availability

# def getThreat():
#     return CVE['CVSSMetrics'] 
# def getExploit():
#     return CVE['Exploits']
# def getPatch():
#     return CVE['Patchs']


            

# CVE-ID CVSSMetrics(CVSSScore AV AC UI PR CIA) CWE-ID Patchs Exploits
if __name__ == '__main__':
    # url="https://services.nvd.nist.gov/rest/json/cves/2.0?cveId=CVE-2020-8622"
    # cve = "CVE-2016-7948"

    cveDict = request_data("CVE-2016-7948")
    # print(cveDict['vulnerabilities'][0]['cve'])
    temp=parse_data(cveDict)
    print(temp)