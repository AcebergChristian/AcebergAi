import dash
from dash import html
import feffery_antd_components as fac

train_layout = html.Div(
    [   
        html.Div(
        [
            # radio
            html.Div(
                [
                    fac.AntdRadioGroup(
                        id="train-radio",
                        options=[
                            {
                                'label': item['label'],
                                'value': item['value']
                            }
                            for item in [{'label':'微调', 'value':'fintuning'},
                                        {'label':'蒸馏', 'value':'distillation'}]
                        ],
                        defaultValue='c',
                        optionType='button',
                    )
                ]
            ),
            
            # 内容，需要根据radio变化
            html.Div(
                [
                    
                ],
                id="train-main",
                style={
                    "display": "flex",
                    "justifyContent": "center",
                    "alignItems": "center",
                    "justifyContent": "center",
                    "width": "100%",
                    "height": "calc(100% - 60px)",
                }
            )
        ],
        style={
            "display": "flex",
            "flexDirection": "column",
            "justifyContent": "center",
            "alignItems": "flex-start",
            "gap": 16,
            "width": "86%",
            "height": "96%",   
        }), 
    ],
    id="train-container",
    style={
        "display": "flex",
        "flexDirection": "column",
        "justifyContent": "center",
        "alignItems": "center",
        "width": "100%",
        "height": "100%",
        "backgroundColor": "#ffffff",
    },
)
