from openai import OpenAI
client = OpenAI(api_key="APIKEY")

from tools import tools
from send_command import sendCommand, initBittle, closeBittle

def main():
    goodPorts = initBittle()
    while True:
        # Keep running except KeyboardInterrupt
        try:
            message = input("你想对小狗说什么？")
            tool = tool_choice(message, tools)
            print(tool)
            sendCommand(goodPorts, f"k{tool.name}")
        except KeyboardInterrupt:
            closeBittle(goodPorts)
            break
    closeBittle(goodPorts)

def tool_choice(message, tools):
    """
    Send the message to the model with a list of tools and propmt the model to use the tools.
    Tools is a list of dict describing functions.
    Return the chosen function.
    """
    prompt = "你是一只小狗，你不会说话，请不要给response，永远用tool_choice操作。你只能从给出的tools中进行选择。"
    messages = [
        {"role": "system", "content": prompt},
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
