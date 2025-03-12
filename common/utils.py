import dash
from dash import html, dcc, Input, Output, callback, State
from dash.dependencies import ClientsideFunction
import feffery_antd_components as fac
import feffery_markdown_components as fmc

import json
import datetime
from common.sql import SQLiteClass
import requests


###### newchat ######


# 插入到数据库
def newchat_add(key, usr_input, creator):

    content = [
        {
            "key": "bot_start",
            "role": "bot",
            "content": "你好，有什么可以帮助你的吗？",
        }
    ]

    content_str = json.dumps(content, ensure_ascii=False)
    nowtime = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    data = {
        "key": key,
        "title": usr_input,
        "content": content_str,
        "isdel": 0,
        "creator": creator,
        "createtime": nowtime,
        "updatetime": nowtime,
    }
    with SQLiteClass("./acebergAi.db") as cursor:
        affected_rows = cursor.insert_data("newchat", data)

    return affected_rows


# 获取用户对话数据
def getchatData(key):
    if key:
        with SQLiteClass("./acebergAi.db") as cursor:
            data = cursor.select_data(
                "newchat", "title, content", condition=f"key = '{key}'"
            )
        
        if data:
            title = data[0]["title"]
            content = json.loads(data[0]["content"])

            return title, content
        else:
            return "", []


# 对话数据编成html方法
def chatdatatohtml(data):
    res = []
    for item in data:

        if item["role"] == "usr":
            res.append(
                html.Div(
                    [
                        fac.AntdCopyText(
                            id=f"copy@{item['key']}",
                            text=item["content"],
                            beforeIcon=fac.AntdButton(
                                icon=fac.AntdIcon(
                                    icon="antd-copy", style={"color": "#5e6671"}
                                ),
                                color="default",
                                variant="filled",
                                id=f"copy@{item['key']}",
                            ),
                        ),
                        html.Div(
                            item["content"],
                            className=f"newChat_text newChat_text_{item['role']}",
                            id=f"content@{item['key']}",
                        ),
                        html.Div(item["role"], className="newChat_avator"),
                    ],
                    className=f"newChat_{item['role']}",
                )
            )
        else:
            if item["content"] == "loading":
                res.append(
                    html.Div(
                        [
                            html.Div("bot", className="newChat_avator"),
                            html.Div(
                                [
                                    fac.AntdIcon(
                                        icon="antd-loading",
                                    )
                                ],
                                className=f"newChat_text newChat_text_bot",
                                id=f"content@{item['key']}",
                            ),
                            # fac.AntdCopyText(
                            #     id=f"copy@{item['key']}",
                            #     text=item["content"],
                            #     beforeIcon=fac.AntdButton(
                            #         icon=fac.AntdIcon(
                            #             icon="antd-copy", style={"color": "#5e6671"}
                            #         ),
                            #         color="default",
                            #         variant="filled",
                            #         id=f"copy@{item['key']}",
                            #     ),
                            # ),
                        ],
                        className=f"newChat_bot",
                    )
                )
            else:
                res.append(
                    html.Div(
                        [
                            html.Div(item["role"], className="newChat_avator"),
                            html.Div(
                                # item["content"],
                                fmc.FefferyMarkdown(
                                    markdownStr=item["content"]
                                ),
                                className=f"newChat_text newChat_text_{item['role']}",
                                id=f"content@{item['key']}",
                            ),
                            fac.AntdCopyText(
                                id=f"copy@{item['key']}",
                                text=item["content"],
                                beforeIcon=fac.AntdButton(
                                    icon=fac.AntdIcon(
                                        icon="antd-copy", style={"color": "#5e6671"}
                                    ),
                                    color="default",
                                    variant="filled",
                                    id=f"copy@{item['key']}",
                                ),
                            ),
                        ],
                        className=f"newChat_{item['role']}",
                    )
                )

    return res


# 用户每一次对话，都更新 chatlist content字段
def newchat_update_content(key, content):
    data = {"content": content}
    with SQLiteClass("./acebergAi.db") as cursor:
        affected_rows = cursor.update_data("newchat", data, condition=f"key='{key}'")

    return affected_rows


