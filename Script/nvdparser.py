import logging
from typing import Any, Dict, List
from concurrent.futures import ThreadPoolExecutor, as_completed
import requests

logging.basicConfig(level=logging.DEBUG)


# 使用 requests 库发送HTTP请求到NVD API。
# 为了使脚本更加健壮，对响应对象调用 raise_for_status() 方法，以在请求不成功时引发异常。
def get_cve_info(cve_id: str, session: requests.Session) -> Dict[str, Any]:
    url = f"https://services.nvd.nist.gov/rest/json/cves/2.0?cveId={cve_id}"
    try:
        response = session.get(url, timeout=30)
        response.raise_for_status()
        cve_dict = parse_data(response.json(), cve_id)
    except (requests.exceptions.RequestException, ValueError) as ex:
        logging.error(f"An error occurred when requesting CVE {cve_id}: {ex}")
        cve_dict = {'ID': cve_id}
    return cve_dict


# 更新 parse_data() 函数，直接接收JSON数据作为输入，而不是发起单独的HTTP请求。
def parse_data(json_data: Dict[str, Any], cve_id: str) -> Dict[str, Any]:
    cve_dict: Dict[str, Any] = {'ID': cve_id}

    # 获取CVE描述
    vulnerability = json_data['vulnerabilities'][0]['cve']
    CVSSInfo = vulnerability['metrics']
    References = vulnerability.get('references', [])

    # 将Exploits和Patches筛选为满足条件的项的列表
    Exploits = [[i['tags'], i['url']] for i in References if 'Exploit' in i['tags']]
    Patches = [[i['tags'], i['url']] for i in References if 'Patch' in i['tags']]

    # 只获取CVSS3.X版本的数据 CVSS = CVSSInfo['cvssMetricV30'][0]
    if 'cvssMetricV30' in CVSSInfo:
        CVSS = CVSSInfo['cvssMetricV30'][0]
    elif 'cvssMetricV31' in CVSSInfo:
        CVSS = CVSSInfo['cvssMetricV31'][0]
    else:
        # 如果没有找到任何CVSS数据，抛出异常或者返回默认值等
        CVSS = None

    # 将数据添加到字典中
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
        cve_dict['Exploits'] = Exploits
        cve_dict['Patches'] = Patches

    return cve_dict


# 漏洞利用类型 "" "PoC"("PoC" "EXP")
def filter_exploitation(Exploits):
    if len(Exploits) == 0:
        return ''
    return "PoC"


# 补丁类型 "Official" "TTP" "Workaround" ""
def filter_remediation(Patches):
    if Patches is None:
        return None

    for patch, url in Patches:
        if "Official Advisory" in patch:
            return "Official"

    for patch, url in Patches:
        if "Third Party Advisory" in patch:
            return "TTP"

    return "Workaround"


def get_cve_info_concurrent(cve_list: List[str]) -> List[Dict[str, Any]]:
    session = requests.Session()
    with ThreadPoolExecutor(max_workers=20) as executor:
        futures = [executor.submit(get_cve_info, cve_id, session) for cve_id in cve_list]

    results = []
    for future in as_completed(futures):
        result = future.result()
        results.append(result)

    session.close()
    return results


if __name__ == '__main__':
    cve_list = ['CVE-2021-3156', 'CVE-2021-23243', 'CVE-2021-22986', 'CVE-2021-22987']
    cve_info_list = get_cve_info_concurrent(cve_list)
    for cve_info in cve_info_list:
        print(cve_info)
