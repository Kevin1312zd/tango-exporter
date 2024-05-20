from prometheus_client import start_http_server, Gauge
from tango import DeviceProxy
import time
import yaml

class tangoexp:
    def __init__(self,proxy,actuatorbus_id,attribute_list):

        self.proxy=proxy        
        self.actuatorbus_id=actuatorbus_id
        self.attribute_list=attribute_list
        self.metric_data={} 
    
    def create_gauge(self):
        #创建Tango proxy
        device_proxy=DeviceProxy(self.proxy)

        for attribute_name in self.attribute_list:
        # 根据属性名称创建Gauge指标
            metric=Gauge(f"ActuatorBus_{self.actuatorbus_id}_{attribute_name}",f"{attribute_name} of ActuatorBus_{self.actuatorbus_id}", ['Actuator_id'])

            #根据属性采集Tango数据
            data=device_proxy.read_attribute(attribute_name).value
            #创建指标和Tango数据的字典
            self.metric_data[metric]=data

    def collect_metrics(self):

        for metric,data in self.metric_data.items():
            print(data)
            for i,value in enumerate(data):
                metric.labels(Actuator_id=f"Actuator_{i}").set(value)


if __name__ == '__main__':

    with open('./actuator.yaml', 'r', encoding='utf-8') as f:
        result = yaml.load(f.read(), Loader=yaml.FullLoader)

    device_proxy_01='tango://localhost:20002/sys/actuatorbus/01'
    actuatorbus_id='01'

    #attribute_list=['position','current', 'velocity','temperature']
    attribute_list=['temperature','position']

    actuatorbus_01=tangoexp(result['ActuatorBus_01']['device_proxy'],result['ActuatorBus_01']['actuatorbus_id'],result['attribute_list'])
    actuatorbus_01.create_gauge()

    # 指定Tango-exporter暴露的端口号
    start_http_server(20017)

    #不断传入数据
    while True:

        actuatorbus_01.collect_metrics()

        time.sleep(1)