import csv

Database = {}
# CVE-ID	CVSS	CWE-ID	Exploitation	Remediation	CVSS  Metrics
f = open('newDB.csv','r',encoding='utf8')
reader = csv.DictReader(f)
# print(reader) # <csv.DictReader object at 0x000002241D730FD0>
for line in reader: # reader为了方便理解我们可以把它看成是一个列表嵌套OrderedDict(一种长相类似于列表的数据类型)
    Database[line['CVE']] = line

file = open('newDB.csv', mode='a',encoding='utf-8',newline='')
writer = csv.DictWriter(file,fieldnames=['CVE','ESC','ISC','BSC','BaseSeverity','CVSS','Exploit','Patch'])
# csv_writer = csv.DictWriter(file,fieldnames=['CVE-ID','CVSS','CWE-ID','Exploits','Patchs','CVSS  Metrics'])
# writer.writeheader()

def baseSeverity(baseScore):
    BSC = float(baseScore)
    if BSC == 0.0:
        return 'None'
    elif BSC < 4:
        return 'Low'
    elif BSC < 7:
        return 'Medium'
    elif BSC < 9:
        return 'High'
    else:
        return 'Critical'
        
def update(cvedict, filterdict):
    updatedict = {}
    updatedict['CVE'] = cvedict['CVE-ID']
    updatedict['ESC'] = cvedict['ESC']
    updatedict['ISC'] = cvedict['ISC']
    updatedict['BSC'] = cvedict['CVSS  Metrics']['baseScore']
    updatedict['BaseSeverity'] = baseSeverity(updatedict['BSC'])
    updatedict['CVSS'] = filterdict['vector']
    updatedict['Exploit'] = filterdict['exploit']
    updatedict['Patch'] = filterdict['fix']

    Database[updatedict['CVE']] = updatedict
    print(updatedict)
    writer.writerow(updatedict)
