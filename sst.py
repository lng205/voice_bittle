import datetime
import hashlib
import base64
import hmac
import json
from urllib.parse import urlencode
import time
from wsgiref.handlers import format_date_time
from datetime import datetime
from time import mktime
import _thread as thread

import pyaudio
from key import APPID

STATUS_FIRST_FRAME = 0  # 第一帧的标识
STATUS_CONTINUE_FRAME = 1  # 中间帧标识
STATUS_LAST_FRAME = 2  # 最后一帧的标识


class Ws_Param(object):
    # 初始化
    def __init__(self, APPID, APIKey, APISecret):
        self.APPID = APPID
        self.APIKey = APIKey
        self.APISecret = APISecret

    # 生成url
    def create_url(self):
        url = 'wss://ws-api.xfyun.cn/v2/iat'
        # 生成RFC1123格式的时间戳
        now = datetime.now()
        date = format_date_time(mktime(now.timetuple()))

        # 拼接字符串
        signature_origin = "host: " + "ws-api.xfyun.cn" + "\n"
        signature_origin += "date: " + date + "\n"
        signature_origin += "GET " + "/v2/iat " + "HTTP/1.1"
        # 进行hmac-sha256进行加密
        signature_sha = hmac.new(self.APISecret.encode('utf-8'), signature_origin.encode('utf-8'),
                                 digestmod=hashlib.sha256).digest()
        signature_sha = base64.b64encode(signature_sha).decode(encoding='utf-8')

        authorization_origin = "api_key=\"%s\", algorithm=\"%s\", headers=\"%s\", signature=\"%s\"" % (
            self.APIKey, "hmac-sha256", "host date request-line", signature_sha)
        authorization = base64.b64encode(authorization_origin.encode('utf-8')).decode(encoding='utf-8')
        # 将请求的鉴权参数组合为字典
        v = {
            "authorization": authorization,
            "date": date,
            "host": "ws-api.xfyun.cn"
        }
        # 拼接鉴权参数，生成url
        url = url + '?' + urlencode(v)
        return url


# 收到websocket错误的处理
def on_error(ws, error):
    print("### error:", error)


# 收到websocket关闭的处理
def on_close(ws,a,b):
    print("### closed ###")


# 收到websocket连接建立的处理
# 整个会话时长最多持续60s，或者超过10s未发送数据，服务端会主动断开连接。
def on_open(ws):
    def run(*args):
        frameSize = 1280  # Size of the audio frame
        intervel = 0.04  # Time between sending audio (in seconds)
        status = STATUS_FIRST_FRAME  # Status of the audio frame

        # Setup PyAudio
        p = pyaudio.PyAudio()
        stream = p.open(format=pyaudio.paInt16,
                        channels=1,
                        rate=16000,
                        input=True,
                        frames_per_buffer=frameSize)
        while True:
            buf = stream.read(frameSize, exception_on_overflow=False)
            if not buf:
                status = STATUS_LAST_FRAME

            # First frame
            if status == STATUS_FIRST_FRAME:
                d = {"common": {"app_id": APPID},
                        "business": {"domain": "iat", "language": "zh_cn",
                                     "accent": "mandarin", "vinfo":1,"vad_eos":10000},
                        "data": {"status": 0, "format": "audio/L16;rate=16000",
                                "audio": str(base64.b64encode(buf), 'utf-8'),
                                "encoding": "raw"}}
                ws.send(json.dumps(d))
                status = STATUS_CONTINUE_FRAME
            # Intermediate frames
            elif status == STATUS_CONTINUE_FRAME:
                d = {"data": {"status": 1, "format": "audio/L16;rate=16000",
                                "audio": str(base64.b64encode(buf), 'utf-8'),
                                "encoding": "raw"}}
                ws.send(json.dumps(d))

    thread.start_new_thread(run, ())
