from typing import Optional

from iot.factories import AsrProcessorFactory
from iot.integration.baidu import BaiduCloudClient, BaiduApi
from iot.models import AsrProcessor


@AsrProcessorFactory.set
class BuiltinAsrProcessor(AsrProcessor):
    client: BaiduCloudClient

    def __init__(self):
        self.client = BaiduApi.register()

    def asr(self, path: str) -> Optional[str]:
        result_str = self.client.asr(path)
        return result_str
