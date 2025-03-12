import dash
from dash import callback, Input, Output, State, html, clientside_callback
from dash import dcc 
from urllib.parse import urlparse, urlunparse
from pages.login import login_layout
from pages.layout import layout
from dash.dependencies import ClientsideFunction
from static.routes import menuroutes
import uuid

from api.login import login, logout


import feffery_antd_components as fac
from common.tools import sha256_encrypt
from common.utils import newchat_add



from components.home import home_layout
from components.newChat import newChat_layout
from components.historyChat import historyChat_layout
from components.acebergAis import acebergAis_layout
from components.train import train_layout
from components.api import api_layout
from components.todown import todown_layout


# exception
from components.exception import exception_layout



# 装饰器：检查 localStorage 中的登录状态
def login_required(f):
    def wrapper(*args, **kwargs):
        # 判断localstorage里是否有登陆信息，没有则回到 /login
        pathname, data = args
        if data:
            pass
        else:
            return login_layout, '/login'
        return f(*args, **kwargs)
    return wrapper


def register_callbacks(app):
    
    @callback(
        Output('maincontainer', 'children'),
        Output('mainurl', 'pathname'),
        
        Input('mainurl', 'pathname'),
        State('loginStatus', 'data'),
        prevent_initial_call=True,
    )
    @login_required
    def display_page(pathname, data):
        
        if pathname == '/login':
            if data and data['status'] == 'login':
                return layout, '/home'
            else:
                return login_layout, '/login'
        else:
            if data and data['status'] == 'logout':
                return login_layout, '/login'
            else:
                return layout, pathname

    
    # 从路由到 mainContent
    @callback(
        Output('layout-mainContent', 'children'), 
        Input('url', 'pathname'),
        prevent_initial_call=True,
    )
    def route_to_menu(pathname):

        name = urlparse(pathname).path.lstrip('/').split('/')[0]

        if name:
            layout_to_render = globals()[f"{name}_layout"]
            return layout_to_render
        else:
            if pathname == '/':
                return globals()["home_layout"]
            else:
                return exception_layout
        
        # if name:
        #     # 检查 name 是否在菜单的键中
        #     routeskeys = [item['key'] for item in routes]
            
        #     if name in routeskeys:
        #         layout_to_render = globals()[f"{name}_layout"]
        #         return layout_to_render
        #     else:
        #         return 'exception'
        # else:
        #     return 'home'


    ######## login页面 ########
    
    # 登陆到home页面
    @callback(
        Output('mainurl', 'pathname', allow_duplicate=True),
        Output('login-message', 'children'),  # 添加此行以返回消息
        Output('loginStatus', 'data'),
        [Input('login-btn_login', 'nClicks')],
        State('username', 'value'),
        State('password', 'value'),
        prevent_initial_call=True,
    )
    def login_to_home(nClicks, username, password):
        if nClicks is not None and nClicks > 0:
            res = login(username, sha256_encrypt(password))
            if res[0]:
                # 用户数据存到localStorage, key为'loginStatus'
                user_data = {'username': username,'password':sha256_encrypt(password), 'status': 'login'}  
                
                return '/home', dash.no_update, user_data  # 登录成功，返回主页和 cookie 数据
            else:
                return dash.no_update, fac.AntdMessage(content=res[3], type='error'), dash.no_update
            
        return dash.no_update, dash.no_update, dash.no_update
    


    ######## home页面 ########

    # 从home页面退出
    @callback(
        Output('mainurl', 'pathname', allow_duplicate=True),
        Output('loginStatus', 'data', allow_duplicate=True),
        Input('layout-rightContent-nav-dropdown', 'clickedKey'), 
        Input('layout-rightContent-nav-dropdown', 'nClicks'),
        State('loginStatus', 'data'),
        prevent_initial_call=True,
    )
    def home_to_login(clickedKey, nClicks, data):
        if nClicks and nClicks > 0:
            if clickedKey == 'logout':
                res = logout(data['username'], data['password']) # 更新数据库状态
                if res[0]:
                    user_data = {'username': '', 'password': '', 'status': 'logout'}
                    return '/login', user_data
                else:
                    return dash.no_update, dash.no_update
        
        return dash.no_update, dash.no_update
    


    # home页面 点击menu item
    def create_menu_callback(item):
        @callback(
            Output('layout-mainContent', 'children', allow_duplicate=True),
            Output('url', 'pathname', allow_duplicate=True),
            Input(item['id'], 'n_clicks'),
            State('loginStatus', 'data'),
            prevent_initial_call=True,
        )
        def menu_callback(n_clicks, loginStatus):
            if n_clicks:
                try:
                    path = item['path']
                    layout_to_render = globals()[f"{path}_layout"]
                    if path == 'newChat':
                        key = f'newchat_{str(uuid.uuid4())}'
                        creator = loginStatus['username']
                        isadd = newchat_add(key, '', creator)
                        if isadd:
                            return layout_to_render, f'/{path}/{key}'
                        else:
                            return globals()['home_layout'], dash.no_update
                        
                    else:
                        return layout_to_render, f'/{path}'
                except:
                    return dash.no_update, dash.no_update
                    # return exception_layout, "/exception"
    
    for item in menuroutes:
        create_menu_callback(item)
    



    # 右上角的用户头像下拉菜单
    @callback(
        Output('layout-rightContent-nav-dropdown-accountrole', 'children'),
        Input('mainurl', 'pathname'),
        State('loginStatus', 'data'),
        prevent_initial_call=True,
    )
    def nav_dropdown_accountrole(pathname, data):
        name = f"当前用户({data['username']})" if data else "未登录"
        return name
    
    
  