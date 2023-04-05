import argparse
import yaml
import json

# 解析命令行参数
parser = argparse.ArgumentParser(description='Extract the depend_on relationships from a Docker Compose file.')
parser.add_argument('compose_file', metavar='COMPOSE_FILE', type=str, help='the path to the Docker Compose file')
parser.add_argument('output_file', metavar='OUTPUT_FILE', type=str, help='the path to the output file')
args = parser.parse_args()

# 读取docker-compose.yaml文件
with open(args.compose_file, 'r') as file:
    compose_data = yaml.safe_load(file)

# 解析depend_on关系
depends_on = {}
for service, data in compose_data['services'].items():
    if 'depends_on' in data:
        for parent in data['depends_on']:
            if parent not in depends_on:
                depends_on[parent] = []
            depends_on[parent].append(service)

# 将结果保存到文件
with open(args.output_file, 'w') as file:
    json.dump(depends_on, file)