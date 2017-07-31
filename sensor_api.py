from sensor_utils import *

# Basic temperature sensor
class SensorMCP9808:
    def __init__(self):
        import Adafruit_MCP9808.MCP9808 as MCP9808

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


# Basic temperature and humidity sensor
class SensorSI7021:
    exists = False

    def __init__(self):
        assert (SensorSI7021.exists == False) # Only one allowed
        SensorSI7021.exists = True
        import HTU21DF

    def TEMPERATURE(self):
        HTU21DF.htu_reset
        temp_c = HTU21DF.read_temperature()
        return c_to_f(temp_c)

    def HUMIDITY(self):        
        return HTU21DF.read_humidity()


class local_sensor_types:
    def MCP9808(**kwargs):
        return SensorMCP9808() # TODO: pass address

    def SI7021(**kwargs):
        return SensorSI7021()
