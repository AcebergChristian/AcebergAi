import dash
from dash import html
import feffery_antd_components as fac

acebergAis_layout = html.Div(
    [
        html.Div(
            [
                # acebergAis Logo
                html.Div(
                    [
                        fac.AntdImage(
                            id="login-logo",
                            src="../assets/images/logo.png",
                            style={"width": 48, "borderRadius": 8},
                            preview=False,
                        ),
                        html.Div(
                            "AcebergAis",
                            style={
                                "fontSize": 32,
                                "color": "#5e6671",
                            },
                        ),
                    ],
                    id="acebergAis-logo",
                    style={
                        "display":"flex",
                        "direction": "row",
                        "justifyContent": "center",
                        "gap": "16px",
                        "alignItems": "center",
                        "width": "100%",
                        "height": "40px",
                    },
                ),
                
                html.Div(
                    "大家好, 这里是 AcebergAis, 提供一些Agent服务",
                    style={
                        "fontSize": 14,
                        "color": "#5e6671",
                        "width": "100%",
                        "height": "20px",
                        "text-align": "center",
                    },
                ),
                
                # tab分类
                html.Div(
                    [
                        fac.AntdTabs(
                            id='acebergAis-tab',
                            items=[
                                {'label': '全部', 'key': 'all'},
                                {'label': '艺术', 'key': 'art'},
                                {'label': '效率', 'key': 'efficiency'},
                                {'label': '学习', 'key': 'learn'},
                                {'label': '生活', 'key': 'life'}
                            ],
                            defaultActiveKey='all'
                        ),
                        html.Div(
                            [
                            
                            ],
                            id='acebergAis-tab-content',
                            style={
                                "display":"flex",
                                "direction": "row",
                                "flexWrap": "wrap",
                                "justifyContent": "flex-start",
                                "gap": "12px",
                                "alignContent": "flex-start",
                                "width": "100%",
                                "height": "100%",
                            }
                        ),
                    ],
                    id="acebergAis-agent",
                    style={
                        "display":"flex",
                        "flexDirection": "column",
                        "justifyContent": "center",
                        "alignItems": "center",
                        "gap": "16px",
                        "width": "100%",
                        "height": "calc(100% - 60px)",
                    },
                ),
            ],
            style={
                "display": "flex",
                "flexDirection": "column",
                "justifyContent": "flex-start",
                "alignItems": "center",
                "gap": "20px",
                "width": "680px",
                "height": "100%",
                "paddingTop": "60px",
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
