from threading import Lock
from typing import ClassVar

from iot.config import Config
from iot.factories import RecorderFactory, PlayerFactory, AsrProcessorFactory, TtsProcessorFactory
from iot.messages import MessagesProcessor
from iot.models import Recorder, Player, AsrProcessor, TtsProcessor
from iot.utils import get_all_core_packages, load_models, mkdir


class Context:
    """
    Context上下文，所有类成员都是单例
    """
    config: ClassVar["Config"] = None
    recorder: ClassVar["Recorder"] = None
    player: ClassVar["Player"] = None
    asr_processor: ClassVar["AsrProcessor"] = None
    tts_processor: ClassVar["TtsProcessor"] = None
    messages_processor: ClassVar["MessagesProcessor"] = None

    uni_lock: Lock = None

    @classmethod
    def load_context(cls):
        if not cls.config:
            cls.config = Config()
            cls.config.load_config()
        cls.__build_context()
        cls.__load_builtins()
        if not cls.recorder:
            cls.recorder = RecorderFactory.get(cls.config['DEVICE_REC'])
        if not cls.player:
            cls.player = PlayerFactory.get(cls.config['DEVICE_PLY'])
        if not cls.asr_processor:
            cls.asr_processor = AsrProcessorFactory.get(cls.config['ASR_PROCESSOR'])
        if not cls.tts_processor:
            cls.tts_processor = TtsProcessorFactory.get(cls.config['TTS_PROCESSOR'])
        if not cls.messages_processor:
            cls.messages_processor = \
                MessagesProcessor(hostname=cls.config['MQTT_HOST'], port=int(cls.config['MQTT_PORT']))
        if not cls.uni_lock:
            cls.uni_lock = Lock()

    @classmethod
    def __load_builtins(cls):
        models = get_all_core_packages()
        for model in models:
            load_models(model)

    @classmethod
    def __build_context(cls):
        mkdir(cls.config['RESOURCE_PATH'], ['wav', 'txt'])

    @classmethod
    def __str__(cls):
        return f'''{{
            config: {cls.config},
            recorder: {cls.recorder.__class__.__name__},
            player: {cls.player.__class__.__name__},
            asr_processor: {cls.asr_processor.__class__.__name__},
            tts_processor: {cls.tts_processor.__class__.__name__},
            messages_processor: {cls.messages_processor.__class__.__name__}
        }}
        '''
