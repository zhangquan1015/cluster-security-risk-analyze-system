from concurrent.futures import ThreadPoolExecutor, as_completed
import requests


# 使用 requests 库发送HTTP请求到NVD API。
# 为了使脚本更加健壮，对响应对象调用 raise_for_status() 方法，以在请求不成功时引发异常。
def get_cve_info(cve_id):
    url = f"https://services.nvd.nist.gov/rest/json/cves/2.0?cveId={cve_id}"
    try:
        response = requests.get(url, timeout=30)
        response.raise_for_status()
        cve_dict = parse_data(response.json(), cve_id)
    except (requests.exceptions.RequestException, ValueError) as ex:
        print(ex)
        cve_dict = {'ID': cve_id}
    return cve_dict


# 更新 parse_data() 函数，直接接收JSON数据作为输入，而不是发起单独的HTTP请求。
def parse_data(json_data, cve_id):
    cve_dict = {'ID': cve_id}

    # 要保存的键
    Patches = []
    Exploits = []
    References = []

    # 获取CVE描述
    vulnerability = json_data['vulnerabilities'][0]['cve']
    CVSSInfo = vulnerability['metrics']
    if 'references' in vulnerability:
        References = vulnerability['references']

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
            Patches.append([advisory, url])

    # 只获取CVSS3.X版本的数据 CVSS = CVSSInfo['cvssMetricV30'][0]
    if 'cvssMetricV30' in CVSSInfo:
        CVSS = CVSSInfo['cvssMetricV30'][0]
    elif 'cvssMetricV31' in CVSSInfo:
        CVSS = CVSSInfo['cvssMetricV31'][0]
    else:
        # 如果没有找到任何CVSS数据，抛出异常或者返回默认值等
        CVSS = None

    if CVSS:
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
        cve_dict['Patch'] = filter_remediation(Patches)
    return cve_dict


# 漏洞利用类型 "" "PoC"("PoC" "EXP")
def filter_exploitation(Exploits):
    if len(Exploits) == 0:
        return ''
    return "PoC"


# 补丁类型 "Official" "TTP" "Workaround" ""
def filter_remediation(Patches):
    if len(Patches) == 0:
        return ''
    fix = "Workaround"
    for patch in Patches:
        if "Advisory" in patch[0]:
            if "Official" in patch[0]:
                fix = "Official"
                break
            fix = "TTP"
    return fix


# get_cve_info_multi_threaded() 函数返回一个生成器，按照线程完成的顺序产生每个线程的结果。
def get_cve_info_multi_threaded(cve_ids):
    # 将最大工作线程数设置为10，但可以根据需要进行调整。
    with ThreadPoolExecutor(max_workers=10) as executor:
        futures = [executor.submit(get_cve_info, cve_id) for cve_id in cve_ids]
        for future in as_completed(futures):
            yield future.result()


if __name__ == '__main__':
    cve_list = ['CVE-2021-3156', 'CVE-2021-23243', 'CVE-2021-22986', 'CVE-2021-22987']
    cve_info_list = get_cve_info_multi_threaded(cve_list)
    for cve_info in cve_info_list:
        print(cve_info)