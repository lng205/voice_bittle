from sst import AudioStreamer
from tools import tools, tool_choice
import json
from send_command import sendCommand, initBittle, closeBittle
import time

prompt = "你是一只机器小狗，你不会说话，请不要给response，永远用tool_choice操作。你只能从给出的tools中进行选择。"
history = []
goodPorts = None

# Set to True if you are using a real device
DEVICE = False
TIMETEST = True

def on_message(message):
    timestamp = time.time()
    result = ""
    if message:
        for i in message["ws"]:
            for w in i["cw"]:
                result += w["w"]
        result = result.strip("，。！？")

    if result:
        print("识别结果: " + result)

        # Ask LLM to choose a tool
        global history
        tool = tool_choice(prompt, result, tools, history)
        history.append({"role": "user", "content": result})
        arguments = json.loads(tool.arguments)
        print(f"选择了{tool}")
        if TIMETEST:
            print("LLM返回耗时: ", time.time() - timestamp, "s")

        if DEVICE:
            # Send the command to the robot
            if not arguments:
                sendCommand(goodPorts, "k" + tool.name)
            else:
                sendCommand(goodPorts, tool.name, eval(arguments["data"]))


if __name__ == "__main__":
    if DEVICE:
        goodPorts = initBittle()
    audio_streamer = AudioStreamer(callback=on_message)
    print("开始录音")
    try:
        while True:
            time.sleep(1)
    except KeyboardInterrupt:
        audio_streamer.close()
        if DEVICE:
            closeBittle(goodPorts)
        print("结束程序")