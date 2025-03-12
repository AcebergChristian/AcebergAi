import dash
from dash import html
import feffery_antd_components as fac

from config import down_desc

todown_layout = html.Div(
    [
        html.Div(
            [
                # todown Logo
                html.Div(
                    [
                        fac.AntdImage(
                            id="login-logo",
                            src="../assets/images/logo.png",
                            style={"width": 48, "borderRadius": 8},
                            preview=False,
                        ),
                        html.Div(
                            "AcebergAi",
                            style={
                                "fontSize": 32,
                                "color": "#5e6671",
                            },
                        ),
                    ],
                    id="todown-logo",
                    style={
                        "display":"flex",
                        "direction": "row",
                        "justifyContent": "center",
                        "gap": "16px",
                        "alignItems": "center",
                        "width": "100%",
                        "height": "40px",
                        "marginTop": "60px",
                    },
                ),
                
                # 下载分类
                html.Div(
                    [
                        html.Div(
                            [
                                fac.AntdIcon(icon=item['icon'], style={'fontSize': 26}),
                                html.Div(item['title'])
                            ],
                            className=("todown-items"),
                            style={
                                "display": "flex",
                                "flexDirection": "column",
                                "justifyContent": "center",
                                "alignItems": "center",
                                "width": "150px",
                                "height": "150px",
                            }
                        )
                        for item in [{"icon":"di-windows", "title":"Windows"},
                                     {"icon":"antd-mobile", "title":"IOS"},
                                     {"icon":"pi-compass", "title":"MacOs"}]
                    ],
                    id='todown-content',
                    style={
                        "display":"flex",
                        "direction": "row",
                        "flexWrap": "wrap",
                        "justifyContent" : "space-around",
                        "alignContent": "flex-start",
                        "gap": "60px",
                        "width": "100%",
                        "height": "180px",
                        "overflowY": "scroll",
                        "overflowX": "hidden",
                    }
                ),
                
                # 下载文字
                html.Div([
                    html.Div(
                        down_desc
                    )
                    
                    ],
                    style={
                        "display":"flex",
                        "direction": "row",
                        "flexWrap": "wrap",
                        "alignContent": "flex-start",
                        "alignItems": "center",
                        "width": "100%",
                        "overflowY": "scroll",
                        "overflowX": "hidden",
                        "color": "rgba(0, 0, 0, 0.56)",
                        'fontSize': '14px',
                    })
            ],
            style={
                "display": "flex",
                "flexDirection": "column",
                "justifyContent": "flex-start",
                "alignItems": "center",
                "gap": "80px",
                "width": "680px",
                "height": "100%"
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
        "background": "url(../assets/images/downback.png) no-repeat center center",
        "backgroundSize": "cover"
    },
)
