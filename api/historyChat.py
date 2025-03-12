import dash
from dash import html, dcc, Input, Output, callback, State
from dash.dependencies import ClientsideFunction
from dash.exceptions import PreventUpdate
import feffery_antd_components as fac

from common.sql import SQLiteClass
from common.utils import historychat, historyChatdatatohtml, historyChat_delone, historyChat_delAll




# 注册 historyChat 的回调
def register_callbacks_historyChat(app):

    @callback(
        Output('historyChat-content', 'children'),
        Input('layout-mainContent', 'children'),
        State('loginStatus', 'data'),
        prevent_initial_call=False,
    )
    def historyChat_chatContent(children, loginStatus):
        if children:
            usr = loginStatus['username']
            historyChat_data = historychat(usr)
            res = historyChatdatatohtml(historyChat_data)
            
            return res
        else:
            return dash.no_update
        

    # 点击详情按钮事件
    @callback(
        Output('url', 'pathname', allow_duplicate=True),
        Input({'type': 'historyChat—infobtn', 'index': dash.dependencies.ALL}, 'nClicks'),
        prevent_initial_call=True
    )
    def historyChat_info_callback(nClicks):
        ctx = dash.callback_context
        if not ctx.triggered:
            raise PreventUpdate

        # 获取触发按钮的 ID
        button_id = ctx.triggered[0]['prop_id'].split('.')[0]
        button_id = eval(button_id)  # 将字符串转换为字典
        key = button_id['index']

        # 检查 n_clicks 的值
        if not any(nClicks):  # 如果所有按钮的 n_clicks 都为 None 或 0
            raise PreventUpdate

        return f'/newChat/{key}'
    
    
    # 点击删除按钮事件
    @callback(
        Output('url', 'pathname', allow_duplicate=True),
        Input({'type': 'historyChat—delbtn', 'index': dash.dependencies.ALL}, 'nClicks'),
        prevent_initial_call=True
    )
    def historyChat_info_callback(nClicks):
        ctx = dash.callback_context
        if not ctx.triggered:
            raise PreventUpdate

        # 获取触发按钮的 ID
        button_id = ctx.triggered[0]['prop_id'].split('.')[0]
        button_id = eval(button_id)  # 将字符串转换为字典
        key = button_id['index']

        # 检查 n_clicks 的值
        if not any(nClicks):  # 如果所有按钮的 n_clicks 都为 None 或 0
            raise PreventUpdate
        
        isdel = historyChat_delone(key)
        if isdel:
            return f'/historyChat'
        else:
            return dash.no_update        
        
        
    # 点击删除全部
    @callback(
        Output('url', 'pathname', allow_duplicate=True),
        Input('historyChat—delAllbtn', 'nClicks'),
        prevent_initial_call=True
    )
    def historyChat_info_callback(nClicks):
        if nClicks:
            isdelAll = historyChat_delAll()
            if isdelAll:
                return f'/historyChat'
            else:
                return dash.no_update
        else:
            return dash.no_update


    # 点击查询 title or content
    @callback(
        Output('historyChat-content', 'children', allow_duplicate=True),
        Input('historyChat—search', 'nClicksSearch'),
        State('historyChat—search', 'value'),
        State('loginStatus', 'data'),
        prevent_initial_call=True,
    )
    def historyChat_likesearch(nClicksSearch, value, loginStatus):
        try:
            if nClicksSearch:
                
                usr = loginStatus['username']
                historyChat_data = historychat(usr, input=value)
                res = historyChatdatatohtml(historyChat_data)
                
                return res
            else:
                return dash.no_update
            
        except Exception as e:
            return dash.no_update