from collections import UserDict

from dotenv import dotenv_values


class Config(UserDict):

    def load_config(self):
        self.data = dotenv_values()
        if 'RESOURCE_PATH' not in self.data:
            raise KeyError("Config missing: RESOURCE_PATH")
        if 'DEVICE_REC' not in self.data:
            self['DEVICE_REC'] = 'BuiltinRecorder'
        if 'DEVICE_PLY' not in self.data:
            self['DEVICE_PLY'] = 'BuiltinPlayer'
        if 'ASR_PROCESSOR' not in self.data:
            self['ASR_PROCESSOR'] = 'BuiltinAsrProcessor'
        if 'TTS_PROCESSOR' not in self.data:
            self['TTS_PROCESSOR'] = 'BuiltinTtsProcessor'
        if 'MQTT_HOST' not in self.data:
            self['MQTT_HOST'] = '127.0.0.1'
        if 'MQTT_PORT' not in self.data:
            self['MQTT_PORT'] = '1883'
        if 'TERMINAL_MODE' not in self.data: # 终端模式：0-监听用户 1-监听设备 2-两者都监听
            self['TERMINAL_MODE'] = '2'

    def __getitem__(self, item):
        if not self.data:
            self.load_config()
        return self.data[item]

    def __setitem__(self, key, value):
        if not self.data:
            self.load_config()
        self.data[key] = value
