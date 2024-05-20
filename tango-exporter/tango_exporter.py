from prometheus_client import start_http_server, Gauge
from tango import DeviceProxy
import time
# 创建一个Gauge指标
temperature_metric = Gauge('ActuatorBus_01_temperature', 'Temperature of ActuatorBus_01', ['Actuator_id'])
def collect_metrics():
    # 连接到Tango设备服务器
    device_proxy = DeviceProxy('tango://localhost:20002/sys/actuatorbus/01')
    # 获取温度指标值
    temperature_data = device_proxy.read_attribute('temperature').value
    # 设置Gauge指标的值
    for i,temperature in enumerate(temperature_data):
        temperature_metric.labels(Actuator_id=f"Actuator_{i}").set(temperature)
if __name__ == '__main__':
    # 指定Tango-exporter暴露的端口号
    start_http_server(20017)
    #不断传入数据
    while True:
        collect_metrics()
        time.sleep(1)