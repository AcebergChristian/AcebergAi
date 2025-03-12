import dash
from dash import html, dcc, Input, Output, callback
import feffery_antd_components as fac


carousellist = [
    "拥抱AcebergAi, AI赋能新境界",
    "洞察知识脉络,微调雕琢细节,训练激发潜能",
    "畅享智慧交流,助力创新,引领变革"
]

login_layout = html.Div(
    [ 
        html.Div(id='login-message'),
        
        
        
        
        html.Div(
            [
                fac.AntdImage(
                    id='login-logo',
                    src="../assets/images/logo.png",
                    style={
                        "width": 36,
                        "borderRadius": 8
                    },
                    preview=False
                ),
                
                html.Div(
                    "AcebergAi Pro",
                    style={
                        "fontSize": 18,
                        "color": "#ffffff",
                    }
                )
            ],
            id='login-logo',
            style={
                "display": "flex",
                "flexDirection": "row",
                "justifyContent": "flex-start",
                "alignItems": "center",
                "gap": 16,
                "position": "absolute",
                "top": 28,
                "left": 28,
            },
        ),
        
        
        # 走马灯div
        html.Div(
            [
                fac.AntdCarousel(
                    [
                        fac.AntdCenter(
                            item,
                            style={
                                'color': 'white',
                                'fontSize': 16,
                                'height': 300,
                                'backgroundColor': 'rgba(0, 0, 0, 0)',
                            },
                        )
                        for item in carousellist
                    ],
                    dotPosition='left',
                    arrows=True,
                ),
            ],
            id='login-carousel',
            style={
                'display': 'flex',
                'justifyContent': 'center',
                'alignItems': 'center',
                'width': 500,
                'height': '100%',
                'backgroundImage': 'linear-gradient(to bottom, #1b2331, #0d2e6e)',  # 使用线性渐变 
            }
        ),
        
           
           
        fac.AntdSpace(
            [
                # fac.AntdImage(
                #     src="../assets/images/logox.png",
                #     style={"width": 140, "marginTop": 32, "borderRadius": 8},
                #     preview=False,
                # ),
                html.Div(
                    [
                        fac.AntdSpace(
                                    [
                                        html.H3("Aceberg Ai赋能平台",style={"color":"#333333","margin":0}),
                                        html.H4("Design by Aceberg",style={"color":"#333333","margin":0}),
                                    ],
                                    direction="vertical",
                                    style={"margin": '30px 0 0 20px'},
                        ),
                        
                        fac.AntdCenter(
                            [
                                fac.AntdSpace(
                                    [
                                        html.H5(
                                            "username",
                                            style={
                                                "color":"#333333"
                                            }
                                        ),
                                        fac.AntdInput(
                                            id="username",
                                            placeholder="account: admin",
                                            style={"width": 240},
                                            autoComplete='off',
                                        ),
                                    ],
                                    style={"marginTop":16},
                                )
                            ],
                            style={"backgroundColor": "null"},
                        ),
                        fac.AntdCenter(
                            [
                                fac.AntdSpace(
                                    [
                                        html.H5("password",
                                                style={"color":"#333333"}),
                                        fac.AntdInput(
                                            id="password",
                                            placeholder="password: admin",
                                            style={"width": 240},
                                            mode="password",
                                            autoComplete='off',
                                        ),
                                    ]
                                )
                            ],
                            style={"backgroundColor": "null"},
                        ),
                        fac.AntdCenter(
                            [
                                fac.AntdButton(
                                    "登陆",
                                    id="login-btn_login",
                                    style={"width": "80%", "marginTop": 32},
                                    type='primary'
                                )
                            ],
                            style={"backgroundColor": "null"},
                        ),
                    ],
                    style={
                        "width": 360,
                        "height": 420,
                        "backgroundColor": "rgba(255,255,255,0.86)",
                        "borderRadius": 6,
                    },
                ),
            ],
            align="center",
            direction="vertical",
            style={
                "display": "flex",
                "flexDirection": "row",
                "justifyContent": "center",
                "alignItems": "center",
                "width": "100%",
                "height": "100%",
                "overflowY": "scroll"
            },
        ),
    ],
    style={
        "display": "flex",
        "flexDirection": "row",
        "justifyContent": "center",
        "alignItems": "center",
        "width": "100%",
        "height": "100%",
        "backgroundSize": "cover",
        # "overflowY": "hidden",
        "backgroundImage": "url('../assets/images/bg.jpeg')",
    },
)

