import dash
from dash import html, dcc, Input, Output, callback, State
from dash.dependencies import ClientsideFunction
import feffery_antd_components as fac

from common.utils import acebergAis_items

import random






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
            className=("acebergAis_item"),
            key=item["key"],
            id=f"acebergAisitem{item['key']}"
        )
        for item in listdata
    ]
    return res



# 注册 acebergAis 的回调
def register_callbacks_acebergAis(app):

    # 进入页面就执行
    @app.callback(
        Output("acebergAis-tab-content", "children"),
        Input("layout-mainContent", "children"),
        prevent_initial_call=False,
    )
    def acebergAis_chatContent_path(children):
        if children:
            res = chatdatatohtml('all', acebergAis_items)
            return res
        else:
            return dash.no_update
        
    
    # 点击 tab 切换时执行
    @app.callback(
        Output("acebergAis-tab-content", "children", allow_duplicate=True),
        Input("acebergAis-tab", "activeKey"),
        prevent_initial_call=True,
    )
    def acebergAis_chatContent_activeKey(activeKey):
        if activeKey:
            res = chatdatatohtml(activeKey, acebergAis_items)
            return res
        else:
            return dash.no_update
        
    
    # 点击跳到对应的chat
    def acebergAis_clickitem(item):
        @app.callback(
            Output("url", "pathname", allow_duplicate=True),
            Input(f"acebergAisitem{item['key']}", "n_clicks"),
            prevent_initial_call=True,
        )
        def acebergAis_clickitem_callback(n_clicks):
            if n_clicks:
                return f"/newChat/{item['key']}"
            else:
                return dash.no_update
            
    for item in acebergAis_items:
        acebergAis_clickitem(item)