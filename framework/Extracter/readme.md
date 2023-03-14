[提取nvd信息](nvdparser.py)

提取nvd信息
输出范例
```
if __name__ == '__main__':
    # url="https://services.nvd.nist.gov/rest/json/cves/2.0?cveId=CVE-2020-8622"
    # cve = "CVE-2016-7948"

    cveDict = request_data("CVE-2015-8317")
    # print(cveDict['vulnerabilities'][0]['cve'])
    temp=parse_data(cveDict)
    print(temp)
```
{'CVE-ID': 'CVE-2016-7948', 'CVSS': ['3.0', 'CVSS:3.0/AV:N/AC:L/PR:N/UI:N/S:U/C:H/I:H/A:H'], 'CWE-ID': ['CWE-787'], 'Exploits': [], 'Patchs': [['Unknown', 'https://cgit.freedesktop.org/xorg/lib/libXrandr/commit/?id=a0df3e1c7728205e5c7650b2e6dce684139254a6']], 'CVSS  Metrics': {'version': '3.0', 'vectorString': 'CVSS:3.0/AV:N/AC:L/PR:N/UI:N/S:U/C:H/I:H/A:H', 'attackVector': 'NETWORK', 'attackComplexity': 'LOW', 'privilegesRequired': 'NONE', 'userInteraction': 'NONE', 'scope': 'UNCHANGED', 'confidentialityImpact': 'HIGH', 'integrityImpact': 'HIGH', 'availabilityImpact': 'HIGH', 'baseScore': 9.8, 'baseSeverity': 'CRITICAL'}}


filterdatabase.py
查看检索到的patch和exploit的版本类型
需要和exploit-DB绑定


nvdparser 查询漏洞信息
filter 对patch exploit进行过滤 保存信息于oldDB.csv

localDB最信息进行提取 储存重要信息到newDB.csv

