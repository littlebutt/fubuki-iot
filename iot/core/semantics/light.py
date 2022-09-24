from iot.semantics import SemanticsGroup
from iot.models import SemanticsModel, SemanticsFromEnum, SemanticsRedirectEnum, FunctionDeviceModel, SemanticsFunc


def light_semantics_model_func(*args) -> FunctionDeviceModel:
    param = args[1]
    if param == "卧室":
        return FunctionDeviceModel(smt_code="default03",
                                   topic="light",
                                   is_raw=False,
                                   acoustics="好的，正在为你打开卧室灯",
                                   data={
                                       'position': 'bedroom'
                                   })
    elif param == "客厅":
        return FunctionDeviceModel(smt_code="default03",
                                   topic="light",
                                   is_raw=False,
                                   acoustics="好的，正在为你打开客厅灯",
                                   data={
                                       'position': 'livingroom'
                                   })
    else:
        return FunctionDeviceModel(smt_code="default03",
                                   topic="light",
                                   is_raw=False,
                                   acoustics="好的，正在为你打开餐厅灯",
                                   data={
                                       'position': 'dinningroom'
                                   })


@SemanticsGroup.add_model
class SwitchOnSemanticsModel(SemanticsModel):
    code = "default03"
    frm = SemanticsFromEnum.USER
    topic = 'default/light'
    regex = "打开(.*)灯"
    regex_num = 2
    redirect = SemanticsRedirectEnum.MESSAGE
    func: SemanticsFunc = light_semantics_model_func