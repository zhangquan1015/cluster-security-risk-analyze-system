import csv
import argparse

parser = argparse.ArgumentParser()
parser.add_argument('--budget', type=float, required=True, help='The remaining budget for the defender')
args = parser.parse_args()

# 读取csv文件并转换为Python数据结构
with open('data.csv') as csvfile:
    reader = csv.DictReader(csvfile)
    data = list(reader)

# 对数据进行排序，以使Risk值最高的CVE排在最前面
sorted_data = sorted(data, key=lambda x: x['Risk'], reverse=True)

# 创建一个空的列表来存储已修复的CVE，并创建一个变量来跟踪Cost_Defender的余额
fixed_cves = []
remaining_budget = args.budget  # 使用传入的参数作为初始的Cost_Defender余额
repaired_risk_sum = 0
vuln_repaired_count = 0
cost_fix_sum = 0
# 在迭代排序后的CVE时，它检查Cost_Defender的余额是否足够修复当前CVE。如果余额足够，它将该CVE添加到已修复的列表中，并从Cost_Defender中扣除修复费用。否则，它跳过当前CVE。
for cve in sorted_data:
    if float(cve['Cost_Defender']) <= remaining_budget:
        repaired_risk_sum += float(cve['Risk'])
        vuln_repaired_count += 1
        fixed_cves.append(cve)
        remaining_budget -= float(cve['Cost_Defender'])
        cost_fix_sum += float(cve['Cost_Defender'])
        # print("修复 Container: {} 的 CVE: {}{}".format(cve['Container'], cve['CVE'],','),end='')
        # print("剩余修复Cost_Defender:{},已修复的Risk:{}".format(remaining_budget,repaired_risk_sum))

# 输出修复的漏洞数和修复的Risk的总和
print('修复的漏洞数为：', vuln_repaired_count)
print('修复的Risk的总和为：', repaired_risk_sum)
print('消耗的Cost_fix成本:',cost_fix_sum)

# # 按照CVE(Container)->CVE(Container)的顺序打印已修复的CVE和Container
# for i in range(len(fixed_cves)):
#     if i != 0: 
#         print('->',end='')
#     print("CVE: {} (Container: {})".format(fixed_cves[i]['CVE'], fixed_cves[i]['Container']),end='')
#     # print("CVE: {} (Container: {}) -> CVE: {} (Container: {})".format(fixed_cves[i]['CVE'], fixed_cves[i]['Container'], fixed_cves[i+1]['CVE'], fixed_cves[i+1]['Container']))
# print()
# 将已修复的CVE列表保存为新的csv文件
filename = 'fixed_cves.csv'
with open(filename, 'w', newline='') as csvfile:
    fieldnames = ['Container', 'Image', 'CVE', 'NetDep', 'FunDep', 'Cost_Defender', 'Cost_Attacker', 'Risk']
    writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
    writer.writeheader()
    for cve in fixed_cves:
        writer.writerow(cve)

print("已修复的CVE和Container已保存到文件: {}".format(filename))