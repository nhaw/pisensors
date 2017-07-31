class nest_getters:
    def TEMPERATURE(device):
        return device.temperature
    def TARGET(device):
        return device.target
    def COOLING(device):
        return 1 if 'cooling' in device.hvac_state.lower() else 0
    def ENABLED(device):
        return 1 if 'cool' in device.mode.lower() else 0
    def HUMIDITY(device):
        return device.humidity
