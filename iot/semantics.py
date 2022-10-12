import re
from typing import Dict, Tuple, Union, ClassVar, Optional

from loguru import logger

from iot.models import SemanticsModel, SemanticsFromEnum, SemanticsRedirectEnum, FunctionDeviceModel, UniverseNoticeModel


class SemanticsGroup:
    # 来自用户的语义模型，key为正则表达式，value为语义模型
    __inner_group_from_users: ClassVar[Dict[str, "SemanticsModel"]] = {}
    # 来自设备的语义模型，key为topic，value为语义模型
    __inner_group_from_devices: ClassVar[Dict[str, "SemanticsModel"]] = {}

    @classmethod
    def add_model(cls, model: type):
        model = model()
        if model.frm == SemanticsFromEnum.USER:
            cls.__inner_group_from_users[model.regex] = model
            logger.info("已加载用户语义模型：" + model.code)
        else:
            cls.__inner_group_from_devices[model.topic] = model
            logger.info("已加载设备语义模型：" + model.code)

    @classmethod
    def get_model(cls, key: str) -> Optional["SemanticsModel"]:
        for k in cls.__inner_group_from_users.keys():
            if k == key or re.match(k, key):
                return cls.__inner_group_from_users[k]
        for k in cls.__inner_group_from_devices.keys():
            if k == key:
                return cls.__inner_group_from_devices['k']
        return None

    @classmethod
    def process_usr_command(cls, function_device_model: FunctionDeviceModel) -> Tuple[Optional[FunctionDeviceModel],
                                                                                      SemanticsRedirectEnum]:
        if function_device_model.is_raw:
            for pattern in cls.__inner_group_from_users.keys():
                if res := re.match(pattern, function_device_model.data):
                    model = cls.__inner_group_from_users[pattern]
                    topic = model.topic
                    logger.info(f"{function_device_model.data}hits model: {model.code}")
                    args = []
                    for i in range(model.regex_num):
                        args.append(res.group(i))
                    called: Union[FunctionDeviceModel, UniverseNoticeModel]
                    try:
                        logger.info(f"{model.func} called，args：" + " ".join(args))
                        called = model.func(*args)
                        called.topic = topic if topic is not None else called.topic
                        logger.success(f"{model.func}called with success：" + called.__str__())
                    except Exception as e:
                        logger.error(f"{model.func}called in ERROR：{e}")
                        return None, SemanticsRedirectEnum.MISS
                    if model.redirect == SemanticsRedirectEnum.SEMANTICS:
                        logger.info(f"SemanticsModel redirects to SEMANTICS")
                        return cls.process_usr_command(called)
                    return called, model.redirect
        else:
            for pattern, model in cls.__inner_group_from_users.items():
                if model.code == function_device_model.smt_code:
                    logger.info(f"{function_device_model.data}hits model: {model.code}")
                    called: Union[FunctionDeviceModel, UniverseNoticeModel]
                    try:
                        logger.info(f"{model.func} called")
                        called = model.func(function_device_model)
                        logger.success(f"{model.func}called with success：" + called.__str__())
                    except Exception as e:
                        logger.error(f"{model.func}called in ERROR：{e}")
                        return None, SemanticsRedirectEnum.MISS
                    if model.redirect == SemanticsRedirectEnum.SEMANTICS:
                        logger.info(f"SemanticsModel redirects to SEMANTICS")
                        return cls.process_usr_command(called)
                    return called, model.redirect
        logger.warning(f"{function_device_model.data} cannot hit any model")
        return None, SemanticsRedirectEnum.MISS

    @classmethod
    def process_dvc_command(cls, universe_notice_model: UniverseNoticeModel) -> Tuple[Optional[UniverseNoticeModel],
                                                                                      SemanticsRedirectEnum]:
        if not universe_notice_model.verbose:
            logger.info(f"{universe_notice_model.message} returns directly")
            return universe_notice_model, SemanticsRedirectEnum.ACOUSTICS
        for topic in cls.__inner_group_from_devices.keys():
            if topic == universe_notice_model.topic:
                logger.info(f"{universe_notice_model.data} hits topic {topic}")
                model = cls.__inner_group_from_devices[topic]
                called: Union[FunctionDeviceModel, UniverseNoticeModel]
                try:
                    logger.info(f"{model.func} called")
                    called = model.func(universe_notice_model)
                    logger.success(f"{model.func}called with success：" + called.__str__())
                except Exception as e:
                    logger.error(f"{model.func}called in ERROR：{e}")
                    return None, SemanticsRedirectEnum.MISS
                if model.redirect == SemanticsRedirectEnum.SEMANTICS:
                    logger.info(f"SemanticsModel redirects to SEMANTICS")
                    return cls.process_dvc_command(called)
                return called, model.redirect
        logger.warning(f"{universe_notice_model.data} cannot hit any model")
        return None, SemanticsRedirectEnum.MISS
