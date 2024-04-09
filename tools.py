from openai import OpenAI
from key import OPENAI_API_KEY

client = OpenAI(api_key=OPENAI_API_KEY)

def tool_choice(prompt, message, tools, history):
    """
    Send the message to the model with a list of tools and propmt the model to use the tools.
    Tools is a list of dict describing functions.
    Return the chosen function.
    """
    messages = [
        {"role": "system", "content": prompt},
        *history,
        {"role": "user", "content": message},
    ]

    completion = client.chat.completions.create(
        model="gpt-3.5-turbo", messages=messages, tools=tools, tool_choice="auto"
    )

    return completion.choices[0].message.tool_calls[0].function

tools = [
    {
        "type": "function",
        "function": {
            "name": "m",
            "descriptioin":
            """
            Moving the joints of the robot to a specific angle.
            Your available joint servos are:
            0: head,
            8: Left Front Arm, 9: Right Front Arm, 10: Right Back Arm, 11: Left Back Arm,
            12: Left Front Knee, 13: Right Front Knee, 14: Right Back Knee, 15: Left Back Knee,
            E.g.:
            ['m', [0, -20]]
            0 indicates the index number of joint servo
            20 indicates the rotation angle (this angle refers to the origin rather than additive).
            The unit is in degrees.

            ['m',  [0, 45, 0, -45, 0, 45, 0, -45]]
            and these joint servo rotation commands are executed SEQUENTIALLY, not at the same time.
            The meaning of this example is:
            the joint servo with index number 0 is first rotated to the 45-degree position,
            then rotated to the -45 degree position, and so on. After these motion commands are completed,
            """,
            "parameters": {
                "type": "object",
                "properties": {
                    "data": {
                        "type": "string",
                        "description": "The index number and rotation angle of the joint servo",
                    }
                }
            }
        }
    },
    {
        "type": "function",
        "function": {
            "name": "i",
            "description":
            """
            Issue multiple commands at one time.
            Your available joint servos are:
            0: head,
            8: Left Front Arm, 9: Right Front Arm, 10: Right Back Arm, 11: Left Back Arm,
            12: Left Front Knee, 13: Right Front Knee, 14: Right Back Knee, 15: Left Back Knee,
            E.g.:
            ['i', [ 8, -15, 9, -20]]
            The meaning of this example is:
            the joint servos with index numbers 8, 9 are rotated to the -15, -20 degree positions at the same time.
            After these motion commands are completed,
            """,
            "parameters": {
                "type": "object",
                "properties": {
                    "data": {
                        "type": "string",
                        "description": "The index number and rotation angle of the joint servo",
                    }
                }
            }
        }
    },
    {
        "type": "function",
        "function": {
            "name": "b",
            "description":
            """
            Buzzer control.
            E.g.:
            ['b', [10,2]]
            10 indicates the music tone
            2 indicates the lengths of duration, corresponding to 1/duration second

            ['b',[0, 1, 14, 8, 14, 8, 21, 8, 21, 8, 23, 8, 23, 8, 21, 4, 19, 8, 19, 8, 18, 8, 18, 8, 16, 8, 16, 8, 14, 4]]
            0, 14, 14, 21... indicate the music tones
            1, 8, 8, 8 indicates the lengths of duration, corresponding to 1/duration second
            """,
            "parameters": {
                "type": "object",
                "properties": {
                    "data": {
                        "type": "string",
                        "description": "The music tone and the lengths of duration",
                    }
                }
            }
        }
    },
    {
        "type": "function",
        "function": {
            "name": "balance",
            "description": "Balance on one leg",
        }
    },
    {
        "type": "function",
        "function": {
            "name": "buttUp",
            "description": "Butt up",
        }
    },
    # {
    #     "type": "function",
    #     "function": {
    #         "name": "calib",
    #         "description": "Calibrate the gyroscope",
    #     }
    # },
    {
        "type": "function",
        "function": {
            "name": "dropped",
            "description": "Dropped",
        }
    },
    {
        "type": "function",
        "function": {
            "name": "lifted",
            "description": "Lifted",
        }
    },
    {
        "type": "function",
        "function": {
            "name": "lnd",
            "description": "Landing",
        }
    },
    {
        "type": "function",
        "function": {
            "name": "rest",
            "description": "Rest",
        }
    },
    {
        "type": "function",
        "function": {
            "name": "sit",
            "description": "Sit",
        }
    },
    {
        "type": "function",
        "function": {
            "name": "str",
            "description": "Stretch",
        }
    },
    {
        "type": "function",
        "function": {
            "name": "up",
            "description": "Up",
        }
    },
    {
        "type": "function",
        "function": {
            "name": "zero",
            "description": "Zero",
        }
    },
    {
        "type": "function",
        "function": {
            "name": "ang",
            "description": "Angry",
        }
    },
    {
        "type": "function",
        "function": {
            "name": "bf",
            "description": "Back flip",
        }
    },
    {
        "type": "function",
        "function": {
            "name": "bx",
            "description": "Boxing",
        }
    },
    {
        "type": "function",
        "function": {
            "name": "ck",
            "description": "Check",
        }
    },
    {
        "type": "function",
        "function": {
            "name": "cmh",
            "description": "Come here",
        }
    },
    {
        "type": "function",
        "function": {
            "name": "dg",
            "description": "Dig",
        }
    },
    {
        "type": "function",
        "function": {
            "name": "ff",
            "description": "Front flip",
        }
    },
    {
        "type": "function",
        "function": {
            "name": "fiv",
            "description": "High five",
        }
    },
    {
        "type": "function",
        "function": {
            "name": "gdb",
            "description": "Good boy",
        }
    },
    {
        "type": "function",
        "function": {
            "name": "hds",
            "description": "Hand stand",
        }
    },
    {
        "type": "function",
        "function": {
            "name": "hi",
            "description": "Hi",
        }
    },
    {
        "type": "function",
        "function": {
            "name": "hg",
            "description": "Hug",
        }
    },
    {
        "type": "function",
        "function": {
            "name": "hsk",
            "description": "Hand shake",
        }
    },
    {
        "type": "function",
        "function": {
            "name": "hu",
            "description": "Hands up",
        }
    },
    {
        "type": "function",
        "function": {
            "name": "jmp",
            "description": "Jump",
        }
    },
    {
        "type": "function",
        "function": {
            "name": "chr",
            "description": "Cheers",
        }
    },
    {
        "type": "function",
        "function": {
            "name": "kc",
            "description": "Kick",
        }
    },
    {
        "type": "function",
        "function": {
            "name": "mw",
            "description": "Moon walk",
        }
    },
    {
        "type": "function",
        "function": {
            "name": "nd",
            "description": "Nod",
        }
    },
    {
        "type": "function",
        "function": {
            "name": "pd",
            "description": "Play dead",
        }
    },
    {
        "type": "function",
        "function": {
            "name": "pee",
            "description": "Pee",
        }
    },
    {
        "type": "function",
        "function": {
            "name": "pu",
            "description": "Push up",
        }
    },
    {
        "type": "function",
        "function": {
            "name": "pu1",
            "description": "Push up single arm",
        }
    },
    {
        "type": "function",
        "function": {
            "name": "rc",
            "description": "Recover",
        }
    },
    {
        "type": "function",
        "function": {
            "name": "rl",
            "description": "Roll",
        }
    },
    {
        "type": "function",
        "function": {
            "name": "scrh",
            "description": "Scratch",
        }
    },
    {
        "type": "function",
        "function": {
            "name": "snf",
            "description": "Sniff",
        }
    },
    {
        "type": "function",
        "function": {
            "name": "tbl",
            "description": "Table",
        }
    },
    # {
    #     "type": "function",
    #     "function": {
    #         "name": "ts",
    #         "description": "Test servo",
    #     }
    # },
    {
        "type": "function",
        "function": {
            "name": "wh",
            "description": "Shake your head. This function can effectively express disagreement.",
        }
    },
    {
        "type": "function",
        "function": {
            "name": "zz",
            "description": "Zz",
        }
    },
  # {
  #   "type": "function",
  #   "function": {
  #     "name": "get_current_weather",
  #     "description": "Get the current weather in a given location",
  #     "parameters": {
  #       "type": "object",
  #       "properties": {
  #         "location": {
  #           "type": "string",
  #           "description": "The city and state, e.g. San Francisco, CA",
  #         },
  #         "unit": {"type": "string", "enum": ["celsius", "fahrenheit"]},
  #       },
  #       "required": ["location"],
  #     },
  #   }
  # }
]

