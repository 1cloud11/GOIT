from abc import ABC, abstractmethod
import pickle
import json


class SerializationInterface(ABC):
    @abstractmethod
    def __init__(self, filename, somedata):
        self.filename = filename
        self.somedata = somedata
    
    @abstractmethod
    def serialize_it(self):
        pass


class SerializeBin(SerializationInterface):
    def __init__(self, filename, somedata):
        self.filename = filename
        self.somedata = somedata

    def serialize_it(self):
        with open(self.filename, 'wb') as fw:
            pickle.dump(self.somedata, fw)


class SerializeJson(SerializationInterface):
    def __init__(self, filename, somedata):
        self.filename = filename
        self.somedata = somedata

    def serialize_it(self):
        with open(self.filename, 'w') as fw:
            json.dump(self.somedata, fw) 


cla1 = SerializeBin('qwe.bin', 'qweqweqweqwe')
cla1.serialize_it()

cla2 = SerializeJson('qwa.json', 'asdasdasdasd')
cla2.serialize_it()