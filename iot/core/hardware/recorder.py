from loguru import logger

from iot.context import Context
from iot.factories import RecorderFactory
from iot.integration.audio import AudioClient
from iot.models import Recorder

import keyboard
import time as tm

from iot.utils import get_slash


@RecorderFactory.set
class BuiltinRecorder(Recorder):

    def awake(self) -> bool:
        logger.info("按下f唤醒智能终端...")
        keyboard.wait("f")
        return True

    def record(self, time: int) -> str:
        data = AudioClient.record(time=time)
        local_time = tm.strftime('%Y-%m-%d_%H-%M-%S', tm.localtime())
        path = f'{Context.config["RESOURCE_PATH"]}{get_slash()}wav{get_slash()}{local_time}.wav'
        AudioClient.save(data=data, path=path)
        return path
