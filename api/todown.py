import dash
from dash import html, dcc, Input, Output, callback, State
from dash.dependencies import ClientsideFunction
import feffery_antd_components as fac

from common.sql import SQLiteClass
import random
import json


fakedata = [
    {"key": "1", "type": "art", "title": "无限音乐人", "description": "无限音乐人"},
    {"key": "2", "type": "art", "title": "茶艺大师", "description": "茶艺大师"},
    {"key": "3", "type": "art", "title": "艺术家", "description": "艺术家"},
    {"key": "4", "type": "efficiency", "title": "工作提醒", "description": "提醒工作提醒工作提醒工作提醒工作提醒工作提醒工作提醒工作提醒工作提醒工作提醒工作提醒工作提醒工作提醒工作提醒工作提醒工作提醒工作提醒工作提醒工作提醒"},
    {
        "key": "5",
        "type": "efficiency",
        "title": "excel全能",
        "description": "excel全能",
    },
    {"key": "6", "type": "learn", "title": "数学家", "description": "数学家"},
    {"key": "7", "type": "learn", "title": "现代诗诗人", "description": "现代诗诗人"},
    {"key": "8", "type": "learn", "title": "物理学家", "description": "物理学家"},
    {"key": "9", "type": "life", "title": "旅行助手", "description": "旅行助手"}
]

# 获取用户对话数据
# def getchatData(db):
#     with SQLiteClass("./acebergBehavior.db") as cursor:
#         data = cursor.select_data(
#             "todown",
#             "eventKey, eventName"
#         )
#     res = [{"label": item["eventName"], "value": item["eventKey"]} for item in data]
#     return res


# 对话数据编成html方法
def chatdatatohtml(agenttype, data):
    if agenttype == "all":
        listdata = data
    else:
        listdata = [item for item in data if item["type"] == agenttype]

    res = [
        html.Div(
            [
                html.Div(
                    [
                        html.Div(
                            [
                                html.Div(
                                    [item["title"].capitalize()[0]],
                                    style={
                                        "width": "40px",
                                        "height": "40px",
                                        "borderRadius": "50%",
                                        "backgroundColor": ['#317cfb', '#73b0fb', '#fd9052', '#9c61e8', '#f82c26'][random.randint(0, 4)],
                                        "textAlign": "center",
                                        "lineHeight": "42px",
                                        "fontSize": "20px",
                                        "color": "#fff",
                                    },
                                ),
                                html.Div(
                                    [
                                        html.Div(
                                            item["title"],
                                            style={
                                                "fontWeight": "bold",
                                                "color": "#494a4c",
                                            },
                                        ),
                                        html.Div(
                                            item["description"],
                                            style={
                                                "fontSize": "12px",
                                                "color": "#5e6671",
                                                "width": "100%",
                                                "height": "60px",
                                                "overflow": "hidden",
                                            }
                                        ),
                                    ],
                                    style={
                                        "display": "flex",
                                        "flexDirection": "column",
                                        "justifyContent": "space-between",
                                        "alignItems": "flex-start",
                                        "width": "calc(100% - 70px)",
                                        "height": "calc(100% - 40px)",
                                    },
                                ),
                            ],
                            style={
                                "display": "flex",
                                "flexDirection": "row",
                                "justifyContent": "flex-start",
                                "alignItems": "flex-start",
                                "gap": "12px",
                                "margin": "12px 0 0 20px",
                                "width": "calc(100% - 12px)",
                            },
                        ),
                    ]
                ),
            ],
            className=("todown_item"),
            key=item["key"],
        )
        for item in listdata
    ]
    return res


# 注册 todown 的回调
def register_callbacks_todown(app):

    # 进入页面就执行
    @app.callback(
        Output("todown-tab-content", "children"),
        Input("layout-mainContent", "children"),
        prevent_initial_call=False,
    )
    def todown_chatContent_path(children):
        if children:
            res = chatdatatohtml('all', fakedata)
            return res
        else:
            return dash.no_update
        
    
    # 点击 tab 切换时执行
    @app.callback(
        Output("todown-tab-content", "children", allow_duplicate=True),
        Input("todown-tab", "activeKey"),
        prevent_initial_call=True,
    )
    def todown_chatContent_activeKey(activeKey):
        if activeKey:
            res = chatdatatohtml(activeKey, fakedata)
            return res
        else:
            return dash.no_update
