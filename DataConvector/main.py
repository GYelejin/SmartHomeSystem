import paho.mqtt.client as mqtt
import json
import logging
import xml.etree.ElementTree as ET

with open("appsettings.json", "r") as read_file:
    config = json.load(read_file)

logging.basicConfig(filename="app.log", level=logging.INFO,
                    format='%(asctime)s %(levelname)s:%(message)s')
logging.info("Program started")

class InvalidDevice:
    """
    A class representing an invalid device.

    Attributes:
    - Id (int): The ID of the device.
    - DeviceType (str): The type of the device.
    - DataFormat (str): The format of the data.
    - ValueType (str): The type of the value.
    - Information (dict): A dictionary containing information about the device.
    """

    def __init__(self, Id, DeviceType, DataFormat, ValueType, Information):
        """
        Initializes an InvalidDevice object.

        Parameters:
        - Id (int): The ID of the device.
        - DeviceType (str): The type of the device.
        - DataFormat (str): The format of the data.
        - ValueType (str): The type of the value.
        - Information (dict): A dictionary containing information about the device.
        """
        self.Id = Id
        self.DeviceType = DeviceType
        self.DataFormat = DataFormat
        self.Information = Information
        self.generate_data()

    def invalid_topic(self):
        """
        Returns an invalid topic based on the data format.

        Returns:
        - str: An invalid topic.
        """
        return {
            "Invalid1": f"Device{self.Id}",
            "Invalid2": f"Binary-{self.Id}-Sensor",
            "Invalid3": f"XmlSensor_{self.Id}",
            "Invalid4": f"CSV-{self.Id}",
            "Invalid5": f"Sensor{self.Id}"
        }[self.DataFormat]

    def chooseConvector(self):
        """
        Returns a function that converts data based on the value type.

        Returns:
        - function: A function that converts data.
        """
        def Invalid2(data):
            convectors = {
                "Double": lambda data: str(int(data, 16) / 100),
                "Integer": lambda data: str(int(data, 16)),
                "Binary": lambda data:  "On" if int(data, 16) == 0 else "Off"
            }
            return convectors[self.ValueType]
        convectors = {
            "Invalid1": lambda data: literal_eval(data)["value"],
            "Invalid2": lambda data: Invalid2(data)(data),
            "Invalid3": lambda data: ET.fromstring(data+"</sensor>")[0][1].text,
            "Invalid4": lambda data: data.split(";")[1],
            "Invalid5": lambda data: data
        }
        return convectors[self.DataFormat]

    def get_valid_value(self, value):
        """
        Returns a valid value based on the Convector function.

        Parameters:
        - value (str): The value to be converted.

        Returns:
        - str: A valid value.
        """
        return self.Convector(value)

    def valid_topic(self):
        """
        Returns a valid topic.

        Returns:
        - str: A valid topic.
        """
        return "/".join([self.Information["MqttHomeDeviceTopic"],
                          self.Information["ServiceName"],
                          "HassAnalogSensor" if self.DeviceType != "Plug" else "HassBinarySensor", self.Id])

    def config_msg(self):
        """
        Returns a configuration message.

        Returns:
        - bytes: A configuration message.
        """
        device_class = "plug" if self.DeviceType == "Plug" else self.Information['DeviceClass']
        state_topic = f"+/+/HassBinarySensor/{self.Id}" if self.DeviceType == "Plug" else f"+/+/HassAnalogSensor/{self.Id}"
        payload_on = "On" if self.DeviceType == "Plug" else None
        payload_off = "Off" if self.DeviceType == "Plug" else None
        value_template = "{ { value_json.state | is_defined } }" if self.DeviceType == "Plug" else "{{" + f"value_json.{self.Information['DeviceTypeAlias']} | is_defined" + "}}"
        return json.dumps({
            "state_topic": state_topic,
            "name": f"{self.Information['Name']}-{self.Information['DeviceTypeAlias']}",
            "unique_id": f"{self.Id}-{self.Information['Name']}-{self.Information['DeviceTypeAlias']}",
            "device_class": device_class,
            "payload_on": payload_on,
            "payload_off": payload_off,
            "value_template": value_template,
            "unit_of_measurement": self.Information["Unit"],
            "device": {
                "connections": [],
                "identifiers": [self.Id],
                "manufacturer": self.Information['Manufacturer'],
                "model": self.Information['Model'],
                "name": self.Information['Name']
            }
        }).encode('utf8')

    def config_topic(self):
        """
        Returns a configuration topic.

        Returns:
        - str: A configuration topic.
        """
        return "/".join(["homeassistant", "binary_sensor" if self.DeviceType == "Plug" else "sensor", "-".join([self.Id, self.Information["Name"], self.Information["DeviceTypeAlias"]]), "config"])

    def normal_post(self, value):
        """
        Returns a JSON string containing information about the device and the converted value.

        Parameters:
        - value (str): The value to be converted.

        Returns:
        - str: A JSON string containing information about the device and the converted value.
        """
        logging.info(f"Convectored Value: {value} -> {self.Convector(value)}")
        logging.info("Sended Message: " + str({"Id": self.Id,"name" : self.Id, self.Information["DeviceTypeAlias"]: self.Convector(value)}))
        return json.dumps({"Id": self.Id,"name" : self.Id, self.Information["DeviceTypeAlias"]: self.Convector(value)})

    def generate_data(self):
        """
        Generates data for the device.
        """
        unit_of_measurement = {'Temperature': '°C', 'Voltage': 'V',
                               'PressureHpa': 'hPa', 'Current': 'A', 'FrequencyHz': 'Hz', 'Humidity': '%'}
        devicetypealias = {"Temperature": "temp", "Voltage": "volt", "PressureHpa": "pres",
                           "Current": "amps", "FrequencyHz": "freqh", "Humidity": "hum", "Plug": "state"}
        hass_device_class = {"Temperature": "temperature", "Voltage": "voltage", "PressureHpa": "pressure",
                           "Current": "current", "FrequencyHz": "frequency", "Humidity": "humidity", "Plug": "state"}
        self.Information["DeviceTypeAlias"] = devicetypealias[self.DeviceType]
        self.Information["Unit"] = unit_of_measurement[self.DeviceType]
        self.Information["DeviceClass"] = hass_device_class[self.DeviceType]
        self.InvalidTopic = (self.invalid_topic(), 0)
        self.ValidTopic = self.valid_topic()
        self.ConfigTopic = (self.config_topic(), 0)
        self.ConfigMsg = self.config_msg()
        self.Convector = self.chooseConvector()

