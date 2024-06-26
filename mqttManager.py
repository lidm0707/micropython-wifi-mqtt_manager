import time
from umqtt.simple import MQTTClient
from binascii import a2b_base64, b2a_base64, hexlify, unhexlify
import ujson



class MqttManager:
    def __init__(self,name ='mqttClient',debug = False):
        self.name = name
        self.stage = False
        self.debug = debug
        self.config = 'config.json'
        self.network = 'mqtt'
        self.mqttC = MQTTClient

    
    def isConnected(self):
        return self.stage
        
    def writeConfig(self,id,password,server):
            print('write mqtt')
            key = 'mqtt'
            try:
                with open(self.config) as file:
                    data = ujson.load(file)
                    # Check if key is in file
                    if key in data:
                        # Delete Key
                        del data[key]
                        cacheDict = dict(data)
                        # Update Cached Dict
                        cacheDict.update({key:{'id':id , 'password':password,'server':server}})
                        with open(self.config,'w') as file:
                            # Dump cached dict to json file
                            ujson.dump(cacheDict, file)
                            print('mqtt is saved')            
            except Exception as error:
                if self.debug:
                    print(error)
                pass

    def readConfig(self):
        key = 'mqtt'
        print('use read Config')
        try:
            with open(self.config) as file:
                data = ujson.load(file)           
                if key in data:
                    if data[key]['id'] is not None:
                        #password = hexlify(a2b_base64(data[key]['password'].encode())) 
                        profiles = {}
                        profiles[key] = {}
                        profiles[key]['id'] = data[key]['id']
                        profiles[key]['password'] = data[key]['password']
                        profiles[key]['server'] = data[key]['server']
            return profiles
        except Exception as error:
            if self.debug:
                print(error)
            pass
      
    
    def connect(self):
        profiles = self.readConfig()
        print(profiles)
        if(profiles is not None):
            s = profiles[self.network]['server']
            p = '1883'
            u = profiles[self.network]['id']
            ps = profiles[self.network]['password']
            self.c = self.mqttC(self.name, server = s,port =p , user = u ,password = ps)
            self.c.connect()
            self.stage = True
            try:  
                print('Connected to %s, waiting ' % s)
            except OSError as error:
                if self.debug:
                    print(error)
                pass
                print('can\'t connected')
                print('Could not connect to any MQTT')
            
    def publish(self,topic,msg):
        self.c.publish(topic,msg)
        
    
