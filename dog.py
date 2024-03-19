from openai import OpenAI
from key import *

client = OpenAI(api_key=OPENAI_API_KEY)

from tools import tools, skillFullName
from send_command import sendCommand, initBittle, closeBittle
from sst import Ws_Param, base64
import websocket, ssl, json, time, pyaudio
import _thread as thread

history = []


def main():
    global goodPorts
    goodPorts = initBittle()
    wsParam = Ws_Param(APPID=APPID, APISecret=APISERECT, APIKey=XF_APIKEY)
    wsUrl = wsParam.create_url()
    ws = websocket.WebSocketApp(
        wsUrl, on_message=on_message, on_error=on_error, on_close=on_close
    )
    ws.on_open = on_open
    ws.run_forever(sslopt={"cert_reqs": ssl.CERT_NONE})


def on_open(ws):
    def run():
        frameSize = 1280  # Size of the audio frame
        intervel = 0.04  # Length of the audio frame

        # Common JSON structure for sending data
        data_template = {
            "common": {"app_id": APPID},
            "business": {
                "domain": "iat",
                "language": "zh_cn",
                "accent": "mandarin",
                "vinfo": 1,
                "vad_eos": 30000 # 整个会话时长最多持续60s，或者超过30s未发送数据，服务端会主动断开连接。
            },
            "data": {
                "status": 0,
                "format": "audio/L16;rate=8000",
                "encoding": "raw"
            }
        }
        p = pyaudio.PyAudio()
        stream = p.open(format=pyaudio.paInt16,
                        channels=1,
                        rate=8000,
                        input=True,
                        frames_per_buffer=frameSize)
        print("* 开始录音...")
        while True:
            time.sleep(intervel)
            buf = stream.read(frameSize, exception_on_overflow=False)
            if not buf:
                continue

            data_template["data"]["audio"] = str(base64.b64encode(buf), 'utf-8')
            try:
                ws.send(json.dumps(data_template))
            except Exception as e:
                print(e)

            if data_template["data"]["status"] == 0:
                # Update status after the first frame
                data_template["data"]["status"] = 1

                # Remove the common and business fields after the first frame
                del data_template["common"]
                del data_template["business"]

    thread.start_new_thread(run, ())


def on_message(ws, message):
    try:
        data = json.loads(message)["data"]["result"]["ws"]
        result = ""
        for i in data:
            for w in i["cw"]:
                result += w["w"]
        result = result.strip("，。！？")
        if result:
            print("识别结果: " + result)
            tool = tool_choice(result, tools, history)
            history.append({"role": "user", "content": result})
            arguments = json.loads(tool.arguments)
            print(f"选择了{tool}")
            if not arguments:
                sendCommand(goodPorts, "k" + tool.name)
            else:
                sendCommand(goodPorts, tool.name, eval(arguments["data"]))
    except Exception as e:
        print(e)


def tool_choice(message, tools, history):
    """
    Send the message to the model with a list of tools and propmt the model to use the tools.
    Tools is a list of dict describing functions.
    Return the chosen function.
    """
    prompt = "你是一只机器小狗，你不会说话，请不要给response，永远用tool_choice操作。你只能从给出的tools中进行选择。"
    messages = [
        {"role": "system", "content": prompt},
        *history,
        {"role": "user", "content": message},
    ]

    completion = client.chat.completions.create(
        model="gpt-4-0125-preview", messages=messages, tools=tools, tool_choice="auto"
    )

    return completion.choices[0].message.tool_calls[0].function


def on_error(ws, error):
    print("### error:", error)


def on_close(ws, a, b):
    print("### closed ###")
    ws.run_forever(sslopt={"cert_reqs": ssl.CERT_NONE})


if __name__ == "__main__":
    main()
