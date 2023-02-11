import nvdparser as parse
import filterdatabase as filter
import localdb as db
import csv
import pandas as pd
import os

vulns_path=os.path.join(os.path.dirname(os.path.dirname(__file__)),"Scanner/vulns_list")

# cvelist = ["CVE-2016-7942"]
files = os.listdir(vulns_path)
# print(files)

# header = ('CVE-ID','CVSS','CWE-ID','Exploits','Patchs','CVSS  Metrics','ESC','ISC')
# with open('oldDB.csv', 'a', newline='') as f:
#     writer = csv.writer(f)
#     writer.writerow(header)

for file in files:
    # print(file)
    df = pd.read_csv(os.path.join(vulns_path,file))
    cvelist = df.VulnerabilityID.to_list()
    # cvelist = ["CVE-2016-7942"]
    # print(cvelist)

    file = open('oldDB.csv', mode='a',encoding='utf-8',newline='') #xixi为文件名称
    csv_writer = csv.DictWriter(file,fieldnames=['CVE-ID','CVSS','CWE-ID','Exploits','Patchs','CVSS  Metrics','ESC','ISC'])
    for cve in cvelist:
        # print(cve)
        if cve in db.Database:
            # print(db.Database[cve]['Prioritization Score'])
            # print(db.Database[cve])
            # print("已经存在")
            continue
        else:
            # csv_writer.writeheader()
            print(cve + "不存在")
            dic = parse.parse(cve)
            # print(dic)
            # 是空的即跳过这个CVE漏洞，否则继续运行
            if not dic:
                continue    
            filterdic = filter.filter_information(dic)
            csv_writer.writerow(dic)
            db.update(dic,filterdic)

