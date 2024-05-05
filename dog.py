from sst import AudioStreamer
from tools import tools, tool_choice
import json
from send_command import sendCommand, initBittle, closeBittle
import time




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
        result = result.strip(",銆傦紒锛�")

    if result:
        print("璇嗗埆缁撴灉: " + result)

        # Ask LLM to choose a tool
        global history
        tool = tool_choice(result, tools, history)
        history.append({"role": "user", "content": result})
        arguments = json.loads(tool.arguments)
        print(f"閫夋嫨浜唟{tool}")
        if TIMETEST:
            print("LLM杩斿洖鑰楁椂: ", time.time() - timestamp, "s")

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
    print("寮€濮嬪綍闊�")
    try:
        while True:
            time.sleep(1)
    except KeyboardInterrupt:
        audio_streamer.close()
        if DEVICE:
            closeBittle(goodPorts)
        print("缁撴潫绋嬪簭")