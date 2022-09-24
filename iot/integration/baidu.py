import base64
import json
from typing import Optional
from urllib.request import urlopen
from urllib.request import Request
from urllib.parse import quote_plus, urlencode
from urllib.error import URLError

import requests
from loguru import logger

from iot.context import Context


class BaiduCloudClient:
    __access_token: str = None

    def __init__(self, api_key: str, secret_key: str, access_token: str = None):
        if access_token:
            self.__access_token = access_token
        else:
            url = f'https://aip.baidubce.com/oauth/2.0/token?' \
                  f'grant_type=client_credentials&client_id={api_key}&client_secret={secret_key}'
            response = requests.get(url)
            if response:
                self.__access_token = response.json()['access_token']
                logger.info("access_token " + self.__access_token)

    def asr(self, path: str) -> Optional[str]:
        speech_data = []
        with open(path, 'rb') as speech_file:
            speech_data = speech_file.read()
        length = len(speech_data)
        if length == 0:
            logger.error("Cannot read anything from " + path)
            return None
        speech = base64.b64encode(speech_data)
        speech = str(speech, 'utf-8')
        params = {'dev_pid': 1537,
                  'format': path[-3:],
                  'rate': 16000,
                  'token': self.__access_token,
                  'cuid': 'fubuki_cuid',
                  'channel': 1,
                  'speech': speech,
                  'len': length
                  }
        post_data = json.dumps(params, sort_keys=False)
        req = Request('http://vop.baidu.com/server_api', post_data.encode('utf-8'))
        req.add_header('Content-Type', 'application/json')
        try:
            f = urlopen(req)
            result_str = f.read()
            result = json.loads(result_str)
            if result['err_no'] != 0:
                logger.error("Fail to process ASR " + result['err_msg'])
                return None
            result_str = ' '.join(result['result'])
        except URLError as e:
            logger.error(f"Fail to acquire ASR result from BaiduCloud " + e.reason)
            result_str = None
        return result_str

    def tts(self, text: str, filename: str,
            per: int = 0, spd: int = 5, pit: int = 5, vol: int = 5) -> bool:
        text = quote_plus(text)
        params = {'tok': self.__access_token,
                  'tex': text,
                  'per': per,
                  'spd': spd,
                  'pit': pit,
                  'vol': vol,
                  'aue': 6, # wav file
                  'cuid': 'fubuki_cuid',
                  'lan': 'zh',
                  'ctp': 1}
        data = urlencode(params)
        req = Request('http://tsn.baidu.com/text2audio', data.encode('utf-8'))
        has_error = False
        try:
            f = urlopen(req)
            result_str = f.read()

            headers = dict((name.lower(), value) for name, value in f.headers.items())

            has_error = ('content-type' not in headers.keys() or headers['content-type'].find('audio/') < 0)
        except URLError as e:
            logger.error(f"Fail to acquire tts result from BaiduCloud " + e.strerror)
            result_str = e.reason
            has_error = True
        if not has_error:
            with open(filename, 'wb') as of:
                of.write(result_str)
        else:
            logger.error(f"Fail to save tts result")
        return not has_error


class BaiduApi:
    client: BaiduCloudClient = None

    @classmethod
    def register(cls) -> BaiduCloudClient:
        if cls.client is None:
            cls.access_token = Context.config['BAIDU_ACCESS_TOKEN']
            cls.api_key = Context.config['BAIDU_API_KEY']
            cls.secret_key = Context.config['BAIDU_SECRET_KEY']
            cls.client = BaiduCloudClient(api_key=cls.api_key, secret_key=cls.secret_key, access_token=cls.access_token)
        return cls.client

