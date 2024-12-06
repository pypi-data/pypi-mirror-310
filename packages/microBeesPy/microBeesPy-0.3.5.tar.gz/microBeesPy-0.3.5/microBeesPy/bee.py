from typing import List
from typing import Any
from dataclasses import dataclass


@dataclass
class Configuration:
    actuator_type: str
    actuator_timing: float
    icon: str
    color: List[int]

    @staticmethod
    def from_dict(obj: Any) -> "Configuration":
        _actuator_type = str(obj.get("actuator_type"))
        _actuator_timing = float(obj.get("actuator_timing")) if "actuator_timing" in obj else None
        _icon = str(obj.get("icon"))
        _color = obj.get("color") if "color" in obj else None
        return Configuration(_actuator_type, _actuator_timing, _icon, _color)


@dataclass
class Sensor:
    id: int
    name: str
    lastUpdate: object
    deviceID: int
    prototypeID: int
    prototypeName: str
    device_type: int
    dc_type: str
    unit: str
    payload: List[float]
    value: float

    def __eq__(self, other):
        if not isinstance(other, Sensor):
            return False
        return self.id == other.id

    def __lt__(self, other):
        if not isinstance(other, Sensor):
            return NotImplemented
        return self.id < other.id

    def __le__(self, other):
        if not isinstance(other, Sensor):
            return NotImplemented
        return self.id <= other.id

    def __gt__(self, other):
        if not isinstance(other, Sensor):
            return NotImplemented
        return self.id > other.id

    def __ge__(self, other):
        if not isinstance(other, Sensor):
            return NotImplemented
        return self.id >= other.id

    @staticmethod
    def from_dict(obj: Any) -> "Sensor":
        _id = int(obj.get("id"))
        _name = str(obj.get("name"))
        _lastUpdate = int(obj.get("lastUpdate"))
        _deviceID = int(obj.get("deviceID"))
        _prototypeID = int(obj.get("prototypeID"))
        _prototypeName = str(obj.get("prototypeName"))
        _device_type = int(obj.get("device_type"))
        _dc_type = str(obj.get("dc_type")) if "dc_type" in obj else None
        _unit = str(obj.get("unit")) if "unit" in obj else None
        _payload = obj.get("payload") if "payload" in obj else None
        _value = float(obj.get("value")) if "value" in obj else None
        return Sensor(
            _id,
            _name,
            _lastUpdate,
            _deviceID,
            _prototypeID,
            _prototypeName,
            _device_type,
            _dc_type,
            _unit,
            _payload,
            _value,
        )


@dataclass
class StatusString:
    name: str
    value: str
    icon: str

    @staticmethod
    def from_dict(obj: Any) -> "StatusString":
        _name = str(obj.get("name"))
        _value = str(obj.get("value"))
        _icon = str(obj.get("icon"))
        return StatusString(_name, _value, _icon)


@dataclass
class Actuator:
    id: int
    name: str
    prototypeName: str
    deviceID: int
    configuration: Configuration
    starred: bool
    uptime: int
    sensorID: int
    payload: List[float]
    value: int

    def __eq__(self, other):
        if not isinstance(other, Actuator):
            return False
        return self.id == other.id

    def __lt__(self, other):
        if not isinstance(other, Actuator):
            return NotImplemented
        return self.id < other.id

    def __le__(self, other):
        if not isinstance(other, Actuator):
            return NotImplemented
        return self.id <= other.id

    def __gt__(self, other):
        if not isinstance(other, Actuator):
            return NotImplemented
        return self.id > other.id

    def __ge__(self, other):
        if not isinstance(other, Actuator):
            return NotImplemented
        return self.id >= other.id

    @staticmethod
    def from_dict(obj: Any) -> "Actuator":
        _id = int(obj.get("id"))
        _name = str(obj.get("name"))
        _prototypeName = str(obj.get("prototypeName"))
        _deviceID = int(obj.get("deviceID"))
        _configuration = (
            Configuration.from_dict(obj.get("configuration"))
            if "configuration" in obj
            else None
        )
        _starred = bool(obj.get("starred")) if "starred" in obj else False
        _uptime = int(obj.get("uptime")) if "uptime" in obj else 0
        _sensorID = int(obj.get("sensorID")) if "sensorID" in obj else 0
        _payload = obj.get("payload") if "payload" in obj else None
        _value = int(obj.get("value")) if "value" in obj else None
        return Actuator(
            _id,
            _name,
            _prototypeName,
            _deviceID,
            _configuration,
            _starred,
            _uptime,
            _sensorID,
            _payload,
            _value,
        )

       
