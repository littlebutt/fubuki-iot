# Fubuki Iot —— 物联网智能终端


![PyPI](https://img.shields.io/pypi/v/fubuki-iot) ![GitHub](https://img.shields.io/github/license/littlebutt/fubuki-iot) ![GitHub last commit](https://img.shields.io/github/last-commit/littlebutt/fubuki-iot) ![](https://img.shields.io/github/repo-size/littlebutt/fubuki-iot) ![](https://img.shields.io/badge/QQ-1136681910-9cf?logo=tencentqq&logoColor=9cf)

## 简介

Fubuki Iot是一款开源的物联网智能终端，类似于市面上的天猫精灵，小爱同学等。它可以监听智能家居的消息，也可以根据用户语音向智能家居
发送消息，从而实现家居智能化。与市面上各种终端相比，它具有以下优点：

- 定制化程度更高：用户可以自己实现对家居的控制，甚至对原有的家居电器改造
- 安全性更好：由于可以部署在本地局域网上，因此个人信息不会被上传到外网
- 效率更高：通过MQTT协议完成设备之间的交流，不需要复杂的流程

经过测试，本框架可以很好的支持Windows系统和树莓派（Linux）系统。

## 快速上手

### 安装

#### 方案一：通过`pip`安装

（待完善）

#### 方案二：下载安装

首先在终端执行以下命令：

```shell script
git clone git@github.com:littlebutt/fubuki-iot.git
```

然后进入根目录，执行以下命令安装`fubuki-iot`包

```shell script
python setup.py install
```

#### 方案三：通过`docker`安装

同样像方案三中下载项目到本地，然后执行以下命令

```shell script
docker build -t fubuki-iot:latest .
docker run -it fubuki-iot:latest /bin/bash
```
 就可以进入到容器内部了
 
 ### 启动
 
 本项目内置了 [百度云](https://cloud.baidu.com/) 的语音合成和语音识别的功能，因此使用之前需要免费申请百度云账号，
 点击 [这里](https://login.bce.baidu.com/new-reg?tpl=bceplat&from=portal) 申请。申请之后开通"产品"-"人工智能"-"语音技术"的服务。
 当然，您也可以用开源方案自己训练模型替代内置的语音功能，具体见 **进阶功能** 。
 
 1.创建资源目录
 首先创建一个Python工程 `demo` ，并在根目录下创建一个目录命名为`resources`
 
 2.创建`.env`文件
 
 在新建的工程下创建一个`.env`配置文件，其内容参考如下：
 
 ```text
ENVIRONMENT=dev
RESOURCE_PATH=刚才创建的resources目录，结尾不要加“/”
BAIDU_ACCESS_TOKEN=百度云API的token，可以留空
BAIDU_API_KEY=申请的百度云的AK
BAIDU_SECRET_KEY=申请的百度云的密钥
```

 3.创建主程序

在根目录下创建文件 `app.py`，并写入以下内容

```python
from iot import Terminal


Terminal.run()
```
运行即可启动


### 使用

目前主流的物联网信息交换都采用 [MQTT协议](https://www.runoob.com/w3cnote/mqtt-intro.html) ，因此要实现控制智能设备需要部署MQTT
服务器。本项目建议使用 [EMQX](https://www.emqx.com/zh/mqtt) 服务器，具体安装和部署方法点击 [这里](https://www.emqx.io/docs/en/v5.0/deploy/install.html#tar-gz-linux-macos-windows) 。

若要完整的实现对硬件设备的控制可以参考 **相关资料** 。
#### 内置功能

1.对话

运行智能终端后，按下键盘上的f可以进行录音。对着麦克风说出“在吗”、“你好”后，智能终端会回应“在的”。

2.控制开关和电灯

运行智能终端，按下键盘上的f后对着麦克风说出“打开开关”，然后它会向MQTT服务器的`default/switch` Topic发送以下信息：

```json
{
  "switch": "on"
}
```

同样，对着麦克风说出“关闭开关”后，它会向MQTT服务器的`default/switch` Topic发送以下信息：

```json
{
  "switch": "off"
}
```

具体效果需要由订阅了 `default/switch` Topic的智能设备实现。

此外，运行智能终端，按下键盘上的f后对着麦克风说出“打开卧室/客厅/餐厅灯”也会向MQTT服务器的`default/light` Topic发送以下信息：

```json
{
  "position": "bedroom/livingroom/dinningroom" 
}
```

3.接受按钮信息

运行终端，当由设备向MQTT服务器的 `self/button` 发送如下消息后，终端会说“有人按下了按钮”。

```json
{
  "topic":"self/button",
  "device":"button",
  "verbose":"false",
  "message":"有人按下了按钮"
}
```

#### 自定义功能

1.自定义语音功能

语音功能可以理解为用户和智能终端进行对话，类似于机器人的对话功能。这种功能一般不涉及硬件。在天猫精灵中，
就内置了提醒助手、墨迹天气等语音功能。

首先在自己创建的Python项目的根目录中创建一个包（package）命名为 `models` ，在这个包中创建一个python文件 `acoustics.py`，
在文件中定义一个语义模型：

```python
from iot import SemanticsGroup, SemanticsModel, SemanticsRedirectEnum, SemanticsFromEnum, SemanticsFunc

@SemanticsGroup.add_model
class MySemanticsModel(SemanticsModel):

    code = 'hello'                                  # 语义模型的标识，自定义

    frm = SemanticsFromEnum.USER                    # 语义模型的来源，这里是接受用户的语音命令，所以是USER

    topic = ''                                      # 由于不涉及发布消息，所以这个字段用不到，留空就行

    regex = "(.*)后提醒我(.*)"                       # 匹配用户语音命令的正则表达式，比如这里是一个有关提醒的命令

    regex_num = 3                                   # 上述表达式匹配后的分组（group）的数量，第一个为用户命令全量文本，第二个是“后”前面的文本，第三个是“我”后面的文本

    redirect = SemanticsRedirectEnum.ACOUSTICS      # 语义处理好后的重定向，由于不需要发送消息等后续操作，所以这里是直接语音返回

    func: SemanticsFunc = my_semantics_model_func   # 处理用户命令的回调函数
```

在上面的语义模型中，最后一个字段是一个 `SemanticsFunc` 实例，它是一个返回 `FunctionDeviceModel` 或者 `UniverseNoticeModel` 的方法
因此，需要这样定义：

```python
from typing import Union
from iot import UniverseNoticeModel, FunctionDeviceModel

def my_semantics_model_func(*args) -> Union[FunctionDeviceModel, UniverseNoticeModel]:

    time = args[1]                                      # 获取时间

    content = args[2]                                   # 获取提醒内容

    # 处理提醒命令，可以借助其他API实现

    return FunctionDeviceModel(                         # 最后返回一个功能设备模型

        smt_code='hello',                               # 对应的语义模型标识

        is_raw=True,                                    # 是否为纯文本

        acoustics=f"好的，我会在{time}后提醒你{content}", # 返回给用户的语音内容

        data=""                                         # 由于是纯文本，所以这个字段用不到

    )
```

定义好以后需要在 `app.py` 中加入一行：

```python
from iot import Terminal


Terminal.load_models('demo.models')
Terminal.run()
```

2.自定义设备功能

智能终端最大的优势就是可以通过语音控制智能家居。同样，需要定义一个语义模型实现这个功能：

```python
from typing import Union

from iot import SemanticsGroup, SemanticsModel, SemanticsRedirectEnum, SemanticsFromEnum, SemanticsFunc, UniverseNoticeModel, FunctionDeviceModel


def curtain_semantics_model_func(*args) -> Union[FunctionDeviceModel, UniverseNoticeModel]:
    return FunctionDeviceModel(

        smt_code="hi",

        topic="default/curtain",                        # 发送的Topic，其实后续会被语义模型的Topic覆盖

        is_raw=False,                                   # 不再是纯文本返回了

        acoustics="好的，正在为你打开窗帘",                # 返回给用户的提示信息

        data={                                          # 发送的数据
            'state': 'on'
        }
    )


@SemanticsGroup.add_model
class SwitchOnSemanticsModel(SemanticsModel):

    code = "hi"

    frm = SemanticsFromEnum.USER

    topic = 'default/curtain'

    regex = "打开窗帘"

    regex_num = 1

    redirect = SemanticsRedirectEnum.MESSAGE # 重定向给消息，因为需要发送MQTT消息

    func: SemanticsFunc = curtain_semantics_model_func
```

具体怎么消费这个MQTT消息，即硬件设备如何处理则需要改造硬件，具体参考 **相关资料** 。

3.自定义消息推送

和之前一样，也需要定义一个语义模型：

```python
from typing import Optional

from iot import SemanticsGroup, SemanticsModel, SemanticsRedirectEnum, SemanticsFromEnum, SemanticsFunc, UniverseNoticeModel


def button_semantics_model_func(model) -> UniverseNoticeModel:

    #处理设备推送的统一推送模型

    return UniverseNoticeModel(                 # 这次返回的是统一推送模型

        smt_code='hei', 

        topic='self/weather',                   # topic，被用来检索语义模型的

        device='remote_server',                 # 设备来源

        verbose=False,                          # 是否多语，这里只需要通知以下用户所以选择False

        message="天气播报：短期将有大量降雨"       # 返回给用户的信息
    )


@SemanticsGroup.add_model
class ButtonSemanticsModel(SemanticsModel):

    code = "hei"

    frm = SemanticsFromEnum.DEVICE                  # 来自设备

    topic = 'self/weather'

    regex: Optional[str] = None

    regex_num: Optional[str] = None

    redirect = SemanticsRedirectEnum.ACOUSTICS      #直接返回

    func: SemanticsFunc = button_semantics_model_func

```
至此，可以实现一个简单的物联网终端！

## 进阶功能

如果您对上述基本功能还不满足，可以试一下进阶功能。

1.生命周期和钩子函数

本智能终端在运行时分为以下几个阶段，在不同的阶段可以调用不同的钩子函数实现流程定制化：

```text
                                                             ___________________________________循环______________________________________
                                                             |                                                                           |
    |加载用户模型| ->  |加载上下文| -> |执行启动钩子| -> |监听用户/设备请求| -> |执行前置语义处理钩子| -> |处理请求| -> |执行后置语义处理钩子| ->|转发请求| -> |执行卸载钩子| -> |卸载|
                                                             |                                                                           |
                                                             |——————————————————————————————————循环——————————————————————————————————————|
```

从上图可以看出，一共有四个钩子函数，分别是 `OnStartUpHook`、 `OnModelPreprocessHook` 、 `OnModelPostprocessHook` 和 `OnTearDown`。可以通过以下方法编写钩子函数：

```python
from iot import HooksGroup

@HooksGroup.on_start_up
def start_up(context, semantics_group):
    ...


@HooksGroup.on_tear_down
def tear_down(context, semantics_group):
    ...


@HooksGroup.on_model_preprocess
def model_preprocess(context, function_device_model):
    ...


@HooksGroup.on_model_postprocess
def model_postprocess(context, function_device_model):
    ...
```

钩子函数可以获取到执行阶段的上下文，包括各种处理器信息和配置信息。此外，**启动钩子** 和 **卸载钩子** 可以获取语义处理模型的集合而 **前置语义处理钩子** 和 **后置语义处理钩子** 可以获取到语义模型。

2.自定义设备和语音处理器

本智能终端的设备（麦克风和扬声器）都是用的Windows默认的，如果要用在树莓派或者其他环境则需要自定义设备，包括麦克风（Recorder）和扬声器（Player）。

首先实现对应的类：

```python
from iot import RecorderFactory, Recorder

@RecorderFactory.set
class MyRecorder(Recorder):      # 继承Recorder类，并加上注解
    
    def awake(self) -> bool:          # 实现awake方法，这个方法必须是个阻塞的方法，返回True则开始录音，返回False则推出程序
        ...

    def record(self, time: int) -> str: # 录音，time为录音时长，返回录音后保存的路径
        ...
```

然后在 `.env` 文件中修改默认的麦克风设备:

```text
DEVICE_REC=MyRecorder
```

同样，扬声器也是这样的步骤：

```python
from iot import PlayerFactory, Player

@PlayerFactory.set
class MyPlayer(Player):

    def play(self, path: str) -> None:    # path为存储语音文本的txt文件路径
        ...
```

然后更改 `.env` 文件

```text
DEVICE_PLY=MyPlayer
```

您也可以修改默认的语音处理器，包括语音识别（AsrProcessor）和语音合成（TtsProcessor），方法也是一样的。

```python
from iot import AsrProcessorFactory, AsrProcessor
from typing import Optional


@AsrProcessorFactory.set
class MyAsrProcessor(AsrProcessor):

    def asr(self, path: str) -> Optional[str]: # path为音频文件（一般为wav）的路径，返回语音文字，如果为None则说明处理失败
        ...
```

`.env` 文件

```text
ASR_PROCESSOR=MyAsrProcessor
```

语音合成可以这样修改：

```python
from iot import TtsProcessorFactory, TtsProcessor


@TtsProcessorFactory.set
class MyTtsProcessor(TtsProcessor):

    def tts(self, text: str) -> str:  # text为需要被合成的文字，返回合成后的音频文件路径
        ...
```

`.env` 文件

```text
TTS_PROCESSOR=MyTtsProcessor
```


## 相关资料

1. 如何实现智能设备

2. 智能家居设备交流消息的抓取


## 待实现功能

1.语音追问功能

2.音频等流媒体的播放

3.语音唤醒

4. 语义模型的order