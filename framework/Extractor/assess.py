from cvss import CVSS2, CVSS3
# import numpy as np

def calculate(dict):
    version = dict['version']
    vector = dict['vector']
    exploit = dict['exploit']
    fix = dict['fix']
    
    if version == '2.0':
        c = CVSS2(vector)
    else:
        c = CVSS3(vector)
    
    cvssscore = c.scores()
    # print(type(cvssscore))
    exploit_weight = calculate_exploit_weight(exploit)
    fix_weight = calculate_fix_weight(fix)
    # return np.ceil(cvssscore[0] * exploit_weight * fix_weight)
    return round(cvssscore[0] * exploit_weight * fix_weight,1)

def calculate_exploit_weight(exploit):
    if exploit == 'PoC':
        return 0.95
    elif exploit == 'Unproven':
        return 0.90
    else:
        return 1
def calculate_fix_weight(fix):
    if fix == 'Workaround':
        return 0.98
    elif fix == 'Third Party Fix':
        return 0.95
    elif fix == 'Official Fix':
        return 0.90
    else:
        return 1

# vector = 'AV:L/AC:L/Au:M/C:N/I:P/A:C/E:U/RL:W/RC:ND/CDP:L/TD:H/CR:ND/IR:ND/AR:M'
# c = CVSS2(vector)
# print(vector)
# print(c.clean_vector())
# print(type(c))
# print(c.scores())
# # c.clean_
# print(calculate(vector,2))

# print()

# vector = 'CVSS:3.0/S:C/C:H/I:H/A:N/AV:P/AC:H/PR:H/UI:R/E:H/RL:O/RC:R/CR:H/IR:X/AR:X/MAC:H/MPR:X/MUI:X/MC:L/MA:X'
# c = CVSS3(vector)
# print(vector)
# print(c.clean_vector())
# print(c.scores())
# print(c.severities())