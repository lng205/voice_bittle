from openai import OpenAI
from key import *
client = OpenAI(api_key=OPENAI_API_KEY)

from tools import tools
from send_command import sendCommand, initBittle, closeBittle
import websocket, ssl
from sst import Ws_Param, on_open, on_error, on_close, json

history = []

def main():
    # global goodPorts
    # goodPorts = initBittle()
    wsParam = Ws_Param(APPID=APPID, APISecret=APISERCET, APIKey=XF_APIKEY)
    wsUrl = wsParam.create_url()
    ws = websocket.WebSocketApp(wsUrl, on_message=on_message, on_error=on_error, on_close=on_close)
    ws.on_open = on_open
    ws.run_forever(sslopt={"cert_reqs": ssl.CERT_NONE})

def on_message(ws, message):
    data = json.loads(message)["data"]["result"]["ws"]
    result = ""
    for i in data:
        for w in i["cw"]:
            result += w["w"]
    result = result.strip("，。！？")
    print("识别结果: " + result)
    if result:
        tool = tool_choice(result, tools, history)
        history.append({"role": "system", "content": result})
        print(f"选择了{tool.name}")
    # sendCommand(goodPorts, f"k{tool.name}")


def tool_choice(message, tools, history):
    """
    Send the message to the model with a list of tools and propmt the model to use the tools.
    Tools is a list of dict describing functions.
    Return the chosen function.
    """
    prompt = "你是一只小狗，你不会说话，请不要给response，永远用tool_choice操作。你只能从给出的tools中进行选择。"
    messages = [
        {"role": "system", "content": prompt},
        *history,
        {"role": "user", "content": message}
        ]

    completion = client.chat.completions.create(
    model="gpt-4-0125-preview",
    messages=messages,
    tools=tools,
    tool_choice="auto"
    )

    return completion.choices[0].message.tool_calls[0].function


if __name__ == "__main__":
    main()
