import requests


def parse_data(cve_id):
    # sleep(6) # 防止API访问受限
    url = f"https://services.nvd.nist.gov/rest/json/cves/2.0?cveId={cve_id}"
    req = requests.get(url, timeout=30)  # 请求连接
    req_jason = {}
    try:
        req_jason = req.json()  # 获取数据
    except Exception as ex:
        print("execption")
    cve_dict = {}
    cve_dict["ID"] = cve_id
    if req_jason:

        # 要保存的键
        Patchs = []
        Exploits = []

        # 获取CVE描述
        vuln_trunk = req_jason['vulnerabilities'][0]['cve']
        CVSSInfo = vuln_trunk['metrics']
        if 'references' in vuln_trunk:
            References = vuln_trunk['references']
        CVSSInfo = vuln_trunk['metrics']
        if 'references' in vuln_trunk:
            References = vuln_trunk['references']

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
                Exploits.append([advisory, url])
            if hasPatch:
                Patchs.append([advisory, url])
        CVSS = CVSSInfo['cvssMetricV30'][0]
        cvssData = CVSS['cvssData']

        cve_dict['BSC'] = cvssData['baseScore']
        cve_dict['ESC'] = CVSS['exploitabilityScore']
        cve_dict['ISC'] = CVSS['impactScore']
        cve_dict['NVD'] = cvssData['baseSeverity']
        cve_dict['Attack_Vector'] = cvssData['attackVector']
        cve_dict['Attack_Complexity'] = cvssData['attackComplexity']
        cve_dict['Privileges_Required'] = cvssData['privilegesRequired']
        cve_dict['User_Interaction'] = cvssData['userInteraction']
        cve_dict['Confidentiality'] = cvssData['confidentialityImpact']
        cve_dict['Integrity'] = cvssData['integrityImpact']
        cve_dict['Availability'] = cvssData['availabilityImpact']
        cve_dict['Exploit'] = filter_exploitation(Exploits)
        cve_dict['Patch'] = filter_remediation(Patchs)

    return cve_dict


# 漏洞利用类型 "" "PoC"("PoC" "EXP")
def filter_exploitation(exploits):
    if len(exploits) == 0:
        return
    return "PoC"


# 补丁类型 "Official Fix" "Third Party Fix" "Workaround" ""
def filter_remediation(patchs):
    if len(patchs) == 0:
        return
    fix = "Workaround"
    for patch in patchs:
        if "Advisory" in patch[0]:
            if "Offical" in patch[0]:
                return "Official Fix"
            fix = "Third Party Fix"
    return fix


if __name__ == '__main__':
    cve = parse_data("CVE-2009-5155")
    print(cve)
