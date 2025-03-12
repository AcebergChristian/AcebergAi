import dash
from dash import html, dcc, Input, Output, callback, State
from dash.dependencies import ClientsideFunction
import feffery_antd_components as fac

from common.sql import SQLiteClass
import random
import json
import uuid
import datetime
# 倒入 newchat的新增方法
from common.utils import newchat_add



# 注册home的回调
def register_callbacks_home(app):

    # click send
    @app.callback(
        Output('url', 'pathname'),
        Input('home-send', 'nClicks'),
        State('home-input', 'value'),
        State('loginStatus', 'data'),
        prevent_initial_call=True
    )
    def create_new_chat(nClicks, value, loginStatus):
        if nClicks:
            key = f'newchat_{str(uuid.uuid4())}'
            creator = loginStatus['username']
            
            isadd = newchat_add(key, value, creator)
            if isadd:
                # 这里可以添加逻辑来保存用户输入和新聊天ID
                return f'/newChat/{key}'
            else:
                return dash.no_update
        else:
            return dash.no_update