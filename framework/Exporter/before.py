import pandas as pd
import os
import argparse

parser = argparse.ArgumentParser()
parser.add_argument('--budget', type=float, required=True, help='The remaining budget for the defender')
args = parser.parse_args()

# 创建一个空的列表来存储已修复的CVE，并创建一个变量来跟踪Cost_Defender的余额
fixed_cves = []
remaining_budget = args.budget  # 使用传入的参数作为初始的Cost_Defender余额
repaired_risk_sum = 0
vuln_repaired_count = 0
cost_fix_sum = 0

cluster=input("输入集群名称\n")
cluster='example-voting-app_docker-compos_image'
resource=float(input("输入可利用的修复资源\n"))
myPath = os.path.dirname(__file__)
# print(myPath)
filePath=os.path.join(os.path.join(os.path.dirname(myPath),'Estimator'),'results')
# fileName = os.path.join(filePath,sys.argv[1]+".csv")
fileName = os.path.join(filePath,cluster+".csv")
df = pd.read_csv(fileName)

cve_dict={}
cve_list = df['CVE'].to_list()
cost_list = df['Cost_Defender']
risk_list = df['Risk']

# 按照利润最大化对漏洞优先级进行排序
def profit_ratio(cve):
  cve_table = cve_dict[cve]
  if cve_table['cost'] == 0:
      return cve_table['risk'] / 0.01
  return cve_table['risk'] / cve_table['cost']

for i in range(len(cve_list)):
  cve_id = {}
  cve_id['cost']=cost_list[i]
  cve_id['risk']=risk_list[i]
  cve_dict[cve_list[i]]=cve_id
cve_list.sort(key=profit_ratio,reverse=True)

# print(cve_dict)
mincost=min(cost_list)
# print(mincost)
risk=0
strategy=[]
# 在成本限制下选择最大的利润
for cve in cve_list:
    if resource < mincost:
        break
    if resource >= cve_dict[cve]['cost']:
        resource -= cve_dict[cve]['cost']
        risk += cve_dict[cve]['risk']
        strategy.append(cve)
print("修复全部漏洞需要的资源："+str(sum(cost_list)))
print("最佳的修复策略：",end="")
for i in range(len(strategy)):
    if i != 0: 
        print('->',end='')
    if i < len(strategy) - 1:
        print(strategy[i],end='')
    else:
        print(strategy[i])
print("漏洞修复改善的风险分数：" + str(risk))