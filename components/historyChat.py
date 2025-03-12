import dash
from dash import html
import feffery_antd_components as fac

historyChat_layout = html.Div(
    [
        html.Div(
            [
                # search input
                html.Div(
                    [
                        fac.AntdInput(
                            id='historyChat—search',
                            mode='search',
                            allowClear=True,
                        ),
                        
                        # 按钮bar
                        html.Div(
                            [
                                fac.AntdButton(
                                    fac.AntdIcon(
                                        id='historyChat—delAllbtn',
                                        icon='antd-delete'),
                                )
                            ],
                            id="historyChat-search-btnbar",
                        ),
                    ],
                    id="historyChat-search",
                    style={
                        "display":"flex",
                        "direction": "row",
                        "justifyContent": "space-between",
                        "gap": "16px",
                        "alignItems": "center",
                        "width": "100%",
                        "height": "40px",
                    },
                ),
                # 对话历史
                html.Div(
                    [],
                    id="historyChat-content",
                    style={
                        "width": "100%",
                        "height": "100%",
                        # "height": "calc(100% - 40px)",
                        "overflowY": "scroll",
                        "overflowX": "hidden",
                        "color": "#333333",
                    },
                ),
            ],
            style={
                "display": "flex",
                "flexDirection": "column",
                "justifyContent": "flex-start",
                "alignItems": "center",
                "gap": "12px",
                "width": "680px",
                "height": "calc(100% - 100px)",
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
