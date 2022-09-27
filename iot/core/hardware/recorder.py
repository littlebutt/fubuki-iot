from loguru import logger

from iot.context import Context
from iot.factories import RecorderFactory
from iot.integration.audio import AudioClient
from iot.models import Recorder

import keyboard
import time as tm
import os

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


@RecorderFactory.set
class PocketsphinxRecorder(Recorder):

    def awake(self) -> bool:
        try:
            from pocketsphinx import LiveSpeech, get_model_path
        except ImportError as ie:
            logger.error("没有安装pocketsphinx，具体解决方案请访问https://github.com/bambocher/pocketsphinx-python " + ie.__str__())
            return False

        model_path = get_model_path()
        speech = LiveSpeech(
            verbose=False,
            sampling_rate=16000,
            buffer_size=2048,
            no_search=False,
            full_utt=False,
            hmm=os.path.join(model_path, 'en-us'),
            lm=os.path.join(model_path, 'en-us.lm.bin'),
            dic=os.path.join(model_path, 'cmudict-en-us.dict')
        )
        for phrase in speech:
            logger.info("Got phrase: " + phrase.__str__())
            phrase = phrase.__str__().split()[0]
            if phrase.__str__() in ['hi', 'hello', 'i', 'ah']:
                return True

    def record(self, time: int) -> str:
        data = AudioClient.record(time=time)
        local_time = tm.strftime('%Y-%m-%d_%H-%M-%S', tm.localtime())
        path = f'{Context.config["RESOURCE_PATH"]}{get_slash()}wav{get_slash()}{local_time}.wav'
        AudioClient.save(data=data, path=path)
        return path
