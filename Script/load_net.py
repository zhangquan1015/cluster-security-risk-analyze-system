import argparse
import json
import yaml

parser = argparse.ArgumentParser()
parser.add_argument('input_file', help='Input docker-compose.yaml file name')
parser.add_argument('output_file', help='Output file name')
args = parser.parse_args()

with open(args.input_file, 'r') as f:
    data = yaml.safe_load(f)

services = data['services']
networks = data.get('networks', {'bridge': {}})

network_services = {}
for network_name, network in networks.items():
    network_services[network_name] = []
    for service_name, service in services.items():
        service_network = service.get('networks', {'default': None})['default']
        if service_network is None:
            service_network = 'bridge'
        else:
            service_network = service_network['name']
        if service_network == network_name:
            network_services[network_name].append(service_name)

with open(args.output_file, 'w') as f:
    json.dump(network_services, f, indent=2)
