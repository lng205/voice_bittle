# Voice Bittle

This projects intends to create a demo of a voice assistant for Bittle. The voice assistant will be able to understand voice commands and execute them on the robot.

## Roadmap

1. [x] Control the robot via serial communication
2. [x] Using LLM to understand natural language commands
3. [x] Voice recognition

4. [ ] TODO: handle the multithreading conflict. There are four tasks running in parallel: audio recoding, streaming voice recognition, LLM and serial communication. The current implementation is not stable.

## How to use

1. Run `pip install -r requirements.txt`
2. Add your xunfei APPID, APISERCET, XF_APIKEY and OPENAI_API_KEY to `key.py`
3. Connect the robot to your computer
4. Run `python dog.py`

## File Structure

- `dog.py`: main file; modified from `ref/dog.py`
- `key.py`: store the API keys
- `sst.py`: speech to text; modified from `ref/iat_ws_python3.py`
- `tools.py`: functions sending commands to the robot, used for tool calls
- `send_command/`: a folder containing the files used to set up the serial communication with the robot and send commands to it; copied from OpenCat

## Ref

- [OpenCat](https://github.com/PetoiCamp/OpenCat/tree/main/serialMaster)
- [xunfei](https://www.xfyun.cn/doc/asr/voicedictation/API.html#%E6%8E%A5%E5%8F%A3%E8%AF%B4%E6%98%8E)
