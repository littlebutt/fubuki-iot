from iot.semantics import SemanticsGroup

from iot.models import SemanticsModel, SemanticsFromEnum, SemanticsRedirectEnum, SemanticsFunc, UniverseNoticeModel, \
    FunctionDeviceModel


def qq_recieving_func(**kwargs) -> UniverseNoticeModel:
    ...


@SemanticsGroup.add_model
class QQRecievingSemanticModel(SemanticsModel):
    code = 'qq_receiving'
    frm = SemanticsFromEnum.DEVICE
    topic = 'self/qq'
    redirect = SemanticsRedirectEnum.ACOUSTICS
    func: SemanticsFunc = qq_recieving_func


def qq_sending_func(*args) -> FunctionDeviceModel:
    return FunctionDeviceModel(smt_code="qq_sending",
                               topic="qq/nonebot",
                               is_raw=False,
                               acoustics="好的，消息已为您发送",
                               data={
                                   'target': args[1],
                                   'content': args[2]
                               })


@SemanticsGroup.add_model
class QQSendingSemanticsModel(SemanticsModel):
    code = 'qq_sending'
    frm = SemanticsFromEnum.USER
    regex = '给(.*)发送(.*)'
    regex_num = 3
    redirect = SemanticsRedirectEnum.MESSAGE
    func: SemanticsFunc = qq_sending_func