skillFullName = {
        'balance': 'balance',
        'buttUp': 'buttUp',
        'dropped': 'dropped',
        'lifted': 'lifted',
        'lnd': 'landing',
        'rest': 'rest',
        'sit': 'sit',
        'up': 'up',
        'str': 'stretch',
        'calib': 'calib',
        'zero': 'zero',
        'ang':'angry',
         'bf': 'backFlip',
         'bx': 'boxing',
         'ck': 'check',
         'cmh': 'comeHere',
         'dg': 'dig',
         'ff': 'frontFlip',
         'fiv': 'highFive',
         'gdb': 'goodboy',
         'hds': 'handStand',
         'hi': 'hi',
         'hg': 'hug',
         'hsk': 'handShake',
         'hu': 'handsUp',
         'jmp': 'jump',
         'chr': 'cheers',
         'kc': 'kick',
         'mw': 'moonWalk',
         'nd': 'nod',
         'pd': 'playDead',
         'pee': 'pee',
         'pu': 'pushUp',
         'pu1': 'pushUpSingleArm',
         'rc': 'recover',
         'rl': 'roll',
         'scrh': 'scratch',
         'snf': 'sniff',
         'tbl': 'table',
         'ts': 'testServo',
         'wh': 'waveHead',
         'zz': 'zz',
         }