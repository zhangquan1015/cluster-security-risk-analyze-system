import pandas as pd
import os
import sys
# fileName = "/home/zhangquan/code/cluster-security-risk-analyze-system/framework/Estimator/results/example-voting-app_docker-compos_image.csv"
myPath = os.path.dirname(__name__)
filePath=os.path.join(os.path.join(os.path.dirname(myPath),'Estimator'),'results')
fileName = os.path.join(filePath,sys.argv[1]+".csv")
df = pd.read_csv(fileName)

def profit_ratio(cve):
  cve_table = cve_dict[cve]
  if cve_table['cost'] == 0:
      return cve_table['risk'] / 0.01
  return cve_table['risk'] / cve_table['cost']



cve_dict={}
cve_list = df['CVE-ID'].to_list()
cost_list = df['Cost_Defender']
risk_list = df['Risk']

for i in range(len(cve_list)):
  cve_id = {}
  cve_id['cost']=cost_list[i]
  cve_id['risk']=risk_list[i]
  cve_dict[cve_list[i]]=cve_id
cve_list.sort(key=profit_ratio,reverse=True)



