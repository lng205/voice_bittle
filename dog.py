from sst import AudioStreamer
from tools import tools, tool_choice
import json
from send_command import sendCommand, initBittle, closeBittle
import time

prompt = "你是一只机器小狗，你不会说话，请不要给response，永远用tool_choice操作。你只能从给出的tools中进行选择。"
history = []
goodPorts = None

def on_message(message):
    result = ""
    if message:
        for i in message["ws"]:
            for w in i["cw"]:
                result += w["w"]
        result = result.strip("，。！？")

    if result:
        print("识别结果: " + result)

        # Beeping to indicate that the robot is listening
        global goodPorts
        sendCommand(goodPorts, "b", [10, 4])

        # Ask LLM to choose a tool
        global history
        tool = tool_choice(prompt, result, tools, history)
        history.append({"role": "user", "content": result})
        arguments = json.loads(tool.arguments)
        print(f"选择了{tool}")

        # Send the command to the robot
        if not arguments:
            sendCommand(goodPorts, "k" + tool.name)
        else:
            sendCommand(goodPorts, tool.name, eval(arguments["data"]))


if __name__ == "__main__":
    goodPorts = initBittle()
    audio_streamer = AudioStreamer(callback=on_message)
    print("开始录音")
    try:
        while True:
            time.sleep(1)
    except KeyboardInterrupt:
        audio_streamer.close()
        closeBittle(goodPorts)
        print("结束程序")