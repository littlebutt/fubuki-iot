import time as tm

from iot.context import Context
from iot.factories import TtsProcessorFactory
from iot.integration.baidu import BaiduCloudClient, BaiduApi
from iot.models import TtsProcessor
from iot.utils import get_slash


@TtsProcessorFactory.set
class BuiltinTtsProcessor(TtsProcessor):
    client: BaiduCloudClient

    def __init__(self):
        self.client = BaiduApi.register()

    def tts(self, text: str) -> str:
        local_time = tm.strftime('%Y-%m-%d_%H-%M-%S', tm.localtime())
        path = f'{Context.config["RESOURCE_PATH"]}{get_slash()}txt{get_slash()}{local_time}.txt'
        res = self.client.tts(text=text, filename=path)
        return path
