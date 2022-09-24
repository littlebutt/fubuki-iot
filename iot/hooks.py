from typing import List, Union, Optional, Type

from loguru import logger

from iot.context import Context
from iot.models import OnStartUpHook, OnTearDownHook, OnModelPreprocessHook, OnModelPostprocessHook, \
    FunctionDeviceModel, UniverseNoticeModel
from iot.semantics import SemanticsGroup


class HooksGroup:
    __on_start_up_hooks: List['OnStartUpHook'] = []
    __on_tear_down_hooks: List['OnTearDownHook'] = []
    __on_model_preprocess_hooks: List['OnModelPreprocessHook'] = []
    __on_model_postprocess_hooks: List['OnModelPostprocessHook']= []

    @classmethod
    def on_start_up(cls, on_start_up_hook: OnStartUpHook):
        cls.__on_start_up_hooks.append(on_start_up_hook)
        logger.info("已加载钩子函数 " + on_start_up_hook.__str__())

    @classmethod
    def on_tear_down(cls, on_tear_down_hook: OnTearDownHook):
        cls.__on_tear_down_hooks.append(on_tear_down_hook)
        logger.info("已加载钩子函数 " + on_tear_down_hook.__str__())

    @classmethod
    def on_model_preprocess(cls, on_model_preprocess_hook: OnModelPreprocessHook):
        cls.__on_model_preprocess_hooks.append(on_model_preprocess_hook)
        logger.info("已加载钩子函数 " + on_model_preprocess_hook.__str__())

    @classmethod
    def on_model_postprocess(cls, on_model_postprocess_hook: OnModelPostprocessHook):
        cls.__on_model_postprocess_hooks.append(on_model_postprocess_hook)
        logger.info("已加载钩子函数 " + on_model_postprocess_hook.__str__())

    @classmethod
    def execute_start_up(cls, context: Type[Context], semantics_group: Type[SemanticsGroup]):
        for hook in cls.__on_start_up_hooks:
            hook(context=context, semantics_group=semantics_group)

    @classmethod
    def execute_tear_down(cls, context: Type[Context], semantics_group: Type[SemanticsGroup]):
        for hook in cls.__on_tear_down_hooks:
            hook(context=context, semantics_group=semantics_group)

    @classmethod
    def execute_model_preprocess(cls, context: Type[Context], model: Union[FunctionDeviceModel, UniverseNoticeModel]):
        for hook in cls.__on_model_preprocess_hooks:
            hook(context, model)

    @classmethod
    def execute_model_postprocessor(cls, context: Type[Context], model: Optional[Union[FunctionDeviceModel, UniverseNoticeModel]]):
        for hook in cls.__on_model_postprocess_hooks:
            hook(context, model)