from iot.semantics import SemanticsGroup
from iot.models import SemanticsModel, SemanticsFromEnum, SemanticsRedirectEnum, SemanticsFunc, FunctionDeviceModel


def dialog_semantics_model_func(*args) -> FunctionDeviceModel:
    return FunctionDeviceModel(
        smt_code='default04',
        is_raw=True,
        acoustics="在的",
        data="在的"
    )


@SemanticsGroup.add_model
class DialogSemanticsModel(SemanticsModel):
    code = "default04"
    frm = SemanticsFromEnum.USER
    topic = ''
    regex = "在吗"
    regex_num = 1
    redirect = SemanticsRedirectEnum.ACOUSTICS
    func: SemanticsFunc = dialog_semantics_model_func


def complex_dialog_semantics_model_func(*args) -> FunctionDeviceModel:
    return FunctionDeviceModel(
        smt_code='default04',
        is_raw=False,
        acoustics="",
        data=""
    )


@SemanticsGroup.add_model
class ComplexDialogSemanticsModel(SemanticsModel):
    code = 'default06'
    frm = SemanticsFromEnum.USER
    topic = ''
    regex = "你好"
    regex_num = 1
    redirect = SemanticsRedirectEnum.SEMANTICS
    func: SemanticsFunc = complex_dialog_semantics_model_func