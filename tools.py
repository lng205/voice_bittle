from openai import OpenAI
import zhipuai
from zhipuai import ZhipuAI
from key import OPENAI_API_KEY
from key import ZHIPU_API_KEY 
  


# client = OpenAI(api_key=OPENAI_API_KEY)
client = ZhipuAI(api_key=ZHIPU_API_KEY)

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
        # model="gpt-4-0125-preview", messages=messages, tools=tools, tool_choice="auto"
        
        model="glm-4", messages=messages, tools=tools, tool_choice="auto"
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
            "parameters": {
                "type": "object",
                "properties": {
                    "leg": {
                        "type": "string",
                        "enum": ["left", "right"],
                        "description": "The leg on which the robot should balance."
                    },
                    "duration": {
                        "type": "number",
                        "description": "The duration in seconds for the robot to maintain balance."
                    }
                },
                "required": ["leg", "duration"]
            }
        }
    },
    {
        "type": "function",
        "function": {
            "name": "buttUp",
            "description": "Butt up",
            "parameters": {
                "type": "object",
                "properties": {
                    "height": {
                        "type": "number",
                        "description": "The height to which the robot should raise its buttocks."
                    },
                    "duration": {
                        "type": "number",
                        "description": "The duration in seconds for the butt up position to be maintained."
                    }
                },
                "required": ["height", "duration"]
            }
        }
    },
    {
        "type": "function",
        "function": {
            "name": "dropped",
            "description": "Dropped",
            "parameters": {
                "type": "object",
                "properties": {
                    "item": {
                        "type": "string",
                        "description": "The item that the robot should drop."
                    },
                    "location": {
                        "type": "string",
                        "description": "The target location where the item should be dropped."
                    }
                },
                "required": ["item", "location"]
            }
        }
    },
    {
        "type": "function",
        "function": {
            "name": "lifted",
            "description": "Lifted",
            "parameters": {
                "type": "object",
                "properties": {
                    "object": {
                        "type": "string",
                        "description": "The object that the robot should lift."
                    },
                    "height": {
                        "type": "number",
                        "description": "The height to which the object should be lifted."
                    }
                },
                "required": ["object", "height"]
            }
        }
    },
    {
        "type": "function",
        "function": {
            "name": "lnd",
            "description": "Landing",
            "parameters": {
                "type": "object",
                "properties": {
                    "location": {
                        "type": "string",
                        "description": "The location where the robot should land."
                    },
                    "orientation": {
                        "type": "string",
                        "enum": ["front", "back", "left", "right"],
                        "description": "The desired orientation of the robot upon landing."
                    }
                },
                "required": ["location", "orientation"]
            }
        }
    },
    {
        "type": "function",
        "function": {
            "name": "rest",
            "description": "Rest",
            "parameters": {
                "type": "object",
                "properties": {
                    "position": {
                        "type": "string",
                        "enum": ["sitting", "lying", "standing"],
                        "description": "The resting position of the robot."
                    },
                    "duration": {
                        "type": "number",
                        "description": "The duration in seconds for the robot to rest in the specified position."
                    }
                },
                "required": ["position", "duration"]
            }
        }
    },
    {
        "type": "function",
        "function": {
            "name": "sit",
            "description": "Sit",
            "parameters": {
                "type": "object",
                "properties": {
                    "duration": {
                        "type": "number",
                        "description": "The duration in seconds for the robot to maintain the sitting position."
                    }
                },
                "required": ["duration"]
       }
        }
    },
    {
        "type": "function",
        "function": {
            "name": "str",
            "description": "Stretch",
            "parameters": {
                "type": "object",
                "properties": {
                    "bodyPart": {
                        "type": "string",
                        "enum": ["arms", "legs", "back", "neck"],
                        "description": "The body part to stretch."
                    },
                    "duration": {
                        "type": "number",
                        "description": "The duration in seconds for the stretch."
                    }
                },
                "required": ["bodyPart", "duration"]
            }
        }
    },
    {
        "type": "function",
        "function": {
            "name": "up",
            "description": "Up",
            "parameters": {
                "type": "object",
                "properties": {
                    "direction": {
                        "type": "string",
                        "enum": ["up", "down"],
                        "description": "The direction in which the robot should move."
                    },
                    "duration": {
                        "type": "number",
                        "description": "The duration in seconds for the movement."
                    }
                },
                "required": ["direction", "duration"]
            }
        }
    },
    {
        "type": "function",
        "function": {
            "name": "zero",
            "description": "Zero",
            "parameters": {
                "type": "object",
                "properties": {
                    "servo": {
                        "type": "string",
                        "description": "The servo that should be reset to zero."
                    }
                },
                "required": ["servo"]
            }
        }
    },
    {
        "type": "function",
        "function": {
            "name": "ang",
            "description": "Angry",
            "parameters": {
                "type": "object",
                "properties": {
                    "duration": {
                        "type": "number",
                        "description": "The duration in seconds for the angry expression."
                    }
                },
                "required": ["duration"]
            }
        }
    },
    {
        "type": "function",
        "function": {
            "name": "bf",
            "description": "Back flip",
            "parameters": {
                "type": "object",
                "properties": {
                    "direction": {
                        "type": "string",
                        "enum": ["left", "right"],
                        "description": "The direction of the back flip."
                    },
                    "duration": {
                        "type": "number",
                        "description": "The duration in seconds for the back flip."
                    }
                },
                "required": ["direction", "duration"]
            }
        }
    },
{
    "type": "function",
    "function": {
        "name": "bf",
        "description": "Back flip",
        "parameters": {
            "type": "object",
            "properties": {
                "difficulty": {
                    "type": "string",
                    "description": "The level of difficulty for the back flip (easy, medium, hard)."
                },
                "surface": {
                    "type": "string",
                    "description": "The type of surface on which the back flip will be performed (grass, mat, hardwood)."
                }
            },
            "required": ["difficulty", "surface"]
        }
    }
},
{
    "type": "function",
    "function": {
        "name": "bx",
        "description": "Boxing",
        "parameters": {
            "type": "object",
            "properties": {
                "opponent": {
                    "type": "string",
                    "description": "The name or identifier of the opponent for the boxing match."
                },
                "rounds": {
                    "type": "integer",
                    "description": "The number of rounds in the boxing match."
                }
            },
            "required": ["opponent", "rounds"]
        }
    }
},
{
    "type": "function",
    "function": {
        "name": "ck",
        "description": "Check",
        "parameters": {
            "type": "object",
            "properties": {
                "item": {
                    "type": "string",
                    "description": "The item to check (e.g., health, inventory, status)."
                },
                "criteria": {
                    "type": "string",
                    "description": "The criteria for the check (e.g., quantity, condition, level)."
                }
            },
            "required": ["item", "criteria"]
        }
    }
},
{
    "type": "function",
    "function": {
        "name": "cmh",
        "description": "Come here",
        "parameters": {
            "type": "object",
            "properties": {
                "target": {
                    "type": "string",
                    "description": "The target to approach (e.g., person, object, location)."
                },
                "speed": {
                    "type": "string",
                    "description": "The speed at which to approach the target (e.g., walk, jog, run)."
                }
            },
            "required": ["target", "speed"]
        }
    }
},
{
    "type": "function",
    "function": {
        "name": "dg",
        "description": "Dig",
        "parameters": {
            "type": "object",
            "properties": {
                "location": {
                    "type": "string",
                    "description": "The location where digging will occur."
                },
                "depth": {
                    "type": "integer",
                    "description": "The desired depth of the digging."
                }
            },
            "required": ["location", "depth"]
        }
    }
},

    {
    "type": "function",
    "function": {
        "name": "ff",
        "description": "Front flip",
        "parameters": {
            "type": "object",
            "properties": {
                "direction": {
                    "type": "string",
                    "description": "The direction of the flip (forward, backward, sideways)."
                },
                "surface": {
                    "type": "string",
                    "description": "The type of surface on which the flip will be performed (mat, carpet, concrete)."
                }
            },
            "required": ["direction", "surface"]
        }
    }
},
{
    "type": "function",
    "function": {
        "name": "fiv",
        "description": "High five",
        "parameters": {
            "type": "object",
            "properties": {
                "target": {
                    "type": "string",
                    "description": "The person or entity to give a high five to."
                },
                "height": {
                    "type": "integer",
                    "description": "The height at which to give the high five (in centimeters)."
                }
            },
            "required": ["target", "height"]
        }
    }
},
{
    "type": "function",
    "function": {
        "name": "gdb",
        "description": "Good boy",
        "parameters": {
            "type": "object",
            "properties": {
                "pet": {
                    "type": "string",
                    "description": "The name or identifier of the pet to praise."
                },
                "action": {
                    "type": "string",
                    "description": "The specific action or behavior being praised."
                }
            },
            "required": ["pet", "action"]
        }
    }
},
{
    "type": "function",
    "function": {
        "name": "hds",
        "description": "Hand stand",
        "parameters": {
            "type": "object",
            "properties": {
                "duration": {
                    "type": "integer",
                    "description": "The duration in seconds for which the handstand should be held."
                },
                "surface": {
                    "type": "string",
                    "description": "The type of surface on which the handstand will be performed (grass, mat, concrete)."
                }
            },
            "required": ["duration", "surface"]
        }
    }
},
{
    "type": "function",
    "function": {
        "name": "hi",
        "description": "Hi",
        "parameters": {
            "type": "object",
            "properties": {
                "greeting_type": {
                    "type": "string",
                    "description": "The type of greeting (friendly, formal, casual)."
                },
                "recipient": {
                    "type": "string",
                    "description": "The person or entity to whom the greeting is directed."
                }
            },
            "required": ["greeting_type", "recipient"]
        }
    }
},
{
    "type": "function",
    "function": {
        "name": "hg",
        "description": "Hug",
        "parameters": {
            "type": "object",
            "properties": {
                "target": {
                    "type": "string",
                    "description": "The person or entity to hug."
                },
                "duration": {
                    "type": "integer",
                    "description": "The duration of the hug in seconds."
                }
            },
            "required": ["target", "duration"]
        }
    }
},
{
    "type": "function",
    "function": {
        "name": "hsk",
        "description": "Hand shake",
        "parameters": {
            "type": "object",
            "properties": {
                "duration": {
                    "type": "number",
                    "description": "持续时间（秒）"
                },
                "strength": {
                    "type": "number",
                    "description": "握手力度（1-10）"
                }
            },
            "required": ["duration", "strength"]
        }
    }
},
{
    "type": "function",
    "function": {
        "name": "hu",
        "description": "Hands up",
        "parameters": {
            "type": "object",
            "properties": {
                "duration": {
                    "type": "number",
                    "description": "举手持续时间（秒）"
                },
                "height": {
                    "type": "number",
                    "description": "举手高度（厘米）"
                }
            },
            "required": ["duration", "height"]
        }
    }
},
{
    "type": "function",
    "function": {
        "name": "jmp",
        "description": "Jump",
        "parameters": {
            "type": "object",
            "properties": {
                "height": {
                    "type": "number",
                    "description": "跳跃高度（厘米）"
                },
                "count": {
                    "type": "number",
                    "description": "跳跃次数"
                }
            },
            "required": ["height", "count"]
        }
    }
},
{
    "type": "function",
    "function": {
        "name": "chr",
        "description": "Cheers",
        "parameters": {
            "type": "object",
            "properties": {
                "volume": {
                    "type": "number",
                    "description": "欢呼音量（1-10）"
                },
                "duration": {
                    "type": "number",
                    "description": "欢呼持续时间（秒）"
                }
            },
            "required": ["volume", "duration"]
        }
    }
},
{
    "type": "function",
    "function": {
        "name": "kc",
        "description": "Kick",
        "parameters": {
            "type": "object",
            "properties": {
                "force": {
                    "type": "number",
                    "description": "踢击力度（1-10）"
                },
                "target": {
                    "type": "string",
                    "description": "踢击目标"
                }
            },
            "required": ["force", "target"]
        }
    }
},
{
    "type": "function",
    "function": {
        "name": "mw",
        "description": "Moon walk",
        "parameters": {
            "type": "object",
            "properties": {
                "speed": {
                    "type": "number",
                    "description": "月球漫步速度（厘米/秒）"
                },
                "distance": {
                    "type": "number",
                    "description": "月球漫步距离（厘米）"
                }
            },
            "required": ["speed", "distance"]
        }
    }
},
{
    "type": "function",
    "function": {
        "name": "nd",
        "description": "Nod",
        "parameters": {
            "type": "object",
            "properties": {
                "duration": {
                    "type": "number",
                    "description": "点头持续时间（秒）"
                },
                "repeats": {
                    "type": "number",
                    "description": "点头次数"
                }
            },
            "required": ["duration", "repeats"]
        }
    }
},
{
    "type": "function",
    "function": {
        "name": "pd",
        "description": "Play dead",
        "parameters": {
            "type": "object",
            "properties": {
                "duration": {
                    "type": "number",
                    "description": "装死持续时间（秒）"
                },
                "stage": {
                    "type": "string",
                    "description": "装死场景"
                }
            },
            "required": ["duration", "stage"]
        }
    }
},
{
    "type": "function",
    "function": {
        "name": "pee",
        "description": "Pee",
        "parameters": {
            "type": "object",
            "properties": {
                "volume": {
                    "type": "number",
                    "description": "尿量（毫升）"
                },
                "location": {
                    "type": "string",
                    "description": "尿尿地点"
                }
            },
            "required": ["volume", "location"]
        }
    }
},
{
    "type": "function",
    "function": {
        "name": "pu",
        "description": "Push up",
        "parameters": {
            "type": "object",
            "properties": {
                "count": {
                    "type": "number",
                    "description": "俯卧撑次数"
                },
                "pace": {
                    "type": "string",
                    "description": "俯卧撑节奏（快/慢）"
                }
            },
            "required": ["count", "pace"]
        }
    }
},
{
    "type": "function",
    "function": {
        "name": "pu1",
        "description": "Push up single arm",
        "parameters": {
            "type": "object",
            "properties": {
                "count": {
                    "type": "number",
                    "description": "单手俯卧撑次数"
                },
                "arm": {
                    "type": "string",
                    "description": "使用的手臂（左/右）"
                }
            },
            "required": ["count", "arm"]
        }
    }
},
{
    "type": "function",
    "function": {
        "name": "rc",
        "description": "Recover",
        "parameters": {
            "type": "object",
            "properties": {
                "time": {
                    "type": "number",
                    "description": "恢复时间（秒）"
                },
                "method": {
                    "type": "string",
                    "description": "恢复方法（休息/深呼吸）"
                }
            },
            "required": ["time", "method"]
        }
    }
},
{
    "type": "function",
    "function": {
        "name": "rl",
        "description": "Roll",
        "parameters": {
            "type": "object",
            "properties": {
                "direction": {
                    "type": "string",
                    "description": "滚动方向（左/右）"
                },
                "distance": {
                    "type": "number",
                    "description": "滚动距离（厘米）"
                }
            },
            "required": ["direction", "distance"]
        }
    }
},
{
    "type": "function",
    "function": {
        "name": "scrh",
        "description": "Scratch",
        "parameters": {
            "type": "object",
            "properties": {
                "location": {
                    "type": "string",
                    "description": "抓挠部位"
                },
                "intensity": {
                    "type": "number",
                    "description": "抓挠强度（1-10）"
                }
            },
            "required": ["location", "intensity"]
        }
    }
},
{
    "type": "function",
    "function": {
        "name": "snf",
        "description": "Sniff",
        "parameters": {
            "type": "object",
            "properties": {
                "object": {
                    "type": "string",
                    "description": "嗅探对象"
                },
                "duration": {
                    "type": "number",
                    "description": "嗅探持续时间（秒）"
                }
            },
            "required": ["object", "duration"]
        }
    }
},
{
    "type": "function",
    "function": {
        "name": "tbl",
        "description": "Table",
        "parameters": {
            "type": "object",
            "properties": {
                "height": {
                    "type": "number",
                    "description": "桌面高度（厘米）"
                },
                "width": {
                    "type": "number",
                    "description": "桌面宽度（厘米）"
                },
                "material": {
                    "type": "string",
                    "description": "桌面材质（木质/金属/玻璃）"
                }
            },
            "required": ["height", "width", "material"]
        }
    }
},
{
    "type": "function",
    "function": {
        "name": "wh",
        "description": "Shake your head. This function can effectively express disagreement.",
        "parameters": {
            "type": "object",
            "properties": {
                "duration": {
                    "type": "number",
                    "description": "摇头持续时间（秒）"
                },
                "intensity": {
                    "type": "number",
                    "description": "摇头力度（1-10）"
                }
            },
            "required": ["duration", "intensity"]
        }
    }
},
{
    "type": "function",
    "function": {
        "name": "zz",
        "description": "Zz",
        "parameters": {
            "type": "object",
            "properties": {
                "duration": {
                    "type": "number",
                    "description": "睡眠时间（分钟）"
                },
                "comfort": {
                    "type": "number",
                    "description": "舒适度（1-10）"
                }
            },
            "required": ["duration", "comfort"]
        }
    }
}
#     {
#         "type": "function",
#         "function": {
#             "name": "balance",
#             "description": "Balance on one leg",
#         }
#     },
#     {
#         "type": "function",
#         "function": {
#             "name": "buttUp",
#             "description": "Butt up",
#         }
#     },
#     # {
#     #     "type": "function",
#     #     "function": {
#     #         "name": "calib",
#     #         "description": "Calibrate the gyroscope",
#     #     }
#     # },
#     {
#         "type": "function",
#         "function": {
#             "name": "dropped",
#             "description": "Dropped",
#         }
#     },
#     {
#         "type": "function",
#         "function": {
#             "name": "lifted",
#             "description": "Lifted",
#         }
#     },
#     {
#         "type": "function",
#         "function": {
#             "name": "lnd",
#             "description": "Landing",
#         }
#     },
#     {
#         "type": "function",
#         "function": {
#             "name": "rest",
#             "description": "Rest",
#         }
#     },
#     {
#         "type": "function",
#         "function": {
#             "name": "sit",
#             "description": "Sit",
#         }
#     },
#     {
#         "type": "function",
#         "function": {
#             "name": "str",
#             "description": "Stretch",
#         }
#     },
#     {
#         "type": "function",
#         "function": {
#             "name": "up",
#             "description": "Up",
#         }
#     },
#     {
#         "type": "function",
#         "function": {
#             "name": "zero",
#             "description": "Zero",
#         }
#     },
#     {
#         "type": "function",
#         "function": {
#             "name": "ang",
#             "description": "Angry",
#         }
#     },
#     {
#         "type": "function",
#         "function": {
#             "name": "bf",
#             "description": "Back flip",
#         }
#     },
#     {
#         "type": "function",
#         "function": {
#             "name": "bx",
#             "description": "Boxing",
#         }
#     },
#     {
#         "type": "function",
#         "function": {
#             "name": "ck",
#             "description": "Check",
#         }
#     },
#     {
#         "type": "function",
#         "function": {
#             "name": "cmh",
#             "description": "Come here",
#         }
#     },
#     {
#         "type": "function",
#         "function": {
#             "name": "dg",
#             "description": "Dig",
#         }
#     },
#     {
#         "type": "function",
#         "function": {
#             "name": "ff",
#             "description": "Front flip",
#         }
#     },
#     {
#         "type": "function",
#         "function": {
#             "name": "fiv",
#             "description": "High five",
#         }
#     },
#     {
#         "type": "function",
#         "function": {
#             "name": "gdb",
#             "description": "Good boy",
#         }
#     },
#     {
#         "type": "function",
#         "function": {
#             "name": "hds",
#             "description": "Hand stand",
#         }
#     },
#     {
#         "type": "function",
#         "function": {
#             "name": "hi",
#             "description": "Hi",
#         }
#     },
#     {
#         "type": "function",
#         "function": {
#             "name": "hg",
#             "description": "Hug",
#         }
#     },
#     {
#         "type": "function",
#         "function": {
#             "name": "hsk",
#             "description": "Hand shake",
#         }
#     },
#     {
#         "type": "function",
#         "function": {
#             "name": "hu",
#             "description": "Hands up",
#         }
#     },
#     {
#         "type": "function",
#         "function": {
#             "name": "jmp",
#             "description": "Jump",
#         }
#     },
#     {
#         "type": "function",
#         "function": {
#             "name": "chr",
#             "description": "Cheers",
#         }
#     },
#     {
#         "type": "function",
#         "function": {
#             "name": "kc",
#             "description": "Kick",
#         }
#     },
    
