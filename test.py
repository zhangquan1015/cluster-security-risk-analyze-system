import os
import framework.loader.loader as load

curPath = os.path.dirname(os.path.realpath(__file__))
dataPath = os.path.join(curPath,"database")
# os.
dataName = os.listdir(dataPath)

for i in dataName:
    yamlPath = os.path.join(dataPath,i)
    f = open(yamlPath,'r',encoding='utf-8')
    # print(yamlPath)
    # myYaml = yaml.load(f)
    # print(myYaml)
    print(load.loader(yamlPath))