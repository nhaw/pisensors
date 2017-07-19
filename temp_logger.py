#!/usr/bin/env python


#import httplib
#conn = httplib.HTTPConnection('api.thingspeak.com', httplib.HTTPS_PORT)
#req = conn.request('GET', '/update?api_key=Q85L9QZN3KY28NBZ&field1=0')
#resp1 = conn.getresponse()
#print resp1.status, resp1.reason
#conn.close()

import urllib
import urllib2
import time
import Adafruit_MCP9808.MCP9808 as MCP9808


def log(value_f, field = 1):
    params = urllib.urlencode({'api_key':'Q85L9QZN3KY28NBZ', 'field{}'.format(field):str(value_f)})
    url = 'https://api.thingspeak.com/update?' + params
    ret = urllib2.urlopen(url)
    code = ret.getcode()
    if code != 200:
        print 'Code for field {} value {} wass not OK: {}'.format(field, value_f, code)


def c_to_f(c):
	return c * 9.0 / 5.0 + 32.0

# Default constructor will use the default I2C address (0x18) and pick a default I2C bus.
#
# For the Raspberry Pi this means you should hook up to the only exposed I2C bus
# from the main GPIO header and the library will figure out the bus number based
# on the Pi's revision.
#
# For the Beaglebone Black the library will assume bus 1 by default, which is
# exposed with SCL = P9_19 and SDA = P9_20.
sensor = MCP9808.MCP9808()

# Optionally you can override the address and/or bus number:
#sensor = MCP9808.MCP9808(address=0x20, busnum=2)

# Initialize communication with the sensor.
sensor.begin()

SLEEP_SECONDS = 10.0

# Loop printing measurements every second.
print('Press Ctrl-C to quit.')
prev_value = None
while True:
    try:
        temp = sensor.readTempC()
        temp_f = c_to_f(temp)
        is_different = temp_f != prev_value
        print('Temperature: {0:0.3F}*C / {1:0.3F}*F {2}'.format(temp, temp_f, '(delta)' if is_different else ''))
        if temp_f != prev_value:
            log(temp_f)
        prev_value = temp_f
    except Exception as ex:
        print('Exception: {}'.format(ex))

    time.sleep(SLEEP_SECONDS)
