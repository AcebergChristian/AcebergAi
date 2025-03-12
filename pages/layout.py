import dash
from dash import html, dcc, Input, Output, callback
import feffery_antd_components as fac
from static.routes import menuroutes


layout = html.Div(
    [
        dcc.Location(id="url", refresh=False),
        # 左侧菜单栏
        html.Div(
            [
                fac.AntdTooltip(
                    html.Div(
                        [
                            (
                                fac.AntdDropdown(
                                    fac.AntdIcon(
                                        className="menu-div-icon", icon=item["icon"]
                                    ),
                                    menuItems=[
                                        {
                                            "title": fac.AntdSpace(
                                                [
                                                    fac.AntdAvatar(
                                                        icon="antd-user",
                                                        style={
                                                            "background": "#f7f8f9",
                                                            "color": "#9ea5b5",
                                                            "width": 20,
                                                            "height": 20,
                                                        },
                                                    ),
                                                    fac.AntdText(
                                                        [],
                                                        id="layout-rightContent-nav-dropdown-accountrole",
                                                    ),
                                                ]
                                            ),
                                            "key": "user",
                                        },
                                        {
                                            "title": fac.AntdSpace(
                                                [
                                                    fac.AntdAvatar(
                                                        icon="antd-power-off",
                                                        style={
                                                            "background": "#f7f8f9",
                                                            "color": "#9ea5b5",
                                                            "width": 24,
                                                            "height": 24,
                                                        },
                                                    ),
                                                    "logout",
                                                ]
                                            ),
                                            "key": "logout",
                                        },
                                    ],
                                    trigger="hover",
                                    placement="topRight",
                                    id="layout-rightContent-nav-dropdown",
                                )
                                if item["id"] == "userCenter"
                                else fac.AntdDropdown(
                                    fac.AntdIcon(
                                        className="menu-div-icon", icon=item["icon"]
                                    ),
                                    menuItems=[
                                        {
                                            "title": fac.AntdImage(
                                                id="menu-scanphoto",
                                                src="../assets/images/scan.png",
                                                style={"width": 120, "borderRadius": 8},
                                                preview=False,
                                            ),
                                            "key": "scanphoto",
                                        },
                                    ],
                                    trigger="hover",
                                    placement="topRight",
                                    id="layout-rightContent-nav-dropdown",
                                )
                                if item["id"] == "toScan"
                                else (
                                    fac.AntdIcon(
                                        className="menu-div-icon", icon=item["icon"]
                                    )
                                    if item["id"] != "logo"
                                    else html.Div(
                                        [
                                            fac.AntdImage(
                                                src=item["icon"],
                                                style={"width": 32},
                                                preview=False,
                                            ),
                                            fac.AntdDivider(
                                                style={"margin": "12px auto 8px auto"}
                                            ),
                                        ]
                                    )
                                )
                            )
                        ],
                        className=(
                            "menu-div" if item["id"] != "logo" else "menu-div-logo"
                        ),
                        id=item["id"],
                    ),
                    title=item["title"] if item["id"] != "userCenter" and item["id"] != "toScan" else None,
                    placement="right",
                )
                for item in menuroutes
            ],
            id="layout-menu",
            style={
                "display": "flex",
                "flexDirection": "column",
                "alignItems": "center",
                "justifyContent": "center",
                "gap": 8,
                "position": "absolute",
                "top": "calc(50% - 200px)",
                "left": 20,
                "backgroundColor": "#fafbff",
                "height": 420,
                "width": 60,
                # 隐藏滚动条
                "scrollbarWidth": "none",
                "borderRadius": 8,
                "boxShadow": "0 2px 8px rgba(0, 0, 0, 0.15)",
            },
        ),
        # 主要内容
        html.Div(
            [],
            id="layout-mainContent",
            style={
                "width": "100%",
                "height": "100%",
                "backgroundColor": "#f3f5fa",
            },
        ),
    ],
    style={
        "display": "flex",
        "flexDirection": "row",
        "flexWrap": "nowrap",
        "width": "100vw",
        "height": "100vh",
        # "backgroundColor": "#f3f5fa",
        # "backgroundImage": "url("https://dss3.bdstatic.com/iPoZeXSm1A5BphGlnYG/skin/54.jpg")",
        "overflowY": "hidden",
        "margin": 0,
        "padding": 0,
    },
)
