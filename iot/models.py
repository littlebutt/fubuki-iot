import abc
from enum import Enum
from typing import Optional, Callable, Union, Dict, TYPE_CHECKING

from pydantic import BaseModel


class Factory(abc.ABC):

    @abc.abstractmethod
    def set(cls, target: type):
        raise NotImplementedError

    @abc.abstractmethod
    def get(cls, target_name):
        raise NotImplementedError


class Recorder(abc.ABC):

    @abc.abstractmethod
    def awake(self) -> bool:
        """
        唤醒终端设备，必须是一个阻塞方法
        :return: 返回True表示唤醒，返回False表示终止程序调用终止方法
        """
        raise NotImplementedError

    @abc.abstractmethod
    def record(self, time: int) -> str:
        """
        录音并存储，用于接受用户的指令，建议存储为wav格式
        :param time: 录音时长，默认3秒
        :return: 录音文件的地址
        """
        raise NotImplementedError


class Player(abc.ABC):

    @abc.abstractmethod
    def play(self, path: str) -> None:
        raise NotImplementedError


class AsrProcessor(abc.ABC):

    @abc.abstractmethod
    def asr(self, path: str) -> Optional[str]:
        """
        对给定路径的音频文件进行语音识别
        :param path: 音频文件的路径
        :return: 语音识别结果，即文字信息。返回`None`说明识别失败
        """
        raise NotImplementedError


class TtsProcessor(abc.ABC):

    @abc.abstractmethod
    def tts(self, text: str) -> str:
        """
        对给定文字进行语音合成
        :param text: 给定文字
        :return: 语音合成音频文件的路径，音频文件建议.wav格式
        """
        raise NotImplementedError


class Hook:

    def __call__(self, *args, **kwargs):
        """
        所有钩子函数都是函数
        :param args:
        :param kwargs:
        :return:
        """
        raise NotImplementedError


class OnStartUpHook(Hook):

    def __call__(self, *args, **kwargs):
        if TYPE_CHECKING:
            assert 'context' in kwargs
            assert 'semantics_group' in kwargs


class OnTearDownHook(Hook):

    def __call__(self, *args, **kwargs):
        if TYPE_CHECKING:
            assert 'context' in kwargs
            assert 'semantics_group' in kwargs


class  OnModelPreprocessHook(Hook):

    def __call__(self, *args, **kwargs):
        if TYPE_CHECKING:
            assert 'context' in kwargs
            assert 'function_device_model' in kwargs or 'universe_notice_mode' in kwargs


class OnModelPostprocessHook(Hook):

    def __call__(self, *args, **kwargs):
        if TYPE_CHECKING:
            assert 'context' in kwargs
            assert 'function_device_model' in kwargs or 'universe_notice_mode' in kwargs


class SemanticsFromEnum(Enum):
    USER = 1,
    DEVICE = 2,


class SemanticsRedirectEnum(Enum):
    ACOUSTICS = 1,
    MESSAGE = 2,
    SEMANTICS = 3,
    MISS = 4,


class FunctionDeviceModel(BaseModel):
    """
    功能设备模型，既是用户发送指令的封装，也是语义转换模块处理后的产物。需结合重定向枚举SemanticsRedirectEnum一起用才有明确语义
    """

    # 对应的semantics_model的code，如果is_raw为False则根据这个字段查找对应的semantics_model
    smt_code: Optional[str]

    # 对应的mqtt的topic，如果重定向到MESSAGE则需要给这个topic发送数据
    topic: Optional[str]

    # raw标志位，如果为True则data为str，在语义处理中根据data做正则匹配选择对应的语义模型
    # 如果为False则根据smt_code选择对应的语义模型
    is_raw: bool

    # 执行成功后返回的语音提示，如果重定向到MESSAGE则作为语音提示，
    # 如果是重定向到ACOUSTICS则也可以表示返回内容，
    # 如果重定向到SEMANTICS则没有意义
    acoustics: str

    # 数据，如果重定向到message则该字段作为mqtt发送的payload，
    # 如果是重定向到ACOUSTICS则也可以表示返回内容，
    # 如果重定向到SEMANTICS则再一次根据is_raw字段判断，如果is_raw为True则根据data字段匹配选择对应的语义模型
    data: Union[str, Dict[str, str]]


class UniverseNoticeModel(BaseModel):
    """
    统一推送模型，需结合重定向枚举SemanticsRedirectEnum一起用才有明确语义
    """

    # 对应的semantics_model的code，用户自用
    smt_code: Optional[str]

    # mqtt发送的topic，如果verbose字段为True，则根据topic字段匹配语义模型
    topic: str

    # 发布mqtt消息的设备名称，用户自用
    device: str

    # verbose标志位，如何处理设备推送消息的一句。如果为False则直接将message字段信息作为语音返回，
    # 如果为True，则data不为None，且根据topic查找语义模型
    verbose: bool

    # 返回的语音文本，如果verbose为True或者重定向为ACCOUSTICS，则直接返回该字段作为语音信息
    message: str

    # 数据，如果重定向给MESSAGE，则为FunctionDeviceModel
    data: Optional[Dict[str, str]]


SemanticsFunc = Callable[..., Union[FunctionDeviceModel, UniverseNoticeModel]]


class SemanticsModel(BaseModel):
    """
    语义模型
    """

    # 语义模型标识，自定义，一般用来检索
    code: str

    # 语义来源，用户或者设备
    frm: SemanticsFromEnum

    # topic，用来检索匹配
    topic: Optional[str]

    # 正则表达式，用来检索匹配
    regex: Optional[str]

    # 正则表达式的group_num
    regex_num: Optional[int]

    # 重定向，结合func的返回结果（模型）决定下一步怎么处理。分为返回语音ACOUSTICS、发布消息MESSAGE、继续语义处理SEMANTICS，
    # 当为MISS时说明没有命中，或者调用func出错
    redirect: SemanticsRedirectEnum

    # 处理语义，若来源为用户则参数为正则匹配结果groups，若为设备则为UniverseNoticeModel.data，
    # 返回元组，第一项是model，第二项是重定向
    func: SemanticsFunc
