from typing import Optional

from iot.semantics import SemanticsGroup
from iot.models import SemanticsModel, SemanticsFromEnum, SemanticsRedirectEnum, SemanticsFunc, UniverseNoticeModel


def button_semantics_model_func(*args) -> UniverseNoticeModel:
    return UniverseNoticeModel(
        smt_code='default05',
        topic='self/button',
        device='button',
        verbose=False,
        message="有人按下了按钮"
    )


@SemanticsGroup.add_model
class ButtonSemanticsModel(SemanticsModel):
    code = "default05"
    frm = SemanticsFromEnum.DEVICE
    topic = 'self/button'
    regex: Optional[str] = None
    regex_num: Optional[str] = None
    redirect = SemanticsRedirectEnum.ACOUSTICS
    func: SemanticsFunc = button_semantics_model_func
