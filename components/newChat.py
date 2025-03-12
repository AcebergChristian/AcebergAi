import dash
from dash import html, dcc
import feffery_antd_components as fac
import feffery_utils_components as fuc


newChat_layout = html.Div(
    [
        # timeout
        fuc.FefferyTimeout(
            id='newChat-timeout'
        ),
        
        html.Div(
            id="test"
        ),
        
        html.Div(
            [
                # top
                html.Div(
                    [
                        html.Div(
                            "AcebergAi Pro",
                            style={
                                "fontSize": 14,
                                "color": "#5e6671",
                            },
                        ),
                    ],
                    id="newChat-top",
                    style={
                        "textAlign": "center",
                        "lineHeight": "40px",
                        "width": "100%",
                        "height": "40px",
                    },
                ),
                # 对话内容
                html.Div(
                    [],
                    id="newChat-content",
                    style={
                        "width": "100%",
                        "height": "560px",
                        "overflowY": "auto",
                        "scrollWidth": 0,
                        "overflowX": "hidden",
                        "color": "#333333",
                    },
                ),
                
                # 用户输入
                html.Div(
                    [
                        fac.AntdInput(
                            id="newChat-input",
                            mode="text-area",
                            style={
                                "width": "100%",
                                "height": "90px",
                            },
                        ),
                        # 按钮组
                        html.Div(
                            [
                                fac.AntdSelect(
                                    id="newChat-model",
                                    defaultValue="deepseek-ai/DeepSeek-R1-Distill-Llama-8B",
                                    options=[
                                        {
                                            'group': 'default',
                                            'options': [
                                                {'label': 'deepseek-ai/DeepSeek-R1-Distill-Llama-8B', 'value':'deepseek-ai/DeepSeek-R1-Distill-Llama-8B'},
                                                {'label': 'deepseek-ai/DeepSeek-R1-Distill-Qwen-7B', 'value':'deepseek-ai/DeepSeek-R1-Distill-Qwen-7B'},
                                                {'label': 'Qwen/Qwen2.5-7B-Instruct', 'value':'Qwen/Qwen2.5-7B-Instruct'}
                                            ],
                                        },
                                        {
                                            'group': 'base',
                                            'options': [
                                                {'label': '微调1', 'value': 'fintuning_1'},
                                                {'label': '微调2', 'value': 'fintuning_2'},
                                                {'label': '蒸馏1', 'value': 'distillation_1'},
                                                {'label': '蒸馏2', 'value': ' distillation_2'},
                                            ],
                                        },
                                    ],
                                    style={'width': 160},
                                ),
                                
                                html.Div(
                                    [
                                        fac.AntdButton(
                                            id="newChat-inputarea-upload",
                                            icon=fac.AntdIcon(icon="antd-link"),
                                            color="default",
                                            variant="text",
                                        ),
                                        fac.AntdButton(
                                            id="newChat-inputarea-send",
                                            icon=fac.AntdIcon(icon="antd-send"),
                                            color="default",
                                            variant="text",
                                        ),
                                    ]
                                ),
                                
                            ],
                            style={
                                "display": "flex",
                                "flexDirection": "row",
                                "justifyContent": "space-between",
                                "alignItems": "center",
                                "gap": 16,
                                "width": "100%",
                                "height": "40px",
                                # "backgroundColor": "#ffffff",
                                "borderRadius": 4,
                            },
                        ),
                    ],
                    id="newChat-inputarea",
                    style={
                        "display": "flex",
                        "flexDirection": "column",
                        "justifyContent": "space-between",
                        "alignItems": "center",
                        "gap": 0,
                        "width":"100%"
                    },
                ),
                
                # bottom
                html.Div(
                    [
                        html.Div(
                            "内容由 AI 大模型生成，请仔细甄别!",
                            style={
                                "fontSize": 12,
                                "color": "#5e6671",
                            },
                        ),
                    ],
                    id="newChat-bottom",
                    style={
                        "textAlign": "center",
                        "lineHeight": "20px",
                        "width": "100%",
                        "height": "20px",
                    },
                )
                
                
            ],
            style={
                "display": "flex",
                "flexDirection": "column",
                "justifyContent": "space-between",
                "alignItems": "center",
                "gap": "8px",
                "width": "680px",
                "height": "100%",
            },
        ),
    ],
    style={
        "display": "flex",
        "flexDirection": "column",
        "justifyContent": "center",
        "alignItems": "center",
        "width": "100%",
        "height": "100%",
    },
)
