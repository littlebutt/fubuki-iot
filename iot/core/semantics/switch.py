from iot.semantics import SemanticsGroup
from iot.models import SemanticsModel, SemanticsFromEnum, SemanticsRedirectEnum, FunctionDeviceModel, SemanticsFunc


def switch_semantics_model_func(*args) -> FunctionDeviceModel:
    param = args[0]
    if param == "打开开关":
        return FunctionDeviceModel(smt_code="default01",
                                   topic="switch",
                                   is_raw=False,
                                   acoustics="好的，已为您打开开关",
                                   data={
                                       'switch': 'on'
                                   })
    else:
        return FunctionDeviceModel(smt_code="default02",
                                   topic="switch",
                                   is_raw=False,
                                   acoustics="好的，已为您关闭开关",
                                   data={
                                       'switch': 'off'
                                   })


@SemanticsGroup.add_model
class SwitchOnSemanticsModel(SemanticsModel):
    code = "default01"
    frm = SemanticsFromEnum.USER
    topic = 'default/switch'
    regex = "打开开关"
    regex_num = 1
    redirect = SemanticsRedirectEnum.MESSAGE
    func: SemanticsFunc = switch_semantics_model_func


@SemanticsGroup.add_model
class SwitchOffSemanticssModel(SemanticsModel):
    code = "default02"
    frm = SemanticsFromEnum.USER
    topic = 'default/switch'
    regex = "关闭开关"
    regex_num = 1
    redirect = SemanticsRedirectEnum.MESSAGE
    func: SemanticsFunc = switch_semantics_model_func