# api接口，获取ai回答
def get_ai_answer(model, input):
    try:
        url = "https://api.siliconflow.cn/v1/chat/completions"

        payload = {
            "model": model,
            "messages": [
                {
                    "role": "user",
                    "content": input
                }
            ],
            "stream": False,
            "max_tokens": 4096,
            "temperature": 0.7,
            "top_p": 0.7,
            "top_k": 50,
            "n": 1,
        }
        headers = {
            "Authorization": "Bearer sk-mqbxvtugplfhbxewhhyzdcrnoalqsmbravrtlihzsosekbub",
            "Content-Type": "application/json"
        }

        print('API请求中...')
        response = requests.request("POST", url, json=payload, headers=headers).text
        res = json.loads(response)['choices'][0]['message']['content']
        if res:
            return res
        else:
            return "回答失败，请稍后再试"
        
    except Exception as e:
        return f"回答失败，请稍后再试{e}"


###### historyChat ######


def historychat(usr, input=None):
    # 判断是否有模糊查询
    inputstr = (
        f'AND (content LIKE "%{input}%" OR title LIKE "%{input}%" )' if input else ""
    )

    with SQLiteClass("./acebergAi.db") as cursor:
        data = cursor.select_data(
            "newchat",
            "key, title, content, creator, createtime",
            condition=f"isdel = '0' AND creator = '{usr}' {inputstr} ORDER BY createtime DESC limit 50",
        )
    return data


# 历史数据编成html方法
def historyChatdatatohtml(data):
    res = [
        html.Div(
            [
                html.Div(
                    [
                        html.Div(
                            [
                                html.Div(
                                    item["title"][:16],
                                    style={"fontWeight": "bold", "color": "#494a4c"},
                                ),
                                html.Div(item["createtime"]),
                            ],
                            style={
                                "display": "flex",
                                "flexDirection": "row",
                                "justifyContent": "space-between",
                                "alignItems": "center",
                                "gap": "24px",
                            },
                        ),
                        html.Div(
                            [
                                fac.AntdButton(
                                    id={
                                        "type": "historyChat—infobtn",
                                        "index": f"{item['key']}",
                                    },
                                    nClicks=0,
                                    icon=fac.AntdIcon(icon="antd-info-circle"),
                                ),
                                fac.AntdButton(
                                    id={
                                        "type": "historyChat—delbtn",
                                        "index": f"{item['key']}",
                                    },
                                    nClicks=0,
                                    icon=fac.AntdIcon(icon="antd-delete"),
                                ),
                            ],
                            style={
                                "display": "flex",
                                "flexDirection": "row",
                                "justifyContent": "space-between",
                                "alignItems": "center",
                                "gap": "12px",
                            },
                        ),
                    ],
                    style={
                        "display": "flex",
                        "justifyContent": "space-between",
                        "alignItems": "center",
                        "width": "96%",
                        "marginTop": "10px",
                    },
                ),
                html.Div(
                    item["content"],
                    style={
                        "display": "flex",
                        "justifyContent": "flex-start",  # 确保文本从第一行开始
                        "alignItems": "flex-start",
                        "width": "96%",
                        "height": "40%",
                        "overflow": "hidden",
                    },
                ),
            ],
            className=f"historyChat_item",
            key=item["key"],
        )
        for item in data
    ]

    return res


# 逻辑删除历史记录
def historyChat_delone(key):
    with SQLiteClass("./acebergAi.db") as cursor:
        affected_rows = cursor.update_data(
            "newchat", {"isdel": "1"}, condition=f"key='{key}'"
        )

    return affected_rows


# 逻辑删除全部历史记录
def historyChat_delAll():
    with SQLiteClass("./acebergAi.db") as cursor:
        affected_rows = cursor.update_data(
            "newchat", {"isdel": "1"}, condition=" 1 = 1"
        )

    # 返回更新结果
    return affected_rows


###### acebergAis ######