def on_message(client, userdata, message):
    data = message.payload.decode('utf8')

    logging.info(f"Receive message with topic: {message.topic}\nMessage payload:{data}")

    client.publish(devices[message.topic].ValidTopic,
                   payload=devices[message.topic].normal_post(data))

client = mqtt.Client("Convector")
client.connect(config["MqttConfiguration"]["MqttUri"])

client.on_message = on_message

devices = {sensor.invalid_topic(): sensor for sensor in [InvalidDevice(device["DeviceDescription"]["Identifier"], 
            device["DeviceDescription"]["DeviceType"], 
            device["DeviceDescription"]["DataFormat"], 
            device["DeviceDescription"]["ValueType"], 
            {"Name": device["DeviceDescription"]["Name"],
             "Model":  device["DeviceDescription"]["Model"],
             "Manufacturer": device["DeviceDescription"]["Manufacturer"],
             "MqttHomeDeviceTopic": config["MqttConfiguration"]["MqttHomeDeviceTopic"],
             "ServiceName": config["ProgramConfiguration"]["ServiceName"]}) for device in config["ProgramConfiguration"]["Devices"] if device["DeviceDescription"]["DataFormat"] != "Correct"]}

client.subscribe(list(devices.keys()))

client.loop_forever()

client.subscribe(list(devices.keys()))

client.loop_forever()