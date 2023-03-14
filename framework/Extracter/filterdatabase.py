
def filter_information(CVE):
    info = {}
    info['version'] = CVE['CVSS'][0]
    info['vector'] = CVE['CVSS'][1]
    info['exploit'] = filter_exploitation(CVE['Exploits'])
    info['fix'] = filter_remediation(CVE['Patchs'])
    return info

# def filter_threat(CVE):
#     return db['CVSS'][1]
#     # return 'AV:L/AC:L/Au:M/C:N/I:P/A:C/E:U/RL:W/RC:ND/CDP:L/TD:H/CR:ND/IR:ND/AR:M'
def filter_exploitation(exploits):
    if len(exploits) == 0:
        return "Not Defined"
    for exploit in exploits:
        if "Advisory" in exploit[0]:
            return "PoC"
    return "Unproven"
# "Unproven" "PoC"  "Not Defined"
# "Unproven" "PoC" "EXP"
def filter_remediation(patchs):
    if len(patchs) == 0:
        return "Unavailable"
    fix = 'Workaround'
    for patch in patchs:
        if "Advisory" in patch[0]:
            if "Offical" in patch[0]:
                return "Official Fix"
            fix = "Third Party Fix"
    return fix

# Workaround；Third Party Fix；Official Fix； "Unavailable"