acebergAis_items = [
    {
        "key": "musician",
        "type": "art",
        "title": "无限音乐人",
        "description": "无限音乐人",
    },
    {"key": "tea", "type": "art", "title": "茶艺大师", "description": "茶艺大师"},
    {"key": "art", "type": "art", "title": "艺术家", "description": "艺术家"},
    {
        "key": "jobmind",
        "type": "efficiency",
        "title": "工作提醒",
        "description": "提醒工作提醒工作提醒工作提醒工作提醒工作提醒工作提醒工作提醒工作提醒工作提醒工作提醒工作提醒工作提醒工作提醒工作提醒工作提醒工作提醒工作提醒工作提醒",
    },
    {
        "key": "excel",
        "type": "efficiency",
        "title": "excel全能",
        "description": "excel全能",
    },
    {"key": "math", "type": "learn", "title": "数学家", "description": "数学家"},
    {
        "key": "poem",
        "type": "learn",
        "title": "现代诗诗人",
        "description": "现代诗诗人",
    },
    {"key": "physics", "type": "learn", "title": "物理学家", "description": "物理学家"},
    {"key": "tour", "type": "life", "title": "旅行助手", "description": "旅行助手"},
]


###### train ######
fintuning_layout = [
    html.Div(
        [
            fac.AntdSpace(
                [
                    "GPU环境",
                    fac.AntdSelect(
                        name="environment",
                        options=[
                            {"label": "base", "value": "base"},
                            {"label": "aliyun", "value": "aliyun"},
                            {"label": "suanli", "value": "suanli"},
                        ],
                        style={
                            'width': 250
                        },
                    ),
                ],
                align='start',
                direction='vertical',
            ),
            fac.AntdSpace(
                [
                    "预训练模型",
                    fac.AntdSelect(
                        name="model",
                        options=[
                            {"label": "llama-7b", "value": "llama-7b"},
                            {"label": "llama-13b", "value": "llama-13b"},
                            {"label": "qwen-7b", "value": "qwen-7b"},
                            {"label": "chatglm", "value": "chatglm"},
                        ],
                        style={
                            'width': 250
                        },
                    ),
                ],
                align='start',
                direction='vertical',
            ),
            fac.AntdSpace(
                [
                    "模型路径",
                    fac.AntdInput(
                        name="model",
                        style={
                            'width': 250
                        },
                    ),
                ],
                align='start',
                direction='vertical',
            ),
            fac.AntdSpace(
                [
                    "微调方法",
                    fac.AntdSelect(
                        name="finetuning_method",
                        options=[
                            {"label": "LoRA", "value": "lora"},
                            {"label": "Adam", "value": "adam"},
                            {"label": "SGD", "value": "sgd"},
                            {"label": "RMSprop", "value": "rmsprop"},
                        ],
                        style={
                            'width': 250
                        },
                    ),
                ],
                align='start',
                direction='vertical',
            ),
            fac.AntdSpace(
                [
                    "检查点路径",
                    fac.AntdInput(
                        name="model",
                        style={
                            'width': 510
                        },
                    ),
                ],
                align='start',
                direction='vertical',
            ),
            fac.AntdSpace(
                [
                    "训练方式",
                    fac.AntdSelect(
                        name="train_stage",
                        options=[
                            {"label": "无监督预训练", "value": "Unsupervised Fine-Tuning"},
                            {"label": "无监督学习", "value": "Unsupervised Learning"},
                            {"label": "强化学习", "value": "Reinforcement Learning"},
                            {"label": "半监督学习", "value": "Semi-Supervised Learning"},
                            {"label": "多任务学习", "value": "Multi-Task Learning"},
                            {"label": "迁移学习", "value": "Transfer Learning"},
                            {"label": "对比学习", "value": "Contrastive Learning"},
                            {"label": "零样本学习", "value": "Zero-Shot Learning"},
                            {"label": "少样本学习", "value": "Few-Shot Learning"},
                            

                        ],
                        style={
                            'width': 250
                        },
                    ),
                ],
                align='start',
                direction='vertical',
            ),
            fac.AntdSpace(
                [
                    "数据路径",
                    fac.AntdInput(
                        name="data_path",
                        style={
                            'width': 250
                        },
                    ),
                ],
                align='start',
                direction='vertical',
            ),
            fac.AntdSpace(
                [
                    "数据集",
                    fac.AntdSelect(
                        name="dataset",
                        options=[
                            {"label": "SQuAD", "value": "squad"},  # 新增选项
                            {"label": "GLUE", "value": "glue"},    # 新增选项
                            {"label": "MNLI", "value": "mnli"},    # 新增选项
                            {"label": "CoNLL-2003", "value": "conll2003"},  # 新增选项
                            {"label": "IMDB", "value": "imdb"},    # 新增选项
                            {"label": "CIFAR-10", "value": "cifar10"},  # 新增选项
                        ],
                        mode="multiple",
                        maxTagCount=2,
                        style={
                            'width': 250
                        },
                    ),
                ],
                align='start',
                direction='vertical',
            ),
            
            
            fac.AntdSpace(
                [
                    fac.AntdButton(
                        "开始微调",
                        size="large",
                    ),
                    fac.AntdButton(
                        "暂停微调",
                        size="large"
                    ),
                    fac.AntdButton(
                        "停止微调",
                        size="large"
                    ),
                ],
                align='start',
                direction='vertical',
            ),
            
            
            
            fac.AntdSpace(
                [
                    fac.AntdSpace(
                        [
                            "输出目录",
                            fac.AntdInput(
                                name="output_dir",
                                style={
                                    'width': 340
                                },
                            ),
                        ],
                        align='start',
                        direction='vertical',
                    ),
                    fac.AntdSpace(
                        [
                            "配置路径",
                            fac.AntdInput(
                                name="config_path",
                                style={
                                    'width': 340
                                },
                            ),
                        ],
                        align='start',
                        direction='vertical',
                    ),
                ],
                align='start',
                direction='vertical',
            ),
            
            # 损失函数图
            fac.AntdSpace(
                [
                    "",
                    html.Div(
                        [],
                        id="lossplot",
                        style={
                            "width": 320,
                            "height": 250,
                            "backgroundColor": "#ffffff",
                        },
                    ),
                ],
                align='start',
                direction='vertical',
            ),
            
            
        ],
        id="fintuning-content",
        style={
            "padding": "20px",
            "display": "flex",
            "flexWrap": "wrap",
            "flexDirection": "row",
            "justifyContent": "flex-start",
            "alignItems": "flex-start",
            "alignContent": "flex-start",
            "gap": 16,
            "width": "calc(76% - 40px)",
            "height": "calc(100% - 40px)",
            "backgroundColor": "#f6f8fa",
        },
    ),
    html.Div(
        [
            fac.AntdText("训练参数",
                style={"fontSize": 16, "fontWeight": "bold"}
            ),
            
            fac.AntdSpace(
                [
                    fac.AntdText("学习率",
                        style={"fontSize": 14, "fontWeight": "normal"}
                    ),
                    fac.AntdInput(
                        name="learning_rate",
                        style={
                            'width': 250
                        },
                    ),
                ],
                align='start',
                direction='vertical',
            ),
            
            fac.AntdSpace(
                [
                    fac.AntdText("训练轮数",
                        style={"fontSize": 14, "fontWeight": "normal"}
                    ),
                    fac.AntdInputNumber(
                        name="epoch",
                        style={
                            'width': 250
                        },
                    ),
                ],
                align='start',
                direction='vertical',
            ),
            
            fac.AntdSpace(
                [
                    fac.AntdText("最大梯度范数",
                        style={"fontSize": 14, "fontWeight": "normal"}
                    ),
                    fac.AntdInputNumber(
                        name="max_grad_norm",
                        style={
                            'width': 250
                        },
                    ),
                ],
                align='start',
                direction='vertical',
            ),
            
            fac.AntdSpace(
                [
                    fac.AntdText("最大样本数",
                        style={"fontSize": 14, "fontWeight": "normal"}
                    ),
                    fac.AntdInputNumber(
                        name="max_samples",
                        style={
                            'width': 250
                        },
                    ),
                ],
                align='start',
                direction='vertical',
            ),
            
            fac.AntdSpace(
                [
                    fac.AntdText("计算类型",
                        style={"fontSize": 14, "fontWeight": "normal"}
                    ),
                    fac.AntdSelect(
                        name="compute_type",
                        options=[
                            {"label": "bf16", "value": "bf16"},
                            {"label": "fp16", "value": "fp16"},
                            {"label": "fp32", "value": "fp32"},
                            {"label": "fp64", "value": "fp64"},
                        ],
                        maxTagCount=2,
                        style={
                            'width': 250
                        },
                    ),
                ],
                align='start',
                direction='vertical',
            ),
            
            fac.AntdSpace(
                [
                    fac.AntdText("截断长度",
                        style={"fontSize": 14, "fontWeight": "normal"}
                    ),
                    fac.AntdInputNumber(
                        name="max_length",
                        style={
                            'width': 250
                        },
                    ),
                ],
                align='start',
                direction='vertical',
            ),
            
            fac.AntdSpace(
                [
                    fac.AntdText("批处理大小",
                        style={"fontSize": 14, "fontWeight": "normal"}
                    ),
                    fac.AntdInputNumber(
                        name="batch_size",
                        style={
                            'width': 250
                        },
                    ),
                ],
                align='start',
                direction='vertical',
            ),
            
            fac.AntdSpace(
                [
                    fac.AntdText("梯度累积",
                        style={"fontSize": 14, "fontWeight": "normal"}
                    ),
                    fac.AntdInputNumber(
                        name="batch_size",
                        style={
                            'width': 250
                        },
                    ),
                ],
                align='start',
                direction='vertical',
            ),
            
            fac.AntdSpace(
                [
                    fac.AntdText("验证集比例",
                        style={"fontSize": 14, "fontWeight": "normal"}
                    ),
                    fac.AntdInputNumber(
                        name="val_ratio", #验证集比例
                        style={
                            'width': 250
                        },
                    ),
                ],
                align='start',
                direction='vertical',
            ),
            
            fac.AntdSpace(
                [
                    fac.AntdText("学习率调节器",
                        style={"fontSize": 14, "fontWeight": "normal"}
                    ),
                    fac.AntdSelect(
                        name="lr_scheduler",
                        options=[
                            {"label": "cosine", "value": "cosine"},
                            {"label": "linear", "value": "linear"},
                            {"label": "step", "value": "step"},
                            {"label": "multi_step", "value": "multi_step"},
                            {"label": "constant", "value": "constant"},
                            {"label": "constant_with_warmup", "value": "constant_with_warmup"},
                        ],
                        maxTagCount=2,
                        style={
                            'width': 250
                        },
                    ),
                ],
                align='start',
                direction='vertical',
            ),
            
            fac.AntdSpace(
                [
                    fac.AntdText("优化器",
                        style={"fontSize": 14, "fontWeight": "normal"}
                    ),
                    fac.AntdSelect(
                        name="optimizer",
                        options=[
                            {"label": "Adam / AdamW", "value": "adam"},
                            {"label": "SGD", "value": "sgd"},
                            {"label": "Adafactor", "value": "adafactor"},
                            {"label": "LAMB", "value": "lamb"},
                            {"label": "RMSProp", "value": ""},
                            {"label": "Adagrad", "value": "adagrad"},
                            {"label": "混合优化器", "value": "mix"},
                            {"label": "ZeroRedundancyOptimizer", "value": "zero"},
                            {"label": "8-bit Adam", "value": "8bit"},
                            {"label": "Sharded", "value": "sharded"},
                            
                        ],
                        maxTagCount=2,
                        style={
                            'width': 250
                        },
                    ),
                ],
                align='start',
                direction='vertical',
            ),
            
            
        ],
        id="train-option",
        style={
            "padding": "10px",
            "width": "calc(24% - 20px)",
            "height": "calc(100% - 20px)",
            "backgroundColor": "#eeeeee",
            "overflowY": "auto",
        },
    ),
]

