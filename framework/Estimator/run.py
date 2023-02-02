import csv
import os

if (os.path.exists('results.csv')):
    os.remove('results.csv')

file_vulns = open('results.csv', mode='a',encoding='utf-8',newline='')
writer = csv.DictWriter(file_vulns,fieldnames=['Container','Image','CVE-ID','Cost_Defender','Cost_Attacker','Profit_Defender','Impact_Attacker',
'Topological dependency','Functional dependency','Risk'])
# ['CVE-ID','Threat','Exploitation','Remediation','CWE-ID','Prioritization Score','Prioritization Level'])
# architecturedict
# Container,Image,NetWork,Function

def update(cvedict, architecturedict,prioritization_score):
    updatedict = {}
    updatedict['CVE-ID'] = cvedict['CVE-ID']
    updatedict['Threat'] = filterdict['vector']
    updatedict['Exploitation'] = filterdict['exploit']
    updatedict['Remediation'] = filterdict['fix']
    updatedict['CWE-ID'] = cvedict['CWE-ID']
    updatedict['Prioritization Score'] = prioritization_score
    updatedict['Prioritization Level'] = prioritization_level(prioritization_score)
    Database[updatedict['CVE-ID']] = updatedict
    writer.writerow(updatedict)k

Database = {}
# CVE-ID	CVSS	CWE-ID	Exploitation	Remediation	CVSS  Metrics
f = open('localdbfilter.csv','r',encoding='utf8')
reader = csv.DictReader(f)
# print(reader) # <csv.DictReader object at 0x000002241D730FD0>
for line in reader: # reader为了方便理解我们可以把它看成是一个列表嵌套OrderedDict(一种长相类似于列表的数据类型)
    # print(line) # OrderedDict([('id', '1'), ('name', 'jason'), ('age', '18')]) 
    # print(line['id'],line['name'],line['age']) # 可以通过键进行索引取值（类似于字典）
    Database[line['CVE-ID']] = line
    # print(line['CVE-ID'])

file = open('localdbfilter.csv', mode='a',encoding='utf-8',newline='')
writer = csv.DictWriter(file,fieldnames=['CVE-ID','Threat','Exploitation','Remediation','CWE-ID','Prioritization Score','Prioritization Level'])
# csv_writer = csv.DictWriter(file,fieldnames=['CVE-ID','CVSS','CWE-ID','Exploits','Patchs','CVSS  Metrics'])
# writer.writeheader()
def update(cvedict, filterdict,prioritization_score):
    updatedict = {}
    updatedict['CVE-ID'] = cvedict['CVE-ID']
    updatedict['Threat'] = filterdict['vector']
    updatedict['Exploitation'] = filterdict['exploit']
    updatedict['Remediation'] = filterdict['fix']
    updatedict['CWE-ID'] = cvedict['CWE-ID']
    updatedict['Prioritization Score'] = prioritization_score
    updatedict['Prioritization Level'] = prioritization_level(prioritization_score)
    Database[updatedict['CVE-ID']] = updatedict
    writer.writerow(updatedict)

def prioritization_level(score):
    if 0.0 <= score < 3.0:
        # return "Defer"
        return "4"
    elif 3.0 <= score < 6.0:
        # return "Scheduled"
        return "3"
    elif 6.0 <= score < 9.0:
        # return "Out-of-Cycle" 
        return "2"   
    else:
        # return "Immediate"
        return "1"