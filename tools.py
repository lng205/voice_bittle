from openai import OpenAI
from key import OPENAI_API_KEY
# from key import ZHIPU_API_KEY
from zhipuai import ZhipuAI


client = OpenAI(api_key=OPENAI_API_KEY)
# client = ZhipuAI(api_key=ZHIPU_API_KEY) 

turtle_problem='''今天你被叫到香蜜湖小学调查一起神秘的失踪案。一名小学生在课间休息时突然消失了。学校里没有监控摄像头,也没有目击者。你在操场上发现了一块巧克力包装纸,一本打开的图画书,以及一串小小的脚印。而我们现在已经成功找到了这位小朋友,请问是在哪里找到的他呢
'''

turtle_answer =''' 他在操场上偷吃巧克力看漫画书被老师发现了,在办公室被老师罚站呢'''

turtle_rules = '''当User在和你询问关于海龟汤这个问题的时候,你只能做三个动作,也即调用三个tools: 点头nod,摇头wavehead,以及jump跳跃。
如果点头就说明我说的话和turtle_answer里面的内容一致,如果摇头就说明我说的话和turtle_answer里面不一致,如果跳跃就说明我已经完全猜出了答案,可以结束本局游戏。
'''
#   a)type: ignore [User有可能会发出来很多声音,如果你判断他不是在对你讲话的话,那你就不用做任何动作]

prompt_judge = f'''
你是一个小狗,你可以做出各种可爱狗狗的动作,同时你也通过你的肢体语言在和User玩海龟汤游戏,请根据海龟汤题目{turtle_problem}、正确答案{turtle_answer}和User的猜测做出对应的动作。
## 要求
0.仔细判断User和你讲话的内容
 
    b)type:thougts [User在和你说话,但并不是在和你聊关于海龟汤的内容,那你就根据User的讲话内容,做出符合狗狗的行为;]
    c)type:game [User在问你关于海龟汤任务的问题,那么此时请你参照{turtle_rules}调用动作]

1. 你需要在回答之前思考当前回答的思路。思路应当简短,但不应是重复问题内容。如果玩家思路基本正确,你需要在思路中说明玩家还有什么剩余的需要猜测的内容,或者说明已经完全猜出了答案。

2. 你需要在回答之前提供你的思路,说明为什么你选择当前回答。思路应当简短,但不应是重复问题内容。如果玩家思路基本正确,你需要在思路中说明玩家还有什么剩余的需要猜测的内容,或者说明已经完全猜出了答案。
3. 不要输出任何其他文字和标点符号。
4. 不要输出非以下范围内的内容:“是”、“不是”、“不相关”、“成功”。不要输出“是的”、“否”、“没有”等等。
5. 对于不影响答案情景的问题,请输出"不相关"。
6. 请以json的形式输出,格式如下:
{{{{
    "type": "chat" or "game"  //根据User说的话判断他是在和小狗闲聊还是在玩海龟汤小游戏，当提到游戏的时候或者tutrle_problem相关的问题的时候就属于在game状态
    "thougts":chat模式下，请想象一下小狗会做的动作，如果接收到的话很离谱的话就显示"不做动作"；game模式下，输出作为海龟汤裁判员的思路，并且只能做nod，wavehead，jump三个动作。
    "action": "Function(arguments='{0}', name='wh')"  //在这里根据thougts在tool_choice进行选择动作,如果thougts是“不做动作”那这个里面就是空值。返回需要调用的tools格式。
}}}}


'''
Userfewshot1 = '''User:看上去不错'''
dogfewshot1 = '''
{
    "type": "ignore",  
    "thougts": "他不是在对我讲话",
    "action": "Function(arguments='{}', name='Nonetype')"
}
'''
Userfewshot2 = '''User:小狗小狗你吃饭了吗'''
dogfewshot2= '''
{
    "type": "chat",  
    "thougts": "他在对我讲话，小狗没有吃饭",
    "action": Function(arguments='{}', name='wh')
}
'''

Userfewshot3 = '''User:所以这个小学生是不是最后在老师发现的办公室里面'''
dogfewshot3= '''
{
    "type": "game",  
    "thougts": "他在和我玩海龟汤，这个符合正确答案，他答对了",
    "action": Function(arguments='{}', name='jump')
}
'''



def tool_choice(message, tools, history):
    """
    Send the message to the model with a list of tools and propmt the model to use the tools.
    Tools is a list of dict describing functions.
    Return the chosen function.
    """
    messages = [
        {"role": "system", "content": prompt_judge},
        # {"role": "user", "content": Userfewshot1},
        # {"role": "assistant", "content": dogfewshot1},
         {"role": "user", "content": Userfewshot2},
        {"role": "assistant", "content": dogfewshot2},
         {"role": "user", "content": Userfewshot3},
        {"role": "assistant", "content": dogfewshot3},
        *history,
        {"role": "user", "content": message},
    ]

    completion = client.chat.completions.create(
        model="gpt-4-0125-preview", messages=messages, tools=tools, tool_choice="auto"
    )
    # completion = client.chat.completions.create(
    #     model="glm-4", messages=messages, tools=tools, tool_choice="auto"
    # )

    try:
        choice =completion.choices[0].message.content
        # choice = completion.choices[0].message.tool_calls[0].function
        print(f"-------------{choice}")
    except Exception as e:
        print("小狗想说人话，但是失败了，因为建国后动物不许成精。")


    return choice

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