import paho.mqtt.client as mqtt
from influxdb import InfluxDBClient
import json
import logging

logging.basicConfig(filename="app.log", level=logging.INFO, format='%(asctime)s %(levelname)s:%(message)s')
logging.info("Program started")

with open("appsettings.json", "r") as read_file:
    config = json.load(read_file)

def get_topic():
    """
    Returns a list of tuples containing MQTT topics and QoS levels based on the configuration file.
    """
    return [("/".join([config["MqttConfiguration"]["MqttHomeDeviceTopic"], config["ProgramConfiguration"]["ServiceName"], "HassAnalogSensor" if device["DeviceDescription"]["DeviceType"] != "Plug" else "HassBinarySensor", device["DeviceDescription"]["Identifier"]]), 0) for device in config["ProgramConfiguration"]["Devices"]]

def get_device_types():
    """
    Returns a list of device types based on the configuration file.
    """
    return [device["DeviceDescription"]["DeviceType"] for device in config["ProgramConfiguration"]["Devices"]]

def get_data_type_aliaes(sensor_id):
    """
    Returns the data type alias for a given sensor ID based on the configuration file.
    """
    return type_name[data_id_type[int(sensor_id)-1]]

def convert_data_type(value, type_name):
    """
    Converts the data type of a value based on the device type.
    """
    return "1" if value == "On" and type_name == "Plug" else value

def on_message(client, userdata, message):
    """
    Callback function that is called when a message is received from the MQTT broker.
    """
    data = eval(message.payload.decode('utf8'))
    logging.info(f"Receive message with topic: {message.topic}\n {' '*28}Message payload:{data}")
    dbclient.write([f"{data_id_type[int(data['Id'])-1].lower()},id={data['Id']} value={convert_data_type(data[get_data_type_aliaes(data['Id'])], data_id_type[int(data['Id'])-1])}"], {"db":config["InfluxdbConfiguration"]["InfluxdbName"]}, protocol="line")

data_id_type = get_device_types()
type_name = config["ProgramConfiguration"]["TypesAliaes"]

dbclient = InfluxDBClient(host=config["InfluxdbConfiguration"]["InfluxdbUri"], port=config["InfluxdbConfiguration"]["InfluxdbPort"])

client = mqtt.Client("InfluxDBreader")
client.connect(config["MqttConfiguration"]["MqttUri"])
client.on_message = on_message
client.subscribe(get_topic())
client.loop_forever()
