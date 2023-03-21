import pandas as pd
import os
import argparse

# 创建 ArgumentParser 对象
parser = argparse.ArgumentParser()

# 添加参数
parser.add_argument('--cluster', type=str, help='input value')
parser.add_argument('--budget', type=float, help='The remaining budget for the defender')

# 解析参数
args = parser.parse_args()

if args.cluster:
    # 如果命令行参数中指定了 input 参数，则使用命令行参数的值
    cluster_name = args.cluster
else:
    # 否则，从标准输入中获取 input 参数的值
    cluster_name = input("Please enter the name of the cluster to evaluate: ")

if args.budget:
    cost_defender_limit = args.budget
else:
    cost_defender_limit = int(input("Please enter the cost limit: "))


# 读取csv1和csv2文件
estimator_path = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', 'Estimator','results'))
extracter_path = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', 'Extracter'))
csv1 = pd.read_csv(os.path.join(estimator_path,cluster_name+ '.csv'))
csv2 = pd.read_csv(os.path.join(extracter_path, 'newDB.csv'))
# csv1 = pd.read_csv('data.csv')
# csv2 = pd.read_csv('csv2.csv')

# 定义Cost_Defender的限制
# cost_defender_limit = args.budget
# cost_defender_limit = int(input("Please enter the cost limit: "))

# 筛选Cost_Defender小于等于限制的行
csv1 = csv1[csv1['Cost_Defender'] <= cost_defender_limit]

# 将csv1和csv2按照CVE进行合并
merged = pd.merge(csv1, csv2, on='CVE')

# 将BSC和Risk添加到csv1中
csv1['BSC'] = merged['BSC']
csv1['Risk'] = merged['Risk']

# 按照BSC的降序对csv1进行排序
csv1 = csv1.sort_values(by='BSC', ascending=False)

# 在csv1中添加一个名为'Repaired'的列
csv1['Repaired'] = False

# 定义已修复的BSC的总和、已修复的漏洞数和已修复的Risk的总和
bsc_repaired_sum = 0
vuln_repaired_count = 0
repaired_risk_sum = 0
cost_fix_sum = 0

# 遍历csv1中的每一行，按照BSC的降序进行修复
for index, row in csv1.iterrows():
    # 判断是否已经修复了所有的BSC或者修复的cost的总和已经超过Cost_Defender的限制
    if cost_fix_sum >= cost_defender_limit or vuln_repaired_count >= len(csv1):
        break
    
    # 如果当前漏洞的Cost_Defender小于等于剩余的Cost_Defender，则修复该漏洞
    if row['Cost_Defender'] <= cost_defender_limit - cost_fix_sum:
        # 更新已修复的BSC的总和、已修复的漏洞数和已修复的Risk的总和
        bsc_repaired_sum += row['BSC']
        vuln_repaired_count += 1
        repaired_risk_sum += row['Risk']
        cost_fix_sum += row['Cost_Defender']
        
        # 在csv1中标记该漏洞已经被修复
        csv1.at[index, 'Repaired'] = True

# 输出修复的BSC的总和、修复的漏洞数和修复的Risk的总和
print('The sum of repaired BSC is:', bsc_repaired_sum)
print('The number of repaired vulnerabilities is:', vuln_repaired_count)
print('The sum of repaired Risk is:', repaired_risk_sum)
print('Remaining Cost_fix cost:', cost_defender_limit - cost_fix_sum)

# 创建一个空的DataFrame来保存修复的CVE和Container等信息
repaired_vulns = pd.DataFrame(columns=['CVE', 'Container', 'BSC', 'Cost_Defender' ,'Risk'])

# 遍历csv1中的每一行，将已修复的漏洞添加到repaired_vulns中
filename = 'repaired_vulns.csv'
for index, row in csv1.iterrows():
    if row['Repaired'] == True:
        # repaired_vulns = repaired_vulns.append({'CVE': row['CVE'], 'Container': row['Container'], 'BSC': row['BSC'], 'Risk': row['Risk']}, ignore_index=True)
        repaired_vulns = pd.concat([repaired_vulns, pd.DataFrame({'CVE': row['CVE'], 'Container': row['Container'], 'BSC': row['BSC'], 'Cost_Defender' : row['Cost_Defender' ] ,'Risk': row['Risk']}, index=[0])], ignore_index=True)
# 保存repaired_vulns到csv文件
repaired_vulns.to_csv(filename, index=False)
print("The repaired CVE and Container have been saved to file: {}".format(filename))