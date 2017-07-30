#!/usr/bin/env python

import time
import os
import sys
import json
import thingspeak_simple
import Adafruit_MCP9808.MCP9808 as MCP9808


def TEMPERATURE(device):
    return device.temperature
def TARGET(device):
    return device.target

# TODO: move this into a config
config_filename = os.path.join(os.environ['HOME'],'sensors/config/nest')
if os.path.exists(config_filename):
    config_fp = open(config_filename, 'r')
    STRUCTURES = json.load(config_fp)
else:
    print >> sys.stderr, 'Missing nest structures config file {}'.format(config_filename)
    STRUCTURES = []

print('STRUCTURES={}'.format(STRUCTURES))


config_filename = os.path.join(os.environ['HOME'],'sensors/config/local')
if os.path.exists(config_filename):
    config_fp = open(config_filename, 'r')
    LOCAL_SENSORS = json.load(config_fp)
else:
    print >> sys.stderr, 'Missing local sensor structures config file {}'.format(config_filename)
    LOCAL_SENSORS = []

print('LOCAL={}'.format(LOCAL_SENSORS))



updates_by_key = {}

def process_structure(s, structure):
    print ('Structure %s' % structure.name)
    print ('    Away: %s' % structure.away)
    print ('    Devices:')

    for device in structure.thermostats:
        for d in s['devices']:
            if device.name == d['name']:
                process_device(d, device)

def process_device(d, device):
    key = d['channel-write-key']
    for (field_name,field_getter) in d['fields']:
        assert device.temperature_scale.upper() == 'F'
        field_val = field_getter(device)
        updates_by_key.setdefault(key,[]).append((field_name,field_val))
        
        
    ##print ('        Device: %s' % device.name)
    ##print ('        Where: %s' % device.where)
    ##print ('            Mode     : %s' % device.mode)
    ##print ('            Fan      : %s' % device.fan)
    ##print ('            Temp     : %0.1fF' % device.temperature)
    ##print ('            TempScale: %s' % device.temperature_scale)
    ##print ('            Humidity : %0.1f%%' % device.humidity)
    ##print ('            Target   : %0.1fF' % device.target)
    ##print ('            Eco High : %0.1fF' % device.eco_temperature.high)
    ##print ('            Eco Low  : %0.1fF' % device.eco_temperature.low)
    ##print ('            hvac_emer_heat_state  : %s' % device.is_using_emergency_heat)


def c_to_f(c):
    return c * 9.0 / 5.0 + 32.0


if len(STRUCTURES) != 0:
    import nest

    # heatmap project
    client_id = '60a12ef8-6a6b-4080-9eb7-5645f63bce38'
    client_secret = 'HGSmL4lwowSNCLgH5WWvcYYGL'
    access_token_cache_file = os.path.join(os.environ['HOME'], 'nest.json')
        
    napi = nest.Nest(client_id=client_id, client_secret=client_secret, access_token_cache_file=access_token_cache_file)

    if napi.authorization_required:
        print('Go to ' + napi.authorize_url + ' to authorize, then enter PIN below')
        pin = raw_input("PIN: ")
        napi.request_token(pin)
    
    for structure in napi.structures:
        for s in STRUCTURES:
            if structure.name == s['name']:
                process_structure(s, structure)


# Basic temperature sensor
class SensorMCP9808:
    def __init__(self):
        # Default constructor will use the default I2C address (0x18) and pick a default I2C bus.
        #
        # For the Raspberry Pi this means you should hook up to the only exposed I2C bus
        # from the main GPIO header and the library will figure out the bus number based
        # on the Pi's revision.
        #
        # For the Beaglebone Black the library will assume bus 1 by default, which is
        # exposed with SCL = P9_19 and SDA = P9_20.
        self.sensor = MCP9808.MCP9808()
        # Optionally you can override the address and/or bus number:
        #sensor = MCP9808.MCP9808(address=0x20, busnum=2)

        self.sensor.begin()

    def TEMPERATURE(self):
        temp_c = self.sensor.readTempC()
        return c_to_f(temp_c)

    def HUMIDITY(self):
        raise Exception('HUMIDITY not implemented')

        
class local_sensor_types:
    def MCP9808(**kwargs):
        return SensorMCP9808() # TODO: pass address

        
# Local temp sensor
for sensor_desc in LOCAL_SENSORS:
    sensor = eval(sensor_desc['sensor-class'], local_sensor_types.__dict__)()
    entry = updates_by_key.setdefault(sensor_desc['channel-write-key'],[])
    fields = sensor_desc['fields']
    print(fields)
    for (field, accessor_name) in fields.items():
        accessor = getattr(sensor, accessor_name)
        value = accessor()
        entry.append((field,value))

print('Uploading at {}'.format(time.asctime()))
for (key,fields) in updates_by_key.items():
    print('{} => {}'.format(key, fields))
    code = thingspeak_simple.log(key, fields)
    print('upload code={}'.format(code))
