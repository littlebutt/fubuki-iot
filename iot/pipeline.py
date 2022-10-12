from loguru import logger

from iot.config import Config
from iot.context import Context
from iot.hooks import HooksGroup
from iot.integration.mqtt import MQTT_UserData, MQTT_Client, MQTT_Message
from iot.semantics import SemanticsGroup
from iot.models import SemanticsRedirectEnum, UniverseNoticeModel, FunctionDeviceModel
from iot.utils import raw_to_function_device_model


class Pipeline:

    @staticmethod
    def before(**kwargs):
        if not kwargs:
            config = Config()
            config.data = kwargs
            Context.config = config
        logger.info("开始加载智能终端上下文")
        Context.load_context()
        logger.info("上下文加载完成 " + Context.__str__())
        HooksGroup.execute_start_up(context=Context, semantics_group=SemanticsGroup)

    @staticmethod
    def user_loop():

        while True:
            logger.info("开始监听用户指令")
            if Context.recorder.awake():
                with Context.uni_lock:
                    logger.info("智能终端被唤醒")
                    path = Context.tts_processor.tts("我在，你说")
                    Context.player.play(path)
                    time = int(Context.config['RECORDER_TIME']) if 'RECORDER_TIME' in Context.config else 3
                    path = Context.recorder.record(time)
                    logger.info("已完成录音，路径：" + path)
                    message = Context.asr_processor.asr(path)
                    if message is None:
                        logger.warning("语音识别发生错误")
                        Pipeline.play_error_reminder()
                        continue
                    logger.info("已完成语音识别，内容：" + message)
                    model = raw_to_function_device_model(message)
                    HooksGroup.execute_model_preprocess(context=Context, model=model)
                    result, redirection = SemanticsGroup.process_usr_command(model)
                    HooksGroup.execute_model_postprocessor(context=Context, model=model)
                    if redirection == SemanticsRedirectEnum.ACOUSTICS:
                        logger.info("语义转换成功，重定向至ACOUSTICS")
                        path = Context.tts_processor.tts(result.acoustics if result.acoustics else result.data)
                        Context.player.play(path)
                        continue
                    elif redirection == SemanticsRedirectEnum.MESSAGE:
                        logger.info("语义转换成功，重定向至MESSAGE")
                        Context.messages_processor.publish(result)
                        path = Context.tts_processor.tts(result.acoustics)
                        Context.player.play(path)
                        continue
                    else:
                        logger.info("语义转换失败")
                        Pipeline.play_error_reminder()
                        continue
            break

    @staticmethod
    def device_loop():
        def inner_callback(client: MQTT_Client, user_data: MQTT_UserData, message: MQTT_Message):
            with Context.uni_lock:
                payload = str(message.payload, 'utf-8')
                logger.info(f"获取到来自设备消息，topic：{message.topic} payload：{payload}")
                universe_notice_model = None
                try:
                    universe_notice_model = UniverseNoticeModel.parse_raw(payload)
                    logger.success("成功转换成统一推送模型")
                except Exception as e:
                    logger.error("转换成统一推送模型失败 " + e.__str__())
                    return
                universe_notice_model.topic = message.topic
                HooksGroup.execute_model_preprocess(context=Context, model=universe_notice_model)
                result, redirection = SemanticsGroup.process_dvc_command(universe_notice_model)
                HooksGroup.execute_model_postprocessor(context=Context, model=universe_notice_model)
                if not result.verbose:
                    logger.info("语义转换成功，重定向至ACOUSTICS并直接返回")
                    path = Context.tts_processor.tts(result.message)
                    Context.player.play(path)
                else:
                    if redirection == SemanticsRedirectEnum.MESSAGE:
                        logger.info("语义转换成功，重定向至MESSAGE")
                        model = FunctionDeviceModel.parse_obj(result.data)
                        Context.messages_processor.publish(model)
                    elif redirection == SemanticsRedirectEnum.ACOUSTICS:
                        logger.info("语义转换成功，重定向至ACOUSTICS")
                        path = Context.tts_processor.tts(result.message)
                        Context.player.play(path)
                    else:
                        logger.info("语义转换失败")
                        Pipeline.play_error_reminder()

        logger.info("开始监听设备消息...")
        Context.messages_processor.subscribe('self/#', inner_callback)

    @staticmethod
    def after():
        HooksGroup.execute_tear_down(context=Context, semantics_group=SemanticsGroup)

    @staticmethod
    def play_error_reminder() -> None:
        reminder = "抱歉，好像遇到了点问题"
        path = Context.tts_processor.tts(reminder)
        Context.player.play(path)