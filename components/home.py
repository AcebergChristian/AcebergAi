import dash
from dash import html
import feffery_antd_components as fac


home_layout = html.Div(
            [
                html.Div(
                    [
                        fac.AntdImage(
                            id="login-logo",
                            src="../assets/images/logo.png",
                            style={"width": 48, "borderRadius": 8},
                            preview=False,
                        ),
                        html.Div(
                            "AcebergAi Pro",
                            style={
                                "fontSize": 32,
                                "color": "#5e6671",
                            },
                        ),
                    ],
                    id="home-logo",
                    style={
                        "display": "flex",
                        "flexDirection": "row",
                        "justifyContent": "flex-start",
                        "alignItems": "center",
                        "gap": 16
                    },
                ),
                
                # 用户输入
                html.Div(
                    [ 
                    fac.AntdInput(
                        mode="text-area",
                        style={
                            "width": 600,
                            "height": 120,
                        },
                        id="home-input",
                    ),
                    
                    ],
                ),
                
                # 按钮组
                html.Div(
                    [
                        fac.AntdButton(
                            icon=fac.AntdIcon(icon='antd-link'),
                            color="default",
                            variant="text"
                        ),
                        fac.AntdButton(
                            id="home-send",
                            icon=fac.AntdIcon(icon='antd-send'),
                            color="default",
                            variant="text"
                        )
                    ],
                    style={
                        "display": "flex",
                        "flexDirection": "row",
                        "justifyContent": "flex-end",
                        "alignItems": "center",
                        "gap": 16,
                        "width": 600,
                        "height": 40,
                        # "backgroundColor": "#ffffff",
                        "borderRadius": 4
                    }
                )
            ],
            style={
                "display": "flex",
                "flexDirection": "column",
                # "justifyContent": "center",
                "alignItems": "center",
                "gap": 18,
                "width": "100%",
                "height": "100%",
                "marginTop": 200,
            }
        )