#     {
#         "type": "function",
#         "function": {
#             "name": "mw",
#             "description": "Moon walk",
#         }
#     },
#     {
#         "type": "function",
#         "function": {
#             "name": "nd",
#             "description": "Nod",
#         }
#     },
#     {
#         "type": "function",
#         "function": {
#             "name": "pd",
#             "description": "Play dead",
#         }
#     },
#     {
#         "type": "function",
#         "function": {
#             "name": "pee",
#             "description": "Pee",
#         }
#     },
#     {
#         "type": "function",
#         "function": {
#             "name": "pu",
#             "description": "Push up",
#         }
#     },
#     {
#         "type": "function",
#         "function": {
#             "name": "pu1",
#             "description": "Push up single arm",
#         }
#     },
#     {
#         "type": "function",
#         "function": {
#             "name": "rc",
#             "description": "Recover",
#         }
#     },
#     {
#         "type": "function",
#         "function": {
#             "name": "rl",
#             "description": "Roll",
#         }
#     },
#     {
#         "type": "function",
#         "function": {
#             "name": "scrh",
#             "description": "Scratch",
#         }
#     },
#     {
#         "type": "function",
#         "function": {
#             "name": "snf",
#             "description": "Sniff",
#         }
#     },
#     {
#         "type": "function",
#         "function": {
#             "name": "tbl",
#             "description": "Table",
#         }
#     },
#     # {
#     #     "type": "function",
#     #     "function": {
#     #         "name": "ts",
#     #         "description": "Test servo",
#     #     }
#     # },
#     {
#         "type": "function",
#         "function": {
#             "name": "wh",
#             "description": "Shake your head. This function can effectively express disagreement.",
#         }
#     },
#     {
#         "type": "function",
#         "function": {
#             "name": "zz",
#             "description": "Zz",
#         }
#     },
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