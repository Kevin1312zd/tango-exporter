import yaml

with open('./actuator.yaml', 'r', encoding='utf-8') as f:
    result = yaml.load(f.read(), Loader=yaml.FullLoader)
print(result['ActuatorBus_list'])