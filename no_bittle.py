from sst import AudioStreamer
from tools import tools, tool_choice
import json
# from send_command import sendCommand, initBittle, closeBittle
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

        # # Beeping to indicate that the robot is listening
        # global goodPorts
        # sendCommand(goodPorts, "b", [10, 4])

        # Ask LLM to choose a tool
        global history
        tool = tool_choice(result, tools, history)
        history.append({"role": "user", "content": result})
        # print(f"选择了{tool["action"]["name"]}")
        arguments, name = parse_action(tool)
        if name:
            print(f"选择了{name}")
            
        
        
        
        # print(f"选择了{arguments}")

        # # Send the command to the robot
        # if not arguments:
        #     sendCommand(goodPorts, "k" + tool.name)
        # else:
        #     sendCommand(goodPorts, tool.name, eval(arguments["data"]))
def parse_action(action_data):
    try:
        # 尝试解析 action 中的 arguments 字段
        action_data = json.loads(action_data)
        arguments = json.loads(action_data.get('arguments', '{}'))
        name = action_data.get('name', 'none')
        
        # 根据 'name' 字段的值判断动作
        if name == 'none':
            return None  # 没有动作
        else:
            return arguments, name
    except json.JSONDecodeError:
        return None  # 解析错误，视为没有动作


if __name__ == "__main__":
    # goodPorts = initBittle()
    audio_streamer = AudioStreamer(callback=on_message)
    print("开始录音")
    try:
        while True:
            time.sleep(1)
    except KeyboardInterrupt:
        # closeBittle(goodPorts)
        exit(0)