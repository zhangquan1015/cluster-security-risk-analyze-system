import os
import yaml
import csv
import dockerfileParser

# 打开docker-compose.yaml文件并解析
with open('docker-compose.yaml', 'r') as f:
    data = yaml.safe_load(f)

# 创建CSV文件
with open('compose.csv', 'w', newline='') as csvfile:
    writer = csv.writer(csvfile)
    writer.writerow(['service', 'image', 'baseimage', 'build', 'Dockerfile'])

    # 遍历所有的service
    for service_name, service_data in data['services'].items():
        image = service_data.get('image')
        build = service_data.get('build')

        # 如果build是一个字符串，则尝试查找Dockerfile的baseimage
        if isinstance(build, str):
            dockerfile_path = os.path.join(service_data['build'], 'Dockerfile')
            if os.path.exists(dockerfile_path):
                build = dockerfile_path
            baseimage = dockerfileParser.get_base_image_from_dockerfile(dockerfile_path)

        # 将service的image、build和Dockerfile写入CSV文件中
        writer.writerow([service_name, image, baseimage, build, dockerfile_path])
