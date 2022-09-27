from concurrent.futures.thread import ThreadPoolExecutor
from typing import Union, Iterable, Optional

from iot.context import Context

from iot.pipeline import Pipeline
from iot.utils import load_models


class Terminal:

    @classmethod
    def load_models(cls, path: Optional[Union[str, Iterable[str]]]):
        if not path:
            return
        if type(path) is Iterable:
            for p in path:
                load_models(p)
        else:
            load_models(path)

    @classmethod
    def run(cls, *args, **kwargs):
        Pipeline.before(**kwargs)
        terminal_mode = Context.config['TERMINAL_MODE']
        if terminal_mode == '0':
            Pipeline.user_loop()
        elif terminal_mode == '1':
            Pipeline.device_loop()
        elif terminal_mode == '2':
            with ThreadPoolExecutor(max_workers=2) as pool:
                pool.submit(Pipeline.user_loop)
                pool.submit(Pipeline.device_loop)
        Pipeline.after()