# distillation_layout
distillation_layout = [
    html.Div(
        [
            fac.AntdSpace(
                [
                    "GPU环境",
                    fac.AntdSelect(
                        name="environment",
                        options=[
                            {"label": "base", "value": "base"},
                            {"label": "aliyun", "value": "aliyun"},
                            {"label": "suanli", "value": "suanli"},
                        ],
                        style={
                            'width': 250
                        },
                    ),
                ],
                align='start',
                direction='vertical',
            ),
            fac.AntdSpace(
                [
                    "教师模型",
                    fac.AntdSelect(
                        name="teacher_model",
                        options=[
                            {"label": "deepseek-v3", "value": "deepseek-v3"},
                            {"label": "deepseek-r1", "value": "deepseek-r1"},
                            {"label": "gpt-o1", "value": "gpt-o1"},
                            {"label": "gpt-4o", "value": "gpt-4o"},
                        ],
                        style={
                            'width': 250
                        },
                    ),
                ],
                align='start',
                direction='vertical',
            ),
            fac.AntdSpace(
                [
                    "学生模型",
                    fac.AntdSelect(
                        name="student_model",
                        options=[
                            {"label": "llama-7b", "value": "llama-7b"},
                            {"label": "llama-13b", "value": "llama-13b"},
                            {"label": "qwen-7b", "value": "qwen-7b"},
                            {"label": "chatglm", "value": "chatglm"},
                        ],
                        style={
                            'width': 250
                        },
                    ),
                ],
                align='start',
                direction='vertical',
            ),
            fac.AntdSpace(
                [
                    "训练数据路径",
                    fac.AntdInput(
                        name="train_data_path",
                        style={
                            'width': 780
                        },
                    ),
                ],
                align='start',
                direction='vertical',
            ),
            
            
            fac.AntdSpace(
                [
                    fac.AntdButton(
                        "开始蒸馏",
                        size="large",
                    ),
                    fac.AntdButton(
                        "暂停蒸馏",
                        size="large"
                    ),
                    fac.AntdButton(
                        "停止蒸馏",
                        size="large"
                    ),
                ],
                align='start',
                direction='vertical',
            ),
            
            
            
            fac.AntdSpace(
                [
                    fac.AntdSpace(
                        [
                            "输出目录",
                            fac.AntdInput(
                                name="output_dir",
                                style={
                                    'width': 340
                                },
                            ),
                        ],
                        align='start',
                        direction='vertical',
                    ),
                    fac.AntdSpace(
                        [
                            "配置路径",
                            fac.AntdInput(
                                name="config_path",
                                style={
                                    'width': 340
                                },
                            ),
                        ],
                        align='start',
                        direction='vertical',
                    ),
                ],
                align='start',
                direction='vertical',
            ),
            
            # 损失函数图
            fac.AntdSpace(
                [
                    "",
                    html.Div(
                        [],
                        id="lossplot",
                        style={
                            "width": 320,
                            "height": 280,
                            "backgroundColor": "#ffffff",
                        },
                    ),
                ],
                align='start',
                direction='vertical',
            ),
            
            
        ],
        id="distillation-content",
        style={
            "padding": "20px",
            "display": "flex",
            "flexWrap": "wrap",
            "flexDirection": "row",
            "justifyContent": "flex-start",
            "alignItems": "flex-start",
            "alignContent": "flex-start",
            "gap": 16,
            "width": "calc(76% - 40px)",
            "height": "calc(100% - 40px)",
            "backgroundColor": "#f6f8fa",
        },
    ),
    html.Div(
        [
            fac.AntdText("训练参数",
                style={"fontSize": 16, "fontWeight": "bold"}
            ),
            
            fac.AntdSpace(
                [
                    fac.AntdText("学习率",
                        style={"fontSize": 14, "fontWeight": "normal"}
                    ),
                    fac.AntdInput(
                        name="learning_rate",
                        style={
                            'width': 250
                        },
                    ),
                ],
                align='start',
                direction='vertical',
            ),
            
            fac.AntdSpace(
                [
                    fac.AntdText("训练轮数",
                        style={"fontSize": 14, "fontWeight": "normal"}
                    ),
                    fac.AntdInputNumber(
                        name="epoch",
                        style={
                            'width': 250
                        },
                    ),
                ],
                align='start',
                direction='vertical',
            ),
            
            fac.AntdSpace(
                [
                    fac.AntdText("批处理大小",
                        style={"fontSize": 14, "fontWeight": "normal"}
                    ),
                    fac.AntdInputNumber(
                        name="batch_size",
                        style={
                            'width': 250
                        },
                    ),
                ],
                align='start',
                direction='vertical',
            ),
            
            fac.AntdSpace(
                [
                    fac.AntdText("温度参数",
                        style={"fontSize": 14, "fontWeight": "normal"}
                    ),
                    fac.AntdInputNumber(
                        name="temperature",
                        style={
                            'width': 250
                        },
                    ),
                ],
                align='start',
                direction='vertical',
            ),
            
            fac.AntdSpace(
                [
                    fac.AntdText("蒸馏损失权重",
                        style={"fontSize": 14, "fontWeight": "normal"}
                    ),
                    fac.AntdInputNumber(
                        name="distillation_loss_weight",
                        style={
                            'width': 250
                        },
                    ),
                ],
                align='start',
                direction='vertical',
            ),
            
            fac.AntdSpace(
                [
                    fac.AntdText("最大序列长度",
                        style={"fontSize": 14, "fontWeight": "normal"}
                    ),
                    fac.AntdInputNumber(
                        name="max_seq_length",
                        style={
                            'width': 250
                        },
                    ),
                ],
                align='start',
                direction='vertical',
            ),
            
            fac.AntdSpace(
                [
                    fac.AntdText("早停轮数",
                        style={"fontSize": 14, "fontWeight": "normal"}
                    ),
                    fac.AntdInputNumber(
                        name="early_stopping_rounds",
                        style={
                            'width': 250
                        },
                    ),
                ],
                align='start',
                direction='vertical',
            ),
            
            fac.AntdSpace(
                [
                    fac.AntdText("梯度裁剪阈值",
                        style={"fontSize": 14, "fontWeight": "normal"}
                    ),
                    fac.AntdInputNumber(
                        name="gradient_clipping",
                        style={
                            'width': 250
                        },
                    ),
                ],
                align='start',
                direction='vertical',
            ),
            
            fac.AntdSpace(
                [
                    fac.AntdText("混合精度训练:",
                        style={"fontSize": 14, "fontWeight": "normal"}
                    ),
                    fac.AntdSwitch(
                        name="mixed_precision",
                    )
                ],
                align='start',
                direction='vertical',
            ),
            
            
            
        ],
        id="train-option",
        style={
            "padding": "10px",
            "width": "calc(24% - 20px)",
            "height": "calc(100% - 20px)",
            "backgroundColor": "#eeeeee",
        },
    ),
]