@dataclass
class InstanceData:
    progMode: int
    targetTemp: float
    temperature: float
    childlock: bool
    deviceMode: int

    @staticmethod
    def from_dict(obj: Any) -> 'InstanceData':
        _progMode = int(obj.get("progMode")) if "progMode" in obj  else 0
        _targetTemp = float(obj.get("targetTemp")) if "targetTemp" in obj else 0
        _temperature = float(obj.get("temperature")) if "temperature" in obj else 0
        _childlock = bool(obj.get("childlock")) if "childlock" in obj else False
        _deviceMode = int(obj.get("deviceMode")) if "deviceMode" in obj else 0
        return InstanceData(_progMode, _targetTemp, _temperature, _childlock, _deviceMode)
    
@dataclass
class Bee:
    id: int
    label: str
    serial: str
    gate_serial: str
    gate_id: int
    lastUpdate: float
    name: str
    active: bool
    productID: int
    prototypeName: str
    rssi: int
    lastActivation: float
    icon: str
    configuration: Configuration
    instanceData: InstanceData
    sensors: List[Sensor]
    actuators: List[Actuator]

    def __eq__(self, other):
        if not isinstance(other, Bee):
            return False
        return self.id == other.id

    def __lt__(self, other):
        if not isinstance(other, Bee):
            return NotImplemented
        return self.id < other.id

    def __le__(self, other):
        if not isinstance(other, Bee):
            return NotImplemented
        return self.id <= other.id

    def __gt__(self, other):
        if not isinstance(other, Bee):
            return NotImplemented
        return self.id > other.id

    def __ge__(self, other):
        if not isinstance(other, Bee):
            return NotImplemented
        return self.id >= other.id

    @staticmethod
    def from_dict(obj: Any) -> "Bee":
        _id = int(obj.get("id"))
        _label = str(obj.get("label")) if "label" in obj else ""
        _serial = str(obj.get("serial"))
        _gate_serial = str(obj.get("gate_serial"))
        _gate_id = int(obj.get("gate_id"))
        _lastUpdate = float(obj.get("lastUpdate"))
        _name = str(obj.get("name")) if "name" in obj else ""
        _active = bool(obj.get("active"))
        _productID = int(obj.get("productID"))
        _prototypeName = str(obj.get("prototypeName"))
        _rssi = int(obj.get("rssi")) if "rssi" in obj else 0
        _lastActivation = (
            float(obj.get("lastActivation")) if "lastActivation" in obj else 0
        )
        _icon = str(obj.get("icon")) if "icon" in obj else ""
        _configuration = (
            Configuration.from_dict(obj.get("configuration"))
            if "configuration" in obj
            else None
        )
        _sensors = (
            [Sensor.from_dict(y) for y in obj.get("sensors")]
            if "sensors" in obj
            else None
        )
        _actuators = (
            [Actuator.from_dict(y) for y in obj.get("actuators")]
            if "actuators" in obj
            else None
        )
        _instanceData = (
            InstanceData.from_dict(obj.get("instance_data"))
            if "instance_data" in obj
            else None
        )
        return Bee(
            _id,
            _label,
            _serial,
            _gate_serial,
            _gate_id,
            _lastUpdate,
            _name,
            _active,
            _productID,
            _prototypeName,
            _rssi,
            _lastActivation,
            _icon,
            _configuration,
            _instanceData,
            _sensors,
            _actuators,
        )
