import nvdparser as parse
import filterdatabase as filter
import localdb as db
import csv
import assess
import pandas as pd
import os

# import pandas as pd
# print(db.Database)
# info = parse.filter_information("CVE-2015-8317")
# print(assess.calculate(info['vector'],info['version'],info['exploit'],info['fix']))
# cve = "CVE-2015-8317"

vulns_path=os.path.join(os.path.dirname(os.path.dirname(__file__)),"Scanner")
# cvelist = ["CVE-2015-8317"]
df = pd.read_csv(os.path.join(vulns_path,"vulns_list.csv"))
cvelist = df.CVEID.to_list()
# print(cvelist)
file = open('localdb.csv', mode='a',encoding='utf-8',newline='') #xixi为文件名称
csv_writer = csv.DictWriter(file,fieldnames=['CVE-ID','CVSS','CWE-ID','Exploits','Patchs','CVSS  Metrics'])
for cve in cvelist:
    print(cve)
    if cve in db.Database:
        print(db.Database[cve]['Prioritization Score'])
        # print(db.Database[cve])
    else:
        # csv_writer.writeheader()
        dic = parse.parse(cve)
        if not dic:
            continue    
        filterdic = filter.filter_information(dic)
        # print(dic)
        # print(file1)
        csv_writer.writerow(dic)
        prioritization_score = assess.calculate(filterdic)
        print(prioritization_score)
        db.update(dic,filterdic,prioritization_score)
        # print(prioritization_score)
        # db.Database()