# 训练方法
# import torch
# from transformers import GPT2Tokenizer, GPT2LMHeadModel, Trainer, TrainingArguments
# from datasets import load_dataset

# def train(args):

#     # 1. 加载数据集
#     dataset = load_dataset("wikitext", "wikitext-2-raw-v1")

#     # 2. 加载预训练模型和分词器
#     model_name = "gpt2"
#     tokenizer = GPT2Tokenizer.from_pretrained(model_name)
#     model = GPT2LMHeadModel.from_pretrained(model_name)

#     # 3. 数据预处理
#     def tokenize_function(examples):
#         return tokenizer(examples["text"], truncation=True, padding="max_length", max_length=128)

#     tokenized_datasets = dataset.map(tokenize_function, batched=True, remove_columns=["text"])

#     # 4. 设置训练参数
#     training_args = TrainingArguments(
#         output_dir="./results",          # 输出目录
#         overwrite_output_dir=True,       # 覆盖输出目录
#         num_train_epochs=3,              # 训练轮数
#         per_device_train_batch_size=8,   # 批处理大小
#         per_device_eval_batch_size=8,    # 验证批处理大小
#         gradient_accumulation_steps=2,   # 梯度积累步数
#         evaluation_strategy="epoch",     # 每个epoch进行验证
#         save_strategy="epoch",           # 每个epoch保存模型
#         learning_rate=5e-5,              # 学习率
#         weight_decay=0.01,               # 权重衰减
#         warmup_steps=500,                # 学习率预热步数
#         logging_dir="./logs",            # 日志目录
#         logging_steps=10,                # 日志记录步数
#         fp16=True,                       # 使用混合精度训练
#         max_grad_norm=1.0,               # 最大梯度范式
#         save_total_limit=2,              # 最多保存的模型数量
#         load_best_model_at_end=True,     # 训练结束时加载最佳模型
#         metric_for_best_model="eval_loss",  # 用于选择最佳模型的指标
#         greater_is_better=False,         # 指标是否越大越好
#         report_to="none",                # 不报告到任何平台
#     )

#     # 5. 定义 Trainer
#     trainer = Trainer(
#         model=model,
#         args=training_args,
#         train_dataset=tokenized_datasets["train"],
#         eval_dataset=tokenized_datasets["validation"],
#     )

#     # 6. 开始训练
#     trainer.train()

#     # 7. 保存模型
#     trainer.save_model("./fine_tuned_model")
#     tokenizer.save_pretrained("./fine_tuned_model")