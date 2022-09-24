from typing import Dict, ClassVar

from iot.models import Factory, Recorder, Player, AsrProcessor, TtsProcessor


class RecorderFactory(Factory):
    __recorder: ClassVar[Dict[str, "Recorder"]] = {}

    @classmethod
    def set(cls, target):
        cls.__recorder[target.__name__] = target()

    @classmethod
    def get(cls, target_name):
        if target_name not in cls.__recorder:
            raise KeyError("Cannot find Recorder")
        return cls.__recorder[target_name]


class PlayerFactory(Factory):
    __player: ClassVar[Dict[str, "Player"]] = {}

    @classmethod
    def set(cls, target):
        cls.__player[target.__name__] = target()

    @classmethod
    def get(cls, target_name):
        if target_name not in cls.__player:
            raise KeyError("Cannot find Player")
        return cls.__player[target_name]


class AsrProcessorFactory(Factory):
    __asr_processor: ClassVar[Dict[str, "AsrProcessor"]] = {}

    @classmethod
    def set(cls, target):
        cls.__asr_processor[target.__name__] = target()

    @classmethod
    def get(cls, target_name):
        if target_name not in cls.__asr_processor:
            raise KeyError("Cannot find AsrProcesor")
        return cls.__asr_processor[target_name]


class TtsProcessorFactory(Factory):
    __tts_processor: ClassVar[Dict[str, "TtsProcessor"]] = {}

    @classmethod
    def set(cls, target):
        cls.__tts_processor[target.__name__] = target()

    @classmethod
    def get(cls, target_name):
        if target_name not in cls.__tts_processor:
            raise KeyError("Cannot find TtsProcessor")
        return cls.__tts_processor[target_name]